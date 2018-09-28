---
title: Jitsi
date: 2018-09-28
tags: aosabook
---

# Jitsi中文翻译 #
## Chapter 10. Jitsi引言 ##
Jitsi是一个允许人们进行视频和语音通话，共享桌面和交换文件和消息的应用。更重要的是它允许人们通过大量不同的的协议，从标准化的 XMPP（可扩展消息和状态协议）和 SIP（会话初始化协议）到专有的如雅虎和 Windows Live信使 (MSN)来做这些事情。它可以在微软视窗、苹果 Mac OSX、Linux，FreeBSD上运行。它大部分是用java编写的，但也包含部分用机器码编写的代码。在本章中，我们将会看到Jitsi 的基于 OSGi 的体系结构，看看它是如何实现和管理协议的，并回顾一下，我们能从构建这个软件中学到什么。
## 10.1.设计 Jitsi（Designing Jitsi） ##
在设计Jitsi（在那时被称为SIP通信器）的时候，我们必须牢记的三个重要约束（限制*constraint*）是：多协议支持、 跨平台的操作和开发者友好性。

从一个开发者的角度来看，多协议实质上是对所有的协议都有一个通用的接口。换句话说，当一个使用者发送消息的时候，不管当前选择的协议是否事实上使用了一个叫做''sendXmppMessage''或者''sendSipMsg''的方法，我们的图形用户界面需要总是调用相同的''sendMessage''方法。

事实是，我们大部分的代码都是在java兼容的基础上写的（*written in java satisfies*满足因素），在很大程度上，我们的第二个限制因素是跨平台操作。尽管如此（*still*），还有java的运行环境（*JRE*）不支持或者不是按照我们喜欢的方式去做的事情，例如从你的网络摄像头获取视频。因此，我们需要在 Windows上使用 DirectShow、而在Mac OS X上使用QTKit，和在linux上使用Video for Linux 2。就像协议一样（*just as with protocols*），控制视频通话部分的代码不能被这些细节干扰（它们本身已经足够复杂了）。

最后，开发者友好意味着人们能够很容易的添加新的特性（*features*）。在今天，有成百上千万的人，通过成千上万的不同方式使用网络电话（*VoIP*）。各种各样的服务提供商和服务器销售商想出了不同的关于新特性的使用案例和创意。我们必须保证对他们来说按照他们的方式使用jitsi是很容易的。某些需要添加一些新的东西的人应该只需要去阅读和理解他们正在修改或扩展的部分的项目（的代码）。相似的，一个人做出的改变应该对任何一个其他人的工作产生尽可能少的影响（*impact*）。

综上所述（*概括地说*），我们需要一个环境，在那里面代码的不同部分之间相对独立（*from each other*）。能够简单地根据操作系统替换一些部分必须是可能的。还有一些，比如说协议，并行运行但实现相同的功能（*act the same*）；完全重写这些部分中的任意一个，而且能够在剩下的部分没有任何改变的情况下工作，必须是可能的。最后，我们想要能够简单地开关各个部分的能力和通过因特网下载插件到我们的列表的能力。

我们简单地考虑了下写我们自己的框架（*framework*），但马上就放弃了这个想法。我们非常渴望尽可能快地开始写网络电话（*VoIP*）和即时通讯（*IM*）的代码，而且花几个月时间来写一个插件框架显得不那么令人兴奋。有的人建议OSGI（*面向Java的动态模型系统*），而且看起这是最适合的了。
## 10.2.Jitsi和OSGI框架（Jitsi and the OSGi Framework） ##
人们已经写过关于OSGI的一整本书，所以我们不会去讲这个框架的一切。取而代之的，我们将只解释这个框架给了我们什么已经我们如何在Jitsi中使用它的。最为重要的是，OSGI是关于模块（*about modules*）的。在OSGI应用中，特征被分成了不同的句柄（*bundles*）。一个OSGI束不仅仅是一个普通的tar文件，例如像那些用来给java库和java应用分类的。Jitsi就是这样的句柄的合集。有一个负责连接到windows实时消息传送（*Live Messenger*），另一个做XMPP，还有另一个处理图形用户界面，等等。所有这些束一起运行在提供给的环境中，在我们这个事例中，也就是通过Apache Felix，一个开源的OSGI实现。

所有这些模块需要共同协作，图形用户界面的那个句柄需要通过协议句柄发送消息，而协议句柄反过来需要通过处理消息历史的束来保存那些消息。这就是OSGI服务存在的原因：它们代表了一个句柄的对任何其他人可见的部分。一个OSGI服务通常是一组允许使用特定功能，例如，登录、通过网络发送消息、或者恢复最近通话记录，的java接口。那些真正实现这些功能的类被叫做服务实现，他们大部分带着实现的服务接口的名字，通过在最后加一个“''Impl''”的后缀（例如''ConfigurationServiceImpl''）。OSGI框架允许开发者隐藏服务实现，因此保证它们在它们所处的句柄的外部是绝对不可见的。这样，其它的束只能通过服务接口使用它们。

大部分的束也有激活器（*activators*），激活器是定义了开始和停止方法的简单的接口。每次Flix加载或者移除一个在Jitsi里面的句柄，它便调用这些方法，从而使得这个句柄能够提前准备运行或者关闭。当调用这些方法的时候， Flix传给它们一个叫做句柄环境（*BundleContext*）的参数，句柄环境给了句柄连接OSGI环境的一个方式。这样，它们就能找到任何它们需要使用的OSGI服务或者它们自己注册一个（图10.1）。

图10.1：OSGI句柄的激活

![](http://aosabook.org/cdn/images/aosabook/jitsi/OSGI.png)

那么让我们看一下它真正是怎么工作。想象一个不停地存储和恢复特性（*properties*）的服务，在Jitsi里面我们把它叫做配置服务（*ConfigurationService*），像下面的代码所示的那样：
```
package net.java.sip.communicator.service.configuration;

public interface ConfigurationService
{
  public void setProperty(String propertyName, Object property);
  public Object getProperty(String propertyName);
}
```
一个配置服务的非常简单的实现如下所示：
```
package net.java.sip.communicator.impl.configuration;

import java.util.*;
import net.java.sip.communicator.service.configuration.*;

public class ConfigurationServiceImpl implements ConfigurationService
{
  private final Properties properties = new Properties();

  public Object getProperty(String name)
  {
    return properties.get(name);
  }

  public void setProperty(String name, Object value)
  {
    properties.setProperty(name, value.toString());
  }
}
```
注意在''net.java.sip.communicator.service''包中，这个服务是怎么定义的，与此同时，实现是在''net.java.sip.communicator.impl''中实现的。所有在Jitsi中的服务和实现都是被分开像这样的两个包下。OSGI允许句柄只让一些包在它们的JAR外面是可见的。所以这种隔离使得句柄能够很容易地提供它们的服务，同时隐藏它们的实现。

为了让人们能够开始使用我们的实现，我们最后需要做的事情是在句柄环境（''BundleContext''）中注册它并且指出它给出了配置服务的一个实现，下面演示了如何做到这一点：
```
package net.java.sip.communicator.impl.configuration;

import org.osgi.framework.*;
import net.java.sip.communicator.service.configuration;

public class ConfigActivator implements BundleActivator
{
  public void start(BundleContext bc) throws Exception
  {
    bc.registerService(ConfigurationService.class.getName(), * service name
         new ConfigurationServiceImpl(), * service implementation
         null);
  }
}
```
一旦''ConfigurationServiceImpl''这个类在束环境（''BundleContext''）中注册了，其它的束能够开始使用它。这里是一个例子，展示了一些随机句柄是如何能够使用我们的配置服务的：
```
package net.java.sip.communicator.plugin.randombundle;

import org.osgi.framework.*;
import net.java.sip.communicator.service.configuration.*;

public class RandomBundleActivator implements BundleActivator
{
  public void start(BundleContext bc) throws Exception
  {
    ServiceReference cRef = bc.getServiceReference(
                              ConfigurationService.class.getName());
    configService = (ConfigurationService) bc.getService(cRef);

    * And that's all! We have a reference to the service implementation
    * and we are ready to start saving properties:
    configService.setProperty("propertyName", "propertyValue");
  }
}
```
再一次注意这个在''net.java.sip.communicator.plugin''中的包，我们使得束能够使用在其它束中定义的服务但是既不输出也不实现它们中的任何一个。配置表（*Configuration forms*）是这样的插件的一个很好的例子：它们是Jitsi用户界面的补充以允许用户能够配置应用的某些方面。当用户改变他们的喜好的时候，配置表与配置服务（''ConfigurationService''）交互或者直接与负责一个特征的句柄交互。然而其它句柄没有一个需要与它们以任何方式交互（图10.2）

图10.2服务结构

![](http://aosabook.org/cdn/images/aosabook/jitsi/PKGs.png)

## 10.3.构建和运行一个句柄（Building and Running a Bundle） ##
既然我们已经知道如何在一个句柄里面写代码，接下来让我们谈一下包。所有的句柄在运行的时候需要给OSGi环境指示三个不同的东西，对其他人可见的java包（例如外部包），还有他们想要从其它人那里使用的包（例如输入包），还有他们句柄激活器类的名字。句柄通过他们将要被部署进的jar文件的证明来做这件事情。

对于我们上面定义的ConfigurationService，它的证明文件可能如下：

```
Bundle-Activator: net.java.sip.communicator.impl.configuration.ConfigActivator
Bundle-Name: Configuration Service Implementation
Bundle-Description: A bundle that offers configuration utilities
Bundle-Vendor: jitsi.org
Bundle-Version: 0.0.1
System-Bundle: yes
Import-Package: org.osgi.framework,
Export-Package: net.java.sip.communicator.service.configuration
```

在创建了jar证明之后，我们可以来创建句柄本身。在Jitsi里面我们使用Apache Ant来处理所有构建相关的任务。为了给Jitsi的构造程序添加一个句柄。你需要在项目的根目录里面编辑build.xml文件。句柄JARs在build.xml文件的底部创建，伴随着一个bundle-xxx的目标。为了构建我们的配置服务，我们需要下面的代码：

```
<target name="bundle-configuration">
  <jar destfile="${bundles.dest}/configuration.jar" manifest=
    "${src}/net/java/sip/communicator/impl/configuration/conf.manifest.mf" >

    <zipfileset dir="${dest}/net/java/sip/communicator/service/configuration"
        prefix="net/java/sip/communicator/service/configuration"/>
    <zipfileset dir="${dest}/net/java/sip/communicator/impl/configuration"
        prefix="net/java/sip/communicator/impl/configuration" />
  </jar>
</target>
```

就像你看到的那样，这个Ant目标使用我们的配置证明简单地创建了一个JAR文件并且把它加入到了来自service和impl层的配置包里面。现在我们需要做的唯一一件事情就是让Felix加载它。

我们已经提到Jitsi仅仅是一个OSGi句柄的集合。当一个使用者执行这个应用时。他们事实上通过一系列它需要加载的句柄来启动Felix。你能够在我们的lib目录里面的一个叫做felix.client.run.properties的文件里面发现那个清单。Felix根据启动等级来启动句柄：所有这些在一个特定的等级是为了保证在子等级句柄开始加载的前面完成。虽然你不能在上面的举例代码里面看到这些，我们的配置服务把属性存在文件里面，从而它需要使用我们的FileAccessService，这个东西在fileaccess.jar文件里面发出。因此我们能够确认ConfigurationService在FileAccessService后面启动。

```
?    ?    ?
felix.auto.start.30= \
  reference:file:sc-bundles/fileaccess.jar

felix.auto.start.40= \
  reference:file:sc-bundles/configuration.jar \
  reference:file:sc-bundles/jmdnslib.jar \
  reference:file:sc-bundles/provdisc.jar \
?    ?    ?
```
如果你看一下felix.client.run.properties文件，你会在开始看到一系列包;

```
org.osgi.framework.system.packages.extra= \
  apple.awt; \
  com.apple.cocoa.application; \
  com.apple.cocoa.foundation; \
  com.apple.eawt; \
?    ?    ?
```
这个清单告诉Felix它需要使什么包对于来自系统类路径的句柄是可见的。这就意味着在这个清单上的包能够被句柄导入且没有任何被其它句柄导出的包（例如加入到他们的Import-Package证明头文件）。这个清单大多包含了来自OS-specific JRE的部分的包，以及Jitsi开发者很少加入新的包的包；在大多数情况下，包被设置为对句柄可见的。

## 10.4.协议提供者服务（Protocol Provider Service） ##
ProtocolProviderService定义了在Jitsi里面所有协议实现行为的方法。它是所有其它句柄（例如用户界面）当他们需要通过Jitsi连接的网络发送和接受信息，打电话以及分享文件时使用的接口。

这些协议服务接口都能在net.java.sip.communicator.service.protocol包里面发现。它们是服务的多重实现，每个支持的协议有一个，而且所有都存在net.java.sip.communicator.impl.protocol.protocol_name里面。

让我们从sevice.protocol目录开始。最为突出的一个是这个ProtocolProviderService接口。一旦当某个人需要执行一个协议相关的任务的时候，它们就去在BundleContext里面找一个那个服务的实现。这些服务和它们的实现让Jitsi能够连接到任何支持的网络来检索连接状态和细节以及最为重要的是获取真正实现了沟通任务例如聊天和打电话的实现的类的引用。

### 10.4.1.操作集合 ###
就像我们先前提到的那样。 ProtocolProviderService需要给各种各样的沟通协议和它们的不同点划分等级。然而这个对于所有协议共享的特点尤其简单，例如发送信息，对于只有一些协议支持的任务事情变得复杂多了。有时候这些不同来自服务本身：例如大部分SIP服务不支持服务器存储联系人列表，但这个对所有其它协议来说相对都被很好地支持了。MSN和AIM是另外的很好地例子：一方面他们没有一个提供对离线用户发送消息的能力，但是所有其它的却可以做到（这个已经被改变了）

底线是我们的ProtocolProviderService需要有一个方法处理这些不同，所以其他句柄，例如GUI，相对执行；给一个AIM联系人加一个打电话按钮是没有意义的，如果没有方法来实际上打一个电话。

对于营救的操作集合（图10.3）.不那么令人吃惊的是，他们是操作的集合，并且提供Jitsi句柄用来控制协议实现的接口。你在一个操作集合接口里面发现的方法都和一个特定的特征相关联。例如OperationSetBasicInstantMessaging包含了创建和发送实时信息以及注册允许Jitsi来检索收到的信息的方法。另一个例子是，OperationSetPresence有一些用来询问你的列表里面的联系人的状态以及为你 设置一个状态的方法。所以当GUI更新它显示的一个联系人的状态或者给一个联系人发送消息的时候。它最先能够询问相对应的提供者他们是否支持在线和发送消息，这个ProtocolProviderService为那个目的定义的方法如下：
```
public Map<String, OperationSet> getSupportedOperationSets();
public <T extends OperationSet> T getOperationSet(Class<T> opsetClass);
```

### 10.4.2.账户，工厂以及提供者实例 ###


## 10.5.媒体服务（Media Service） ##
当通过IP与实时聊天系统打交道时，有一个需要理解的很重要的事情：像SIP和XMPP那样的协议，虽然被很多人看做是普通的网络通话协议，实际上不是那些通过因特网传送语音和视频的协议。这个任务是被实时传输协议（RTP）处理的。SIP和XMPP仅仅负责为RTP准备所有需要的东西，比如说决定RTP数据包需要发送到的地址，还有协商音频和视频被编码的格式（也就是codec），等等。它们也处理例如定位使用者、维护他们的使用（*presence*）、使电话响铃很多很多...这就是为什么像SIP和XMPP这样的协议经常被指作是信号（*signalling*）协议。

这在Jitsi的语境中是什么意思？好，首先它的意思是你在SIP和JabberJitsi包中都不会发现任何控制音频和视频流的代码。这类代码存在在我们的媒体服务（*MediaService*）里面。媒体服务和它的实现在''net.java.sip.communicator.service.neomedia''和''net.java.sip.communicator.impl.neomedia''里面。

^  **为什么neomedia？**  ^
| 在neomedia中的neo指它代替了我们最初使用但之后必须完全重写的一个相似的包。这是事实上就是我们想出一个大拇指规则的方法（*rules of thumb*）：几乎从来不值得花很多时间来设计一个百分之百预见未来（*future-proof*）的应用。很显然没有办法把所有事情都考虑到，所有你无论如何注定必须在之后做改变。另外很有可能一个煞费苦心（*painstaking*）设计的部分会给你带来那些你永远不需要的复杂性，因为你准备的情况绝对不会发生。 |

除了媒体服务本身以外，有两个尤其重要的接口：媒体设备（*MediaDevice*）和媒体流（*MediaStream*）。
### 10.5.1. 捕获、流动和回放（Capture, Streaming, and Playback） ###
媒体设备代表了我们在一个电话期间使用的捕获和回放设备（图10.4）。你的麦克风和扬声器，你的耳机和网络摄像头都是这种媒体设备的例子，但是它们不是所有媒体设备。一个电话会议使用一个音频混合设备（*AudioMixer*）为了混合从积极地参与者那里收到的语音，与此同时在jitsi中桌面流和共享通话从你的桌面端抓取视频。在所有的实例中，媒体设备仅代表了一种单一的媒体类型。也就是说，他们只能要么是音频要么是视频，不能同时两者都是。这意味着，举例来说，如果你有一个集成了麦克风的网络摄像头，Jitsi把它们看成两个设备：一个只能抓取视频，另一个只能抓取声音。

然而，单独的设备不足够用来打一个电话或视频通话。除了播放和抓取媒体，一个设备必须同时能够通过网络发送他们。这就是媒体流的出处。一个媒体流接口是用来把一个媒体设备连接到你的对话者（*interlocutor*）。它代表了在一个通话中你交换的进来和出去的数据包。

和设备一样，一个流只可以负责一个媒体类型。这意味着以防音频/视频通话，Jitsi必须创两个分开的媒体流然后分别连接到对应的音频或者视频媒体设备。

图10.4：不同设备的媒体流

![](http://aosabook.org/cdn/images/aosabook/jitsi/Media.png)
### 10.5.2. 多媒体数字信号解码器（Codecs） ###
另一个在媒体流中的重要概念是关于媒体格式的（
MediaFromats
），也被叫做codecs。默认情况下，大部分操作系统让你能够通过48KHzPCM抓取音频或者类似的东西。这就是我们经常说的“原声（
raw audio
）”而且你从WAV文件中获取的音频类型是：高质量和巨大的尺寸。 用PCM格式通过因特网尝试和传输音频是非常不切实际的。

这就是codecs存在的意义：他们让你通过一系列不同的方式提交和传输音频或者视频。一些音频codecs例如iLBC，8KHz Speex，或者G.729，有着很低的带宽需要但是声音有点模糊。另外的例如wideband Speex和G.722给呢绝佳的音频质量但是同时也需要更多的带宽。有一些codecs尝试传送高质量音频的同时保持带宽在一个合理的层次。H.264，流行的视频codec，就是一个很好地例子。不过用来交换的是会议期间需要的计算数量。如果你使用Jitsi来进行一场H.264视频通话，你将会看到一个质量很好地图像，而且你的带宽需求也相当合理，但是你的CPU在高速运转。

所有这些都是过度单纯化的想法，但是想法是codec的选择全都是关于妥协的。你或者牺牲带宽，质量，CPU强度，或者这些的组合。使用VoIP工作的人们很少需要知道更多关于codecs的东西。
### 10.5.3. 连接协议提供者（Connecting with the Protocol Providers） ###
当前在Jitsi中支持音频/视频的协议都通过相同的方式使用我们的媒体设备。首先他们询问媒体设备关于系统中有的设备：

''public List<MediaDevice> getDevices(MediaType mediaType, MediaUseCase useCase);''


媒体类型（*MediaType*）指出了我们队音频还是视频感兴趣。媒体使用事例（*MediaUseCase*）参数目前只在视频设备中被考虑。它告诉媒体设备我们是否想要获取能够在一个通常的电话（*MediaUseCase.CALL*）中使用的设备，在这个事例中，它返回一个可用的网络摄像头的列表，或者一个桌面共享的会话管理器（*session*）（*MediaUseCase.DESKTOP*）在这个事例中它返回用户桌面的引用。

接下来的一步就是获得一个对一个特定设备可用的格式列表。我们通过`MediaDevice.getSupportedFormats`方法做这件事：

''public List<MediaFormat> getSupportedFormats();''\
一旦它有了这个列表，协议实现就把它发送给远程集团（*party*），这个集团回复它们中的一个子集来表示它支持哪些。这个交互也被叫做提供/答复（*Offer|Answer*）模型，而且它经常使用会话管理器描述协议（*Session Description Protocol*）或者它的某个形式。

在交换了格式和一些端口号和IP地址后，VoIP协议创建、配置和开始流媒体，粗略地说，这个初始化过程和下面的代码一起：
```
/ first create a stream connector telling the media service what sockets
* to use when transport media with RTP and flow control and statistics
* messages with RTCP
StreamConnector connector =  new DefaultStreamConnector(rtpSocket, rtcpSocket);
MediaStream stream = mediaService.createMediaStream(connector, device, control);

* A MediaStreamTarget indicates the address and ports where our
* interlocutor is expecting media. Different VoIP protocols have their
* own ways of exchanging this information
stream.setTarget(target);

* The MediaDirection parameter tells the stream whether it is going to be
* incoming, outgoing or both
stream.setDirection(direction);

* Then we set the stream format. We use the one that came
* first in the list returned in the session negotiation answer.
stream.setFormat(format);

* Finally, we are ready to actually start grabbing media from our
* media device and streaming it over the Internet
stream.start();
```
现在你可以在你的网络摄像头前摇摆，抓着麦克风说“Hello world!”
## 10.6.用户界面服务（UI Service） ##
迄今为止，我们已经讲完了Jitsi处理协议，发送和接受消息以及打电话的部分。然而，更为重要的是，Jitsi是被真实的人以及类似的使用的应用程序，它其中一个最为重要的方面是Jitsi的用户界面。用户界面使用设备的大部分时间，其它所有在Jitsi中的句柄都暴露了。然而有些情况，事情却正好相反。

插件是第一个能想到的例子。在Jitsi中的插件经常需要能够和用户交互。这意味着它们必须在用户界面中打开、关闭、移动或者添加组件给当前的窗口和面板。这就是我们的UI服务起作用的地方。在Jitsi中它允许在主窗口上的基本的控制，并且这也是在MAC OS X中我们的图标停驻的方式，而且窗口通知区域让用户能控制应用程序。

除了和联系人列表简单互动之外，插件也可以扩展它。在Jitsi中实现了对聊天加密的支持的接口（OTR）就是个很好的例子。我们的OTR句柄在用户界面的各个部分需要注册几个图形界面的部分。他在聊天窗口加了一个挂锁按钮和在所有联系人的右键菜单里的分段（*sub-section*）。

好消息是它能够通过很少的方法调用来做成这件事。OTR句柄的OSGI激活器，''OtrActivator''，包含以下的代码语句：
```
Hashtable<String, String> filter = new Hashtable<String, String>();

* Register the right-click menu item.
filter(Container.CONTAINER_ID,
    Container.CONTAINER_CONTACT_RIGHT_BUTTON_MENU.getID());

bundleContext.registerService(PluginComponent.class.getName(),
    new OtrMetaContactMenu(Container.CONTAINER_CONTACT_RIGHT_BUTTON_MENU),
    filter);

* Register the chat window menu bar item.
filter.put(Container.CONTAINER_ID,
           Container.CONTAINER_CHAT_MENU_BAR.getID());

bundleContext.registerService(PluginComponent.class.getName(),
           new OtrMetaContactMenu(Container.CONTAINER_CHAT_MENU_BAR),
           filter);
```

正如你所看到的，给我们的图形用户界面添加新的组件简单地归结到了注册OSGi服务。另一方面，我们的用户界面服务实现在寻找它的插件组件接口的实现。它一旦探测到一个新的实现被注册了，他就获得对它的引用然后把它加到在OSGi服务过滤器中声明的容器中。

下面演示了在右键菜单项目中这是如何发生的，在UI句柄中，代表了右键菜单的类，''MetaContactRightButtonMenu''，包含了如下的代码行：
```
* Search for plugin components registered through the OSGI bundle context.
ServiceReference[] serRefs = null;

String osgiFilter = "("
    + Container.CONTAINER_ID
    + "="+Container.CONTAINER_CONTACT_RIGHT_BUTTON_MENU.getID()+")";

serRefs = GuiActivator.bundleContext.getServiceReferences(
        PluginComponent.class.getName(),
        osgiFilter);
* Go through all the plugins we found and add them to the menu.
for (int i = 0; i < serRefs.length; i ++)
{
    PluginComponent component = (PluginComponent) GuiActivator
        .bundleContext.getService(serRefs[i]);

    component.setCurrentContact(metaContact);

    if (component.getComponent() == null)
        continue;

    this.add((Component)component.getComponent());
}
```
这就是它的一切。你在Jitsi中看到的大部分窗口准确地做着相同的事情，他们浏览那些实现了有着声明了他们想要被添加为匹配容器的滤波器的插件组件接口服务的句柄环境。插件就像举着写有他们的目的地的标志牌的搭顺风车的人，把Jitsi窗口看成把他们带上的司机。

