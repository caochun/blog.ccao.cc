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


### 领域模型



## 前后端分离架构

<https://github.com/spring-petclinic/spring-petclinic-rest.git>

### REST


# 前端技术

## 发展历程

### 早期


### Angular

https://github.com/spring-petclinic/spring-petclinic-angularjs.git

https://github.com/spring-petclinic/spring-petclinic-angular

### ReactJS

https://github.com/spring-petclinic/spring-petclinic-reactjs

### VUE