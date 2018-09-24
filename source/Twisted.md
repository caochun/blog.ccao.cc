# Twisted #
　　Twisted是用Python实现的事件驱动的网络引擎框架。它诞生于21世纪初，当时，任何语言中供网络游戏开发者们使用的可扩展的、跨平台库很少。Twisted的创作者们试图在当时现有的网络环境下开发游戏，但举步维艰。因此，它们急需一个可扩展的、事件驱动的、跨平台的网络框架。他们吸取以往游戏和网络应用开发者的经验和教训，并着手开发。

　　Twisted支持许多常见的运输层和应用层协议，包括TCP，UDP，SSL/TLS，HTTP，IMAP，SSH，IRC和FTP。就像Python一样，Twisted包括“内置电池”（"batteries-included"）。Twisted为所有这些协议提供了客户端和服务器实现，此外，它可以很方便地在命令行中配置和部署产品级的Twisted应用。

***

## 1 为什么需要 Twisted ##
　　2000年的时候，Twistd的创造者glyph正致力于开发一个叫《Twisted Reality》的基于文字的多人游戏。游戏采用Java编写，有许多线程——每个连接都有3个线程。处理读入的线程会阻塞读入操作；处理输出的线程会阻塞某些写入操作；逻辑处理线程在等待计时器超时或者时间进队列时会睡眠。当玩家们在虚拟世界中移动和交互的同时，线程死锁，缓存冲突，加锁的逻辑从没正确过——线程的使用使得软件非常复杂，错误百出且极难拓展。

　　为了找到替代方案，他发现了Python——尤其是Python中从流对象比如sockes和pipes（Single UNIX Specification, Version 3 (SUSv3)描述了''select''的API）处理多路I/O的''select''模块。在那时，Java没有提供操作系统的''select''接口或者其他异步I/O的API(针对非阻塞式I/O的''java.nio''包2002年在J2SE 1.4版本中发布)。通过Python使用''select''搭建起来的游戏原型证实了这种方法比起多线程版本，要更加简便和可靠。

　　glyph迅速转向了Python，''select''和事件驱动编程——他用Python的'select'API为游戏编写了客户端和服务器。但他并不止步于此。作为基础，他希望能够将网络活动（"network activity"）转变为在游戏中对对象的方法调用。怎样能在游戏中收取邮件，就像Nethack mailer daemon一样？怎样能让每个玩家都有一个主页？Glyph发现他需要好用的IMAP和HTTP客户端和服务器，这些都是用Python的''select''模块。

　　他首先转向了90年代中期开发的一个基于Python的''asyncore''模块的网络服务器编写平台——Medusa。''asyncore''是一个异步处理socket的模块，它在操作系统''select''API的基础上建立了一个调度器和回调接口。

　　对glyph来说这是个振奋人心的发现，但Medusa有两个缺点：
  - 在2001年glyph开始开发Twisted Reality的时候，Medusa已经逐步停止维护了。
  - ''asyncore''对sockets的封装太少了，应用开发者还是需要直接操作sockets。这意味着开发者仍然要仔细考虑可移植性。除此之外，在当时，''asyncore''的Windows支持还存在问题，而glyph还是想要在Windows平台上运行一个图形化客户端。

　　因此，Glyph需要自己实现一个网络平台，他也意识到Twisted Reality已经打开了一个新议题的大门，这和他的游戏一样有趣。

　　后来，Twisted Reality就变成了网络平台Twisted，它可以做到当时Python中网络平台做不到的事情：
  * 使用事件驱动编程取代多线程编程。
  * 跨平台：为主流操作系统提供的事件通知系统提供通用接口。
  * 内置电池（"batteries-included"）：提供流行的应用层协议的实现，因此Twisted对开发者来说很有用。
  * 符合RFC规范——健壮的测试集证实其良好的一致性。
  * 便于一并使用多种网络协议。
  * 可扩展的。

***

## 2 Twisted 的架构 ##

　　Twisted是事件驱动引擎。事件驱动编程在Twisted设计哲学中占有重要地位，因此我们得花一些时间来看一看什么是事件驱动编程。

　　事件驱动编程是一种编程范式，在这种范式中，程序执行顺序由外部事件决定。它的特点是当事件发生时，通过时间循环和回调来执行动作。两个其他常见的编程范式是（单线程）同步和多线程编程。

　　下面用一个例子来比较单线程，多线程和事件驱动编程模型的异同。图表21.1说明了一个在这三种模型下随着时间变化的执行情况。这个程序有3个任务要完成，每一个在等待I/O完成时阻塞自己。阻塞在I/O上花费的时间用灰色标出。

![](/images/56.png)
<html>图表 21.1: 线性模型</html>

　　在程序的单线程同步模型中，任务有序执行。如果一个任务在I/O上被阻塞了一会，所有其他任务不得不等待一直到该任务结束，然后它们依次执行。这种确切的顺序和处理序列是很容易推出的。然而，程序会不必要地变慢，原因在于即使任务不需要相互依赖，它们还是需要相互等待。

　　在多线程模型中，这三个在工作中阻塞的任务分别在独立控制的线程中。这些线程被操作系统管理，并且可能在多处理器上并行运行或者在单处理器上交错执行。这使得一些线程被阻塞在资源上时，其他线程可以继续执行。这经常比类似的同步程序更有时间效率，但是需要写代码来保护可能被多线程同步访问的共享资源。多线程程序更难被推出，因为这类程序不得不通过线程同步机制如锁、可重入函数、线程局部存储或者其他机制来处理线程安全问题，一旦实现不正确可能会导致微妙且令人痛苦的bug。

　　事件驱动版本的程序交错执行3个任务，但只需要单个控制线程。当执行I/O或者其他高代价的操作时，一个回调会在事件循环中被注册，然后当I/O完成后继续执行。这个回调描述了当一个事件完成时怎样处理。事件循环等待事件，并在它们到来时分派给等待中的回调。这允许程序在没有额外线程使用的情况下执行。事件驱动程序更容易被推断，因为程序员不必担心线程安全。

　　事件驱动程序经常是一个好的选择，当处于如下情况时：

  - 多个任务，它们……
  - 高度独立（所以它们不必相互通信、等待），并且……
  - 在等待事件时，部分任务被阻塞。

　　当一个应用要在任务间共享可变数据时这也是个好的选择，因为没有同步处理。

　　网络应用正是有这3个属性，它们使得网络应用非常适合事件驱动编程模型。

### 现有应用的复用 ###
　　当Twisted被创建时，就已经有许多不同网络协议的客户端和服务器存在了。为什么glyph不使用诸如Apache，IRCd，BIND，OpenSSH或者任何其他已经存在的应用，而是选择从头开始实现Twisted。

　　问题在于所有那些服务器实现都有从头写起的网络代码，以c为代表，并且应用代码直接和网络层耦合。这使得它们很难用作库。当它们被一起使用需要被当作黑盒对待，这不给开发者任务复用代码的机会，尤其是那些想要在多协议下暴露数据的人。此外，服务器和客户端实现通常是独立应用，它们不分享代码。扩展这些应用，并且保持跨平台的客户端-服务器兼容相当困难，没有这个必要。

　　有了Twisted，客户端和服务器用Python编写并且界面一致。这使得很多事很简单，例如编写新的客户端和服务器，在客户端和服务器间分享代码，在协议间分享应用逻辑，以及测试代码。

### Reactor（反应堆）模式 ###
　　Twisted实现了*reactor*设计模式，它描述了在单线程环境中从多个源多路分解并分派事件给它们的处理例程。

　　Twisted的核心是reactor事件循环。reactor知晓网络、文件系统、和其他定时器事件。它等待然后处理这些事件，从平台特定行为抽象出来并提供接口，使得响应网络栈中任意事件变得简单。

　　reactor基本实现了：

```
while True:
    timeout = time_until_next_timed_event()
    events = wait_for_events(timeout)
    events += timed_events_until(now())
    for event in events:
        event.process()
```

　　Twisted目前在所有平台上的默认reactor都是基于''poll''API （UNIX规范第3版（SUSv3）中描述）。此外，Twisted支持许多特定平台的高容量且多路复用的API。特定平台的reactor包括基于FreeBSD's''kqueue''机制的KQueue reactor，支持''epoll''接口的系统（目前是Linux 2.6）中的''epoll''reactor，以及基于Windows下的输入输出完成端口的IOCP reactor。

　　轮询实现相关的细节例子，Twisted所关心的包括：

  * 网络和文件系统限制
  * 缓冲表现
  * 如何检测连接丢失
  * 错例下返回值

　　Twisted reactor的实现还考虑正确使用底层的无阻塞API以及正确处理模糊边界情况。Python根本不暴露IOCP API，所以Twisted维护它自己的实现。

### 管理回调链 ###
　　回调是事件驱动程序的基本部分，并且是reactor通知应用事件已经完成的方式。当事件驱动程序增长时，在一个应用中处理成功或错误的事件案例将会更加复杂。不能注册一个正确的回调将会导致程序阻塞在永远不会发生的事件上，并且错误可能需要从网络栈中通过应用的多个层次传送一连串的回调。

　　下面是Python语言的伪代码，让我们通过比较同步和异步版本的URL玩具获取实用的代码，来检验事件驱动程序的一些缺陷。

同步URL获取：

```
import getPage

def processPage(page):
    print page

def logError(error):
    print error

def finishProcessing(value):
    print "Shutting down..."
    exit(0)

url = "http://google.com"
try:
    page = getPage(url)
    processPage(page)
except Error, e:
    logError(error)
finally:
    finishProcessing()
```

异步URL获取：

```
from twisted.internet import reactor
import getPage

def processPage(page):
    print page
    finishProcessing()

def logError(error):
    print error
    finishProcessing()

def finishProcessing(value):
    print "Shutting down..."
    reactor.stop()

url = "http://google.com"
# getPage takes: url, 
#    success callback, error callback
getPage(url, processPage, logError)

reactor.run()
```

　　在异步URL获取中，''reactor()''开始reactor事件循环。在同步和异步模式下，假设''getPage''函数完成页面的检索工作。当检索成功时''processPage''被引用，并且如果在试图检索页面时引起''Exception''，''logError''将被引用。在任何一种情况下，''finishProcessing''将在之后调用。

　　在异步模式下''logError''的回调对应同步模式下''try/except''块中的''except''部分。''processPage''的回调对应着''else''，并且无条件的''finishProcessing''回调对应着''finally''。

　　在同步模式下，代码结构直接显示出有一个''try/except''块，''logError''和''processPage''这两者间只会取其一调用一次，而''finishProcessing''总是会被调用一次。在异步模式下，引用正确的成功和失败案例链是程序员的责任。即使是程序的错误，在''processPage''或者''logError''的回调链之后没有调用''finishProcessing''，reactor将永远不会停止，程序永远不会运行。

　　这个玩具例子暗示了在Twisted最初开发的几年这样的复杂令程序员感到沮丧。Twisted通过发展出一个叫做''Deferred''的对象来回应这种复杂性。

#### Deferred ####
　　''Deferred''对象是一种抽象的概念，即结果还不存在。它还帮助管理结果的回调链。当被一个函数返回，''Deferred''保证在某个时刻这个函数会有一个结果。单返回的''Deferred''包含所有相关的注册事件的回调。所以只有这个对象需要在函数间传递，这样追踪一个对象比独立地管理回调简单得多。

　　''Deferred''s 有一对回调链，一个是成功（回调），另一个是错误（回调）。''Deferred''s 开始拥有两个空链。在事件处理中，每个时刻都为处理成功和失败添加成对的回调。当异步结果到达，''Deferred''将被激活，并且成功以及错误回调将在两个链中被有序地引用。

　　这是异步模式下URL获取使用''Deferred''s的伪代码：

```
from twisted.internet import reactor
import getPage

def processPage(page):
    print page

def logError(error):
    print error

def finishProcessing(value):
    print "Shutting down..."
    reactor.stop()

url = "http://google.com"
deferred = getPage(url) # getPage returns a Deferred
deferred.addCallbacks(success, logError)
deferred.addBoth(stop)

reactor.run()
```

　　在这个模式下，同样的事件处理函数将被引用，但是它们将被单个''Deferred''注册而不是分散在代码各处被当作参数传递给''getPage''。

　　''Deferred''被创建时包括两个回调阶段。首先，在第一阶段''addCallbacks''将''processPage''和''logError''加入它们相关链中。然后在第二阶段中''addBoth''将''finishProcessing''加入两个链中。用图表解释，回调链看起来像图21.2。

![](/images/57.png)
<html>图表 21.2: 回调链</html>

　　''Deferred''s只能被激活一次。试图再次激活它们将会引起''Exception''。这让''Deferred''s的语义更接近那些同步版中的''tyr/except''块，使得处理异步事件容易推断，并且避免了在单个事件中回调多一个少一个而引起的微妙bug。

　　明白''Deferred''s是理解Twisted程序流的一个重要部分。当使用Twisted提供给网络协议的高层次抽象时，根本没有必要直接使用''Deferred''s。

　　''Deferred''抽象功能强大并且被许多其他事件驱动平台所借鉴，包括jQuery，Dojo和Mochikit。

### 传输 ###
　　Transports代表在网络上两个终端通信的连接。Transports负责描述连接细节，例如是面向流式的还是面向数据报的，流控制和可靠性。TCP，UDP和UNIX套接字是transports的例子。它们被设计为“满足最小功能单元，同时具有最大程度的可复用性”，而且从协议实现中分离出来，这让许多协议可以采用相同类型的传输。Transports实现了''ITransports''的界面，它有下列的方式：
| | |
|-|-|
| ''write'' | 以非阻塞的方式按顺序依次将数据写到物理连接上 |
| ''writeSequence'' | 将一个字符串列表写到物理连接上 |
| ''loseConnection'' | 将所有挂起的数据写入，然后关闭连接 |
| ''getPeer'' | 取得连接中对端的地址信息 |
| ''getHost'' | 取得连接中本端的地址信息 |

　　把transports从协议中分离出来也使得测试两个层次变得容易。一个模拟transport能简单地写入一个字符串来检测。

### 协议 ###
　　Protocols描述了怎样异步处理网络事件。HTTP，DNS以及TMAP是应用协议的例子。Protocols实现了''IProtocol''界面，它有下列的方式：

| | |
|-|-|
| ''makeConnection'' | 在运输和服务器间建立连接 |
| ''connectionMade'' | 连接建立时调用 |
| ''dataReceived'' | 数据接收时调用 |
| ''connectionLost'' | 连接关闭时调用 |

　　reactor，protocol和transport之间的关系可以用一个例子很好地阐释。下面是一个echo服务器、客户端的完整实现，首先是服务器：

```
from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        # As soon as any data is received, write it back
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()
```

　　然后是客户端：

```
from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
   def connectionMade(self):
       self.transport.write("hello, world!")

   def dataReceived(self, data):
       print "Server said:", data
       self.transport.loseConnection()

   def connectionLost(self, reason):
       print "connection lost"

class EchoFactory(protocol.ClientFactory):
   def buildProtocol(self, addr):
       return EchoClient()

   def clientConnectionFailed(self, connector, reason):
       print "Connection failed - goodbye!"
       reactor.stop()

   def clientConnectionLost(self, connector, reason):
       print "Connection lost - goodbye!"
       reactor.stop()

reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run()
```

　　运行服务器脚本，开始一个TCP服务器监听端口号为8000的连接。服务器使用''Echo''协议，而且数据经由TCP transport写出。运行客户端产生一个对服务器的TCP连接，回显服务器的反应，然后中断连接并且停止reactor。Factory被用来产生有关两边连接协议的实例。通信在两端是异步的；''connectTCP''负责注册回调到reactor中，以便在数据可获得时得到通知并且从套接字中读取。

### 应用 ###
　　Twisted是用来创建可扩展的，跨平台的网络服务器和客户端的引擎。在生产环境中，以一种标准化的方法来简化部署这些应用的过程对这样一种将被大范围采用的平台来说是很重要的。

　　为此，Twisted开发了Twisted应用基础组件——采用可重用、可配置的方式来部署Twisted应用。这种方式让编程者将应用挂钩到已有工具上来根据各自运行方式自定义，以避免样板化的代码，这包括系统守护进程，日志记录，使用自定义的反应器，分析代码等。

　　该应用的基础架构有四个主要部分：服务，应用，配置管理（通过TAC文件和插件）和''twistd''命令行工具。为了说明这个基础架构，我们要将上一节中介绍的echo服务器转变为应用。

#### Service ####
　　Service可以被开始和停止，并实现了IService接口。Twisted实现了TCP，FTP，HTTP，SSH，DNS等许多协议。很多Service都可以通过单个应用来注册。

　　IService接口的核心是：

| | |
|-|-|
| ''startService'' | 开始当前服务。这包括加载配置数据，建立数据库连接和监听某个端口 |
| ''stopService'' | 关闭当前服务。这包括将状态归档，关闭数据库连接和停止监听某个端口 |

　　我们的echo服务使用TCP，因此我们可以使用 Twisted 中 IService 接口下默认的 TCPServer 实现。

#### 应用 ####
　　Application 指的是代表整个Twisted应用的顶层服务。Services 通过 Application 注册，下面描述的部署工具 twistd 搜索并运行应用。

　　我们将要创建一个echo应用，echo服务通过它来注册。

#### TAC 文件 ####
　　当在一个常规的 Python 文件中管理 Twisted 应用时，开发者需要编写代码来开始和终止 reactor 来配置应用。在 Twisted 应用基础组件中，协议的实现在一个模块中实现。使用这些协议的 Services 在 TAC (Twisted Application Configuration) 文件中注册。reactor 和配置由一个外部工具来管理。

　　为了让我们的 echo 服务器变成 echo 应用。我们可以执行一个简单的算法：

  - 将echo服务器的 Protocol 部分移到它们各自的模块中去。
  - 在 TAC 文件中：
    - 创建一个echo应用。
    - 创建一个''TCPServer''Service的实例，它将使用我们的''EchoFactory''，然后通过前面创建的应用完成注册。

　　管理reactor的代码由twistd来维护，这个内容在下面讨论。这个应用的代码最终将会是这样：

　　''echo.py''文件：
```
from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
    return Echo()
```

　　''echo_server.tac''文件：
```
from twisted.application import internet, service
from echo import EchoFactory

application = service.Application("echo")
echoService = internet.TCPServer(8000, EchoFactory())
echoService.setServiceParent(application)
```

#### twistd ####
　　''twistd'' (pronounced "twist-dee") 是一个用来部署Twisted应用的跨平台工具。它执行TAC文件并启动和终止应用。作为Twisted网络编程中“内置电池”的一部分，''twistd''带有许多有用的配置标记，包括使应用变为守护进程，定位日志文件，设定权限级别，在chroot下运行，使用非默认的reactor，或者在profiler下运行应用。

　　我们可以这样运行我们的echo服务应用：
```
$ twistd -y echo_server.tac
```

　　在这个简单的案例中，twistd启动了应用的一个守护进程实例，日志记录在twistd.log中。在启动和停止应用之后，日志会是这样：
```
2011-11-19 22:23:07-0500 [-] Log opened.
2011-11-19 22:23:07-0500 [-] twistd 11.0.0 (/usr/bin/python 2.7.1) starting up.
2011-11-19 22:23:07-0500 [-] reactor class: twisted.internet.selectreactor.SelectReactor.
2011-11-19 22:23:07-0500 [-] echo.EchoFactory starting on 8000
2011-11-19 22:23:07-0500 [-] Starting factory <echo.EchoFactory instance at 0x12d8670>
2011-11-19 22:23:20-0500 [-] Received SIGTERM, shutting down.
2011-11-19 22:23:20-0500 [-] (TCP Port 8000 Closed)
2011-11-19 22:23:20-0500 [-] Stopping factory <echo.EchoFactory instance at 0x12d8670>
2011-11-19 22:23:20-0500 [-] Main loop terminated.
2011-11-19 22:23:20-0500 [-] Server Shut Down.
```

　　通过Twisted应用基础组件来运行服务使得开发人员能够不用再编写类似守护进程和记录日志这样的模块化代码。这也为部署应用建立起一个标准命令行接口。

#### 插件 ####
　　除了基于TAC的系统，还有一种方法运行Twisted应用——插件系统。TAC系统通过一个应用配置文件简化了注册预定义服务的过程。插件系统同样方便地将为自定义服务注册为''twistd''工具子命令，并扩展了应用程序的命令行接口。

　　使用插件系统时：
  - 只要 plugin API 需要保持稳定，这方便了第三方开发者扩展软件。
  - 集成了插件发现能力。当程序第一次运行时插件可以被夹在并保存，或者每次重新触发被重新发现，或者运行时刻反复轮询。这允许在程序启动后发现安装的新插件。

　　通过Twisted插件系统来扩展程序，只需要创建实现了''IPlugin''接口的对象并把它们放到插件系统便于寻找它们的特定的位置。

　　将echo服务转换为一个Twisted应用之后，将其转换为Twisted插件也很直接。在我们之前的''echo''模块中，包含了''Echo''协议和''EchoFactory''定义，我们还加入了一个名为''twisted''的目录，它包含了名为''plugins''的子目录，子目录中包含了我们的echo插件定义。这个插件将允许我们启动一个echo服务器，并通过参数的方式为''twistd''工具指明需要使用的端口号：
```
from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet

from echo import EchoFactory

class Options(usage.Options):
    optParameters =  "port", "p", 8000, "The port number to listen on." 

class EchoServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "echo"
    description = "A TCP-based echo server."
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        return internet.TCPServer(int(options["port"]), EchoFactory())

serviceMaker = EchoServiceMaker()
```

　　现在，我们的echo服务器将会作为''twistd --help''输出结果中的一个服务器选项。运行''twistd echo --port=1235''将会启动在端口号为1235上的echo服务器。

　　Twisted还带有一个可拔插的针对服务器的认证系统''twisted.cred''。插件系统常见的用途就是为一个应用添加认证模式。我们可以使用''twisted.credAuthOptionMixin''来为各种不同的认证类型增加命令行支持，或者增加新的认证类型。举例来说，我们可以使用插件系统来添加基于本地Unix密码数据库或LDAP服务器的认证。

　　''twistd''还带有许多Twited支持的协议的插件，这使启动服务器的工作只需要一行命令。这里有几个附带Twisted的''twistd''服务器的例子：

　　''twistd web --port 8080 --path .''

　　启动8080端口的HTTP服务器，在当前工作目录中负责处理静态和动态页面请求。

　　''twistd dns -p 5553 --hosts-file=hosts''

　　启动5553端口的DNS服务器，用''/etc/hosts''中的格式解析''hosts''文件中的域名

　　''sudo twistd conch -p tcp:2222''

　　启动2222端口的ssh服务器。ssh密钥必须单独指定。

　　''twistd mail -E -H localhost -d localhost=emails''

　　启动ESMTP POP3服务器，为本机接收邮件并保存至''emails''目录中。


　　''twistd''使得为测试客户端搭建一个服务器很容易。但它同样是可插拔的、产品级的代码。

　　从这个角度看，Twisted通过TAC文件，插件和''twistd''的应用程序部署机制很成功。然而，据信，大多数大型Twisted部署不得不重写一些这类的管理和监控组件。Twisted的架构并没有完全满足系统管理员的需求。这也反映了一个事实，那就是Twisted并不曾从那些专精于部署和维护应用的系统管理员那里得到建设性的建议。

　　在这方面，Twisted应该在未来建设架构的时候积极地从专家和终端用户那里获取可靠的反馈。

***

## 3 反思和教训 ##
　　Twisted刚走过十年。自从该项目成立以来，收到了二十一世纪早期网络游戏启发，如今它已经在很大程度上实现了作为一个可扩展，跨平台，事件驱动网络引擎的目标。Twisted在谷歌、卢卡斯电影、Jstin.TV和Launchpad软件合作平台等生产环境中被广泛使用。Twisted中的服务器实现是许多其他开源应用的核心，比如BuildBot，BitTorrent和Tahoe-LAFS等。

　　Twisted自从最初开发以来只有几次主要结构上的变动。其中一个主要的增加就是上面讨论的''Deferred''，它是作为管理延后结果和它们的回调链。

　　还有一次重要的移除——Twisted应用持久化在目前的实现中已经难觅踪影。

### Twisted 应用持久化 ###
　　Twisted 应用持久化（TAP）曾将应用配置和状态保存在pickle中。用这种方式启动应用有两个步骤：

  * 创建一个代表一个应用的pickle，使用现在已经废弃的''mktap''工具。
  * 使用''twisted''来进行unpickle操作并启动应用。

　　这个过程受到Smalltalk images的启发，因为我们讨厌那种难以编写的专设配置语言，不希望它们在项目中扩散。我们希望用Python来表示配置细节。

　　TAP文件很快引入了不希望出现的复杂性。在Twisted中改变类可能这些类的实例并没有在pickle中得到改变。在Twisted新版本中在pickle对象上使用类方法和属性可能导致应用崩溃。因此，"upgrader"的概念被引入用来升级pickles到新的API版本。但这样，就必须维护很多upgraders，pickle版本和单元测试来覆盖所有可能的升级路线，想全面地跟踪所有接口变化依然很难而且容易出错。

　　TAP以及相关的组件全部被废除了，最终从Twisted中完全去除掉。取而代之的是TAC文件和插件系统。TAP这个缩写被重新定义为Twisted应用插件（Twisted Application Plugin），如今已经很难在Twisted中找到pickle系统的踪迹了。

　　TAP失败的教训是：如果可维护性要达到合理化的程度，则持久性数据就需要有一个明确的模式。更一般的是，我们学到了如何为项目增加复杂度：当为了解决问题而需要引入一个新系统时，我们要正确理解这个方案的复杂性，并经过测试。在将方案付诸于项目前，我们要确保新系统所带来的价值应该明显大于其复杂性。

### web2：重写的教训 ###
　　项目管理关于重写Twisted Web实现的决策对于Twisted的外在形象以及代码维护者对代码库中其他部分的结构性改善的能力有着长远的影响，尽管不是主要的结构上的决策，但也值得讨论。

　　在21世纪初，Twisted的开发者决定完全重写''twisted.web''的API，在Twisted代码库中将其作为一个单独的项目实现，这就是''web2''。''web2''在''twisted.web''的基础上包含了诸多改善，包括完整的HTTP 1.1支持和流式数据的API。

　　''web2''本只是试验性的，但最终为大型项目采用，甚至意外地被Debian系统上打包并发布了。''twisted.web''和''web2''的开发一直并行持续了多年，新用户常常被这两个同时出现的项目搞混，关于究竟应该使用哪种实现也缺乏明确的提示，这使得新用户很沮丧。然而从未转换到''web2''，终于在2001年''web2''从代码库和网站中被移除了。''web2''中的一些改善也慢慢被移植会了''web''中。

　　''web2''也部分导致Twisted招致难以导航和对新用户结构上不友好的恶名。许多年后，Twisted社区依旧难以摆脱这个坏印象。

　　''web2''的教训是：从头开始重构一个项目通常都是不好的做法。但如果必须这么做，请确保开发者社区能够懂得这么做的长远意义，而且在重写期间要确保在用户社区中要有明确的选择某种实现。

　　如果Twisted得以回到过去并重做一次''web2''，开发者应该弃用''twisted.web''并做一系列向后兼容的修改，而不是重写。

### 紧跟互联网步伐 ###
　　我们使用互联网的方式还在持续演进中。实现多种协议作为软件核心的决策使得Twisted负担重重——它需要维护所有这些协议的代码。当标准和新协议被采纳时，实现需要及时跟进并保持严格的向后兼容性。

　　Twisted主要是一个志愿者驱动型项目，项目发展的限制因素不是社区的热情，而在于志愿者的时间。举例而言，RFC 2616中定义的HTTP 1.1在1999年发布，而在2005年的时候在Twisted中HTTP协议添加HTTP 1.1支持的工作才开始。这项工作直到2009年结束。1998年在RFC 2460中定义的对IPv6的支持仍在进行中但2011年还没有合并。

　　随着所支持的操作系统的接口改变，实现也要跟着演进。比如，''epoll''事件通知机制是在2002年加入到Linux 2.5.44版中的，Twisted随之也发展出基于''epoll''的reactor事件循环来利用这个新的系统接口。2007年时，苹果公司发布的OS 10.5 Leopard系统中，系统调用''poll''的实现不支持外设，对于苹果公司来说这个问题足以让他们在系统自带的Python中屏蔽掉''select.poll''接口。Twisted不得不自行解决这个问题，并从那时起就对用户提供文档说明。

　　有时候，Twisted的开发并没有紧跟网络世界的变化，有一些改进被移到核心层之外的程序库中去了。比如Wokkel project，这是对Twisted的Jabber/XMPP支持的改进合集，已经作为“待合入”的独立项目有几年之久了，但还没有看到合入的希望。在2009年也曾经尝试过增加WebSocket到Twisted中，因为浏览器已经开始采纳对新协议的支持了。但开发计划最终却转到其他外部项目中去了，因为开发者们决定暂不包含新的协议，直到IETF把它从草案转变成标准以后再说。

　　所有这一切都在说明，库和附加组件的扩散有力的证明了Twisted的灵活性和可扩展性。通过采用严格的测试驱动开发策略以及文档化和编码规范标准，使项目避免回退。在维护大量所支持的协议和平台的同时保持了向后兼容性。Twisted是一个成熟、稳定的项目，将持续具有活跃的开发状态。

　　Twisted期待着在下一个十年里成为你遨游互联网的引擎。



***

> 原文：http://aosabook.org/en/twisted.html
