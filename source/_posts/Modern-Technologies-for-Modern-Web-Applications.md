---
title: Modern Technologies for Modern Web Applications
date: 2018-07-26 15:47:59
tags:
---

# Modern Web Application

当前的企业信息系统一般采用Web技术进行设计和开发，如图所示。

{% qnimg webtech/webapp.png %}

这是github上的某一位普通用户开发的他所在企业的Web应用的一个简化版本，代码位于[DimitriZhao/sinosteel](https://github.com/DimitriZhao/sinosteel)这个git仓库。之所以从这个系统开始讲，是因为这个系统用到了当前Web应用开发的主流技术栈，包括应用框架、开发工具和管理流程等。

这个系统的总体架构如下。

{% qnimg webtech/architecture.png %}

本文讲会从Web应用的历史讲起，讲讲为什么现在的Web应用会发展到这样一种架构，并针对其中各项技术做简介，希望能让读者快速理解Web应用开发框架。


## 历史：从HTML到Web应用

上世纪九十年代起，万维网（英语：World Wide Web，亦作“WWW”或“Web”）替代电子邮件成为了互联网最重要的应用。Tim Berners-Lee这位英国计算机科学家写了第一个浏览器供用户通过互联网访问一个个“网页”，从而快速获取各类信息，交换知识。网页用现在大家熟知的超文本标记语言（英语：HyperText Markup Language，简称：HTML）来展示内容，包括文字、图片视频、音频等，从而用令人赏心悦目的形式为大家带来了丰富多彩的内容。大多数的网页自身包含有超链接指向其他相关网页，这样通过超链接，把有用的相关资源组织在一起的集合，就形成了一个所谓的信息“网”。（以上内容总结自Wikipedia[相关页面](https://zh.wikipedia.org/wiki/%E4%B8%87%E7%BB%B4%E7%BD%91)）

因此九十年代到两千年这段时期，大家纷纷开始通过HTML这种语言来编撰出很多网页，并构建出一个个网站来为用户提供各类信息，以下是一个经典的Hello World程序的例子：

``` html
<!DOCTYPE html>
<html>
  <head>
    <title>This is a title</title>
  </head>
  <body>
    <p>Hello world!</p>
  </body>
</html>
```

HTML描述了一个网页的结构语义随着线索的呈现，也就是说HTML是定义了内容的展现方式，通过基本的HTML技术来实现网页并构建网站的过程，本质上来说是一个将一组静态内容发布出来以供用户消费的过程，当时著名软件公司发开了各类网页编辑器来进行网页开发，例如Dreamweaver、Frontpage等。静态网站的工作原理如下图所示。

{% qnimg webtech/static.png %}



不过人们很快就不满足于这种每次浏览器访问都看到一样内容的静态网页技术，在静态内容的发布的基础上有了动态内容的需要。最典型的就是当年各大门户网站上都有个“访客计数器”，页面每次被访问，这个计数器就递增，从而统计来访用户数量（实际上是页面被请求的数量）。当时一个网站的价值大概与这个数字成正比，数字足够大，就能把投入到这个网站开发的钱数直接加个零卖给下家。

要实现这样一个每次访问都呈现不同内容的页面，单纯的HTML就不行了，因此出现了所谓的动态网页技术。简单来说，动态网页就是把代码潜入到页面上去，每次用户请求时执行这段代码得到结果后再把结果返回给用户。CGI是当时最为著名的用来实现这一点的黑科技。[CGI](https://zh.wikipedia.org/wiki/%E9%80%9A%E7%94%A8%E7%BD%91%E5%85%B3%E6%8E%A5%E5%8F%A3)全称Common Gateway Interface，中文叫做通用网关接口，可以让一个用户从网页浏览器向执行在服务器上的程序请求数据（而不是直接获取一个静态页面）。其工作原理如下图所示：

{% qnimg webtech/dynamic.png %}



当年一般用Perl语言来编写CGI程序，例如这段代码基于用户通过html的form传入到变量打印一个字符串。

``` perl
#!perl -w  
use CGI qw/:standard/;  
{  
  my $cgi= new CGI;  
  print $cgi->header,  
  $cgi->start_html('A Simple Example'),  
  $cgi->h1('A Simple Example');  
   
  if ( $cgi->param())  
  {  
    print "Your name is ",  
    $cgi->param('name');  
  }  
   
  $cgi->end_html();  
}  
```

写CGI来实现动态内容展示存在一些问题，首先CGI代码运行在一个独立的进程中，效率和安全性都堪忧，其次，写起来很麻烦，CGI规范繁杂，perl语言也相当难学。因此不久以后出现了动态页面技术，例如php、asp、jsp等。例如我们可以用jsp写这么个页面：

``` html
<html>
<head><title>First JSP</title></head>
<body>
  <%
    double num = Math.random();
    if (num > 0.95) {
  %>
      <h2>You'll have a luck day!</h2><p>(<%= num %>)</p>
  <%
    } else {
  %>
      <h2>Well, life goes on ... </h2><p>(<%= num %>)</p>
  <%
    }
  %>
  <a href="<%= request.getRequestURI() %>"><h3>Try Again</h3></a>
</body>
</html>
```

代码和页面混合在一起使得页面的最终呈现是由这个页面再被用户请求时页面内的代码执行结果决定的，从而实现内容的动态展示。在此基础上，出现了更极端的技术（比如Java Servlet），直接对用户发来的请求解释并生成结果以及用来呈现结果的html。其工作原理如下图所示：

{% qnimg webtech/servlet.png %}

以下为Servlet的示例代码：


``` java
// Import required java libraries
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

// Extend HttpServlet class
public class HelloWorld extends HttpServlet {
 
   private String message;

   public void init() throws ServletException {
      // Do required initialization
      message = "Hello World";
   }

   public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
      
      // Set response content type
      response.setContentType("text/html");

      // Actual logic goes here.
      PrintWriter out = response.getWriter();
      out.println("<h1>" + message + "</h1>");
   }

   public void destroy() {
      // do nothing.
   }
}
```

之所以叫Servlet，是跟Java中的Applet技术对应的。Applet代表一个运行在用户端的小程序（小应用），Servlet则是运行在服务器端的一个应用。这个应用通过Web技术形式（以HTTP为通信协议，以HTML为内容格式）与用户交互，因此用Servlet或类似技术实现的Web系统，一般就称之为Web应用。

有兴趣的话可以Clone这个[仓库](https://github.com/njuics/sa2017.git)去运行一下ServletDemo这个例子。


## MVC Web

细心的你会发现，其实Java Servlet和早起的CGI技术原理上是一样的：用户发送一个HTTP请求到服务器，服务器端执行一段代码，代码产生结果，渲染为HTML结构的页面返回给用户。但为什么现在你主要用的时Servlet技术开发Web应用而不是CGI呢？因为现在我们在Servlet之上构造了一层MVC的设计模式。


之前那段Servlet代码中的`doGet()`函数是执行主体。

``` java
public void doGet(HttpServletRequest request, HttpServletResponse response)
      throws ServletException, IOException {
      
      // Set response content type
      response.setContentType("text/html");

      // Actual logic goes here.
      PrintWriter out = response.getWriter();
      out.println("<h1>" + message + "</h1>");
   }
```

当然这个例子中的`doGet`执行的逻辑过于简单了点，一般来说，我们在这个函数中做三件事：

1. 对方法参数对象`request`进行处理解析获得用户输入；
2. 执行一段业务逻辑代码，对用户输入进行处理，得到一个业务层面的计算结果；
3. 在方法参数对象`response`里讲计算结果用HTML的形式写入，让用户得到输出。

如下图所示：

{% qnimg webtech/doget.png %}

直接这么写的问题在于所有的输入处理、业务计算和输出组织都是混在一起的，特别时输出部分需要通过字符串拼接等方式形成一个比较负责的html页面去展示结果，为维护带来了很大的不便。程序员一般HTML写得很难看，但会做页面设计的美工又不懂得Java语言，所以直接这样写Servlet不利于分工后协作，效率极低。因此出现了将用HTML进行结果渲染这个过程独立出来的技术，一般称之为模板引擎（Template Engine），例如[Freemarker](https://freemarker.apache.org/)、[Velocity](http://velocity.apache.org/)和[Thymeleaf](https://www.thymeleaf.org/)等，从概念上看这种技术就是将应用的表现层独立了出来，如下图。

{% qnimg webtech/ui.png %}

这么做的好处很显然，你可以单独写一个模板，让美工做得很漂亮，然后在代码运行时用运行结果去填充这个模板，渲染成一个页面，具体可以参考下面这个例子。


``` html
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
    <title>Sample Page</title>
  </head>
  <body>
    <b>Time Now:</b> ${requestScope["time"]}
  </body>
</html>
```

``` java

protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException { 

    request.setAttribute("time", new Date()); // 'time' would be  shown on JSP page             
    RequestDispatcher view = request.getRequestDispatcher("WEB-INF/templates/sample.jsp");      
    view.forward(request, response);
}

```

这样一来程序员和美工就可以愉快地在一起工作了。但从程序员的角度来看，还有一部分问题没解决，就是用户输入参数的处理和业务逻辑计算代码还是在一起的，不能分别维护。因此我们再次进行分割，变成以下的样子：

{% qnimg webtech/mvc.png %}


我们将业务逻辑部分再切出来，用户请求发送过来驱动Servlet的某个`doGet`方法开始运行，方法内主要负责的事时解析获得用户输入内容，将输入交给一个核心部件进行计算处理获得结果后再将结果交给模板引擎进行渲染，所以这个Servlet虽然没有做最核心的计算和漂亮页面的展示，但它控制了整个执行过程，称之为“控制器”；控制器解析出的用户输入内容被交给第二个部分进行计算处理，这个部分实际上就是系统的核心，执行的是关键性的计算过程，并得到一个计算结果，我们称之为“模型”；用来渲染这个计算结果的展示部分称之为“视图”。

仔细体会一下这样分割的好处，我想至少有这么几点：

1. 其他都不变的情况下，如果有调整页面设计，只要改HTML模板就行了，代码不用动；
2. 如果一个核心算法要改进，那该模型的实现就行了，其他都不用动；或者说如果某个计算过程有新的实现，那让控制器调用新的模型实现就行；
3. 如果用户输入参数改了，那我们可以在控制器层面把参数变动处理了，其他部分可以不受影响。

因此这样一来，你可以找三个人分别来干这三件事。这实际上是软件技术中一直孜孜以求的一个模板，叫做[“关注分离”(Separation of concerns，SOC)](https://zh.wikipedia.org/wiki/%E5%85%B3%E6%B3%A8%E7%82%B9%E5%88%86%E7%A6%BB)。

下面开始进入正题：Spring MVC。

## Spring

Spring是一个开源框架，为简化企业级应用开发和运行管理而生。早期Spring指的是一个IoC(DI)和AOP容器框架，叫Spring Framework。关于IoC（Inversion of Control，中文叫“反转控制”）、DI（Dependency Injection，中文叫“依赖注入”）和AOP（Aspect-Oriented Programming，中文叫“面向切面编程”）等概念在后面逐步展开介绍。这些都是非常重要的软件技术概念。
Spring目前成为了应用最广泛的Java开发框架，甚至连早期特别红火的EJB技术也基本完全没落了，主流的企业级应用十之八九都以Spring为平台，这主要是由于Spring在此核心框架基础之上衍生出了[很多项目](http://spring.io/projects)来提供面向应用开发的完整框架、工具等，被称之为"Spring全家桶"。

{% qnimg webtech/spring.png %}

## Spring MVC

Spring在其核心框架Spring Framework中提供了Web应用开发支持。

{% qnimg webtech/springframework.png %}

### 结构

Spring的Web支持开发MVC模式的Web应用。具体而言，Spring预先实现了一个特定的Servlet叫做`DispatcherServlet`，这个Servlet会根据用户的配置，将不同的请求（URL）转发给不同的代码（Controller）进行处理，Controller处理完得到结果将结果渲染到一个页面中返回给用户。

{% qnimg webtech/springmvc.png %}

这其中涉及到一些内部技术，例如`HandlerMapper`、`ViewResolver`等，但这些跟用户在业务层编程关系不大，所以目前无需了解得过细，原理知道即可。

### 示例工程及相关工具

快速学习一项具体技术的方法不是去买本很厚的书回来从头开始看，而是找个例子当葫芦，然后你照着画个瓢。国内很多热心人士也在网上po出很多例子，但一般而言各人在技术理解的层面上深度准确度都不尽相同，这些例子一般也不随着技术本身的发展而同步更新，因此还是尽量找权威机构的技术材料来看会比较好。Spring公司在其[官方网站](https://spring.io/)上提供了一系列很好的[教程](https://spring.io/guides)让开发人员可以快速了解技术，后面我们会讲到这中间的若干篇。

我们先来看教程中关于Web应用的一个最简单例子--[Serving Web Content with Spring MVC](https://spring.io/guides/gs/serving-web-content/
)。

这篇教程中要我们用[git](https://git-scm.com/)工具获取示例代码。Git是一个目前最流行的版本控制工具，相比原来普遍使用的CVS、SVN等有很多优势。现在最热门的开源网站[Github](https://github.com/)实际上就是一个对上百万（可能上千万）个仓库进行管理、分享的系统。关于Git工具的使用可以看一下简要介绍，比如[这个](http://rogerdudler.github.io/git-guide/index.zh.html)。简言之，你现在先从<https://git-scm.com/>上下载git并安装，然后用clone命令获取代码。

``` bash
git clone https://github.com/spring-guides/gs-serving-web-content.git
```

然后进入代码仓库目录
``` bash
cd gs-serving-web-content
```

你会看到其中有`initial`和`complete`两个目录（和其他的一些文件目录）。教程想让你从一个工程的最初创建状态（`initial`中所含的内容）开始，一步一步操作，最后到达完成状态（`complete`中的内容）。为简单起见，我们就直接讲解一下后者，关于这个目录中的代码和资源文件怎么创建怎么编辑开发的过程可以仔细读教程。

`complete`目录下存在多个各个文件夹和文件，其中`src`目录内是项目的源代码和相关资源文件，其他的则是用来对这些源代码和资源文件进行编译、连接、打包等处理过程的“构建工具”需要的内容。

**构建工具**是一个把源代码生成可执行应用程序的过程自动化的程序（例如Android app生成apk）。如果你之前主要用eclipse开发，那可能觉得构建工具这个概念比较陌生，但构建工具这个概念和技术已经存在了几十年了，如果你在Unix/Linux系统下软件开发的或者在Unix/Linux下从别人开发的源代码进行软件安装的话，一定知道“Makefile”这个文件，这个文件实际上就是告诉`make`这个构建工具如何编译代码、如何最后生成可执行文件的一个配置文件，有兴趣的话可以读一下这篇[Make 命令教程](http://www.ruanyifeng.com/blog/2015/02/make.html)。

我们在这个工程中以及以后的示例中都会使用构建工具来进行编译运行等操作，而不是用eclipse。也许你觉得这件事情挺难理解的，为什么不用eclipse呢？那我告诉你用构建工具的重要优势之一：它可以帮你进行**依赖管理**。我们在用eclipse开发的时候，通常都会用到第三方的一些库（Library），在eclipse中我们可以在项目配置页中指定一个目录作为Library，告诉eclipse要从那里面去搜索你所要用到的类，然后你可以从网上去下载一堆jar文件，放入这个Library文件夹中，但如果项目依赖的jar很多，这件事就会比较累，而且你引入的jar可能又以来其他jar，你还得把其他jar也下载下来放进去，更复杂的是每个jar还有版本，你要非常仔细地选择合适的版本，这就会让你很头疼。如果某个jar更新了你希望保持同步，那之前做过的事情又要重新来一遍。这就是手工进行依赖管理的过程。使用构建工具的话，这个过程就会自动化完成。

互联网上有个网站<https://mvnrepository.com/>，这个网站上维护了1100万左右的jar包，你可以用构建工具随意来获取你所需要的jar，这个工具的名称叫[Maven]<https://maven.apache.org/>。`complete`目录下的`pom.xml`就是一个配置文件，告诉Maven你依赖的jar包有哪些，你的代码怎么编译，编译后如何运行等等。`mvnw`和`mvnw.cmd`是两个用来运行Maven的脚本文件，暂时可以不用管。另外`build.gradle`、`gradle`、`gradlew`和`gradlew.bat`是另外一套构建工具Gradle所需的配置和脚步。早期只有Maven这个工具，后来有人觉得Maven用xml作为配置文件太繁琐，所以开发了gradle，而gradle跟Maven一样还是从mvnrepository搜索下载依赖，构建过程的原理也一样。

### 构建并运行

所以目前我们简单点，只看Maven，请从Maven官方网站下载并安装Maven工具，如果你在complete目录下运行以下命令正确了，说明你之前的这些步骤都做对了。

``` bash
mvn spring-boot:run
```

第一次运行的话可能需要等待很久，时间主要被Maven花在从网络上下载这个工程所需要的依赖文件。等待几分钟（网络慢的话可能需要十几分钟）后，这个应用就会运行起来。用浏览器访问`http://localhost:8080/`即可。首页上有链接引导你访问`http://localhost:8080/greeting`，得到`Hello, World!`这个结果页面，你也可以在url后面加上`name`参数，例如访问`http://localhost:8080/greeting?name=John`得到`Hello, John!`结果页面。

> Checkpoint: 完成这一步的话至少你的开发环境目前基本配置正确了。

显然，它运行起来看起来是个web工程，而且你如果足够细心的话会发现刚才运行的时候控制台日志里有这样的几行：

```
2018-08-10 13:50:40.558  INFO 1444 --- [  restartedMain] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 8080 (http)
2018-08-10 13:50:40.584  INFO 1444 --- [  restartedMain] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
2018-08-10 13:50:40.584  INFO 1444 --- [  restartedMain] org.apache.catalina.core.StandardEngine  : Starting Servlet Engine: Apache Tomcat/8.5.31
```

这意味着刚才的运行过程中Tomcat应用服务器和Servlet引擎被启动。但跟之前开发Web应用不一样，我们没有把工程打包为war然后部署到一个独立运行的Tomcat，这个工程像是直接自动完成了打包war、启动tomcat、部署war这些所有步骤。


我们打开代码看看这到底是怎么回事吧。

### 代码解释

我们可以用IDE打开代码，推荐使用[IntelliJ IDEA](https://www.jetbrains.com/idea/)，当然这个开发工具是要钱的。不想买的话可以用微软发布的[Visual Studio Code](https://code.visualstudio.com/)（简称Code）。Code实际上只是个编辑器，不是集成开发环境，因为我们可以用Maven进行自动化构建，所以用Code看代码写代码也就足够了。Code具有非常开放的架构，很多第三方的插件使得Code实际上非常强大，推荐使用。

用Code打开`complete`目录，其中`src/main/java/`是代码所在目录，之所以有这个目录结构是Maven工程的规范要求。工程名空间是`package hello`，所以`src/main/java/hello`是Java文件代码实际所在之处，包括`Application.java`和`GreetingController.java`。

首先我们要看的不是这些java文件，而是位于`complete`目前下的`pom.xml`文件。POM是Project Object Model的缩写，代表工程对象模型，也就关于工程和各种配置细节的信息，Maven使用这些信息构建工程。详细信息可以参考<http://wiki.jikexueyuan.com/project/maven/pom.html>。

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.springframework</groupId>
    <artifactId>gs-serving-web-content</artifactId>
    <version>0.1.0</version>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.0.3.RELEASE</version>
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-thymeleaf</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
            <optional>true</optional>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

</project>
```

其中

1. `<groupId>`、`<artifactId>`、`<version>`三个tag合起来说，当前这个工程是`org.springframework`这个组织的，工程名叫`gs-serving-web-content`，版本是`0.1.0`，这很好理解；
2. `<dependencies>`这个tag里定义了当前工程直接依赖的第三方库（或称为“包”），例如当前工程依赖于`org.springframework.boot`组织开发的`spring-boot-starter-thymeleaf`这个库，Maven工具根据这个信息会自动从mvnrepository里下载对应的jar，你也可以直接访问[网页](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-thymeleaf)；
3. `<properties>`里可以定义一组属性（变量值）；
4. `<build>`下的`<plugins>`里定义当前工程构建需要用到的插件，这里我们用了一个`spring-boot-maven-plugin`插件，正是这个插件使我们能运行`mvn spring-boot:run`；
5. `<parent>`标签定义了这个POM的上一级（父）POM，上一级POM中定义的属性、依赖、插件等都可以被复用。



然后看一下`GreetingController`这个类。

``` java
package hello;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class GreetingController {

    @GetMapping("/greeting")
    public String greeting(@RequestParam(name="name", required=false, defaultValue="World") String name, Model model) {
        model.addAttribute("name", name);
        return "greeting";
    }

}
```

这个类也很简单，定义了一个`greeting`方法，该方法上有个注解（Annotation），其含义比较直观：

1. 为方法`greeting`标上注解`@GetMapping("/greeting")`意味着当前这个方法负责处理用户发来的`GET /greeting`这个请求；
2. 为参数`name`标上注解`@RequestParam(name="name", required=false, defaultValue="World")`意味着从请求中取查询参数`name`作为这个参数的值，缺省为`World`。
3. 为类`GreetingController`标上注解`@Controller`意味着当前这个类是一个**控制器**;

结合我们前面说的MVC的技术理念，有过Web开发经验的就应该看得懂，这就是一个可以响应用户的一个具体请求的Web应用控制器类。然后看`Application.java`。

``` java
package hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}
```

这段代码刚学Java时你就能读懂，这个类里只有一个`main`函数，调用了`SpringApplication`类的`run`方法。

那这两个类存在了为什么我们运行`mvn spring-boot:run`就能启动出Tomcat并部署一个包含了`GreetingController`这个控制器的war呢？这一切的神奇来自于`Application`类上的`@SpringBootApplication`这个注解。这个注解解释起来就费劲了，它实际上是Spring三年前才发布的一项新技术：[Spring Boot](https://spring.io/projects/spring-boot)。其设计目的是用来简化新Spring应用的初始搭建以及开发过程。该框架使用了特定的方式来进行配置，从而使开发人员不再需要定义样板化的配置。平时如果我们需要搭建一个web项目的时候需要配置web.xml、配置数据库连接、配置事务、配置加载配置文件的读取、配置日志文件等等，但是如果使用spring boot呢？很简单，我仅仅只需要非常少的几个配置就可以迅速方便的搭建起来一套web项目。

**简单而言，加了`@SpringBootApplication`这个注解后，Spring底层系统会根据我们的项目信息来帮你进行自动化的配置，比如我们在POM中写了对`spring-boot-starter-web`的依赖，Spring会猜到我们是要开发一个Web应用，因此帮我们自动启动了Tomcat服务器。同时Spring发现有一个类标注了`@Controller`，说明这是个控制器类，Spring会自动创建这个类的对象（这里用到了Spring Framework中的Bean构件管理和依赖注入等底层技术），并自动为Tomcat里运行的DispatcherServlet配置请求转发规则，让所有`GET /greeting`请求被`GreetingController`这个控制器的`greeting`函数所处理。**


上面说的`mvn spring-boot:run`这种方式可以启动当前Spring Boot工程的运行，也可以这样：

``` bash
mvn package
cd target
java -jar gs-serving-web-content-0.1.0.jar
```

`mvn package`把当前这个工程编译，打包为一个jar，jar文件存放在`target`目录下，注意这个jar可以独立运行。这个jar中包含了当前这个应用运行所需的所有东西，只要有java环境就能运行这个应用，这为后面支撑**微服务**架构提供了一个完美的技术方案。

> 关于微服务，我们会在“{% post_link Building-Cloud-Applications-with-Microserivce-Architecture 基于微服务架构开发面向云计算的应用系统 %}”这篇中详细说。

这个例子中的`greeting`函数的第二个参数`model`就是用来存放模型对象的，方法返回一个字符串`greeting`，即告诉系统greeting函数结束后，用名字叫`greeting`的视图模板（`resources/templates/greeting.html`）渲染`model`里的数据，然后返回给用户。这过程跟早期的Struts框架处理流程很接近，此处不赘述。

这个例子很简单，其中主要的特点在于用了Spring Boot来自动配置整个应用。下面看一个经典的更完整的例子。

## Spring PetClinic

Java技术流行了很多年，特别是EJB技术推动了Java成为企业应用开发的首选。当年Sun公司（现在已经被Oracle收购）为了让程序员有效快速了解EJB技术体系，给了一个很典型的示例工程（Java Pet Store，一个在线的宠物商店）。Java EJB技术（现在叫Java EE）目前逐步没落了，Spring快速流行起来，并用一个类似的示例工程来方便技术学习。这个工程叫Pet Clinic（宠物医院）。

{% qnimg webtech/petclinic.png %}

这个例子很有代表性，并且有很多版本来展示不同的技术，甚至微服务架构的应用开发也是基于这个例子来讲解。所以请先熟悉一下这个例子本身。

``` bash
git clone https://github.com/spring-projects/spring-petclinic.git
cd spring-petclinic
mvn spring-boot:run
```

### 代码

打开代码，主要看一下那些Java文件。当然这个工程中还存在很多关于配置、模板和样式等的文件，其内容先暂时不解释，实际项目开发中可以再仔细看，我们先讨论代码设计层面的概念。

工程总体架构大体如下图所示：

{% qnimg webtech/petclinic-framework.png %}


代码细节方面也不繁杂，我们选取其中部分类(宠物及其主人）的关系能看到以下关系：

{% qnimg webtech/petclinic-class.png %}


这个工程是典型的MVC结构。`/resources/templates`下是页面模板，这些模板填上数据后成为用户看到的界面（视图），在此视图上用户可以进行操作（例如点击链接导航或按钮发送数据）发出用户请求，控制器会收到用户请求，并根据映射关系（`@GetMapping`或`@PostMapping`）执行某个特定方法处理请求。一般而言这些控制器会处理数据的增删改查操作，这些数据操作会调用`Repository`类的方法来执行，并将执行结果返回给用户。

这里所说的数据是代码中的`Owner`/`Pet`/`Vet`/`Visit`等及相关父类型。这些类型在这儿很像经常会说到的DTO或者VO，但实际上不一样，而且是很不一样。

- 首先，在这个例子中这些类型上加了很多注释，例如`@Entity`,`@MappedSuperclass`,`@Id`, `@Table`,`@Column`,`@OneToMany`,`@NotEmpty`等等。这些注释的存在是因为在这个例子中用了[对象关系映射](https://zh.wikipedia.org/wiki/%E5%AF%B9%E8%B1%A1%E5%85%B3%E7%B3%BB%E6%98%A0%E5%B0%84)（ORM）技术来实现数据持久化。ORM简单来说就是可以将一个对象状态自动保存到关系型数据库或从关系型数据库取出数据还原出一个对象来的技术。这相对于传统意义上手工书写（拼接）SQL查询字符串来说非常简单高效。这些定义了需要将其对象持久化的类成为**实体类**，其中的那些注释给实现ORM的底层技术提供了信息以实现自动的双向映射。例如`Owner`类标注了`@Entity`和`@Table(name = "owners")`，说明这是个需要ORM技术将其对象保持到数据库的实体类，并且这个类的对象状态保存在一张叫`owners`的表里（每个对象对应表的一行），`@Column(name = "address")`注释告诉ORM`Owner`类的`address`属性对应这个表中的`address`列，且不能为空(`@NotEmpty`)。
- 其次，也是**更重要的一点**，**这些类型实际是重要系统核心**。我们开发一个信息系统，其最根本目的是希望通过这个系统让用户能够对某个领域下的信息进行管理，例如企业内的人事管理系统，那就是要正确地维护人员信息（新增人员、删除人员、查询人员、更新人员信息）或者在此基础上进行一些业务（例如在企业规定的上限以下为某个人加工资），我们所写的视图（页面）是为了为用户渲染这些信息或让用户出发对信息操作的行为，我们所写的控制器是为了接收用户的行为或选择一个视图去展示行为的结果，而系统真正的“计算”则是在视图和控制器之外的。因此在上面的架构图中仓库类和实体类是系统的模型。而其中重中之重是那些实体类。实体类真正刻画了当前这个信息系统到底是管理的那些信息，他们之间存在什么关系。如下图所示，我们可以看出当前系统中我们管理的Owner（宠物主人）和Vet（兽医）都是Person（人），每个Owner可以拥有多个Pet（宠物）而每个Pet只能被一个Owner拥有，每个Pet可以拥有多个/次Visit（探望记录）而每次Visit都是针对一个Pet的。这些是我们对当前这个宠物医院的业务的理解，可以称为“领域知识”。Repository类当对来说没那么重要，可以理解为是这些领域知识的接口暴露（这句话不很严谨），但这些接口提供的增删改查操作，都得以维持实体类本身数据合法性和他们之间的关系合法性为基本条件，因此这些领域知识是系统核心所在。对不对？

{% qnimg webtech/petclinic-entity.png %}


这个例子从设计的角度来看其实并不好，他的主要目的是展示Spring对MVC基本结构应用的支持，和其中的一些重要特效，例如Spring Data JPA等。（后续补充）

### 一个改进版本

有人觉得官方这个例子实际上并不好，做了些改进，放在以下地址：

https://github.com/spring-petclinic/spring-framework-petclinic

请注意看这个工程的说明文件（readme.md），用以下命令启动运行这个工程：

``` bash
mvn tomcat7:run-war
```

我们先来看看这个版本的代码有什么改变，主要包括三点：

- 这个工程不是Spring Boot应用了，工程是个普通web工程，打包为war；
- 在`Controller`和`Repository`中间封装了一层`Service`（`ClinicService`）；
- `Repository`层定义为一组接口，并提供了JDBC、JPA和Spring Data JPA等三种持久化技术的实现方式。

结构上如下图所示：

{% qnimg webtech/petclinic-framework-v2.png %}

这三点不同的第一点并不涉及在设计上的改进，只是把当前工程按传统方式打包部署运行。你可以看到在pom.xml中有这么一行：

``` xml
<packaging>war</packaging>
```

并且在plugin里使用了一个`maven-war-plugin`：

``` xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-war-plugin</artifactId>
    <version>2.3</version>
    <configuration>
        <failOnMissingWebXml>false</failOnMissingWebXml>
    </configuration>
</plugin>
```

[这个插件](https://maven.apache.org/plugins/maven-war-plugin/)负责将工程打成一个war包：

> The WAR Plugin is responsible for collecting all artifact dependencies, classes and resources of the web application and packaging them into a web application archive.

并且还用了一个`tomcat7-maven-plugin`，[这个插件](http://tomcat.apache.org/maven-plugin-2.0/tomcat7-maven-plugin/)让我们打包的war能直接在一个tomcat7服务器中部署运行。

> The Tomcat7 Maven Plugin provides goals to manipulate WAR projects within the Tomcat servlet container version 7.x


我们之所以用`mvn tomcat7:run-war`而不是`mvn spring-boot:run`也正是因此。


关于Maven实际上有很多可以说的，但暂时不能铺开，有兴趣的可以先看看上面提到的[Maven中文教程](http://wiki.jikexueyuan.com/project/maven/)。


关于第三点不同，即把`Repository`层定义为一组接口并提供三种持久化技术的实现方式，这使得持久化的接口和具体实现分离开来，你可以如例子中一样用不同的技术来实现同一组接口：

- JDBC是最为传统的一种实现，通过在JDBC驱动上执行SQL查询来操作数据库存取数据，理论上来看JDBC实现具有最大的灵活性；
- JPA是Java的持久化标准，按照ORM的基本思想（使用一个`EntityManager`进行自动化的对象关系映射）定义了一组标准的Java注解，主流的Hibernate就是JPA的一个实现；
- Spring Data JPA在JPA的基础上又进行了封装，进行更加简便的持久化操作，你会惊奇地发现这个工程中`SpringDataXXXRepository`类型都是接口，具体查询实现可以通过注解进行标记，框架就能帮你自动实现接口方法和对应仓库类；你也可以一个方法都不需要定义和实现，框架会帮你自动生成；你甚至可以用近似自然语言的方式写一个接口方法，Spring能知道你要的是什么。

Spring Data JPA确实是很强大，可以看一下[官方文档](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)。嫌看英文累的话也可以看看国内人写的一些技术文章，例如[这篇](https://www.jianshu.com/p/38d27b633d9c)。这部分后续再补充。


最后来谈一下第二点改进。我们在`Repository`和`Controller`之间加了一个`Service`层。首先这样做了以后，运行流程就发生了一些变化：用户请求由`Controller`收到并处理后，决定调用`Service`的某个具体方法，`Service`在执行过程中可能会创建或删除实体对象、更新实体对象状态，这些变化通过调用`Repository`层对象方法进行实施，得到结果后Service返回给`Controller`，继而再返回给用户（通过View进行渲染后）。

反复揣摩一下这个过程，你会发现这其中的各部分分工是很明确：

1. `Controller`负责从请求中获得用户输入，根据输入决定系统应该做什么，并将做的结果或异常返封装为响应发送给用户（决定通过什么视图去展示给用户看）。这边所说的请求和响应实际上跟通讯协议是有关系的。比如，因为一般Controller通过HTTP协议对外通信，所以用户请求参数需要从HTTP的请求URL中获取，因此有些Controller方法中使用`@PathVariable`来提取查询字符串中的某个参数值。因此Controller的另一个实际作用是进行了通信协议的隔离，使得Controller之后的各个组件（Service/Repository等）完全不需要考虑这个系统所运行的具体环境的。这意味着如果设计得好，那你这个系统很容易换一个MVC框架，甚至你可以把系统迁移到一个RPC通信框架下。
2. `Service`负责做具体的业务过程。例如如何新注册一个用户，如何为用户登记一个宠物等，也就是实现了如何正确维护的信息的业务逻辑，比如用户注册时如果输入的身份证号码跟一个已有用户相同，那当前这个注册就不能进行。这些逻辑也是信息系统的核心，这些逻辑在执行时当然肯定涉及到实体类型`Entity`。还记得我们曾经说过的么？实体类定义的信息和信息之间的关系也是系统的核心。因此，合起来看，**`Service`和`Entity`属于一个信息系统内在表达的核心领域知识**。而`Repository`实际是不是必须的。想象一下，如果你的系统是从来不关机的（也不会断电）可以一直运行下去，并且内存足够大所有数据都可以存在内存，那你为什么需要将数据持久化呢？没有数据库，信息系统还是信息系统。因此，**一个信息系统设计和实现的关键是清楚正确地辨识出这个系统所处理的业务，并在业务过程中正确维护所涉及到的信息及其间关系**，这称之为**领域建模**。开发一个系统的过程应该是从领域建模开始的，而不是首先建表去考虑持久化问题，将领域问题弄清楚并通过计算机系统实现出来，在必须的时候再将数据持久化保存，这才是系统开发的有效方法，称之为**领域驱动开发**。这个词内在含义很深厚，后续补充。
3. `Repository`可以看作是一种辅助设施，用来在需要的时候帮系统将数据进行外部持久化，从概念上来看，它并不那么重要。但从技术上来看，它很关键，特别是关注系统运行性能的时候。

以上这段需要你仔细理解一下，实际上就是这么两个重点：

1. 真正的业务在`Servcie`开始的这部分，`Controller`中不应该包含任何业务逻辑，Controller应该只做从HTTP或其他协议的原始请求中剥离出用户输入，交给合适的Service部件调用合适的业务方法，Service执行业务方法，进行计算，维护实体状态和关系，并在需要时调用仓库类方法将实体持久化到外部存储或从外部存储恢复出某个实体对象，Service执行结束后的结果再由Controller进行处理用某种形式返回给用户；
2. 系统开发应首先从领域知识的梳理和实现着手，也就是说你需要先进行领域建模，你应该先想好系统中有那些信息是要维护管理的，这些信息是什么关系，维护管理他们的过程是怎么样的一个过程。前者可以通过类图表达，后者可以通过时序图表达，你还可以通过逻辑公式等方式表达业务内存在的一些约束条件，然后把这些图和约束关系通过代码实现出来。相比于从数据库为出发点的开发方法，领域建模带来的好处会是很明显的，因为领域模型直接反映你对领域知识的理解，你所谓的“懂业务”实际上就是能建立一个显式化的领域模型。领域建模有一整套思维方式和实践方法，具体的以后慢慢补充。






## 前后端分离架构


上面这个改进的工程在设计方面结构比较清晰了，但还存在一个问题，就是用户视图还是通过HTML模板渲染的（这个例子中用了[JSTL](https://zh.wikipedia.org/wiki/JSTL)）。通过这种技术去呈现交互页面给用户存在几个问题：

1. 用户在页面上进行的操作每次都需要传输回后台服务器进行处理，然后渲染新的页面（或部分页面）再次呈现给用户，这一过程中系统与用户的交互性较差；
2. 页面开发与后端逻辑开发混合在一起，页面（前端）工程师与后端工程师间难以协调，特别是调试过程会变得较为混乱；
3. 如果需要负载均衡的集群化部署，前端修改会需要整个集群中所有实例进行重新部署，维护开销巨大。

因此现代的Web工程一般会将前后端分离开。也就是按照最开始我们给出的这张架构图来进行系统架构

{% qnimg webtech/architecture-annotated.png %}

再一次，好心人士将PetClinc进行了改写成了一个前后端分离的工程。我们先看后端工程：

https://github.com/spring-petclinic/spring-petclinic-rest


跟前一个版本相比，主要区别在于原来那些Controller上的注解从`@Controller`变为了`@RestController`。简单来说`@Controller`意味着这个Controller返回的是一个View，将其渲染后返回给用户，而`@RestController`意味着这个Controller返回的是值（对象），这个值（对象）一般转为Json格式后直接输出给用户。另外工程中加入了用户认证（包括跨域）和数据序列化技术等。这些后续补充解释。

拿到这个数据对象后，如何将这个结果展示给用户看那就是另一个问题了，这个问题就是后面我们会继续介绍的前端工程。这个不渲染页面呈现结果给用户的工程直接返回了数据，整个工程提供了一组接口来为用户提供获得信息的服务，这组接口跟你一般编程时候调用的函数是一样的概念，差别只是你给他传入的参数和得到的结果采用的是[JSON](https://www.json.org/)这种格式（也可以用别的数据格式，但JSON目前是最流行的轻量级格式）。

当前这个工程本身比较容易理解，其中引入了一个新工具，叫[Swagger](https://swagger.io/)。你可以按readme.md里所说运行起改工程后访问这个URL

http://localhost:9966/petclinic/swagger-ui.html

你会发现一个漂亮的页面，这个页面上列出了各个Controller实现的用户可调用的接口，你甚至可以直接在这个页面上为接口编写文档，并且还能直接测试这个接口。这是个很有用的工具！

{% qnimg webtech/swagger.png %}


### REST

接口这个概念大家都知道，为什么我们现在需要把开发出来的这些接口叫做REST接口呢？实际上我们在前面的几个例子中我们写的Controller里的方法就是接口，只不过这些接口调用后用户得到的结果会是渲染过的一个页面。这其中有个问题，就是接口的名称是怎么设计的。看一下`spring-framework-petclinic`工程中的`OwerController`里的两个方法：

``` java
    @RequestMapping(value = "/owners/{ownerId}/edit", method = RequestMethod.GET)
    public String initUpdateOwnerForm(@PathVariable("ownerId") int ownerId, Model model) {
        Owner owner = this.clinicService.findOwnerById(ownerId);
        model.addAttribute(owner);
        return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
    }

    @RequestMapping(value = "/owners/{ownerId}/edit", method = RequestMethod.POST)
    public String processUpdateOwnerForm(@Valid Owner owner, BindingResult result, @PathVariable("ownerId") int ownerId) {
        if (result.hasErrors()) {
            return VIEWS_OWNER_CREATE_OR_UPDATE_FORM;
        } else {
            owner.setId(ownerId);
            this.clinicService.saveOwner(owner);
            return "redirect:/owners/{ownerId}";
        }
    }
```

要看懂这两个方法到底是干嘛用的，你可以看方法名称：`initUpdateOwnerForm()`和`processUpdateOwnerForm()`，你会发现这两个方法都映射到`"/owners/{ownerId}/edit"`这个URL上，前者绑定到是`GET`方法后者是`POST`方法。英文够好的话大概能猜出来前者提取某个Owner信息后放在一个页面上等待用户进行更新操作，后者用POST过来的数据更新某个Owner的信息。如何跟用户沟通这些接口的语意（语意指的是：接口是干什么用的，怎么调用，返回什么，会在什么情况下出现什么错误）呢？这里的用户可能包括测试人员（帮你用[Postman](https://www.getpostman.com/)等测试工具测试你的Controller方法）、页面开发人员（需要知道页面上的链接如何写，Form的Action如何写等）和一般用户（也许有些用户愿意直接访问URL）。这些用户可能看不到或看不懂你的代码，或者不愿意去看你的代码，那唯一的交流方法就是给他们写一个文档。

你为什么会要写这个文档呢？因为你给的接口定义是你自己随意定的，写接口的人和用接口的人之间不存在共同认识，所以写出来的接口用的人看不懂，需要额外写文字说明。这个共同认识应该是什么呢？

<!-- 设计不反映信息世界的本质。一个良好的接口设计，实际上是不需要文档说明的。人甚至机器可以根据接口本身正确产生对其的语意认识。 -->

这个问题实际上在我们现在天天用的HTTP协议设计之初设计者就已经想好了。这个设计者就是[Roy Thomas Fielding](https://en.wikipedia.org/wiki/Roy_Fielding)博士。他是HTTP协议（1.0版和1.1版）的主要设计者、Apache服务器软件的作者之一、Apache基金会的第一任主席。Fielding博士在他2000年发表的博士论文《Architectural Styles and the Design of Network-based Software Architectures》中，提出了一个叫做REST的网络应用架构风格。REST这个词是Representational State Transfer的缩写，中文翻译叫做[表现层状态转换](https://zh.wikipedia.org/zh-hans/%E8%A1%A8%E7%8E%B0%E5%B1%82%E7%8A%B6%E6%80%81%E8%BD%AC%E6%8D%A2)。简而言之，REST是一种设计原则，以便设计实现功能强、性能好、适宜通信的互联网应用系统。

#### 资源

撇开高深的理论不谈，REST架构中给出了互联网应用设计的一个核心思想。回想我们之前所说，我们开发一个信息系统，其目的就是希望能正确有效地管理信息。而互联网应用（或互联网信息系统），就是希望用户可以通过互联网来获得或管理信息。比如早期的静态网站，用户获得的就是一个HTML页面，以及其他相关的图片、视频等资源。对于我们现在看到的petclinic这个系统来说，我们希望用户获得或管理的信息是什么？是Owner、Pet、Vet等。这些信息跟一段视频、一张图片、一段文字本质上是一样的。所以实际上我们可以这么来看：互联网连接的是一个个资源，网络上的一个具体信息、任何事物，只要有被引用到的必要，它就是一个资源。例如：

- 一段文本，一张图片，一首歌曲
- 数据库中的一行数据
- 一个手机号码，某用户的个人信息
- 一种服务

这些都是资源。要让一个资源可以被识别，需要有个唯一标识，在Web中这个唯一标识就是URI(Uniform Resource Identifier)。例如：

- http://www.ex.com/software/releases/latest.tar.gz
- http://www.ex.com/map/roads/USA/CA/17_mile_drive
- http://www.ex.com/search/cs578
- http://www.ex.com/sales/2012/Q1
- http://www.ex.com/relationships/Alice;Bob

为一个资源定义一个标识应该遵循一定的原则：

- 应该易读，例如：`http://www.oschina.net/news/38119/oschina-translate-reward-plan`
- 应该可以表达资源的层级关系，例如：`https://github.com/git/git/commit/e3af72cdafab5993d18fae056f87e1d675913d08/orders/2012/10`，可以用来表示2012年10月的订单记录
- 应该可以表示资源的同级关系，例如：`http:/.../git/block-sha1/sha1.h/compare/e3af72cdafab5993d18fae056f87e1d675913d08; bd63e61bdf38e872d5215c07b264dcc16e4febca`
- 应该可以表达资源的过滤，例如：`https://github.com/git/git/pulls?state=closed`，表示git项目中已经关闭的推入请求

此外，不论什么样的资源，都是通过使用相同的接口进行资源的访问。接口应该使用标准的HTTP方法如GET，PUT和POST，并遵循这些方法的语义。

- GET获：取表示，变更时获取表示（缓存）；
- POST：使用服务端管理的（自动产生）的实例号创建资源，或创建子资源，部分更新资源，如果没有被修改，则不过更新资源（乐观锁）；
- PUT：用客户端管理的实例号创建一个资源，通过替换的方式更新资源，如果未被修改，则更新资源（乐观锁）；
- DELETE：删除资源。

服务方给的响应也是标准的，例如用GET操作时，服务器返回值

- 200（OK） - 表示已在响应中发出
- 204（无内容） - 资源有空表示
- 301（Moved Permanently） - 资源的URI已被更新
- 303（See Other） - 其他（如，负载均衡）
- 304（not modified）- 资源未更改（缓存）
- 400 （bad request）- 指代坏请求（如，参数错误）
- 404 （not found）- 资源不存在
- 406 （not acceptable）- 服务端不支持所需表示
- 500 （internal server error）- 通用错误响应
- 503 （Service Unavailable）- 服务端当前无法处理请求

其他POST、PUT、DELETE类似，此处不赘。

每个资源用规范的URL进行命名，对资源的操作是标准化的四个操作，所有的获取、创建、修改、删除任何一个资源的方式都是规范的，这就叫做**统一接口原则**。

因此回想一下，以前很多时候我们会设计出这样的URI来：

- GET /getUser/1
- POST /createUser
- PUT /updateUser/1
- DELETE /deleteUser/1

这些URL的设计就是不合理的。按统一资源接口要求使用标准的HTTP方法对资源进行操作，URI只应该来表示资源的名称，而不应该包括资源的操作。 通俗来说，URI不应该使用动作来描述。

#### 表现（Representation）／表述／表征

上面说了，“资源”是一种信息实体，它可以有多种外在表现形式。我们把“资源”具体呈现出来的形式，叫做它的“表现层”（Representation）。例如文本可以用txt格式表现，也可以用HTML格式、XML格式、JSON格式表现，甚至可以采用二进制格式，图片可以用JPG格式表现，也可以用PNG格式表现。

我们之前说的URI只代表资源的实体，不代表它的形式。严格地说，有些网址最后的“.html”后缀名是不必要的，因为这个后缀名表示格式，属于“表现层”范畴，而URI应该只代表“资源”的位置。资源的表述包括数据和描述数据的元数据，例如，HTTP头“Content-Type” 就是这样一个元数据属性。客户端可以通过Accept头请求一种特定格式的表述，服务端则通过Content-Type告诉客户端资源的表述形式。例如我们可以分别指定xml或json两种格式要求服务器返回同一个资源的不同表现形式：

{% qnimg webtech/github-json.png %}

{% qnimg webtech/github-xml.png %}

服务器也可以拒绝返回某种不支持的表现形式：

{% qnimg webtech/not-support.png %}

#### 状态转移（State Transfer）

我们在最初使用互联网时首先干的就是浏览网页。当你浏览Web网页时，从一个连接跳到一个页面，再从另一个连接跳到另外一个页面，就是利用了超媒体的概念: 把一个个把资源链接起来。

对于更一般的资源而言，我们可以在表述格式里边加入链接来引导客户端，例如：

{% qnimg webtech/link.png %}

在`Link`头告诉客户端怎么访问下一页和最后一页的记录；在响应体里边，用url来链接项目所有者和项目地址。又例如，我们可以在创建订单后通过链接引导客户端如何去付款：

{% qnimg webtech/link-payment.png %}

这些链接带来了状态转移。

首先明确一下状态这个概念。状态应该区分应用状态和资源状态，客户端负责维护应用状态，而服务端维护资源状态。客户端与服务端的交互必须是无状态的，并在每一次请求中包含处理该请求所需的一切信息。服务端不需要在请求间保留应用状态，只有在接受到实际请求的时候，服务端才会关注应用状态。这种无状态通信原则，使得服务端和中介能够理解独立的请求和响应。在多次请求中，同一客户端也不再需要依赖于同一服务器，方便实现高可扩展和高可用性的服务端。


客户端应用状态在服务端提供的超媒体的指引下发生变迁。服务端通过超媒体告诉客户端当前状态有哪些后续状态可以进入。 
 
#### 完整的故事

看到这儿也许你有点晕，特别时状态转移这件事儿。我们来看一个完整的故事理解一下REST到底说了个什么。

例如我订阅了一个人的博客，想要获取他发表的所有文章（这里“他发表的所有文章”就是一个资源Resource）。于是我就向他的服务发出请求，说“我要获取你发表的所有文章，最好是atom格式的”，这时候服务器向你返回了atom格式的文章列表第一页（这里“atom格式的文章列表”就是表征Representation）。然后？

{% qnimg webtech/story.png %}


- 你看到了第一页的页尾，想要看第二页，这时候有趣的事情就来了。如果服务器记录了应用的状态（stateful），那么你只要向服务询问“我要看下一页”，那么服务器自然就会返回第二页。类似的，如果你当前在第二页，想服务器请求“我要看下一页”，那就会得到第三页。
- 但是REST的服务器恰恰是无状态的（stateless），服务器并没有保持你当前处于第几页，也就无法响应“下一页”这种具有状态性质的请求。因此客户端需要去维护当前应用的状态（application state），也就是“如何获取下一页资源”。
- 当然，“下一页资源”的业务逻辑必然是由服务端来提供。服务器在文章列表的atom表征中加入一个URI超链接（hyper link），指向下一页文章列表对应的资源。客户端就可以使用统一接口（Uniform Interface）的方式，从这个URI中获取到他想要的下一页文章列表资源。
- 上面的“能够进入下一页”就是应用的状态（State）。服务器把“能够进入下一页”这个状态以atom表征形式传输（Transfer）给客户端就是表征状态传输（REpresentational State Transfer）这个概念。

也就是说：服务器生成包含状态转移的表征数据，用来响应客户端对于一个资源的请求；客户端借助这份表征数据，记录了当前的应用状态以及对应可转移状态的方式。

仔细琢磨琢磨，按这个思路去设计系统，是不是不需要写接口文档了？一个没看过你的文档的人甚至机器都能将你提供的资源完全获取得到。

# 前端技术

## 发展历程

### 早期


### Angular

https://github.com/spring-petclinic/spring-petclinic-angularjs.git

https://github.com/spring-petclinic/spring-petclinic-angular

### ReactJS

https://github.com/spring-petclinic/spring-petclinic-reactjs

### VUE