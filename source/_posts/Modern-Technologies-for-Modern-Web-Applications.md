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