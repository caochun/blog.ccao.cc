---
title: Violet
date: 2018-09-28
tags: aosabook
---

# 作者的话 #

2002年，我写了一本关于面向对象设计与模式的本科教材 http://www.aosabook.org/en/bib1.html#bib:horstmann:oodp|Hor05。 和很多书一样，写这本书的动力也源于我对经典课程的失望。一般来说，计算机科学专业的学生，会在他们的第一门编程课上，学习如何设计一个独立的类。然后，直到在高年级的软件工程课中，他们才在面向对象设计方面接受更多的训练。在那门课程中，学生在几个星期内匆忙地学习UML和设计模式，最终也只是走马观花。我这本书是为一个学期的课程准备的，学生需要具备一些Java编程和基本数据结构的知识（通常这些知识来自基于Java的CS1或CS2课程安排①）。这本书在学生所熟悉的内容中涵盖了面向对象设计原则和设计模式的内容。比如用Swing里面的''JScrollPane''类来介绍修饰模式（DecoratorPattern），目的是希望这个例子比经典的Java流的例子更容易让人记住。
> ①译者注：这是国外的计算机专业的课程模式

![图22.1：Violet里的对象图（Object Diagram）](http://www.aosabook.org/cdn/images/aosabook/violet/object-sample.png)

在这本书里，我需要一种轻量级的UML，包括类图、时序图，以及能够显示出Java对象引用的一种对象图（见图22.1）。我还想让学生能够绘制他们自己的UML图。然而，像Rational Rose这样的商业软件，不仅价格昂贵，还难以学习 http://www.aosabook.org/en/bib1.html#bib:shumba:ratrose|Shu05 。而在当时可用的开源替代品，要么功能有限要么缺陷很多①。比如需要使用文字来描述UML图，而不是使用更常见的点击式的界面。特别是ArgoUML软件中的时序图，根本无法使用。

> ①作者注：当时我还不知道Diomidis Spinellis的令人钦佩的UMLGraph程序 http://www.aosabook.org/en/bib1.html#bib:spinellis:umlgraph|Spi03

于是我决定自己尝试去实现一个最简单的UML编辑器，它一要对学生有用，二要是一个可扩展的框架，便于学生理解和修改。就这样，Violet诞生了。

# 22.1 初识Violet #

***

Violet是一个轻量级的UML编辑器，适用于学生、教师以及需要快速创建简单UML图的人士。它非常易于学习和使用。你可以用它绘制类图、时序图、状态图、对象图和用例图。（至今，其他类型的UML图绘制方法也已经有人贡献代码，实现了它们。）它是一个开放源代码并且跨平台的软件。Violet的核心使用了一种简单而灵活的图形框架，该框架充分利用了Java2D图形接口的优势。

Violet的用户界面被故意设计得很简单。你不需要通过一系列冗长乏味的对话框来输入属性和方法。相反，你只需要把它们输入到一个文本框中。只要点几下鼠标，你就能快速地创建出既吸引人又实用的UML图。

Violet并不尝试成为一个工业级的UML绘制程序。下面是Violet不具有的一些特点：
  * Violet不能从UML图生成代码或者说从源代码生成UML图；
  * Violet不会对模型进行语义检查，所以你能使用Violet绘制出自相矛盾的UML图；
  * Violet生成的文件不能导入其他的UML工具中，同样也不能从其他工具中读取他们的模型文件；
  * 除了简单的“自动对齐到网格”，Violet不提供UML图的自动布局功能。

（尝试列出一些软件的局限性，有利于催生出更棒的学生项目）

Violet后来发展出了一批由设计师组成的狂热的追随者群体，他们想让Violet成为一个正规的UML工具，但不要像工业级工具那么重量级，所以我就按照GNU GPL协议在SourceForge上发布了我的代码。2005年，Alexandre de Pellegrin加入了这个项目，并提供了一个Eclipse插件和一个更美观的用户界面。从那时起，他进行了很多的项目架构上的改动，现在他是这个项目的主要维护者。

在这篇文章里，我会讨论一些在Violet中的原始的架构选择以及他的演变。这篇文章一部分的重点会集中在图形编辑上，但是其他部分——比如JavaBeans属性和持久化的使用、Java WebStart以及插件架构，这些应该都是大家普遍感兴趣的。

# 22.2 图形框架 #

***

Violet是基于一个通用的图形编辑框架，这个框架能够渲染和编辑任意形状的节点和边。Violet UML编辑器将类、对象、活动条（时序图中的概念）等抽象为点，边就对应着UML图中的各种边线形状。这个图形框架的另一种实现能扎实ER图和铁路图①。

> ①译者注：railroad diagram，又称语法图，是形式文法的一种图形化表示方法。

![图 22.2：该图形编辑框架的一个简单实例](http://www.aosabook.org/cdn/images/aosabook/violet/Ch8-06.png)

为了更好地解释这个框架，我们来考虑一个非常简单的图形编辑器，它只包括黑色和白色圆节点以及直线边（图22.2）。下面的''SimpleGraph''定义了节点和边的原型对象，解释了原型模式是什么：
```
public class SimpleGraph extends AbstractGraph
  {
    public Node[] getNodePrototypes()
    {
      return new Node[]
      {
        new CircleNode(Color.BLACK),
        new CircleNode(Color.WHITE)
      };
    }
    public Edge[] getEdgePrototypes()
    {
      return new Edge[]
      {
        new LineEdge()
      };
    }
  }
```

原型对象被用来绘制图22.2上方的节点和边的按钮。每当用户在图上添加一个新的节点或边实例，对应的原型对象就会被复制一份。以上提到的Node和Edge是具有下列关键方法的接口：
  * 二者都有一个''getShape''的方法来返回一个边或节点的Java2D的''shape''对象。
  * 在Edge接口中有可以在边的头和尾产生节点的方法
  * Node接口中的''getConnectionPoints''方法可以计算出节点边缘的最佳附着点
  * Edge接口中的''getConnectionPoints''方法可以产生边的俩个端点。这个方法在选中边进行拖动等操作的时候有用。
  * 一个节点可以有随他一起移动的子节点。有很多的方法被提供来枚举和管理这些子节点。

![图22.3：找出节点边界上的一个连接点](http://www.aosabook.org/cdn/images/aosabook/violet/Ch8-07.png)

辅助类''AbstractNode''和''AbstractEdge''实现了大部分的接口要求的方法，类''RectangularNode''和''SegmentedLineEdge''分别提供了可输入一小段文字的方形节点和由线段构成的边的完整实现。

在我们的简单图形编辑器中，我们需要实现子类''CircleNode''和''LineEdge''来提供一个''draw''方法、一个''contains''方法以及''getConnectionPoint''方法来描绘节点边界形状。代码下面已经给出，图22.4展示了这些类的类图（当然是用Violet绘制的）。

```
public class CircleNode extends AbstractNode
{
  public CircleNode(Color aColor)
  {
    size = DEFAULT_SIZE;
    x = 0;
    y = 0;
    color = aColor;
  }
  public void draw(Graphics2D g2)
  {
    Ellipse2D circle = new Ellipse2D.Double(x, y, size, size);
    Color oldColor = g2.getColor();
    g2.setColor(color);
    g2.fill(circle);
    g2.setColor(oldColor);
    g2.draw(circle);
  }
  public boolean contains(Point2D p)
  {
    Ellipse2D circle = new Ellipse2D.Double(x, y, size, size);
    return circle.contains(p);
  }
  public Point2D getConnectionPoint(Point2D other)
  {
    double centerX = x + size / 2;
    double centerY = y + size / 2;
    double dx = other.getX() - centerX;
    double dy = other.getY() - centerY;
    double distance = Math.sqrt(dx * dx + dy * dy);
    if (distance == 0) return other;
    else return new Point2D.Double(
      centerX + dx * (size / 2) / distance,
      centerY + dy * (size / 2) / distance);
  }
  private double x, y, size, color;
  private static final int DEFAULT_SIZE = 20;
}

public class LineEdge extends AbstractEdge
{
  public void draw(Graphics2D g2)
  { g2.draw(getConnectionPoints()); }
  public boolean contains(Point2D aPoint)
  {
    final double MAX_DIST = 2;
    return getConnectionPoints().ptSegDist(aPoint) < MAX_DIST;
  }
}
```

![图22.4：简单图形编辑器的类图](http://www.aosabook.org/cdn/images/aosabook/violet/SimpleGraph-in-Violet.png)

总的来说，Violet为编写图形编辑器提供了一个简单的框架。通过定义节点和边的类，以及在图形类中提供绘制原型节点和边对象的方法，来实现一个编辑器实例。

当然，还有其他的图形框架可供使用，比如JGraph http://www.aosabook.org/en/bib1.html#bib:alder:jgraph|Ald02 和 http://jung.sourceforge.net|JUNG 。但是那些框架都相当的复杂，并且是提供的所绘制图形的框架而不是绘图应用程序的框架。

# 22.3 JavaBeans 属性的使用 #

***

在基于客户端的java技术鼎盛的时期，为了给在GUI构建环境中编辑GUI组件提供可移动的机制，人们开发出了JavaBeans的规范。这样一来，第三方GUI组件就能被任何的一个GUI构建容器所使用，并且在其中它的属性可以像标准按钮、文本组件那些一样被轻松设置。

Java并没有对属性的原生支持。然而，JavaBeans属性可以从getter和setter方法中体现出来，或则通过对应的''BeanInfo''类来指定。你也可以通过属性编辑器来对属性值进行可视化的编辑。JDK自身也包括了一些基本的属性编辑器，举个例子，针对''java.awt.Color''的编辑器。

Violet框架充分使用了JavaBeans规范。比如，''CircleNode''类可以简单的通过提供俩方法来操作颜色这一属性：

```
public void setColor(Color newValue)
public Color getColor()
```
# 22.4 长期的持久化 #

***

像任何编辑器一样，Violet必须将用户绘制的图像保存在一个文件中以方便后续将其加载出来。人们设计了XMI标准，作为UML模型的公共交换模式。但是我阅读之后，发现它冗长、难以理解以及使用。我不认为我是唯一一个觉得XMI拥有极其糟糕的交互性，哪怕是和最简单的模型。

我考虑简单点，直接使用Java提供的序列化的功能，但是读取较老版本的序列化对象有些许困难，因为序列化的实现总是在改动。JavaBeans的设计者也遇见了这种问题，他们为长期的持久化开发了一种标准的XML格式。在Violet中的一个Java对象，也就是一个UML图，是被序列化为了一串语句，方便对其进行创建和修改。

这里有个例子：

```
<?xml version="1.0" encoding="UTF-8"?>
<java version="1.0" class="java.beans.XMLDecoder">
 <object class="com.horstmann.violet.ClassDiagramGraph">
  <void method="addNode">
   <object id="ClassNode0" class="com.horstmann.violet.ClassNode">
    <void property="name">…</void>
   </object>
   <object class="java.awt.geom.Point2D$Double">
    <double>200.0</double>
    <double>60.0</double>
   </object>
  </void>
  <void method="addNode">
   <object id="ClassNode1" class="com.horstmann.violet.ClassNode">
    <void property="name">…</void>
   </object>
   <object class="java.awt.geom.Point2D$Double">
    <double>200.0</double>
    <double>210.0</double>
   </object>
  </void>
  <void method="connect">
   <object class="com.horstmann.violet.ClassRelationshipEdge">
    <void property="endArrowHead">
     <object class="com.horstmann.violet.ArrowHead" field="TRIANGLE"/>
    </void>
   </object>
   <object idref="ClassNode0"/>
   <object idref="ClassNode1"/>
  </void>
 </object>
</java>
```

当''XMLDecoder''类读取这个文件的时候，它会依次执行这些语句（为了方便起见，包名已经省略）

```
ClassDiagramGraph obj1 = new ClassDiagramGraph();
ClassNode ClassNode0 = new ClassNode();
ClassNode0.setName(…);
obj1.addNode(ClassNode0, new Point2D.Double(200, 60));
ClassNode ClassNode1 = new ClassNode();
ClassNode1.setName(…);
obj1.addNode(ClassNode1, new Point2D.Double(200, 60));
ClassRelationShipEdge obj2 = new ClassRelationShipEdge();
obj2.setEndArrowHead(ArrowHead.TRIANGLE);
obj1.connect(obj2, ClassNode0, ClassNode1);
```

只要这些构造函数、属性和方法的语义没有改变，一个更新的的程序版本也可以读取一个又旧版本生成的文件。

生成这样的文件是非常直接了当的。编码器自动枚举每个对象的属性并且对不同于默认属性的属性添加设置语句。大部分基本的数据类型都是由Java平台来处理的；但是我要特殊处理''Point2D''、''Line2D''和''Rectangle2D''。最重要的是编码器必须要知道，一个图形可以被序列化为一系列对''addNode''和''connect''方法的调用：
```
encoder.setPersistenceDelegate(Graph.class, new DefaultPersistenceDelegate()
{
  protected void initialize(Class<?> type, Object oldInstance,
    Object newInstance, Encoder out)
  {
    super.initialize(type, oldInstance, newInstance, out);
    AbstractGraph g = (AbstractGraph) oldInstance;
    for (Node n : g.getNodes())
      out.writeStatement(new Statement(oldInstance, "addNode", new Object[]
      {
        n,
        n.getLocation()
      }));
    for (Edge e : g.getEdges())
      out.writeStatement(new Statement(oldInstance, "connect", new Object[]
      {
        e, e.getStart(), e.getEnd()
      }));
   }
 });
```

一旦编码器被设置好了，保存一个图像就简单了，就像这样：
```
encoder.writeObject(graph);
```
因为编码器只是单纯的执行语句，并不需要特殊的设置。图像的的读取就简单了：
```
Graph graph = (Graph) decoder.readObject();
```

历经各个Violet的版本，这种方法效果拔群，只有一次例外。最近一个的重构改变了一些包的名字，因此就破坏了向后兼容性。一个选择就是保证这些类始终保留在原来的包中，哪怕不在与新包结构相匹配。然而维护者采用的是另外的一种方式，那就是提供了一个XML转换器来为读取旧版本文件时临时重写包名。
# 22.5.Java WebStart #
***
Java WebStart是一门用于从浏览器中启动应用程序的技术。部署者发布一个JNLP文件，该文件会在浏览器中触发一个辅助程序，用于进行下载和运行Java程序。启动的应用程序可以是数字签名过的，但是在这种情况下用户必须接受应用程序的证书。启动的应用程序也可以是未签名过的，但是在这种情况下程序只能运行在一个比Java中的applet沙盒权限稍高的沙盒环境中。
 

我不认为终端用户可以或者应当被信任其有能力去评判数字证书的有效性和它所隐含的安全性。Java平台一个很大的优点就在于其安全性，并且我觉得发挥这个优点是很重要的事。
 

Java WebStart沙盒十分得强大，它可以确保用户可以执行有用的工作，包括装载和存储文件，以及打印。从用户角度看，这些操作都被处理得既安全又易用。当应用程序想访问本地的文件系统时，用户会被告知是否授权给应用程序，并且会让用户来选择可以被程序读写的文件。应用程序仅能得到一个文件流对象，而不能在用户进行选择过程中得到窥探本地文件系统的机会。
 

不过令人讨厌的是，当应用程序在WebStart下运行时，开发者必须自己编码来与''FileOpenService''和''FileSaveService''交互。更令人讨厌的是，并没有一个WebStart接口（API）可以用来被调用去知道当前应用程序是否是由WebStart启动的。
 

类似地，保留用户偏好也必须由以下两种方式实现：当程序正常运行时，使用Java偏好接口（API）来实现保留；当程序在WebStart下运行时，使用WebStart偏好服务来实现保留。然而打印功能却是对程序开发者完全透明的。
 

然而，Violet在这些服务之上提供了简单的抽象层来减轻应用开发者的负担。以下面如何打开一个文件为例：
```
FileService service = FileService.getInstance(initialDirectory);
  * detects whether we run under WebStart
FileService.Open open = fileService.open(defaultDirectory, defaultName, extensionFilter);
InputStream in = open.getInputStream();
String title = open.getName();
```
''FileService.Open''接口有两个实现类：一个是对''JFileChooser''的封装，一个是JNLP的''FileOpenService''。
 

JNLP本身并没有如此方便，在其生命周期里很少有人喜欢它，以至于它已经被广泛的忽略。大多的项目只是简单地为其WebStart应用程序使用一个自签名的证书，然而这对于用户来说是不安全的。这是一种耻辱——开源开发者应该拥护JNLP沙盒并把它作为尝试新项目的一种零风险方式。

# 22.6.Java 2D #
***
Violet大量使用Java 2D库，它是Java API（应用程序接口）中鲜为人知的珍宝。Violet中图形的每个节点和每条边都有一个''getShape''方法，方法返回一个Java 2D所有图形的公共接口''java.awt.shape''的对象。矩形、圆形、路径，以及它们之间的并、交和差运算都可以实现该公共接口。当要创建由任意线段和二次/三次曲线所构成的图形，比如直箭头和弯箭头，''GeneralPath''类就很有用。
 

为了感受Java 2D接口（API）的灵活性，考虑下面这段在''AbstractNode.draw''方法中绘制阴影的代码：
```
Shape shape = getShape();
if (shape == null) return;
g2.translate(SHADOW_GAP, SHADOW_GAP);
g2.setColor(SHADOW_COLOR);
g2.fill(shape);
g2.translate(-SHADOW_GAP, -SHADOW_GAP);
g2.setColor(BACKGROUND_COLOR);
g2.fill(shape);
```
短短几行代码就能让任何形状产生阴影，甚至是开发者在之后新加入的图形。
 

当然，Violet能以任意''javax.imageio''包所支持的图片格式来保存位图图像，包括GIF, PNG, JPEG等格式。当我的发布者向我索要矢量图时，我发现了Java 2D库的另一个优点。当你需要打印矢量图到一个PostScript打印机的时候，Java 2D操作会被翻译成PostScript矢量绘图操作。而如果你要打印矢量图到一个文件中时，输出的文件可以使用如''ps2eps''这样的程序处理，进而导入到Adobe Illustrator或Inkscape中。下面是相关的代码（这里''comp''是一个 Swing 组件，它的''paintComponent''方法用于打印上述图形）：
```
DocFlavor flavor = DocFlavor.SERVICE_FORMATTED.PRINTABLE;
String mimeType = "application/postscript";
StreamPrintServiceFactory[] factories;
StreamPrintServiceFactory.lookupStreamPrintServiceFactories(flavor, mimeType);
FileOutputStream out = new FileOutputStream(fileName);
PrintService service = factories[0].getPrintService(out);
SimpleDoc doc = new SimpleDoc(new Printable() {
  public int print(Graphics g, PageFormat pf, int page) {
      if (page >= 1) return Printable.NO_SUCH_PAGE;
      else {
        double sf1 = pf.getImageableWidth() / (comp.getWidth() + 1);
        double sf2 = pf.getImageableHeight() / (comp.getHeight() + 1);
        double s = Math.min(sf1, sf2);
        Graphics2D g2 = (Graphics2D) g;
        g2.translate((pf.getWidth() - pf.getImageableWidth()) / 2,
            (pf.getHeight() - pf.getImageableHeight()) / 2);
        g2.scale(s, s);

        comp.paint(g);
        return Printable.PAGE_EXISTS;
      }
  }
}, flavor, null);
DocPrintJob job = service.createPrintJob();
PrintRequestAttributeSet attributes = new HashPrintRequestAttributeSet();
job.print(doc, attributes);
```
一开始的时候，我还担心使用通用形状会给性能带来不好的影响，然而事实并非如此。裁剪功能（clipping）工作得很好，只有当那些更新当前视图的形状操作执行时，裁剪功能才会被执行。
# 22.7. 不使用Swing应用程序框架 #
***
大多GUI框架都有一个类似应用程序的概念，它用来管理一组负责处理菜单栏、工具栏、状态栏等的文档集。然而，这个概念从来就不是Java API（应用程序接口）的一部分。JSR 296 ?的提出，原本是为了Swing应用程序提供一个基本的框架，但它目前已经处于闲置状态了。因此，Swing应用程序的作者有两种选择：要么“重新发明轮子”⑤，要么依靠一个第三方的框架。在编写Violet的时候，应用程序框架的主流选择是Eclipse和NetBeans平台，但当时它们看上去都太重量级了。（现如今我们有更多的选择了，比如GUTS ?，它是JSR 296的一个分支。）因此，Violet 被迫重新发明了处理菜单和内部框架（internal frames）的机制。

>? JSR 296 ： http://jcp.org/en/jsr/detail?id=296
>? GUTS ：  http://kenai.com/projects/guts
>
> ⑤译者注：reinvent the wheel，指对一些基本或常见的问题，不采纳现有的成熟的方案。

在Violet中，你可以像下面这样，在属性文件（property files）中指定菜单项：
```
file.save.text=Save
file.save.mnemonic=S
file.save.accelerator=ctrl S
file.save.icon=/icons/16x16/save.png
```
有一个工具方法从前缀（比如这里的 file.save）创建菜单项。.text、.mnemonic这样的后缀，在今天一般被称作“约定优于配置”。使用资源文件来描述这些设置，显然要比调用 API 来建立菜单高级得多，因为这让本地化（localization）变得十分简单。我在另一个开源项目 GridWorld ?中重用了这一机制，它是一个高中计算机科学教学的环境。

>? GridWorld ： http://horstmann.com/gridworld
一个像Violet这样的应用程序允许用户打开多个文档，每个文档包含一个图。当最初编写Violet时，多文档接口（MDI，multiple document interface）仍然被广泛使用。通过使用MDI，主框架（main frame）有一个菜单栏，而每个文档的视图显示在一个有标题栏但没有菜单栏的内部框架中。每个内部框架都包含在主框架中，并且每个内部框架都能被用户修改大小或最小化。而且还有用于对窗口进行层叠或平铺的操作。

因为许多开发者不喜欢多文档接口（MDI），所以这种风格的用户界面早已过时。单文档接口（SDI，single document interface）的应用程序可以显示很多顶层的框架。大概也是因为其可以使用宿主操作系统的标准窗口管理工具来操作这些顶层框架，在一段时间里，SDI 被认为更加高级。当人们最终意识到太多的顶层窗口也不是很方便的时候，标签页界面（tabbed interfaces）出现了。标签页界面中，多个文档再次被放到一个单个的框架中，但每个都是以完整大小显示的，并且可以通过标签（tabs）来选择。这种界面虽然不允许用户并排比较两个文档，但看起来还是胜出了。

Violet最初的版本使用的是MDI接口。Java API 包含了内部框架这一特性，但我需要增加对平铺和层叠窗口的支持。Alexandre 切换到了标签页界面；从某种程度上来说，这种界面在 Java API 中得到了更好的支持。在应用程序框架中，如果文档的显示策略对于开发者是透明的，或许是可以让用户来选择的，那将是非常可取的。


> Alexandre：Alexandre de Pellegrin(http://alexdp.free.fr/violetumlplugin/cv.html)，violet开发者之一。

Alexandre 还增加了对侧边栏、状态栏、欢迎面板、启动闪屏的支持。理想情况下，所有这些都应该是 Swing 应用程序框架所支持的。
# 22.8. Undo/Redo #
***
实现多次撤销/重做看上去是件令人害怕的任务，但是Swing的撤销包（undo package， http://www.aosabook.org/en/bib1.html#bib:horstmann:oodp|Top00 ，第九章）给出了一个很好的架构指南。一个''UndoManager''（撤销管理器）管理一个''UndoableEdit''（可撤销的编辑）对象的栈。栈中的每一个对象都有一个''undo''方法，用于撤销编辑操作，还有一个''redo''方法负责重做编辑操作（执行原本的编辑操作）。一个''CompoundEdit''（复合编辑）是一串''UndoableEdit''操作，它们可以被整体撤销或重做。我们鼓励你定义小的、原子性的编辑操作（比如在图中增加或删除一条边或一个节点），而这些操作可以按需被组织成一个复合的编辑操作。

随之而来的一个挑战就是如何定义一个小的原子操作集合，使得其中每个操作都容易撤消。Violet 中有如下几种原子操作：

  * 增加或删除一个节点或一条边
  * 附着（attach）或拆开（detach）一个节点的子节点
  * 移动一个节点
  * 改变节点或边的属性

上述每种操作都有一个很明显的撤消方法。比如，“增加一个节点”的撤消方法就是删掉这个节点，“移动一个节点”的撤消方法就是按相反的向量移动这个节点。

![图22.6：撤消操作必须撤消模型中的结构化的更改](http://aosabook.org/cdn/images/aosabook/violet/undo.png)

注意，这些原子操作不同于用户界面的动作，也不同于这些动作所调用的''Graph''接口的方法。比如，考虑图 22.6 中的顺序图，假设用户从左侧的方法调用框拖动鼠标到右侧的对象生命线，当鼠标被松开时，下面的方法会被调用：

```
public boolean addEdgeAtPoints(Edge e, Point2D p1, Point2D p2)
```

这个方法不但会增加一条边，而且也可能根据具体参与调用的''Edge''和''Node''子类，进行其他操作。在这个例子中，右侧的对象生命线会增加一个新的方法调用框，那么撤消这一操作的时候，这个新的方法调用框也要被删掉。因此，模型（此例中的图形）还需要记录所需撤消的结构化的更改，而仅仅记录控制器（controller）中的操作是不够的。

正如Swing的撤销包所预想的，在发生一个结构化的更改时，图形、节点、边的这些类需要向''UndoManager'' 发送''UndoableEditEvent''（可撤消的编辑事件）通知。Violet 具有一个更加通用的设计——图形自身通过如下接口管理监听器（listeners）：

```
public interface GraphModificationListener
{
  void nodeAdded(Graph g, Node n);
  void nodeRemoved(Graph g, Node n);
  void nodeMoved(Graph g, Node n, double dx, double dy);
  void childAttached(Graph g, int index, Node p, Node c);
  void childDetached(Graph g, int index, Node p, Node c);
  void edgeAdded(Graph g, Edge e);
  void edgeRemoved(Graph g, Edge e);
  void propertyChangedOnNodeOrEdge(Graph g, PropertyChangeEvent event);
}
```

Violet 框架在每个图形中安装一个监听器，作为与撤消管理器交互的桥梁。对于支持撤消功能来说，为模型增加通用的监听器支持是有点过度设计了（overdesigned）——图形操作可以直接与撤销管理器交互。然而，我还想支持一种实验性质的协作式编辑特性（collaborative editing feature）。

如果你想在你的应用程序中支持撤消和重做，仔细想想你的模型（而非你的用户界面）中的原子操作。在模型中，当结构改变时，触发相应的事件，并允许 Swing 的撤销管理器来收集、组合这些事件。
# 22.9. Plugin Architecture（插件架构） #
***
对于熟悉2D图形编程的程序员来说，为Violet增加新类型的图并不困难。比如，活动图就是由第三方贡献开发的。当我需要创建铁路图和ER图的时候，我发现给Violet 写一个扩展，要比胡乱使用Visio或Dia来得更快。（每种类型的图需要花一天的时间来实现。）

这些实现并不要求你理解整个Violet框架。只需要实现图形、节点和边的接口即可。为了让贡献开发者更容易地脱离Violet框架的演变过程，我设计了一个简单的插件架构。

当然，很多程序都有一个插件架构，其中的很多都说明详尽。当有人建议说Violet应该支持OSGi的时候，我打了个哆嗦，并且取而代之地实现了能够让插件机制工作的最简单的事情。

贡献开发者只需要生成一个包含了图形、节点和边的实现的JAR文件，并把它放''plugins''目录中。当 Violet启动时，它会调用Java的''ServiceLoader''（服务加载器）类来加载这些插件。''ServiceLoader'' 类是用来加载像JDBC驱动这样的服务的。''ServiceLoader''会加载那些能够对指定接口提供实现的 JAR 文件（比如这里的 Graph 接口）。

每个JAR文件必须包含一个名为''META-INF/services''的子目录，该目录中需要包含一个以相应接口的全称命名的文件（比如''com.horstmann.violet.Graph''），文件内容是实现了这一接口的所有类的名字，每行一个。''ServiceLoader''会为插件目录构造一个类加载器（class loader），并加载所有的插件：

```
ServiceLoader<Graph> graphLoader = ServiceLoader.load(Graph.class, classLoader);
for (Graph g : graphLoader) * ServiceLoader<Graph> implements Iterable<Graph>
  registerGraph(g);
```

这是标准Java中的一个简单而实用的设施，并且你或许会在你自己的项目中发现它的价值。
# 22.10. Conclusion #
***
和很多开源项目一样，Violet 诞生于一个未被满足的需求***以最小的混乱代价，来绘制简单的UML图。Java SE 平台令人惊奇的广泛应用使得Violet成为了可能。同时，Violet 也利用了该平台中的很多技术。在这篇文章中，我描述了 Violet 如何利用 JavaBeans、长期的持久化、Java WebStart、Java 2D、Swing 撤消和重做（Undo/Redo），以及服务加载器设施。这些技术并不总是和基础的 Java 及 Swing 一样容易被人理解，但它们可以极大地简化桌面应用程序的架构。它们允许我能够在最开始作为一个独立的开发者，在几个月的业余时间里创建出一个成功的应用程序。依赖这些标准的机制，也让其他人易于改进Violet，或是易于从中提取一些片段应用在他们自己的项目中。


