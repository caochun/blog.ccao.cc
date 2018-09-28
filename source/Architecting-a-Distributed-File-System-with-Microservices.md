---
title: Architecting a Distributed File System with Microservices
date: 2018-06-19 22:29:52
tags:
---


## 总体要求

基于微服务架构，设计一个分布式文件系统。

#### 功能要求：

1. 基于Spring Boot实现NameNode和DataNode两个服务，在Spring Cloud微服务平台上运行一个NameNode实例和多个DataNode实例（无需考虑NameNode单点失效问题）
1. NameNode提供REST风格接口与用户交互，实现用户文件上传、下载、删除，DataNode不与用户直接交互（无需考虑NameNode的IO瓶颈问题）
1. NameNode将用户上传文件文件拆为固定大小的存储块，分散存储在各个DataNode上，每个块保存若干副本。块大小和副本数可通过系统参数配置。



### 非功能性要求：
1. DataNode服务可弹性扩展，每次启动一个DataNode服务NameNode可发现并将其纳入整个系统
1. NameNode负责检查各DataNode健康状态，需模拟某个DataNode下线时NameNode自动在其他DataNode上复制（迁移）该下线服务原本保存的数据块
1. NameNode在管理数据块存储和迁移过程中应实现一定策略尽量保持各DataNode的负载均衡
1. 提供一个namenode上的前端页面


### 接口示例：
* `GET /` - 列出文件系统`/`目录内容
* `GET /user1/a.docx` - 下载`/user1/a.docx`文件
* `PUT /user2/b.zip` - 上传`b.zip`文件到`/user2`目录
* `DEL /user2/b.zip` - 删除`/user2`目录下`b.zip`文件


## 示例代码

<https://github.com/njuics/dev-mdfs>

### 工程简介

示例代码为一个Maven构建管理的Java工程，工程包含若干模块，每个模块又是一个Maven管理的Java工程，各自实现一个微服务实体，包括微服务架构中的基础设施服务（如Config Service、Discovery Service和Tracing Service等）。顶层工程除POM文件外不包含其他源代码，该POM文件定义了各个模块共享的Maven属性、依赖和插件等。

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.14.RELEASE</version>
    </parent>

    <groupId>info.nemoworks.mdfs</groupId>
    <artifactId>mdfs-system</artifactId>
    <version>1.0.0</version>
    <name>${project.artifactId}</name>
    <packaging>pom</packaging>

    <modules>
        <module>mdfs-config-server</module>
    </modules>

    <properties>
        <assertj.version>3.10.0</assertj.version>
        ...
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-sleuth-dependencies</artifactId>
                <type>pom</type>
                <scope>import</scope>
                <version>${sleuth.version}</version>
            </dependency>
            ...
        </dependencies>
    </dependencyManagement>

   ...

</project>
```

> [POM](https://maven.apache.org/pom.html) stands for "Project Object Model". It is an XML representation of a Maven project held in a file named pom.xml. 


#### Config Server

> [Spring Cloud Config](https://cloud.spring.io/spring-cloud-config/) provides server and client-side support for externalized configuration in a distributed system. With the Config Server you have a central place to manage external properties for applications across all environments.

``` java
@EnableConfigServer
@SpringBootApplication
public class ConfigServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
```

我们通过`@EnableConfigServer`直接让Spring Boot启动一个Config Server。Spring Boot是个神器，会自动按你这个Annotation运行一个特定的`SpringBootApplication`


> [Spring Boot](https://spring.io/projects/spring-boot) makes it easy to create stand-alone, production-grade Spring based Applications that you can "just run".

注意，Spring Boot目前最新版是`2.0.x`，但最新版与Spring Cloud 的最新版       `Edgware.SR3`似乎尚不兼容，所以我们还是用`1.5.14.RELEASE`这个版本的Spring Boot。请注意看顶层POM文件内容。

与Spring Petclinic的Microserice版本不同，为了避免麻烦，我将Config Server提供的config数据放在`resources`目录下，你可以看到一堆yml文件。其中的`application.yml`是当前Config Server的应用运行参数

```yml
server.port: 8888

spring:
  application:
     name: config-server
  profiles:
     active: native
```

`profiles.active=native`代表用本地文件作为config来源，这个本地文件默认会搜索classpath（resources目录是在classpath中的），或者你通过`file:///...`去指定，具体参考[Spring Cloud文档](https://cloud.spring.io/spring-cloud-config/multi/multi__spring_cloud_config_server.html)。

其他yml文件为每个其他服务对应的参数配置，启动Config Server后可以用curl命令看看内容是否正确。例如：

```bash
curl http://localhost:8888/discovery-server/default
```

#### Discovery Server



``` java
@EnableEurekaServer
@SpringBootApplication
public class DiscoveryServerApplication {

	public static void main(String[] args) {
		SpringApplication.run(DiscoveryServerApplication.class, args);
	}
}
```

如同Config Server， 我们通过`@EnableEurekaServer`直接让Spring Boot启动一个 Discovery Server，或者叫Service Registry。这个Server实际上是Netflix这个不务正业的视频网站开发的一个微服务平台中的一个组件`Eureka`，Spring Cloud集成了这个组件。Eureka这个词源自希腊，用以表达发现某件事物、真相时的感叹词。关于这个服务，请参考Spring的文档。


> [A service registry](https://spring.io/blog/2015/01/20/microservice-registration-and-discovery-with-spring-cloud-and-netflix-s-eureka) is a phone book for your microservices. Each service registers itself with the service registry and tells the registry where it lives (host, port, node name) and perhaps other service-specific metadata - things that other services can use to make informed decisions about it. Clients can ask questions about the service topology (“are there any ‘fulfillment-services’ available, and if so, where?”) and service capabilities (“can you handle X, Y, and Z?”). You probably already use a technology that has some notion of a cluster (Cassandra, Memcached, etc.), and that information is ideally stored in a service registry. There are several popular options for service registries. Netflix built and then open-sourced their own service registry, Eureka. Another new, but increasingly popular option is Consul. We’ll look principally at some of the integration between Spring Cloud and Netflix’s Eureka service registry.

注意，你如果使用版本号大于`8`的Java环境可能会导致错误。具体原因和解决方法以后再说。

### TBC