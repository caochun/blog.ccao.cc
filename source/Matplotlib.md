# Matplotlib #

matplotlib是一个基于Python的绘图库，完全支持二维图表绘制，对三维图表支持有限。它被广泛用于Python科学计算，该绘图库希望适应广泛的用户需求。matplotlib能支持交互式绘图，它可以根据你所选的用户接口工具来嵌入绘图库，目前它支持包括GTK+、Qt、Tk、FLTK、wxWidgets与Cocoa等所有主流桌面操作系统上的工具包。在Python的交互式shell中，我们可以使用简单的、过程式的命令，交互式地调用matplotlib来生成图形，与使用Mathematica、IDL或者MATLAB绘图非常相似。matplotlib也可以嵌入到无报文头的Web服务器中，以提供基于光栅（如PNG格式）与矢量（如Postscript、PDF以及纸面效果很好的SVG 格式）这两种格式的图形硬拷贝。

##1.硬件锁问题 ##
我们其中一位开发者（John Hunter）与他的研究癫痫症的同事们试图在不借助专有软件的情况下进行脑皮层电图（ECoG）分析，于是便有了最初的matplotlib。John Hunter当时所在的实验室只有一份电图分析软件的许可证，但有各式各样的工作人员，如研究生、医科学生、博士后、实习生、以及研究员，他们轮流共享该专有软件保护器（加密狗）。生物医学界广泛使用MATLAB进行数据分析与可视化，所以Hunter着手使用基于MATLAB的matplotlib来代替专有软件，这样很多研究员都可以使用并且对其进行扩展。但是MATLAB天生将数据当作浮点数的数组来处理。然而在实际情况中，癫痫手术患者的医疗记录具有多种数据形式（CT、MRI、ECoG 与EEG 等），并且存储在不同的服务器上。MATLAB作为数据管理系统勉强能应付这样的复杂性。Hunter感到MATLAB不适合于这项任务，便开始编写一个基于GTK+工具包（一种图形用户界面（GUI）工具包，当时是linux系统下编写视窗系统的主流工具包）的全新的python应用程序。

所以matplotlib这一GTK+应用程序最初便被开发成EEG/ECoG可视化工具。这样的使用方式决定了它最初的软件架构。matplotlib最初的设计也服务于另一个目的：代替命令驱动的交互式图形生成（这一点 MATLAB做得很好）工具。MATLAB的设计方法使得加载数据文件与绘图这样的任务非常简单，而要使用完全面向对象的API则会在语法上过于繁琐。所以 matplotlib也提供状态化的脚本编程接口来快速、简单地生成与 MATLAB类似的图形 。因为 matplotlib是Python库，所以用户可以使用 Python中各种丰富的数据结构，如列表、辞典与集合等等。 
![](/images/46.png)

图1.1 最初版本的matplot：一个ECoG查看器


## 2. matplotlib软件架构概述 ##
顶层的matplotlib对象名为Figure，它包含并且管理某个图形的所有元素。matplotlib必须解决的一个核心架构性任务是实现Figure的绘制与操作，并且做到该框架与Figure渲染到窗口或者硬拷贝（可以简单理解为打印输出）的动作是分离的。这使得我们可以为Figure添加越来越复杂的特性与逻辑，同时保持“后端”或输出设备的相对简化。matplotlib不仅封装了用于向多种设备渲染的绘图接口，还封装了基本事件处理以及多数流行的用户界面工具的视窗功能。因此，用户可以创建相当丰富的交互式图形算法与用户界面工具（用到可能存在的鼠标与键盘），而又不必修改matplotlib已经支持的6种界面工具。

要实现这些，matplotlib的架构被逻辑性地分为三层，这三层逻辑可以视为一个栈。每一层知道如何与它的下一层进行通信，但在下层其实不会感知到上层的存在。这三层从底向上分别为：后端、美工与脚本。

### 2.1 后端 ###
matplotlib逻辑栈最底层是后端，它提供了如下这些抽象接口的具体实现：
  * FigureCanvas 对绘图表面（如“绘图纸”）的概念进行封装。
  * Renderer 执行绘图动作（如“画笔”）。
  * Event 处理键盘与鼠标事件这样的用户输入。

对于如Qt这样的用户界面工具，FigureCanvas中包含的具体实现可以完成三个任务：将自身嵌入到原生的Qt窗口（QtGui.QMainWindow），将 matplotlib的Renderer命令转换到canvas上（QtGui.QPainter），以及将原生Qt事件转换到matplotlib的Event框架下（ 后者产生回调信号让上行监听者进行处理）。抽象基类定义在matplotlib.backend_bases 中 ， 且 所 有 派 生 类 都 定 义 在 如 matplotlib.backends.backend_qt4agg这样的专用模块中。对于专门生成硬拷贝输出（如 PDF、PNG、SVG 或 PS）的纯图像后端而言，FigureCanvas的实现可能只是简单地建立一个类似文件的对象，其中定义默认的文件头、字体与宏函数，以及 Renderer 创建的独立对象（如直线、文本与矩形等）。

Renderer的任务是提供底层的绘图接口来将“墨水”加到“画布”上。正如前文提到的，最初的matplotlib程序是一个基于GTK+的ECoG查看器，而且很多早期设计灵感都源自当时已有的GDK/GTK+的API。最初Renderer的API源自GDK的Drawable接口，后者实现了draw_point、draw_line、draw_rectangle、draw_image、draw_polygon以及draw_glyphs这样的基本方法。我们实现的每个不同后端——最早有PostScript与GD——都实现了GDK的Drawable接口，并将其转换为独立于后端的原生绘图命令。如上所述，这毫无必要地增加了后端的实现复杂度，原因是单独实现Drawable造成函数泛滥。此后，这个API已经被极大的简化，将matplotlib移植到新的用户界面或文件格式已经是非常简单的过程。

一个对matplotlib有利的设计决定是支持使用C++模板库Anti-Grain Geometry（缩写为agg[She06]）的基于像素点的核心渲染器。这是一个高性能库，可以进行2D反锯齿渲染，生成的图像非常漂亮。matplotlib支持将agg 后端渲染的像素缓存插入到每种支持的用户界面中，所以在不同的UI 与操作系统下都能得到精确像素点的图形。因为matplotlib生成的PNG输出也使用agg渲染器，所以硬拷贝与屏幕显示完全相同，也就是说在不同的UI与操作系统下，PNG的输出所见即所得。

matplotlib的Event框架将key-press-event或mouse-motion-event这样的底层UI事件映射到KeyEvent或MouseEvent类。用户可以连接到这些事件进行函数回调，以及图形与数据的交互，如要pick一个或一组数据点，或对图形或其元素的某方面性质进行操作。下面的示例代码演示了当用户键入‘t’时，对Axes窗口中的线段进行显示开关。

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

对底层UI 事件框架的抽象使得matplotlib 的开发者与最终用户都可以编写UI 事件处理代码，而且“一次编写，随处运行”。譬如，在所有用户界面下都可以对matplotlib 图像进行交互式平移与放缩，这种交互式操作就是在matplotlib 的事件框架下实现的。

### 2.2 Artis层 ###
Artist层次结构处于 matplotlib的中间层，负责很大一部分繁重的计算任务。延续之前将后端的 FigureCanvas 看作画纸的比喻，Artis 对象知道如何用Renderer（画笔）在画布上画出墨迹。matplotlib中的 Figure就是一个Artist 对象实例。标题、直线、刻度标记以 及 图 像 等 等 都 对 应 某个Artist 实 例（ 如 图 11.3 ）。Artist 的 基 类 是matplotlib.artist.Artist，其中包含所有 Artist的共享属性，包括从美工坐标系统到画布坐标系统的变换（后面将详细介绍）、可见性、定义用户可绘制区域的剪切板、标签，以及处理“选中”这样的用户交互动作的接口，即在美工层检测鼠标点击事件。 

![](/images/47.png)

图2.1：matplotlib 生成的图形

![](/images/48.png)

图2.2：用于绘制图11.2的Artist 实例的层次结构

Artist层于后端之间的耦合性存在于 draw 方法中。譬如，下面假想的SomeArtist 类是Artist的子类，它要实现的关键方法是 draw，用来传递给后端的渲染器。Artist不知道渲染器要向哪种后端进行绘制（PDF、SVG 与GTK+绘图区等），但知道 Renderer的 API，并且会调用适当的方法（draw_text 或 draw_path）。因为 Renderer 能访问画布，并且知道如何绘制，所以 draw方法将 Artist的抽象表示转换为像素缓存中的颜色、SVG 文件中的轨迹或者其他具体表示。
```
class SomeArtist(Artist):
'An example Artist that implements the draw method'

def draw(self,render):
    """Call the appropriate renderer methods to paint self onto canvas"""
    if not self.get_visible(); return

    #create some objects and use renderer to draw self here
    renderer.draw_path(graphics_context,path,transform)
```

该层次结构中有两种类型的 Artist。基本 Artist 表示我们在图形中能看到的一类对象，如Line2D、Rectangle、Circle 与Text。复合 Artist 是Artist 的集合，如Axis、Tick、与 Figure。每个复合Artsit 可能包含其他复合 Artist 与基本Artist。譬如，Figure包含个或多个Axes，并且Figure的背景是基本的 最重要的复合 Artist 是 Axes，其中定义了大多数 matplot的绘图方法。Axes不仅仅大多数构成绘图背景（如标记、轴线、网格线、色块等）的图形元素，还包括了大量生成本 Artist并添加到Axes 实例中的帮助函数。譬如，表11.1列出了一些Axes函数，这些 函数进行对象的绘制，并将它们存储在Axes实例中。 

表2.1：Axes的方法样例及其创建的Artist 实例


|方法 |创建对象|存储位置 |
|-|-|-|
| Axes.imshow | 一到多个matplotlib.image.AxesImage | Axes.images |
| Axes.hist | 大量matplotlib.patch.Rectangle | Axes.patches |
| Axes.plot | 一到多个matplotlib.lines.Line2D | Axes.lines |

下面这个简单的 Python脚本解释了以上架构。它定义了后端，将 Figure链接至该后端，然后使用数组库numpy 创建10,000个正太分布的随机数，最后绘制出它们的柱状图。

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

### 2.3 脚本层(pyplot) ###
使用以上 API 的脚本效果很好，尤其是对于程序员而言，并且在编写 Web 应用服务器、UI 应用程序或者是与其他开发人员共享的脚本时，这通常是比较合适的编程范式。对于日常用途，尤其对于非专业程序员而要完成一些交互式的研究工作的实验科学家而言，以上API 的语法可能有些难以掌握。大多数用于数据分析与可视化的专用语言都会提供轻量级的脚本接口来简化一些常见任务。matplotlib 在其matplotlib.pyplot接口中便实现了这一点。以上代码改用pyplot之后如下所示。

```
import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(10000)
plt.hist(x, 100)
plt.title(r'Normal distribution with $\mu=0, \sigma=1$')
plt.savefig('matplotlib_histogram.png')
plt.show()
```

![](/images/49.png)

图 2.3 用pyplot绘制的柱状图

pyplot是一个状态化接口，大部分工作是处理样本文件的图形与坐标的生成，以及与所选后端的连接。它还维护了模块级的内部数据结构。这些数据结构表示了直接接收绘图命令的当前图形与坐标。

下面仔细分析示例脚本中比较重要的几行，观察其内部状态的管理方式。

  * import matplotlib.pyplot as plt：当pyplot模块被装载时，它会解析一个在本地本的配置文件中的用户声明的默认后端偏好设置。这有可能是一个像QtAgg一样的用户交互后端后台，在这种情况下，前面的脚本将导入的GUI框架，并启动嵌入了plot的Qt窗口，或者它可能是一个像AGG一样的纯图片后端，在这种情况下，该脚本将产生硬拷贝输出并退出。
  * plt.hist(x, 100)：这是这个脚本的第一条绘图命令，pyplot会检查它自己内部的数据结构，来确定是不是已经有了一个当前的图表实例。如果有，那么它会提取当前的Axes并且直接调用Axes.hist的API。如果没有的话，它就会创建一个图表和Axes，并将这两者设置为当前的，并且直接绘制Axes.hist。
  * plt.title(r'Normal distribution with $\mu=0, \sigma=1$')：像上面一样，pyplot会检查是不是已经有了一个当前的图表和Axes对象。如果有，它就不会创建新的实例，并且直接调用已有Axes实例的Axes.set_title方法。
  * plt.show()：这个命令会让Figure渲染，如果用户已经在配置文件中声明了一个默认的GUI后端，pyplot会启动这个GUI的主循环并输出所有的图表。

下面我们以一个经常用来画线的函数matplotlib.pyplot.plot的简化版本为例，来解释一下一个pyplot函数是如何被封装在matplotlib的面向对象内核中的。其他所有的pyplot脚本交互函数都遵循相同的设计。

```
@autogen_docstring(Axes.plot)
def plot(*args, **kwargs):
    ax = gca()

    ret = ax.plot(*args, **kwargs)
    draw_if_interactive()

    return ret
```

@autogen_docstring(Axes.plot)这个python装饰器会提取对应API的文档字符串，并附加一个被正确格式化的版本到pyplot.plot方法上。我们有一个专用的模块matplotlib.docstring来处理这个docstring魔法。在这个文档字符串签名中的*args和**kwargs是Python中的特别约定，用来表示所有的参数和关键词参数将通过这两者传入这个方法。这使得我们可以按照这些参数来找到对应的API方法。ax=gca()调用状态机来获取当前的Axes对象(每一个Python解释器只能有一个当前的Axes对象)，并且如果有必要的话会创建Figure和Axes对象。ret = ax.plot(*args, **kwargs)这句调用了合适的Axes方法并且存储了将要返回的返回值。因此pyplot接口是一个Artist API内核相当轻的封装，Artist内核通过暴露API方法，尽可能减少代码重复，在这个脚本接口中的调用签名和装饰字符串是最小化的模板代码。

##3.后端重构##
随着时间推移，输出后端的绘图API添加了大量的方法，包括：
```
draw_arc
draw_image 
draw_line_collection 
draw_line 
draw_lines 
draw_point
draw_quad_mesh
draw_polygon_collection
draw_polygon 
draw_rectangle
draw_regpoly_collection
```
不幸的是，越来越多的后端方法意味着写一个新的后端将会花费大量的时间，并且当新特性被加到内核后，更新已有的后端也是一项相当可观的工作。由于每一个后端都由一个精通某种输出格式的独立开发者所开发，有时候会需要很长的时间才能把一个新特性加到后端，从而导致用户会比较困惑新特性可以从哪里调用。


  * draw_path:绘制复合多边形，由直线和贝塞尔段组成，这个接口替换了许多旧的方法：draw_arc, draw_line, draw_lines, 和draw_rectangle。
  * draw_image:绘制光栅图片。
  * draw_text：根据给定的字体绘制文本。
  * get_text_width_height_descent：输入一个字符串，返回它的长宽。

只是用以上这些必要的绘图方法来构建一个新的后端是可以做到的。（我们甚至可以进一步，移除draw_text方法，用draw_path方法来绘制文本，但是我们并没有足够的时间来完成这样的简化。当然，后端仍然可以自由调用它自己的draw_text方法来输出真正的文本。）这对于新开发一个后端以及更简单地运行非常有帮助。但是，在某些情况下，后端可能会想要重写内核的这些行为，来获取更高效地输出。比如，当绘制一些标记时（小的符号，用来指示线图的顶点），采取只写一次标记的形状到文件，并且在所有用到它的地方都作为一个stamp，的方法更加节省空间。在那种情况下，后端可以继承一个draw_markers方法。如果这个方法被继承，后端就只会输出这个标记的形状一次，并且在许多地方输出许多更为简短的命令来重复使用它。如果没有被继承，内核就会简单地多次调用draw_path，多次绘制这个标记。

完整的可选后端API如下：

  * draw_markers: 绘制一系列的标价。
  * draw_path_collection: 绘制一个路径的集合。
  * draw_quad_mesh: 绘制一个四边形网格。

##4.变换##
matplotlib花了很多时间用来将坐标系从一个系统中变换到另一个系统中。这个坐标系统包括：
  * data: the original raw data values
  * axes: the space defined by a particular axes rectangle
  * figure: the space containing the entire figure
  * display: the physical coordinates used in the output (e.g. points in PostScript, pixels in PNG)

每一个Artist都拥有一个变换节点，这个节点知道如何从一个坐标系变换到另一个坐标系。这些变换节点的连接方式是有向图，每个节点都独立于它的父节点。通过有向图中通向根节点的边，数据空间的坐标可以一直变换直到最终。同时，大多数变换都是可逆的。这使得点击图标中的单个元素，获取其数据空间中的坐标成为可能。这个变换图在变换节点之间建立这样的依赖关系：当一个父节点变换了，比如当一个Axes对象的限制发生了改变，任何与这个Axes对象相关的变换就都无效了，因此他们需要被重新绘制。而这个图表中，和其他Axes对象相关的变换，当然，可能会被独立开，以避免不必要的重复计算，从而获得更好地交互表现。

变换节点可能不光是简单的仿射变换，也可能是非仿射变换。仿射变换属于保持直线和距离的比率的哪一类变换，包括旋转，平移，缩放和斜切等。二维的仿射变换用3×3的变换矩阵来表示。变换后的点(x', y')由矩阵乘以原来的点 (x, y) 得到：

![](/images/50.png)

二维坐标可以很容易的使用简单的变换矩阵来完成变换。仿射变换通过矩阵乘法可以将有用的属性组合起来。这意味着要执行一系列的放射变换，可以先将这些变换乘起来，然后这个结果变换矩阵可以用来变换坐标。matplotlib的变换框架为了减少计算量，在变换坐标之前就自动组合了仿射变换。快速的放射变换是相当重要的，因为它能够使GUI界面中的平移和缩放变换更加高效。

而matplotlib中的非仿射变换使用Python的函数来定义，因此他们实在是有些任意。在matplotlib的内核中，非仿射变换用来做对数缩放，极坐标和地理预测(如图 4.1)。这些非仿射变换可以自由地和仿射变换组合。matplotlib会自动地简化仿射变换的部分，并且为了执行非仿射的部分，它回退到任意函数。

![](/images/51.png)

图4.1 相同的数据三种不同的呈现方式：对数，极坐标，兰伯特投影

基于这些简单的模块，matplotlib可以做一些相当高级的东西。混合变换是一种使用了X和Y两个坐标变换的特殊变换。这仅在给定的变换是分离的（也就是X和Y坐标是独立的，但是它们自身可能既是仿射的又是非仿射的）情况下才有可能。举个例子，这被用于绘制X和Y轴都是对数标尺的对数图像。混合变换节点让组合变换可以以任意方式组合。变换图同时还允许共享坐标轴。可以将一个图连接到另一个图，并且保证当其中一个缩放或者平移的时候，另外一个也做出相应的更新来适应其对应的图。在这种情况下，相同的变换节点被简单地由两个坐标轴共享，甚至可能出现在两个完全不同的图表上。图4.2展示了这样的一个例子。其中axes1有一个对数x轴，axes1和axes2共享一个y axes。

![](/images/52.png)

图4.2 变换图示例

##5.折线管道##
当绘制折线图的时候，从原始数据到屏幕输出，中间有许多步骤要执行。在matplotlib的早期版本，这些步骤是纠缠在一起的。此后，他们被重构，从而使它们在一个路径转换的管道中分离开来。这就使得每个后端可以选择执行管道的某一个部分，因为有一些只在某些上下文中才会有用。

  * Transformation：坐标由数据表示转换到图像表示。如果这是一个纯粹的仿射变换（见前面的定义），那么这就和矩阵乘法一样简单。如果涉及到任意变换，变换函数就会被调用，将坐标转换到图像空间。
  * Handle missing data:数据数组中可能会有缺失或者失效的部分。用户可以用NaN来申明这些部分，或者用numpy来隐藏这些数组。矢量输出格式，比如PDF和渲染库（比如Agg）,在绘制折线的时候，就从来没有缺失数据这一概念，因此绘图管道的这一步就必须用MOVETO命令跳过缺失的数据段，并告诉渲染器从一个新的点开始重新绘制。
  * Clipping：图像边界之外的点会增加文件的大小。更重要的是，非常大或者非常小的坐标值会在渲染的时候导致溢出错误，从而生成一堆乱码输出。管道的多边形裁剪这一步是为了避免这两个问题。
  * Snapping：完美垂直和水平的直线，当它们的中心没有对齐到像素中心时，可能会因为抗锯齿而看起来有点模糊（如图 5.1）。管道的snapping这一步首先会决定整个折线是不是有垂直或水平段（比如一个坐标对齐的长方形），如果是这样的话，将这个长方形的每个顶点近似到它各自最近的像素中心点。这一步仅用于光栅输出的后端，因为矢量后端应该继续使用准确的数据点。一些支持矢量文件格式的渲染器，比如Adobe Acrobat，在呈现到屏幕的时候才会做snapping操作。

![](/images/53.png)

图 5.1 像素对齐的细节效果。左边：无像素对齐，右边有像素对齐。
  * Simplification：当绘制非常稠密的图表时，线上的很多顶点实际上并不会显示出来。这在表示噪声波的图表上特别明显。将这些点添加在图表上会增加文件大小，甚至会达到该文件格式所允许的顶点数上限。因此，任何位于相邻两点的连线上的点都将被移除（如图5.2）。这个判定基于用户设置的解析度。

![](/images/54.png)

图 5.2 右图是左边的某个细节部分。右图中圈起来的那个点由于位于相邻两个点的连线上，因此是多余的，所以被路径简化算法自动移除了。

##6.数学公式##
由于许多matplotlib的用户是科学工作者，在图表上直接添加丰富的格式化的数学表达式是非常有用的。可能最被广泛使用的数学表达式语法是Donald Knuth的TeX排版系统。它将像这样的纯文本输入：

```
\sqrt{\frac{\delta x}{\delta y}}
```

转换为格式化的数学表达式。

matplotlib提供了两种方法来渲染数学表达式。第一种就是使用tex语法，在用户机器上使用完整的TeX系统来渲染数学表达式。TeX在它自己的原生DVI（设备独立）格式中输出字符和线的位置。matplotlib然后解析DVI文件并将其转换成一系列的绘图命令，其中某一个输出后端就直接渲染到图表上。这种方法解决了许多模糊的数学语法。不过，它要求用户有一个完整可运行的TeX，因此，matplotlib也有它自己的内部数学渲染引擎，名叫mathtext。

mathtext是一个直接的TeX数学渲染引擎接口，整合了一个相当简单的用pyparsing解析框架写的解析器。这个接口基于TeX的公开版源码。这个简单的解析器建立一个盒子树和连接器（在TeX的命名空间），然后由布局引擎布局。尽管完整的TeX数学渲染引擎被整合进来了，但是一大批的第三方TeX和LaTeX数学库却没有。这个整合的原则是基于用到才会被整合进来，像一些使用频率非常高的，不具备学科单独特性的接口会被整合。这使得mathtext成为一个漂亮轻巧的,能够渲染大多数数学表达式的方式。

##7.回归测试##
从历史上来看，matplotlib并没有大量的低级单元测试。偶然的，如果一系列bug被报告了，会有一个脚本将它复制到对应的在源码树中的目录。缺少自动化测试导致了所有这些常见的问题，最重要的是回退到以前能工作的特性。（我们可能不需要安利你自动化测试是一个好东西）。当然，有这么多的代码，这么多的配置选项和可互换的模块（比如很多的后端），有争议的是，独立的低级别的单元测试可能是远远不够的。相反，我们认为测试一起测试所有的模块才是最具有性价比的。

为此，作为第一次的努力，我们写了一个可以生成许多图表的，用于测试matplotlib各个特性的脚本，尤其针对那些不容易正确的部分。
这使得检测新变化导致的无意间的破损变得更加容易，但是图表的正确性还是需要手动去检查。因为这需要许多手工操作，所有我们不经常做这样的检测。

到了第二阶段，这些普遍的方法都已经自动化了。目前的matplotlib测试脚本生成许多的图表，但是已经不需要手工干预了，那些图表会自动和基准图像比较。所有这些测试都在nose测试框架内运行，并且使得生成哪些测试失败的报告变得非常容易。

使问题复杂化的是，图像的对比是不准确的。在FreeType字体渲染库版本的微妙变化可以使文本稍有不同，在不同的机器上输出。这些差异不足以被认为是“错误的”，但也足以把任何确切的位比较。相反，测试框架计算两个图像的直方图，并计算其差异的根均方。如果这种差异大于给定的阈值，则图像被视为太大，而比较测试失败。当测试失败了，展示两张图片不同的差异图像就会生成（如图 7.1）。开发人员可以决定是否是由于故意改变和更新的基线图像匹配的新的图像，或决定的图像是在事实上不正确和跟踪和修复的错误造成的变化。

![](/images/55.png)

图 7.1 回归测试图比较。从左到右：a)期望的图像,b)测试结果，c)两张图的差异

由于不同的后端可以提供不同的bug，测试框架，测试多个后端的每个情节：PNG、PDF和SVG。对于矢量格式，我们不比较矢量信息直接，因为有多种表达方式有相同的结果时，光栅化。矢量的后台可以自由改变其输出的细节来提高效率而不引起所有失败的测试。因此，矢量的后端，测试框架首先将文件光栅使用外部工具（Ghostscript的PDF和Inkscape SVG）然后使用栅格数据的比较。

使用这种方法，我们能够引导一个合理有效的测试框架，从零开始，更容易比我们已经走上写下许多低级别的单元测试。然而，它不是完美的，测试的代码覆盖率不是很完整，它需要很长的时间来运行所有的测试。（在2.33 GHz英特尔核心2 e6550。约15分钟）因此，一些回归仍然通过裂缝下降，但总体质量的发布以来的测试框架的实施大大提高了。

##8.学到的东西##
一位来自matplotlib发展的重要教训是，正如柯布西耶说：“好的建筑师借”。Matplotlib早期作者主要科学家，自学的程序员试图做他们的工作，没有受过正式训练的计算机科学家。因此，我们没有得到内部设计上的第一次尝试。决定实施一个面向用户的脚本层在很大程度上兼容Matlab API受益项目三个重要方面：它的时间测试接口来创建和自定义图形提供了一个简单的过渡从MATLAB用户基数大，matplotlib，最重要的是我们在matplotlib建筑释放开发者重构内部的面向对象的API几次与大多数用户的影响最小，因为脚本接口不变。虽然我们已经从一开始就已经拥有了一个接口的用户（相对于脚本用户），其中大多数是用户或开发人员能够适应原料药的变化。另一方面，脚本用户可以编写一次代码，相当多的假设它是稳定的，为所有后续版本。

对于内部绘图API，同时我们也借GDK，我们没有花足够的努力确定这是否是正确的绘图API，不得不花费相当大的力气随后经过许多后台写这个API在更简单和更灵活的绘图API的功能扩展。我们会一直采用PDF图纸规范[ ent11b ]很好的服务，这本身就是从几十年的发展经验与Adobe PostScript规范；它会给我们多出的PDF里面的兼容性，石英核心图形框架，和enthought使Kiva绘图。

一个Python的诅咒，这是一个很容易和富于表现力的语言，开发商往往更容易重新发明和重新实现的功能存在于其他包比工作整合其他包的代码。matplotlib可以得益于早期的发展从花费更多的努力在现有的模块集成和API如enthought的Kiva和使工具包解决很多类似的问题，而不是重塑功能。然而，与现有的功能集成，一把双刃剑，因为它可以使建立和释放更复杂，减少内部发展的灵活性。





