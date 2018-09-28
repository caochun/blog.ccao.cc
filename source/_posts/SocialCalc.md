# SocialCalc #

电子表格的历史有超过30年了。第一个电子表格VisiCalc是Dan Bricklin在1978年构思的，并在1979年传播开来。最初的理念是很直接的：一个文本、数字和公式构成的二维表格。公式由普通数学操作符和各种各样函数构成的，并且每个公式可以当做值使用其它当前内容的单元格。

尽管比喻很简单，但是它有很多应用：会计、发明、罗列管理。可能性是无限的。所有的这些都使得VisiCalc编程第一个个人电脑年代的杀手app。 

在这几十年来，很多后继者都做出了巨大的提高，像Lotus 1-2-3，但是核心是一样的。大多数电子表格存储成硬盘文件，当被打开编辑的时候表格就载入到内存。在基于文件的模型下，合作是尤其困难的，如下： 

* 每个使用者需要安装一个电子表格编辑器的版本； 

* 电子邮件、共享文件夹、或者安装一个微妙的版本控制系统，都被加入到簿记中； 

* 改变踪迹是有限的。比如，Excel不保存历史中格式的改变和单元格的注释； 

* 在模板中更新格式或者公式，需要对当前使用那个模板的电子表格文件作出艰苦的改变。 

幸运的是，一个新的合作小组模型产生了，并通过优雅的简单化把这些问题解决了。这就是wiki模型，Ward Cunningham在1994年的时候发明它，并且在两千年的早期通过维基百科风靡。 

wiki模型以主机服务器的网页为特征，而不是文件，不用特别的软件就可以在浏览器编辑。那些超文本网页可以互相容易地连接，甚至包括其它网页的部分，从而构成一个更大的网页。所有参与者观察和编辑最新版本，并且版本历史都被服务器自动地掌握。 

被wiki模型所激励，Dan Bricklin在2005年开始了WikiCalc的工作。它的目标在于把创作缓解和多人wiki编辑，与熟悉的可视化格式和电子表格的隐喻计算结合起来。
## 19.1 WikiCalc ##

WikiCalc的第一个版本（图19.1）有许多和其它电子表格区分开的特性。 
·纯文字、HTML，以及Wiki式的文本标记支持。 
·Wiki文字包含插入链接、图片，以及和从存储格引用值的功能。 
·公式存储格可以引用放在其他网站的 WikiCalc 网页里的值。 
·支持输出到静态网页，以及将动态资料内嵌至其他网页。 
·存储格能使用 CSS 来改变样式。 
·记录所有编辑操作，以供稽核纪录。 
·和Wiki系统一样，保留每一个版本，并可以随时回复 
![图19.1](/images/8.png)
                                             
![图19.2](/images/9.png)
                                             
![图19.3](/images/10.png)
                                             
WikiCalc 1.0的内部架构（图19.2）和信息流（图19.3）是简单的，但是很强大。从几个小型电子表格组建一个主电子表格的能力，是 WikiCalc 的一大强项。举例来说，每位销售员可以把营业额放在自己的电子表格页面里；然后销售经理可以综合这些资料到该区的电子表格中，之后销售副总再综合各区域的数字，构成主电子表格。 每次电子表格之一被更新了，所有的相关电子表格都能反应这个更新。如果有人想看到更详细的信息，他们只要点击去查看这个电子表格后面的电子表格就好了。这种能力减少了更新数字可能出现的多余或者出错的努力，并且确保了所有信息的视图保持最新状态。
为了保证计算数据是最新的，WikiCalc采取了一种"瘦"客户端的设计，保持所有的状态信息在服务器端。每个电子表格在浏览器都用table代表；编辑一个单元格会发送一个ajaxsetcell调用给服务器，并且服务器会告诉浏览器哪个单元格需要更新。 
不足为奇，这个设计取决于浏览器和服务器间的快速联系。当潜伏因素多的时候，用户将开始注意到"Loading..."消息的频繁出现，就像表格19.4展示的那样。这个对于用户交互地编辑并期待实时看到结果是一个问题。 
![图19.4](/images/11.png)
                                             
此外，因为table元素和电子表格有相同的维度，一个100*100的网格将创造10000DOM项目，这拉长了浏览器的记忆资源，限制了网页大小。 因为这些缺点，虽然WikiCalc作为在本地主机运行的独立服务器是方便使用的，但是当做网页内容管理系统的一部分是不切实际的。 在2006年，Dan Bricklin和Socialtext一起组队开始发展SocialCalc，一个用js并基于一些Perl源代码的WikiCalc的重写。 这次重写目的在于大的分布式的合作，并且寻求展示一个视图并更像一个桌面应用。其它设计目标包括： ·能够处理成千的单元格 ·编辑操作具有快速的转向时间 ·客户端审计追踪和撤销/恢复栈 ·更好地使用js和CSS以提供展示功能 ·支持不同版本的浏览器，尽管相应的js需要更大代价 经过三年的开发和发布许多次测试版之后，Socialtext 在 2009 年发布 SocialCalc 1.0，成功实现了设计目标。现在，让我们来看看 SocialCalc 的系统架构。

## 19.2 SocialCalc ##

![图19.5](/images/12.png)
                                             
图19.5和图19.6分别展示了SocialCalc的界面和类图。相比于WikiCalc，服务器的角色被大大减弱了。它的唯一职责是对HTTP GET进行相应，反馈保存格式的整个表单；一旦浏览器收到数据，所有的计算、变动轨迹和用户交流都在JavaScript中实现。
![图19.6](/images/13.png)
                                            
Javascript部分是按照MVC风格来设计的，每个类关注一个方面：

* Sheet是一个数据模型，代表电子制表软件一个内存结构。它包括了从坐标轴到单元格的字典，每个代表一个单元格。空的单元格不需要条目，因此不占内存。

* Cell代表一个单元格的内容和格式，一些普遍的属性在表格19.1。

* RenderContext完成视图，负责把表格转成DOM对象。

* TableControl是主要的控制器，接受鼠标事件和键盘事件。当它收到视图事件，比如滚动、调整大小，它更新与它相关的RenderContext对象。当它收到影响表单内容的更新事件时，它在指令队列中添加新的指令。

* SpreadSheetControl是有工具栏、状态栏、对话框、颜色选择器的最高层用户界面。

* SpreadSheetViewer是一个可选的最高层用户界面，提供只读的交互视图。

|||
|-|-|
| datatype  | t |
| datavalue | 1Q84 |
| color     | black |
| bgcolor   | white |
| font      | italic bold 12pt Ubuntu |
| comment   | Ichi-Kyu-Hachi-Yon |

                                             表19.1                                             

我们采取一种小的基于类的对象系统，包括简单的部分/委托，没有使用继承或者对象的原型。所有符号都被放在SocialCalc.*命名空间，以避免命名冲突。

每个表格的更新都经历了ScheduleSheetCommand方法，这个方法用指令字符串代表编辑。（一些常用的指令显示在表格19.2中。）嵌在SocialCalc中的应用可能自己定义了多余的命令，定义这些命令的时候需要在SocialCalc.SheetCommandInfo.CmdExtensionCallbacks对象中加入回调函数，并且使用startcmdextensin命令调用它们。


|||
|-|-|
| set   | sheet defaultcolor blue |
| set   | A width 100 |
| set    |A1 value n 42 |
| set    |A2 text t Hello |
| set    |A3 formula A1*2 |
| set    |A4 empty |
| set    |A5 bgcolor green |
| merge  |A1:B2 |
| unmerge |A1 |
| erase | A2|
|cut | A3 |
|paste | A4|
|copy | A5|
|sort |A1:B9 A up B down|
|name | define Foo A1:A5|
|name | desc Foo Used in formulas like SUM(Foo)|
|name |delete Foo|
|startcmdextension|UserDefined args|                                             表19.2
                                

## 19.3 Command Run-loop ##

为了提高响应程度，SocialCalc在背景执行所有的重新计算和DOM更新，所以当引擎在命令队列中处理前面的变动时，用户可以保持对一些单元格进行修改。

![图19.7](/images/14.png)
                                             
        
当命令正在运行时，TableEditor对象把busy的标志置为true，随后的命令放到defferredCommands队列中，确保一次序列顺序的执行。事件循环图显示在图19.7中，表格对象不停地发送StatusCallback事件，以通知当前命令执行状态的用户，经历下面这四个步骤：

* ExecuteCommand: 开始后发送cmdstart，命令完成执行后发送cmdend。如果命令间接改变一个单元格的值，则进入Recalc步骤。否则，如果命令改变了一个或多个屏幕上的单元格，则进入Render步骤。如果不是上述的情况（比如copy命令），则跳转到PositionCalculations步骤。

* Recalc（按需）：开始后发送calcstart，当检查单元格的从属链时每100ms发送calcorder，当检查完毕时发送calccheckdone，当所有受影响的单元格收到他们的重算值时发送calcfinished。这个步骤的下一个步骤总是Render步骤。

* Render: 开始后发送schedrender，当<table>元素被更新成格式化的单元格时发送renderdone。这个步骤的下一个总是PositionCalculations步骤。

* PositionCalculations: 开始后发送schedposcalc，在更新完滚动条、当前单元格光标、其它TableEditor的可视成分后发送doneposcalc。

因为所有的命令在执行时都被保存了，我们自然而然地得到所有操作的审查日志。Sheet.CreateAuditString方法提供了一个按新行隔开的字符串作为审查追踪，每个命令都是一个单独行。

ExecuteSheetCommand对每个执行过的命令创建了撤销命令。举个例子，如果单元格A1包括“Foo”，并且用户执行set A1 text Bar，那么撤销命令set A1 text Foo被放到撤销栈中。如果用户点击撤销，那么撤销命令把A2恢复到它原来的值。

## 19.4 Table Editor ##

现在让我们看看TableEditor层次。它计算了屏幕上RenderContext坐标，并且通过两个TableControl管理水平/垂直滚动条。

![图19.8](/images/15.png)
                                     
                                       
在视图层次，由RenderContext类处理，并且与WikiCalc设计不同。我们不是把每个单元格映射到&lt;td>元素，而是简单地创建一个固定大小的&lt;table>来适应浏览器的可视范围，并且用&lt;td>元素预先构建。

当用户通过滚动条滑动表单时，我们动态更新预先画好的&lt;td>元素的innerHTML。这个意味着在很多普遍情况下，我们不必创建或者毁坏&lt;tr>或者&lt;td>元素，这个极大地提高了相应速度。

因为RenderContext只实施可视区域。表单对象的大小可以很大，也不会影响操作。

TableEditor也包括一个CellHandles对象，这个实现了当前编辑单元格的右下角的填充/移动/滑动菜单，即ECell，如图19.9所示。

![图19.9](/images/16.png)

输入框由两个类管理：InputBox和InputEcho。前者管理网格上的编辑行，后者展示及时更新的预览层，覆盖ECell的内容（图19.10）。

![图19.10](/images/17.png)
                                                                          
通常，SocialCalc引擎当打开一个表单进行编辑时和将它存回服务器时，仅需要与服务器通信。出于这个目的，Sheet.ParseSheetSave方法将一个保存格式的字符串转成一个Sheet对象，Sheet.CreateSheetSave方法将Sheet对象转成存储格式。

范式可能通过URL链接指到远程电子表格。recalc命令重新获取外部被引用的电子表格，用Sheet.ParseSheetSave把它们转化，并把它们存储到暂存区中，使得用户引用相同远端表格中的其它单元格的内容，而不用再次获取它的内容。

## 19.5 Save Format ##

存储格式是标准的MIME 多部分/混合形式，包括四个纯文本、UTF-8编码的部分组成，每个部分包括新的换行、冒号分隔的数据域。这些部分包括：
* meta部分罗列了其它部分的类型。
* sheet部分罗列了每个单元格的格式和内容，每个纵列的宽度（非默认格式的情况）、表格的默认格式，以及表格中使用的字体、颜色、边框。
* 可选择的edit部分保存TableEditor的编辑状态，包括ECell上一个位置，列/行的固定大小。
* 可选择的audit部分包括了在之前编辑的历史运行命令。
举个例子，图19.11显示了一个有三个单元格的表格，1874位于A1并且是ECell，A2中是式子2^2*43，A3中以粗体形式显示了计算式SUM(Foo)，表示从A1到A2的Foo范围。
![图19.11](/images/18.png)
                                                                      
表格序列化的存储形式就像这样：
```
    socialcalc:version:1.0
    MIME-Version: 1.0
    Content-Type: multipart/mixed; boundary=SocialCalcSpreadsheetControlSave
    --SocialCalcSpreadsheetControlSave
    Content-type: text/plain; charset=UTF-8

    # SocialCalc Spreadsheet Control Save
    version:1.0
    part:sheet
    part:edit
    part:audit
    --SocialCalcSpreadsheetControlSave
    Content-type: text/plain; charset=UTF-8

    version:1.5
    cell:A1:v:1874
    cell:A2:vtf:n:172:2^2*43
    cell:A3:vtf:n:2046:SUM(Foo):f:1
    sheet:c:1:r:3
    font:1:normal bold * *
    name:FOO::A1\cA2
    --SocialCalcSpreadsheetControlSave
    Content-type: text/plain; charset=UTF-8

    version:1.0
    rowpane:0:1:14
    colpane:0:1:16
    ecell:A1
    --SocialCalcSpreadsheetControlSave
    Content-type: text/plain; charset=UTF-8

    set A1 value n 1874
    set A2 formula 2^2*43
    name define Foo A1:A2
    set A3 formula SUM(Foo)
    --SocialCalcSpreadsheetControlSave--
```
这个形式设计得易于阅读，也相对容易程序化地产生，这使得Drupal的Sheetnode插件使用PHP在这个形式和其它流行的表格形式之前的转换成为可能，比如Ecel和OpenDocument。
现在我们知道了如何在SocialCalc的部分配合到一起，现在我们看看两个现实生活中的扩展SocialCalc的例子。

## 19.6 Rich-text Editing ##

第一个例子是用wiki笔记提升SocialCalc的文本单元格，在表格编辑器中展示它丰富的文本。
![图19.12](/images/19.png)
                                         
在SocialCalc 1.0之后的版本中添加了这个特征，用统一的语法解决了插入图片、链接、文本标记的广泛要求。既然Socialtext已经有一个开源的wiki平台，自然地重复使用了SocialCalc的语法。
为了完成这个，我们需要给text-wiki的textvalueformat提供特定的格式，用它改变文本单元格的默认形式。
什么是textvalueformat？继续往下看。

### 19.6.1 Types and Formats ###

在SocialCalc中，每个单元格都有一个datatype和一个valuetype. 包含文本或者数字的数据单元格对应文本型/数字型的值类型，并且公式单元格有datatype = "f"大概产生数字型或者文本型的值。
回忆绘制步骤，Sheet对象从每个单元格产生HTML。它通过考察每个单元格的valuetype:如果以t开头，那么单元格的textvalueformat属性决定了如何产生；如果以n开头，那么nontextvalueformat属性被使用。
但是，如果单元格的textvalueformat或者nontextvalueformat属性没有准确定义，那么默认的形式可从它的valuetype中查找，如图19.13所示。
![图19.13](/images/20.png)
                                                                         
对text-wiki值格式的支持在SocialCalc.format_text_for_display中：
```
if (SocialCalc.Callbacks.expand_wiki && /^text-wiki/.test(valueformat)) {
    // do general wiki markup
    displayvalue = SocialCalc.Callbacks.expand_wiki(
        displayvalue, sheetobj, linkstyle, valueformat
    );
}
```
不是把wiki-to-HTML扩展器内联到format_text_for_display，而是在SocialCalc.Callbacks中定义了一个新的hook。这是SocialCalc编码体系中推荐的形式，它通过用不同方式扩展wikitext，保持无需此特性的嵌入器的兼容性，提高了模块性。          
  
### 19.6.2 Rendering Wikitext ###
            
接着，我们将使用Wikiwyg（脚注1），一个提供了wikitext和HTML之间两种转换的js库。
我们通过取得单元格的文本内容，通过Wikiwyg的parser和HTML的emitter来定义expand_wiki函数:
```
var parser = new Document.Parser.Wikitext();
var emitter = new Document.Emitter.HTML();
SocialCalc.Callbacks.expand_wiki = function(val) {
    /* Convert val from Wikitext to HTML*/
    return parser.parse(val, emitter);
}
```
最后一个步骤关于在表单初始化后加入set sheet defaulttextvalueformat text-wiki命令的执行：
```
/* We assume there's a <div id="tableeditor"/> in the DOM already */
var spreadsheet = new SocialCalc.SpreadsheetControl();
spreadsheet.InitializeSpreadsheetControl("tableeditor", 0, 0, 0);
spreadsheet.ExecuteCommand('set sheet defaulttextvalueformat text-wiki');
```
合起来，绘制步骤如图19.14工作。
![图19.14](/images/21.png)  
                                                                               
就这样，提高后的SocialCalc现在支持一系列丰富的wiki标注语法：
![](/images/22.png)

试着在A1单元格键入*bold* _italic_ `monospace`，你将看到绘制的丰富的文本显示（图19.15）。   
![图19.15](/images/23.png)
                                                                                        


## 19.7 Real-time Collaboration ##

下面的例子是探索在共享表单上多用户、实时编辑。这个在一开始看起来有些复杂，但是多亏了SocialCallc的模块化设计，我们需要做的就是给每位在线用户向其他参与者传播他们的命令。
为了区分局部命令和远程命令，我们给ScheduleSheetCommands加入了一个isRemote的变量:
```
SocialCalc.ScheduleSheetCommands = function(sheet, cmdstr, saveundo, isRemote) {
   if (SocialCalc.Callbacks.broadcast && !isRemote) {
       SocialCalc.Callbacks.broadcast('execute', {
           cmdstr: cmdstr, saveundo: saveundo
       });
   }
    /* …original ScheduleSheetCommands code here… */
}
```

现在我们需要做的就是定义一个合适的SocialCalc.Callbacks.broadcast回调函数。一旦它在适当的地方，相同的命令将在连接到同一个表单的所有的用户端执行。
当这个特征在2009年在OLPC(One Laptop Per Child(注释2))上由SEETA's Sugar Labs实现，broadcast函数建立在XPCOM 上，用D-Bus/Telepathy，一种OLPC/Sugar网络的标准传播（见图19.16）。     
![图19.16](/images/24.png)   
                                                                                                                                          
工作起来很合理，使得XO实例在同一个Sugar网络上可以在一个普通的SocialCalc表单上合作。但是，这对Mozilla/XPCOM浏览器平台和D-Bus/Telepathy信息平台都是特定的。
### 19.7.1 Cross-browser Transport ###
                             
为了实现跨浏览器和跨操作系统，我们使用Web::Hippie的框架，一个高等级的使用方便JQuery捆绑的JSON-over-WebSocket的抽象，当WebSocket不空闲时使用MXHR（Multipart XML HTTP Request(注释5)）作为稍后的传输机制。
对于有Adobe Flash插件但是没有原生WebSocket支持的浏览器，我们使用web_socket.js项目的WebSocket的Flash模拟器，这一班比MXHR更快更可靠。这个操作流显示在图19.17中。
![图19.17](/images/25.png)
                                                               
在客户端SocialCalc.Callbacks.broadcast函数如下定义：
```
var hpipe = new Hippie.Pipe();

SocialCalc.Callbacks.broadcast = function(type, data) {
    hpipe.send({ type: type, data: data });
};

$(hpipe).bind("message.execute", function (e, d) {
    var sheet = SocialCalc.CurrentSpreadsheetControlObject.context.sheetobj;
    sheet.ScheduleSheetCommands(
        d.data.cmdstr, d.data.saveundo, true // isRemote = true
    );
    break;
});
```
尽管这个工作起来很好，仍然有两个存留的问题要处理。

### 19.7.2. Conflict Resolution ###

第一个问题是命令执行顺序的竞争条件：如果用户A和用户B同时执行了影响相同单元格的操作，接受和执行其他用户传播的命令，他们最终将处于不同的状态，如图19.18.
![图19.18](/images/26.png)
                                                               
                                                               
我们可以使用SocialCalc内置的undo/redo机制来处理这个问题，如图19.19显示。
![图19.19](/images/27.png)                                                               
                                                               
                                                               
这个处理冲突的过程如下。当客户传播一个指令时，它向队列添加这个指令。当客户接收到一个指令时， 检查远程指令和队列。
如果队列为空，则执行远程指令。如果远程指令和队列里的一个指令相同，则去掉队列里的这个指令。
否则，客户检查是否有队列里的指令和接受到的指令之间的冲突。如果有冲突指令，客户先撤销这些命令，并标记它们用于之后的恢复。在撤销冲突指令后，远程指令照常执行。
当从服务器接受到标记恢复的指令时，客户再次执行它，并把它从队列里面删去。

### 19.7.3 Remote Cursors ###           

尽管竞争条件的问题解决了，重写正由其它用户编辑的单元格仍然未达到最佳标准。一个简单的提升是每个客户都向其他用户广播它的鼠标位置，这样每个人都能知道哪些单元格正在被使用。
为了实现这个想法，我们给MoveECellCallback事件添加了另一个broadcast句柄：
```
editor.MoveECellCallback.broadcast = function(e) {
    hpipe.send({
        type: 'ecell',
        data: e.ecell.coord
    });
};

$(hpipe).bind("message.ecell", function (e, d) {
    var cr = SocialCalc.coordToCr(d.data);
    var cell = SocialCalc.GetEditorCellElement(editor, cr.row, cr.col);
    // …decorate cell with styles specific to the remote user(s) on it…
});
```
为了标记表单中的单元格焦点，常见的使用有颜色的边框。但是，一个单元格可能已经定义了它自己的边框属性，边框是单色的，在一个单元格上只能代表一个光标。
因此，在支持CSS3的浏览器上，我们使用box-shadow特性来代表同一个单元格上的重复的同伴光标：
```
/* Two cursors on the same cell */
box-shadow: inset 0 0 0 4px red, inset 0 0 0 2px green;
```
图19.20显示了如果四个人在同一个表单上编辑时的显示：
![图19.20](/images/28.png)                       
                                                               
                                                               
## 19.8 Lesson Learned ##
                                                               
在2009年10月19号VisiCalc最初版本发行30周年之际，发行了SocialCalc 1.0。在DanBricklin的指导下与我同事合作开发Socialtext的经历是弥足珍贵的，我将分享我在那段时间学到的内容。

### 19.8.1. Chief Designer with a Clear Vision ###

在[[http://aosabook.org/en/bib1.html#bib:brooks:design|Bro10]] 中，Fred Brooks提出，当构建复杂系统时，专注于连贯的设计理念，而不是派生的表示，沟通会更加直接。根据Brooks所说，这样的连贯设计理念的规划最好由一个人专注：既然概念的完整是伟大设计中最重要的特性，并且完整的概念来自一人或少数人，明智的管理者会大胆委托有天赋的首席设计师。
在SocialCalc的范例中，有Tracy Ruggles作为我们的首席用户体验设计师是整个项目到达共享构想的关键。既然潜在的SocialCalc引擎具有延展性，功能变更的想法也很真实。Tracy沟通使用设计框架的能力使我们以用户觉得直接的方式展现了功能。

### 19.8.2. Wikis for Project Continuity ###

在我加入SocialCalc项目之前，已经有了超过两年的设计和发展，但是我能够跟上并在一个星期内开始给项目作出贡献，这是由于所有东西都在wiki里。从最早的设计笔记到最近的浏览器支持矩阵，整个过程都在wiki和SocialCalc电子表格中记录了。
阅读项目的工作空间让我很快地和其他人到达同一进度，并且不需要新项目成员传统的手把手的适应期。
这在传统的开源项目中不太可能，大多数沟通在IRC和邮件列表，wiki只是用于记录和资源链接。作为一个新人，从非结构的IRC记录和邮件文件夹中重建文本是更加艰难的。

### 19.8.3. Embrace Time Zone Differences ###

Ruby on Rails的创建人David Heinemeier Hansson曾经评论分布式团队的益处，当他刚开始加入37signals的时候，“Copenhagen和Chicage之间的七个时区说明我们在很少阻隔的情况下做出很多工作。”我们在SocialCalc的开发也是这样，Taipei和Palo Alto之间有九个时区。
我们经常在24小时内完成一个完整的“设计-开发-QA”反馈环，每个方面花费了一个人在其时区的8小时。这不同步的合作让我们生成自我解释的作品（设计框架、代码、测试），这大大提高了我们之间的信任。


### 19.8.4. Optimize for Fun ###

我在2006年CONISLI会议主旨中，总结了我领导一个团队完成Perl6语言的经历。在它们之中，有Roadmap,Forgiveness>Permission,Remove deadlocks,Seek ideas,not consensus,Sketch ideas with code，都在小型的分布式团队中特别相关。
当发挥SocialCalc时，我们注重在团队成员中普及知识，这样没有人会变成一个瓶颈。
此外，我们通过综合供选择的代码探索设计空间处理冲突，当一个更好的设计出现时我们不害怕更换原型。
这些文化特性帮助我们培养信任和情谊，尽管缺少面对面的交流，争执降到最小化，使得SocialCalc的工作有很多乐趣。

### 19.8.5. Drive Development with Story Tests ###

在加入Socialtext之前，我已经提倡过“interleave tests with the specification”处理方式，这个可以在Perl 6说明书里面看到，我们用官方测试标注了语言说明。Ken Pier和Matt Heusser，SocialCalc品质保证团队的两个人，让我开阔了眼界，知道了这个怎么推进到下一个层次，把测试推进到可执行说明的方式。
在GR09的章节16里，Matt解释了我们的故事-测试推动的发展过程，如下：
“工作的最基础的单元时“故事”，它是一个轻量要求文档。一个故事包括了一个特征的简要说明，并包含了完成故事需要考虑的例子，我们把这些例子叫做“接受测试”，并用简明英语描述。
在故事最初的剪辑中，产品主人坚信创造接受测试，这些在代码编辑之前将被开发者和测试者讨论。”
这些故事测试被翻译成wiki测试，一个基于表格的启发自Ward CunninghamFIT框架的说明语言，推动自动化的测试框架，比如Test::WWW::Mechanize和Test::WWW::Selenium。
故事测试作为普遍语言表达和衡量要求的好处，很难说明。它减少误解，也减少了我们每月发行的退化。

### 19.8.6. Open Source With CPAL ###

最后，我们给SocialCalc选择的开源模型，从中有意思的经验教训。
Socialtext给SocialCalc创造了Common Public Attribution License。基于Mozilla Public License，设计CPAL来允许原作者在软件使用者界面上显示属性，并且有一个网络使用条款，当网络上有衍生工作时共享条款。
在Open Source Initiative和Free Software Foundation的准许之后，我们看到出名的网站比如Facebook和Reddit在CPAL发行了他们平台的源代码，这是非常鼓舞人的举动。
因为CPAL是一个“软弱著作”条款，发行者可以自由地把它和其它免费软件结合，只需要发行对SocialCalc的更改。这个使得多种多样的社区能够采取SocialCalc，使它变得极好。
这个开源的电子表格引擎有许多有趣的可能性。如果你找到一个方式把SocialCalc植入你最喜欢的项目，我们特别高兴听到这个消息。

## Footnotes ##

1. https://github.com/audreyt/wikiwyg-js

2. http://one.laptop.org/

3. http://seeta.in/wiki/index.php?title=Collaboration_in_SocialCalc

4. http://search.cpan.org/dist/Web-Hippie/

5. http://about.digg.com/blog/duistream-and-mxhr

6. https://github.com/gimite/web-socket-js

7. http://perlcabal.org/syn/S02.html

8. http://fit.c2.com/

9. http://search.cpan.org/dist/Test-WWW-Mechanize/

10.http://search.cpan.org/dist/Test-WWW-Selenium/

11.https://www.socialtext.net/open/?cpal

12.http://opensource.org/

13.http://www.fsf.org

14.https://github.com/facebook/platform

15.https://github.com/reddit/reddit











                                                                                                                                                                                                                                                                                                       


                                                                                                                                                                                                                                                                                                       
