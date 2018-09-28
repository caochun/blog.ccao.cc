##matplotlib翻译##      
                                   
**翻译人员：马浩杰**

 

 

 

 

 
matplotlib是基于Python的绘图库，广泛用于Python科学计算界。它完整支持二维绘图以及部分支持三维绘图。该绘图库致力于能适应广泛的用户需求。它可以根据所选的用户接口工具来嵌入绘图算法。与此同时，对于使用GTK+、Qt、Tk、FLTK、wxWidgets与Cocoa的所有主要桌面操作系统，matplotlib能支持交互式绘图。在Python的交互式shell中，我们可以使用简单的、过程式的命令交互式地调用matplotlib来生成图形，与使用Mathematica、IDL或者MATLAB绘图非常相似。matplotlib也可以嵌入到无报文头的Web服务器中，以提供基于光栅（如PNG格式）与向量（如Postscript、PDF以及纸面效果很好的SVG格式）这两种格式的图形硬拷贝。


####11.1 硬件锁问题####
我们其中一位开发者（John Hunter）与他的研究癫痫症的同事们试图在不借助专有软件的情况下进行脑皮层电图（ECoG）分析，于是便有了最初的matplotlib。John Hunter当时所在的实验室只有一份电图分析软件的许可证，但有各式各样的工作人员，如研究生、医科学生、博士后、实习生、以及研究员，他们轮流共享该专有软件的硬件电子锁。生物医学界广泛使用MATLAB进行数据分析与可视化，所以Hunter着手使用基于MATLAB的matplotlib来代替专有软件，这样很多研究员都可以使用并且对其进行扩展。但是MATLAB天生将数据当作浮点数的数组来处理。然而在实际情况中，癫痫手术患者的医疗记录具有多种数据形式（CT、MRI、ECoG与EEG等），并且存储在不同的服务器上。MATLAB作为数据管理系统勉强能应付这样的复杂性。由于感到MATLAB不适合于这项任务，Hunter开始编写一个新的建立在用户接口工具GTK+（当时是Linux下的主流桌面视窗系统）之上的Python应用程序。

所以matplotlib这一GTK+应用程序最初便被开发成EEG/ECoG可视化工具。这样的用例决定了它最初的软件架构。matplotlib最初的设计也服务于另一个目的：代替命令驱动的交互式图形生成（这一点MATLAB做得很好）工具。MATLAB的设计方法使得加载数据文件与绘图这样的任务非常简单，而要使用完全面向对象的API则会在语法上过于繁琐。所以matplotlib也提供状态化的脚本编程接口来快速、简单地生成与MATLAB类似的图形。因为matplotlib是Python库，所以用户可以使用Python中各种丰富的数据结构，如列表、辞典与集合等等。

![](http://www.aosabook.org/images/matplotlib/ecog.png)

图11.1：最初的matplotlib程序——ECoG查看器

####11.2 matplotlib软件架构概述####
顶层的matplotlib对象名为Figure，它包含与管理某个图形的所有元素。matplotlib必须完成的一个核心架构性任务是实现Figure的绘制与操作框架，并且做到该框架与Figure到用户视窗接口或硬拷贝渲染行为是分离的。这使得我们可以为Figure添加越来越复杂的特性与逻辑，同时保持“后端”或输出设备的相对简化。matplotlib不仅封装了用于向多种设备渲染的绘图接口，还封装了基本事件处理以及多数流行的用户界面工具的视窗功能。因此，用户可以创建相当丰富的交互式图形算法与用户界面工具（用到可能存在的鼠标与键盘），而又不必修改matplotlib已经支持的6种界面工具。

要实现这些，matplotlib的架构被逻辑性地分为三层。这三层逻辑可以视为一个栈。每层逻辑知道如何与其下的一层逻辑进行通信，但在下层逻辑看来，上层是透明的。这三层从底向上分别为：后端、美工与脚本。

####11.2.1 后端####

matplotlib逻辑栈最底层是后端，它具体实现了下面的抽象接口类：

  * FigureCanvas对绘图表面（如“绘图纸”）的概念进行封装。
  * Renderer执行绘图动作（如“画笔”）。
  * Event处理键盘与鼠标事件这样的用户输入。

对于如Qt这样的用户界面工具，FigureCanvas中包含的具体实现可以完成三个任务：将自身嵌入到原生的Qt视窗（QtGui.QMainWindow）中，能将matplotlib的Renderer命令转换到canvas上（QtGui.QPainter），以及将原生Qt事件转换到matplotlib的Event框架下（后者产生回调信号让上行监听者进行处理）。抽象基类定义在matplotlib.backend_bases中，且所有派生类都定义在如matplotlib.backends.backend_qt4agg这样的专用模块中。对于专门生成硬拷贝输出（如PDF、PNG、SVG或PS）的纯图像后端而言，FigureCanvas的实现可能只是简单地建立一个类似文件的对象，其中定义默认的文件头、字体与宏函数，以及Renderer创建的个别对象（如直线、文本与矩形等）。

Renderer的任务是提供底层的绘图接口，即在画布上绘图的动作。上文已经提到，最初的matplotlib程序是一个基于GTK+的ECoG查看器，而且很多早期设计灵感都源自当时已有的GDK/GTK+的API。最初Renderer的API源自GDK的Drawable接口，后者实现了draw_point、draw_line、draw_rectangle、draw_image、draw_polygon以及draw_glyphs这样的基本方法。我们完成的每个不同后端——最早有PostScript与GD——都实现了GDK的Drawable，并将其转换为独立于后端的原生绘图命令。如上所述，这毫无必要地增加了后端的实现复杂度，原因是单独实现Drawable造成函数泛滥。此后，Renderer已经被极大的简化，将matplotlib移植到新的用户界面或文件格式已经是非常简单的过程。

一个对matplotlib有利的设计决定是支持使用C++模板库Anti-Grain Geometry（缩写为agg[She06]）的基于像素点的核心渲染器。这是一个高性能库，可以进行2D反锯齿渲染，生成的图像非常漂亮。matplotlib支持将agg后端渲染的像素缓存插入到每种支持的用户界面中，所以在不同的UI与操作系统下都能得到精确像素点的图形。因为matplotlib生成的PNG输出也使用agg渲染器，所以硬拷贝与屏幕显示完全相同，也就是说在不同的UI与操作系统下，PNG的输出所见即所得。

matplotlib的Event框架将key-press-event或mouse-motion-event这样的潜在UI事件映射到KeyEvent或MouseEvent类。用户可以连接到这些事件进行函数回调，以及图形与数据的交互，如要pick一个或一组数据点，或对图形或其元素的某方面性质进行操作。下面的示例代码演示了当用户键入‘t’时，对Axes窗口中的线段进行显示开关。

```
import numpy as np
import matplotlib.pyplot as plt

def on_press(event):
    if event.inaxes is None: return
    for line in event.inaxes.lines:
        if event.key=='t':
            visible = line.get_visible()
            line.set_visible(not visible)
    event.inaxes.figure.canvas.draw()

fig, ax = plt.subplots(1)

fig.canvas.mpl_connect('key_press_event', on_press)

ax.plot(np.random.rand(2, 20))

plt.show()
```

对底层UI事件框架的抽象使得matplotlib的开发者与最终用户都可以编写UI事件处理代码，而且“一次编写，随处运行”。譬如，在所有用户界面下都可以对matplotlib图像进行交互式平移与放缩，这种交互式操作就是在matplotlib的事件框架下实现的。


#### 11.2.2 Artis层 ####

Artist层次结构处于matplotlib的中间层，负责很大一部分繁重的计算任务。延续之前将后端的FigureCanvas看作画纸的比喻，Artis对象知道如何用Renderer（画笔）在画布上画出墨迹。matplotlib中的Figure就是一个Artist对象实例。标题、直线、刻度标记以及图像等等都对应某个Artist实例（如图11.3）。Artist的基类是matplotlib.artist.Artist，其中包含所有Artist的共享属性，包括从美工坐标系统到画布坐标系统的变换（后面将详细介绍）、可见性、定义用户可绘制区域的剪切板、标签，以及处理“选中”这样的用户交互动作的接口，即在美工层检测鼠标点击事件。

![](http://www.aosabook.org/images/matplotlib/artists_figure.png)
图11.2：matplotlib生成的图形

![](http://www.aosabook.org/images/matplotlib/artists_tree.png)
图11.3：用于绘制图11.2的Artist实例的层次结构

Artist层于后端之间的耦合性存在于draw方法中。譬如，下面假想的SomeArtist类是Artist的子类，它要实现的关键方法是draw，用来传递给后端的渲染器。Artist不知道渲染器要向哪种后端进行绘制（PDF、SVG与GTK+绘图区等），但知道Renderer的API，并且会调用适当的方法（draw_text或draw_path）。因为Renderer能访问画布，并且知道如何绘制，所以draw方法将Artist的抽象表示转换为像素缓存中的颜色、SVG文件中的轨迹或者其他具体表示。

```
class SomeArtist(Artist):
    'An example Artist that implements the draw method'

    def draw(self, renderer):
        """Call the appropriate renderer methods to paint self onto canvas"""
        if not self.get_visible():  return

        # create some objects and use renderer to draw self here
        renderer.draw_path(graphics_context, path, transform)
```

该层次结构中有两种类型的Artist。基本Artist表示我们在图形中能看到的一类对象，如Line2D、Rectangle、Circle与Text。复合Artist是Artist的集合，如Axis、Tick、Axes与Figure。每个复合Artsit可能包含其他复合Artist与基本Artist。譬如，Figure包含一个或多个Axes，并且Figure的背景是基本的Rectangle。

最重要的复合Artist是Axes，其中定义了大多数matplot的绘图方法。Axes不仅仅包含大多数构成绘图背景（如标记、轴线、网格线、色块等）的图形元素，还包括了大量生成基本Artist并添加到Axes实例中的帮助函数。譬如，表11.1列出了一些Axes函数，这些函数进行对象的绘制，并将它们存储在Axes实例中。

表11.1：Axes的方法样例及其创建的Artist实例
我们有一个专门用来处理文档字符串的模块matplotlib.docstring.

|方法	        |创建对象	                        | 存储位置           |
|-|-|-|
| Axes.imshow 	| 一到多个matplotlib.image.AxesImage	| Axes.images       |
| Axes.hist	| 大量matplotlib.patch.Rectangle	        | Axes.patches      |
| Axes.plot	| 一到多个matplotlib.lines.Line2D 	| xes.lines         |

下面这个简单的Python脚本解释了以上架构。它定义了后端，将Figure链接至该后端，然后使用数组库numpy创建10,000个正太分布的随机数，最后绘制出它们的柱状图。

```
# Import the FigureCanvas from the backend of your choice
#  and attach the Figure artist to it.
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
fig = Figure()
canvas = FigureCanvas(fig)

# Import the numpy library to generate the random numbers.
import numpy as np
x = np.random.randn(10000)

# Now use a figure method to create an Axes artist; the Axes artist is
#  added automatically to the figure container fig.axes.
# Here "111" is from the MATLAB convention: create a grid with 1 row and 1
#  column, and use the first cell in that grid for the location of the new
#  Axes.
ax = fig.add_subplot(111)

# Call the Axes method hist to generate the histogram; hist creates a
#  sequence of Rectangle artists for each histogram bar and adds them
#  to the Axes container.  Here "100" means create 100 bins.
ax.hist(x, 100)

# Decorate the figure with a title and save it.
ax.set_title('Normal distribution with $\mu=0, \sigma=1$')
fig.savefig('matplotlib_histogram.png')
```

####11.2.3 脚本层（pyplot)####

使用以上API的脚本效果很好，尤其是对于程序员而言，并且在编写Web应用服务器、UI应用程序或者是与其他开发人员共享的脚本时，这通常是比较合适的编程范式。对于日常用途，尤其对于非专业程序员而要完成一些交互式的研究工作的实验科学家而言，以上API的语法可能有些难以掌握。大多数用于数据分析与可视化的专用语言都会提供轻量级的脚本接口来简化一些常见任务。matplotlib在其matplotlib.pyplot接口中便实现了这一点。以上代码改用pyplot之后如下所示。

```
import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(10000)
plt.hist(x, 100)
plt.title(r'Normal distribution with $\mu=0, \sigma=1$')
plt.savefig('matplotlib_histogram.png')
plt.show()
```

![](http://www.aosabook.org/images/matplotlib/histogram_demo.png)
图11.4：用pyplot绘制的柱状图

pyplot是一个状态化接口，大部分工作是处理样本文件的图形与坐标的生成，以及与所选后端的连接。它还维护了模块级的内部数据结构。这些数据结构表示了直接接收绘图命令的当前图形与坐标

下面仔细分析示例脚本中比较重要的几行，观察其内部状态的管理方式。
  * import matplotlib.pyplot as plt：当pyplot模块被加载时，它分析本地配置文件。配置文件除了完成一些其他工作外，主要声明了默认的后端。可能是类似QtAgg的用户接口后端，于是上面的脚本将导入GUI框架并启动嵌入了图形的Qt窗口；或者可以是一个类似Agg的纯图像后端，这样脚本会生成硬拷贝输出然后退出。
  * plt.hist(x, 100)：这是脚本中第一个绘图命令。pyplot会检测其内部数据结构已查看是否存在当前Figure实例。如果存在，则提取当前Axes，并将绘图行为导向Axes.hist的API调用。在该脚本中不存在Figure实例，所以会生成一个FIgure与Axes，并将它们设为当前值，然后将绘图行为导向Axes.hist. plt.title(r'Normal distribution with $\mu=0, \sigma=1$'):就像前面一样,pyplot收件检查是否存在Figure和Axes实例.如果存在就直接调用已存在的Axes实例的Axes.set_title.plt.show()方法:这将强制Figure去渲染图像,并且如果用户在配置文件中指定了默认GUI后端,那么就执行GUI主循环并且把所有创造的fugure添加到屏幕中去.

pyplot常用的划线函数matplotlib.pyplot.plot的精简版本在下面代码框中展出,用来阐述pyplot是如何将matplotlib函数包装起来的.其他所有pyplot脚本接口函数都是相似的设计.
```
@autogen_docstring(Axes.plot)
def plot(*args, **kwargs):
    ax = gca()

    ret = ax.plot(*args, **kwargs)
    draw_if_interactive()

    return ret
```

Python修饰符#autogen_docstring(Axes.plot)从相应的API方法中提取出文档字符串,并将适当形式的版本新题添加到pyplot.plot方法中;我们用一个专门用来处理文档字符串的模块matplotlib.docstring.*参数和**被在文件签名的特殊约定在Python中指所有参数和关键字参数被传递到方法.这允许我们把他们向前传递到相应的API.ax = gca()语句调用状态机来获取当前的?实例(每个python解释器只能有一个"当前轴"),并且会在必要的时候创建figure和axes.res = ax.plot(*args, ** kwargs)向前传递函数调用和参数给相应的axes方法,并且保存返回值用作以后返回.因此pyplot接口是对核心ArtistAPI的相当轻薄的包装,主要是尽可能避免为了通过暴漏API函数而导致的代码重复,以实现用最少的样板代码在脚本接口中调用签名和文档字符串.

#### 1.3后端重构 ###
输出后端定义了许多画图API,包括
```
draw_arc, draw_image, draw_line_collection, draw_line, draw_lines, draw_point,
draw_quad_mesh, draw_polygon_collection, draw_polygon, draw_rectangle,
draw_regpoly_collection
```
不幸的是，有太多的方法意味着设计一个后端需要花费很长的时间，并且随着新特性的加入，更新已经存在的后端也需要话费很多的精力，因为每个后端都是由精通某一特定的文件格式的开发者实现．
到了matplotlib 0.98,后端由开发者重构为只包含最少的必要功能，新的后端包含下面的一些API
* <b>draw_path</b>:绘制多边形复合，此接口取代了许多的老办法：draw_arc，draw_line，draw_lines和draw_rectangle.
* <b>draw_image</b>绘制光栅图像
* <b>draw_text</b>按照给定的字体绘制文本
* <b>get_text_width_height_descent</b>给定一个文本字符串，返回它的尺寸
大部分情况下实现其它新的后端只需要实现这些方法就足够了(我们还可以更进一步，并使用draw_path，消除了draw_text方法需要绘制文本，但我们还没有得到解决，使这一简化。当然，后端仍可以自由地实现自己的draw_text方法输出“真实”的文字).这使得获得一个新的后端更容易。然而，在一些情况下，后端可能需要覆盖，以创造更高效的行为。例如，绘制标记（用来表示一个线图顶点的小符号）时，只在文件中塑性一次标记的空间效率更好，然后重复它作为一个“邮票”无处不在使用它。在这种情况下，后端可以实现draw_markers方法。如果它的实施，后端写出标记形状一次，然后写出短得多的命令，重用这个标记在若干位置。如果它没有实现，就会只是简单地调用多次draw_path来绘制标记。
可选的后端API方法有:
* draw_markers: 绘制标记
* draw_path_collection: 绘制路径
* draw_quad_mesh: 绘制四边形网络

#### 11.4Transforms ####
matplotlib花费很多时间将一个坐标系变换到另一个。这些坐标系包括：
* data: 原始数据值
* axes: 由特定轴矩阵限定的空间
* figure: 包含整个数字空间
* display: 在输出中使用的物理坐标

  每个Artist都有一个知道如何从一个坐标系转变到另一个的转换节点．这些节点构成一个有向图．沿着有向图的边走到根，可以将原始数据值转换为最终在文件中的输出坐标．这使得点击一个元素来获取它的数值坐标变得可能．这张图表达了节点之间的依赖关系，当一个父节点的转换改变以后，例如当artist的限制改变时，与该轴的任何转换是无效的，因为他们将需要重新绘制。有关在图中的其他轴变换，当然也可单独使用左，防止不必要recomputations和有助于更好地交互性能。
变换节点可以是简单仿射变换和非仿射变换。仿射变换是保持距离的直线和比例，包括旋转，平移，缩放和倾斜变换的一系列变换。二维仿射变换使用的3×3仿射变换矩阵表示。转化点（x'，y'）是原始点（x，y）进行通过下面矩阵变换得到的:
![](http://aosabook.org/images/matplotlib/matrix.png)


二维坐标可以很容易地通过变换矩阵相乘来进行变换。仿射变换也有，他们可以利用矩阵乘法可以相互组合的有用的属性。这意味着，要执行一系列仿射变换，该变换矩阵可首先相乘一次，所得矩阵可以用于转化坐标。matplotlib的转型框架自动组成（冻结）仿射变换变换坐标，以减少计算量前矩阵在一起.拥有快速仿射变换是很重要的，因为它使得交互式平移和在GUI窗口更有效的放大。
在matplotlib非仿射变换使用Python函数定义的，所以他们是真正的随心所欲。在matplotlib核心，非仿射变换用于对数缩放，极坐标图和地理的预测（图11.5）。这些非仿射变换在转换图中可以和仿射变换自由混合。matplotlib将自动简化仿射部和仅回落到用于非仿射部的任意函数。
![](http://aosabook.org/images/matplotlib/nonaffine_transforms.png)
从这些简单的作品，matplotlib可以做一些非常先进的东西。混合变换是使用一个x轴变换和一个y轴变换的特殊变换节点。当然，这是唯一可能的，如果给定的变换为“可分离”，意思是在x和y坐标是独立的，但在变换本身可以是仿射或非仿射。这是用来，例如，绘制对数曲线，其中任一个或两个x和y轴的可具有对数刻度。具有混合的变换节点允许可扩展到以任意的方式组合。变换图允许的另一件事是轴的共享。这使得当进行平移和缩放"link"一条线的极限到另一条成为可能，在这种情况下，相同的变换节点简单地两个轴，这甚至可能在两个不同的数字之间共享。图11.6显示了一个例子变换图的一些工作，这些先进的功能。axes1具有对数X轴;axes1和axes2共享相同的Y轴。
![](http://aosabook.org/images/matplotlib/transform_tree.png)
#### 11.5. The Polyline Pipeline ####
当标绘线图，也有一些用于把原始数据绘制为屏幕上的线的步骤。在matplotlib的早期版本中，所有这些步骤都纠结在一起。此后，它们被重构，实现为一个“路径转换”流水线中的不连续步骤。这使得每个后端可以选择流水线的某一部分来执行，因为流水线的一些部分只在某些情况下是有用的.
  * 变换：从数据坐标转换为坐标图坐标。如果这是一个纯粹的仿射变换，如上所述，这是作为一个矩阵乘法一样简单。如果这涉及任意变换，变换函数被调用的坐标转换成数字空间。
  * 处理数据丢失:该数据阵列可能有部分在数据丢失或无效。用户可以通过这些值设定为NaN时，或使用numpy的掩蔽阵列任表明这一点。矢量输出格式，如PDF和渲染库，如此Agg，不经常有绘制一个折线时丢失数据的概念，因此，管道的这一步必须用MOVETO命令，告知在丢失的数据段跳跃渲染拿起笔，开始在一个新的点上重新绘制。
  * 剪裁:图中的边界之外的点可以通过包括许多看不见的点增加文件大小。更重要的是，非常大或非常小的坐标值可以在输出文件的渲染，这会导致完全混乱的输出导致溢出错误。管道剪辑的这一步骤，因为它进入和退出图中的边缘，以防止这两个问题的折线。
  * 贴紧：完美垂直线和水平线可以看模糊由于抗混叠时它们的中心未对准到一个像素的中心（参见图11.7）。流水线的捕捉步骤首先确定整个折线是否是由水平和垂直段（例如一个轴对齐的矩形），且如果是这样，轮每个所得顶点到最接近的像素中心。这个步骤仅用于光栅后端，因为矢量后端应继续精确的数据点。在屏幕上查看时的矢量文件格式，如Adobe Acrobat一些渲染器，执行像素贴紧。
![](http://aosabook.org/images/matplotlib/pixel_snapping.png)
Figure 11.7: A close-up view of the effect of pixel snapping. On the left, without pixel snapping; on the right, with pixel snapping.
  * 简化：当绘制真的密集的地块，很多就行了点，实际上可能不是可见的。这是尤其如此表示嘈杂的波形图的。包括在剧情这些点增加文件大小，甚至可能打在允许的文件格式点的数量限制。因此，准确的落在他们的两个相邻点之间的线路上的任何点都拆除（见图11.8）。确定取决于基于什么是可见的由用户指定的一个给定的分辨率的阈值。
![](http://aosabook.org/images/matplotlib/path_simplification.png)
Figure 11.8: The figure on the right is a close-up of the figure on the left. The circled vertex is automatically removed by the path simplification algorithm, since it lies exactly on the line between its neighboring vertices, and therefore is redundant.

#### 11.6. Math Text ####
由于matplotlib的用户往往是科学家，能够直接把格式丰富的数学表达式放上图是非常有用的。也许对于数学表达式使用最广泛的语法是高德纳的TeX的排版系统。这是把输入表示为下面这样的纯文本语言：
```
\sqrt{\frac{\delta x}{\delta y}}
```
格式输出表达式中的字符和线条的位置。
matplotlib提供两种方法来渲染数学公式，首先，usetex,在主机上使用Tex的完全拷贝来渲染数学公式，Tex直接输出DVI(device independent)中定义的数学表达式的字符和线．matplotlib然后分析DVI文件并将其转换为一组绘制命令，然后其输出后端之一直接渲染到图上。这种方法处理晦涩的数学语法。但是，它需要用户有充分的工作和安装的TeX。因此，matplotlib还包括其自身的内部数学渲染引擎，称为mathtext。
mathtext是TeX的数学渲染引擎的直接端口，粘到使用pyparsing [McG07]解析框架编写一个更简单的解析器。这个端口是基于TeX发行的源代码[Knu86]的拷贝。简单解析器构建一颗由盒子和胶（在TeX的命名法）构成的语法书，即随后由布局引擎布局树。虽然其中包括完整的TeX数学渲染引擎，大组第三方TeX和LaTeX的数学库是没有的。在这样的库功能需要被移植的基础上，其中对常用的和非学科特有的功能排在第一位。这使得一个不错的，轻量级的方式来呈现最多的数学表达式。

#### 11.7. Regression Testing ####
从历史上看，matplotlib一直没有大量的低级别的单元测试。有时，如果出现一个严重的错误，就把一个用来重现它的脚本添加到源代码树中。缺乏自动化测试带来了所有的常见问题，尤其是之前工作的特征回归。（我们也许并不需要向你介绍自动化测试是一件好事。）当然，有这么多的代码和这么多的配置选项和可更换件（如后端），这是值得商榷的低一级单位单独测试将永远是不够的;而不是我们已经遵循的信念，这是最具成本效益的测试对于在一起工作的实体。
为此，作为一个第一次努力，编写一个脚本，用于生成一些行使matplotlib各种功能的plot，特别是那些有很难得到正确。这使得测试变得更容易一些，以检测当一个新的变化引起的意外破损，但仍然需要手动验证生成image的正确性。因为这需要大量的手工劳动的，不是很经常做。
作为第二步，这个步骤是自动的。当前matplotlib测试脚本生成多个重复的，但不是需要人工干预，这些地块被自动与基线相比的图像。所有的测试都是nose测试框架，这使得它非常容易产生哪些测试失败的报告内运行。
复杂的问题是，图像比较不能精确。
在FreeType字体渲染库版本的细微变化可以使文本的输出在不同的机器略有不同。这些差异是不够的，被认为是“错误的”，但足以甩开任何确切位对位比较。取而代之的是，测试框架计算两个图像的直方图，并计算它们的差的根均方。如果该差大于给定的阈值，则图像被认为过于不同，并比较测试失败。如果测试失败，差分图像生成该节目在哪里发生了变化曲线（见图11.9）。那么开发人员可以决定是否失败是由于故意的变化和更新基线图像匹配新的形象，还是决定形象，其实是不正确的，跟踪并解决引起变化的bug。
![](http://aosabook.org/images/matplotlib/regression.png)



Figure 11.9: A regression test image comparison. From left to right: a) The expected image, b) the result of broken legend placement, c) the difference between the two images.
由于不同的后端可以促进不同的bug，测试框架将对每个小部分测试多个后端：PNG，PDF和SVG。对于矢量格式，我们不直接比较向量信息，因为有多种方式来表示什么时候光栅化具有相同的最终结果。矢量后端应该随意改变其产出的具体情况，以提高效率，而不会导致所有的测试失败。因此，对于矢量后端，测试框架第一渲染使用外部工具（Ghostscript的对PDF和Inkscape中对SVG）文件到一个光栅，然后使用这些栅格进行比较。
使用这种方法，我们能够更容易地引导从头合理有效的测试框架，比我们去了就写了许多低级别的单元测试。不过，它并不完美;测试的代码覆盖率还不是很完整，这需要很长的时间来运行所有测试。（大约在2.33 GHz英特尔酷睿2 E6550 15分钟。）因此，一些回归仍旧落空的裂缝，但总体而言，因为测试框架，设置了版本的质量有了很大的改善。

#### 11.8. Lessons Learned ####
一个从matplotlib发展的重要教训是，正如勒·柯布西耶说：“好建筑师善于借鉴”.matplotlib的早期作家在很大程度上是科学家，自学成才的程序员试图完成他们的工作，没有经过正式培训的计算机科学家。因此，我们没有得到第一次尝试内部设计权。实现面向用户的脚本层与MATLAB API大体兼容的决定中受益的项目在三个显著方式：它提供了一个经过时间考验的界面来创建和自定义图形，这一个简单的过渡，从的大基地matplotlib做MATLAB用户，以及最重要的是为我们matplotlib的背景架构，它释放的开发商重构内部的面向对象的API几次几乎不影响大多数用户，因为脚本接口不变。虽然我们有API的用户（相对于脚本的用户）从一开始，他们大多是电力用户或开发能适应API的变化。该脚本的用户，在另一方面，可以一次写代码和几乎假定它是所有后续版本稳定。

对于内部绘图API，我们也从GDK借代，我们没有花足够的精力来确定这是否是绘图API的权利，而不得不付出相当大的努力后来经过多次后端是围绕这一API编写围绕一个简单的扩展功能和更灵活的绘图API。我们会一直通过采用PDF图纸规范[Ent11b]，这本身就是从几十年的经验的Adobe曾与它的PostScript规范发展良好的服务;这便给了我们大部分外的开箱即用的PDF本身的石英核芯显卡架构的兼容性，以及Enthought启用Kiva的绘图工具包[Ent11a]。
Python的一个诅咒的是，它是这样一个简单而传神的语言，开发人员经常发现它更容易重新发明和重新实现存在于工作以外包代码包等整合功能。matplotlib可能受益于早期发展从花费更多的精力在集成现有模块和API，如Enthought的基瓦并启用它解决了很多类似的问题，而不是重塑功能的工具包。与现有的功能整合是一个双边缘剑的，因为它可以使构建和释放更复杂，并减少在内部开发灵活性。
