---
title: 'Tutorial: Read a React App'
date: 2018-09-24 23:20:47
tags:
---


# Tutorial：Read a React App

本教程的内容是讲解一个简单的React应用代码。通过对工程的分析来讲解构建一个简单的React应用所需要的各种技术。

---

## 前言
我们在本教程中会假设你已经掌握了以下预备知识：

- HTML
- JavaScript
- DOM

[点击这里查看项目源码][1]
本教程的参考资料和引用来源：

- [阮一峰：JavaScript标准参考教程][2]
- [React官方文档][3]
- [React渲染机制解析][4]
- [React Router中文文档][5]
- [reacttraining.com/react-router/core/api][6]
- [知乎专栏：JavaScript模块演化简史][7]
- [阮一峰的webpack-demos][8]
- [how does redux work][9]

---

## 运行项目

方法一：
1. 确保安装[Node.js][10]最新版本
2. 命令行进入项目根目录执行以下指令：
```
npm install
npm start
```
方法二：（由于不可描述的原因，推荐使用本方法）
1. 确保安装[Node.js][11]最新版本
2. 命令行进入项目根目录执行以下指令：
```
npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm install
```
__从以上指令聊聊包管理__

1. 什么是__Node.js__?
简而言之，__Node.js是一个JavaScript的运行环境__，Node.js是一个后端的Javascript运行环境（支持的系统包括Linux、Windows），这意味着你可以编写系统级或者服务器端的Javascript代码，交给Node.js来解释执行。例如：
```
node helloworld.js
```
Node.js采用了Google Chrome浏览器的v8引擎，并提供了诸如文件操作，网络编程等API。它与浏览器端JavaScript代码运行的不同就在于浏览器端的Javascript代码在运行时会受到各种安全性的限制，对客户系统的操作有限。而Node.js则是全面的后台运行时，为Javascript提供了其他语言能够实现的许多功能。
2. 什么是__NPM__?
NPM（node package manager),通常称为node包管理器，主要功能就是管理node包，包括：安装、卸载、更新、查看、搜索、发布等。React项目在开发，运行时会对一些node包有依赖关系，我们需要通过npm install指令安装它们，例如通过在根目录下执行
```
npm install grunt-cli
```
我们实现了在本地安装该React项目依赖的包之一：grunt-cli。执行install时，项目根目录下会创建node_modules目录，该项目依赖的包将会被安装到这个文件夹下。
为了避免逐个对所依赖的包进行install，同时确保项目依赖的包都能被正确安装，node支持通过package.json对依赖进行描述，如本项目目录下的package.json中有如下代码段：
```
"name": "my-app",
"version": "0.1.0",
"private": true,
"dependencies": {
"antd": "^3.9.2",
"axios": "^0.18.0",
"connected-react-router": "^4.4.1",
"react": "^16.5.0",
"react-dom": "^16.5.0",
"react-redux": "^5.0.7",
"react-router": "^4.3.1",
"redux": "^4.0.0",
"redux-logger": "^3.0.6",
"redux-saga": "^0.16.0"
}
```
它描述了当前React项目的项目名称，项目版本号，私有属性和依赖包列表。package.json的主要属性说明如下：
```
name - 项目名称

version - 项目版本号

script - npm install过程中执行的指令

author - 项目作者姓名

contributors - 项目其他贡献者姓名

dependencies - 项目运行所依赖的模块，本地未安装的模块会被安装到根目录下的node_modules目录

devDependencies - 项目开发所依赖的模块，本地未安装的模块会被安装到根目录下的node_modules目录
```
package.json的详细说明可见[这里][12]。
当我们执行npm install时，npm会依据项目根目录下的package.json的描述，进行依赖包的安装。
3. 什么是__cnpm__？
cnpm是方便国内使用的npm替代工具，它通过使用淘宝镜像确保依赖安装速度，并通过定时与npm同步更新的方式尽可能与npm保持一致。以下指令安装了cnpm并使用淘宝镜像：
```
npm install -g cnpm --registry=https://registry.npm.taobao.org
```
使用时只需把npm指令对应的npm替换为cnpm即可。以下指令即使用cnpm进行依赖安装：
```
cnpm install
```

---

## 关于TypeScript
本项目的React代码文件后缀为.ts，即我们使用的是TypeScript。由于TypeScript支持JavaScript语法，并且代码中并没有过多涉及TypeScript特有的语法（你可以直接复制粘贴代码到.js文件中运行），因此本教程不对TypeScript做过多解释。TypeScript的教程可以在[这里][13]查看。

---

## Render机制

1. ReactDOM
DOM（Document Object Model，文档对象模型）定义了访问HTML和XML文档的标准。HTML是用来描述网页的语言。DOM描述了HTML文档的访问顺序，一般组织为一个DOM树，描述了不同的HTML元素之间的关系，浏览器通过DOM树知道网页应当如何被渲染。
我们已经知道通过定义一个React元素可以在屏幕展示想要看到的东西，如：
```js
const element = <h1>Hello, world</h1>;
```
但不同于浏览器的DOM元素，React元素只是一个对象。React元素包含页面展示内容的描述信息，ReactDOM的职能是依据React元素对DOM树进行更新，使得DOM树内容与React元素定义的内容一致。
为了举例说明ReactDOM如何将React元素映射到DOM树，我们定义一个HTML标签：
```js
<div id="root"></div>
```
它是一个DOM元素，可以通过document.getElementById('root')来获取。
假设需要将element元素插入这个标签，ReactDOM需要进行如下操作：
```js
ReactDOM.render(element, document.getElementById('root'));
```
以本项目根目录下src/index.tsx的代码片段为例：
```js
ReactDOM.render(
    <Provider store={configureStore()}>
        <ConnectedRouter history={history}>
            <Application/>
        </ConnectedRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement
);
```
它创建了一个`<Provider />`元素，并将其插入了在public/index.html中创建的root节点，从而在渲染root节点时，会渲染`<Provider />`及其子节点。
__React中，创建元素并传入ReactDOM.render()是唯一更新UI的方法__。
2. Render
render()方法是一个组件类唯一必要的方法。render()方法会在渲染当前组件时被调用。当render()组件被调用时，它会检测this.props和this.state，并返回以下结果中的一种：

React元素：一般由JSX创建。例如`<div />`和`<MyApp />`，ReactDOM会将它们分别渲染为DOM节点和用户自定义组件。
数组和fragments：你可以用render()方法通过这种方式返回多个组件。fragments在本项目中并未涉及，详见它的[说明文档][14]。
Portals：你可以通过这种方式将当前组件渲染到其他DOM子树中，本项目中并未涉及，详见它的[说明文档][15]。
字符串和数字：它们会被渲染为DOM的文本节点。
布尔类型和null：它们不会被渲染。多数情况下它们是为了支持`return test && <Child />`，其中`test`是布尔类型。

render()方法必须是纯函数，它不改变组件的状态，它们每次被调用时都返回同样的结果，并且render()不与浏览器进行直接交互。
3. React渲染过程
React有效提高了网页性能，它通过自身的render机制实现了这一点。React渲染页面的过程大致可以描述为：在页面打开时，调用render函数构建一颗DOM树，在state/props发生改变时，render函数会被再次调用渲染出另外一棵树。接着，React会用两棵树进行对比，找到需要更新的地方批量改动。
实际的比较过程和算法有一定复杂性，如果你对这一过程感兴趣，我们推荐阅读[这篇文章][16]。

---

## 路由
当浏览网页时，每个页面会有一个URL，当URL变化时，网页内容也会切换。当我们创建一个较为复杂的应用，它通常都会包含诸多页面。假设当前有一个具有两个页面的应用App，两个页面分别是About和Inbox。如果我们要指定两个URL`/about`，`/inbox`，使得点击后分别跳转到About和inbox页面，React通常这样写：
```js
import React from 'react'
import { render } from 'react-dom'

const About = React.createClass({/*...*/})
const Inbox = React.createClass({/*...*/})
const Home = React.createClass({/*...*/})

const App = React.createClass({
  getInitialState() {
    return {
      route: window.location.hash.substr(1)
    }
  },

  componentDidMount() {
    window.addEventListener('hashchange', () => {
      this.setState({
        route: window.location.hash.substr(1)
      })
    })
  },

  render() {
    let Child
    switch (this.state.route) {
      case '/about': Child = About; break;
      case '/inbox': Child = Inbox; break;
      default:      Child = Home;
    }

    return (
      <div>
        <h1>App</h1>
        <ul>
          <li><a href="#/about">About</a></li>
          <li><a href="#/inbox">Inbox</a></li>
        </ul>
        <Child/>
      </div>
    )
  }
})

React.render(<App />, document.body)
```
这样的做法在页面数量较少，组件较为简单时是可行的。但当页面数量增加，组件之间的组合关系变复杂时，我们就需要编写大量的代码来指定URL渲染对应的组件。例如，假设Inbox页面上包含了众多指向其他页面的链接，效果如下：
```
path: /inbox/messages/1234

+---------+------------+------------------------+
| About   |    Inbox   |                        |
+---------+            +------------------------+
| Compose    Reply    Reply All    Archive      |
+-----------------------------------------------+
|Movie tomorrow|                                |
+--------------+   Subject: TPS Report          |
|TPS Report        From:    boss@big.co         |
+--------------+                                |
|New Pull Reque|   So ...                       |
+--------------+                                |
|...           |                                |
+--------------+--------------------------------+
```
那么，在switch语句中Inbox的部分将会变得极为庞大，同时state中route的更新也会变得更加复杂。为了更智能地管理URL和对应的页面，我们需要一个路由库。
React Router是React唯一可用的路由库，它通过管理URL来实现组件的切换和状态的变化。对于之前的举例，使用React Router重构后，代码如下：
```js
import React from 'react'
import { render } from 'react-dom'

// 首先我们需要导入一些组件...
import { Router, Route, Link } from 'react-router'

// 然后我们从应用中删除一堆代码和
// 增加一些 <Link> 元素...
const App = React.createClass({
  render() {
    return (
      <div>
        <h1>App</h1>
        {/* 把 <a> 变成 <Link> */}
        <ul>
          <li><Link to="/about">About</Link></li>
          <li><Link to="/inbox">Inbox</Link></li>
        </ul>

        {/*
          接着用 `this.props.children` 替换 `<Child>`
          router 会帮我们找到这个 children
        */}
        {this.props.children}
      </div>
    )
  }
})

// 最后，我们用一些 <Route> 来渲染 <Router>。
// 这些就是路由提供的我们想要的东西。
React.render((
  <Router>
    <Route path="/" component={App}>
      <Route path="about" component={About} />
      <Route path="inbox" component={Inbox} />
    </Route>
  </Router>
), document.body)
```
显而易见，首先React Router避免了通过window.location.hash的接口来获取URL，避免了多层嵌套带来的处理难题，其次JSX格式的描述具有良好的扩展性，同时能直观展示组件之间的嵌套关系。
`<Route />`提供了一个path作为匹配模式，并提供了一个component作为满足匹配模式时需要渲染的网页。
`<Router />`是一个基础的路由器接口，它用于管理路由的切换和选择，所有上层的路由器都会继承它。
React Router有丰富的组件和工具，并支持自定义路由组件，如本项目中的路由(app.tsx)如下：
```js
<Switch>
    <Route exact path="/login" component={LoginPage}></Route>
    <AuthorizedRoute path="/" component={HomePage}></AuthorizedRoute>
</Switch>
```
其中`<Switch />`是一个React Router库的组件，它类似于C++或是Java中的Switch语块。它在对路由进行匹配时，会顺次匹配自己的子元素`<Route />`，并对第一次匹配到的`<Route />`中的component进行渲染。
而`<AuthorizedRoute />`则是一个自定义组件，它继承了`<Route />`。
React Router的各类工具有很多，篇幅所限不一一列举。
关于React Router的API说明可见[这里][17]。

---

## 模块化
模块化主要是解决代码分割、作用域隔离、模块之间的依赖管理以及发布到生产环境时的自动化打包与处理等多个方面的问题。通俗地讲就是将代码划分为多个独立的片段，一个模块只有通过特定的模块化方案才能调用另一个模块的内容。随着代码库增长，不使用模块化方案将很容易导致命名冲突等问题。

熟悉Java和C++或其他支持模块化语言的用户应当对本项目中的import和export有基本的理解。本项目使用的模块化方案为ES6（ECMAScript2015）方案，它主要的import和export语法示例如下：
```js
//export 语法
export default 42;
export default {};
export default [];
export default foo;
export default function () {}
export default class {}
export default function foo () {}
export default class foo {}


//import 语法
// default imports
import foo from "foo";
import {default as foo} from "foo";

// named imports
import {bar} from "foo";
import {bar, baz} from "foo";
import {bar as baz} from "foo";
import {bar as baz, xyz} from "foo";

// glob imports
import * as foo from "foo";

// mixing imports
import foo, {baz as xyz} from "foo";
import * as bar, {baz as xyz} from "foo";
import foo, * as bar, {baz as xyz} from "foo";
```
同时也含有被广泛支持的CommonJS方案，语法如：
```js
//exports
module.exports = foo;

//imports
const a = require("../b.js");
```
想要对JavaScript模块化的发展和各种方案有所了解的读者可以阅读[这篇专栏][18]。

---

## Redux简介
Redux作为一个前端架构，它需要与React搭配应用。那么首先需要明确一个问题：为什么要用Redux？这个问题具体化一点就是：React有哪些不足需要Redux来解决？


当我们使用React构建应用时，如前文所叙述，组件之间实际被组织为一颗DOM树，组件之间的数据可以通过props参数来传递。而这意味着数据的流动是单向的由父组件传递给子组件。如果需要子组件向父组件传递数据，那么父组件需要涉及一个回调函数并借助props传递给需要向自己传递数据的子组件。



以下例子是一个Counter（本案例来自[这篇教程][19]，有兴趣的读者可以自行阅读），每当点击加号数字就加一，点击减号数字就减一：

{% qnimg webtech/redux-example-counter.png %}

`count`是存储在`App`的state中的，它会作为一个prop被传递下去

{% qnimg webtech/redux-example-easyprops.png %}

为了把数据从子组件传回父组件，需要从App向下传递一个回调函数。

{% qnimg webtech/redux-example-callback.png %}

这种做法在简单的应用中没有问题，但对类似于下图的场景，用于数据传递的代码会变得十分复杂：

{% qnimg webtech/redux-example-tweeter.png %}

图中有三处用到了用户的数据，而它们都被嵌套在多层组件之中。假设用户数据名为`user`，顶层组件名为`App`，那么`App`需要进行如下的props传递：

{% qnimg webtech/redux-example-noodles.png %}

可见，即便用不到`user`数据的组件，如果子组件需要`user`属性，则同样需要继承props，就像针线一样一节一节把树的节点串联起来。这样的做法十分繁琐，不仅无端增加了代码量，而且使代码变得难以理解。而Redux就是为了解决这种情况产生的。Redux把所有的数据都组织在store中，所有的组件通过connect方法来访问store中的数据，依次解决数据沿着DOM树传递时可能产生的窘境。同样是上面的例子，使用Redux后，数据流动如下：

{% qnimg webtech/redux-example-reduxflow.png %}

Redux将应用的state管理在一个单一的store中。在某个组件需要使用时，你可以将state中被用到的部分抽取出来，并连接到该组件，作为该组件的props。它是你可与你把数据存入一个全局位置，并可以把其中的数据传入任何一个应用内部的组件。

__注意__：`state`和`store`通常可以互相替代使用，但实际上，`state`是数据，而`store`是数据存储的地方。

下面我们会展示如何将之前的Counter例子，转换为使用Redux数据的应用。

首先我们创建一个不使用Redux的Counter应用

 - 如果你没有安装过creat-react-app,你需要先安装一次：
 ```
 npm install -g create-react-app
 ```
 
 - 创建一个React项目
```
create-react-app redux-intro
```

 - 打开`src/index.js`，写入如下内容
```js
import React from 'react';
import { render } from 'react-dom';
import Counter from './Counter';

const App = () => (
  <div>
    <Counter />
  </div>
);

render(<App />, document.getElementById('root'));
```
 - 创建一个`src/Counter.js`，写入以下内容
```js
import React from 'react';

class Counter extends React.Component {
  state = { count: 0 }

  increment = () => {
    this.setState({
      count: this.state.count + 1
    });
  }

  decrement = () => {
    this.setState({
      count: this.state.count - 1
    });
  }

  render() {
    return (
      <div>
        <h2>Counter</h2>
        <div>
          <button onClick={this.decrement}>-</button>
          <span>{this.state.count}</span>
          <button onClick={this.increment}>+</button>
        </div>
      </div>
    )
  }
}

export default Counter;
```
`Counter.js`的代码是这样工作的：

 - `count`变量被存储在最顶层的Counter组件中
 - 当用户点击"+"，加号按钮的`onClick`就会被调用，这是一个回调函数，`Counter`组件的`increment`函数就会被调用
 - `increment`函数会把state中的count更新为加一后的值
 - 由于state发生了变化，React重新渲染了Counter（和它的子组件），于是新的count值就被渲染出来

现在，我们将它变为使用Redux框架的React应用：

首先在项目根目录下安装Redux：
```
yarn add redux react-redux
```
注意，这里我们添加了两个依赖：redux和react-redux。react-redux是什么呢？顾名思义它是react和redux连接的桥梁。这么说是因为redux的功能实在是很简单，它将state存储在store里，然后从store里把state传出去，然后state有所变化时再更新一下store，仅此而已。也就是说，__redux与React代码基本无关__。因为实际上是react-redux负责了把state数据传入React组件。


安装完依赖，我们清理一下Counter.js中的代码，将它的state和`increment()`和`decrement()`都清理掉，后续会用Redux相关的代码替代。
```js
import React from 'react';

class Counter extends React.Component {
  increment = () => {
    // fill in later
  }

  decrement = () => {
    // fill in later
  }

  render() {
    return (
      <div>
        <h2>Counter</h2>
        <div>
          <button onClick={this.decrement}>-</button>
          <span>{this.props.count}</span>
          <button onClick={this.increment}>+</button>
        </div>
      </div>
    )
  }
}

export default Counter;
```
注意，这里对比之前的代码还有一个变化：对于`<button />`组件的`{this.state.count`，替换为`{this.props.count}`。这是因为Redux中的数据会以props的形式传入组件。此时Counter组件的props中并没有count，因此代码并不能正确运行，下面我们使用Redux将count参数传入props。


为了把Redux中的数据连接到React组件，我们需要用到react-redux库的`connect`模块，在`src/Counter.js`的开头添加：
```js
import { connect } from ‘react-redux`
```
接着我们需要添加具体负责连接的代码，在底部将
```js
    export default Counter;
```
替换为：

```js
// Add this function:
function mapStateToProps(state) {
  return {
    count: state.count
  };
}

// Then replace this:
// export default Counter;

// With this:
export default connect(mapStateToProps)(Counter);
```
以上代码中，我们把原本用于export的`Counter`，包裹了一层`connect`。


什么是`connect`？`connect`负责将Redux中的数据`state`拉出，并依据`mapStateToProps`把数据传入所连接组件的`props`。也就是建立一个从`state`到`props`的映射。


这里`connect(mapStateToProps)(Counter)`是一个高阶函数的写法：`connect()`函数接收`mapStateToProps`参数，并返回一个“低阶”函数。“低阶”函数参数为一个React组件`Counter`，返回值是一个拥有props的新组件。


`mapStateToProps`顾名思义，这个函数的工作是把`state`集合中的数据筛选一部分出来，构成一个props集合。它的参数是`state`，它通过返回一个对象来告诉`connect`函数：这就是需要向组件添加的props。而`connect`函数会先向`mapStateToProps`传入`state`，再调用`mapStateToProps`获取返回值，再构造一个新的函数并返回。这个函数负责将之前`mapStateToProps`返回值里的内容添加到Counter组件的props中，并返回填充后的组件。


简而言之，`state`是应用全部数据的集合，`props`是实际组件需要用到的数据集合。`mapStateToProps`是集合的映射方式，`Counter`是接收`props`集合的组件。`connect`是实际进行映射工作的函数，它依据映射方式确定方案，再对组件进行加工。


这样，我们就实现了从`state`到`props`的映射。那么目前我们已经具备了React组件，和`connect`方法，但这时React组件还不能正常使用`connect`，因为`state`来自`store`，但`connect`本身并不能创建一个`store`，它只负责从`store`中取出`state`并映射到组件，所以此时运行工程会出现如下报错：

>Could not find “store” in either the context or props of “Connect(Counter)”. Either wrap the root component in a , or explicitly pass "store" as a prop to "Connect(Counter)".

于是我们还需要一个组件向`connect`方法提供`state`。


Redux掌握着整个应用的`state`，为了使得整个应用都能使用Redux中的数据，我们需要使用来自`react-redux`库中的`Provider`组件来包裹`App`组件，这样整个应用中所有的组件都能通过`connect`方法连接到`Provider`提供的`store`并获取所需要的数据。


在`src/index.js`中导入`Provider`并放在`<App />`的外层：
```js
import { Provider } from 'react-redux';

...

const App = () => (
  <Provider>
    <Counter/>
  </Provider>
);
```
此时运行工程，依然会出现上面的报错：
>Could not find “store” in either the context or props of “Connect(Counter)”. Either wrap the root component in a , or explicitly pass "store" as a prop to "Connect(Counter)".

这是因为`<Provider />`本身也无法提供一个`store`。`<Provider />`的工作是，接受一个`store`参数，并为`connect`方法提供这个`store`。那么我们现在还缺少一个`store`。

`store`需要通过`redux`库中的`createStore`方法创建。
于是`src/index.js`需要改成如下形式：
```js
import { createStore } from 'redux';

const store = createStore();

const App = () => (
  <Provider store={store}>
    <Counter/>
  </Provider>
);
```
我们这时会收到一条新的报错：
>Expected the reducer to be a function.

从报错来看，我们需要提供一个reducer函数。事实上，createStore需要一个reducer函数作为参数来创建store。而Redux本身并不复杂，它不会因为createStore需要一个函数参数，而我们没有提供，就主动创建一个空函数作为默认值，而是粗暴地把参数赋值为：0。


那么现在我们需要知道，什么是`reducer`，以及，如何调用。


再次顾名思义，`reducer`本义指的是水管的转换器，它可以将不同直径的水管连接在一起。在这里，它作为`store`的参数，实际作用是`state`的转换器。`reducer`接收一个当前的`state`和一个告知如何对`state`对象进行操作的`action`作为参数，将当前的`state`转换为新的`state`，再把这个新的`state`作为返回值返回。也就是说，一个普通的`reducer`应该是这样：
```js
const initialState = {
  count: 0
};//为state参数设置初始值

function reducer(state = initialState, action) {
  //通过action对state进行更新
  return state;
}
```

于是我们的`src/index.js`应该写成这样：
```js
import { createStore } from 'redux';

const initialState = {
  count: 0
};//为state参数设置初始值

function reducer(state = initialState, action) {
  //通过action对state进行更新
  return state;
}

const store = createStore(reducer);

const App = () => (
  <Provider store={store}>
    <Counter/>
  </Provider>
);
```

将上述代码添加并运行后，你会发现运行是正常的，但是无论怎么操作，Couter的数字都是0。它的原因当然不是来自于语法错误，而是我们当前没有完成的部分：`increment()`和`decrement()`函数，以及`reducer()`函数和`action`参数。


当我们点击组件上的加号和减号按钮，它们会触发`increment()`或是`decrement()`函数，而这两个函数当前为空，因此渲染时`count`永远维持0。


下面就是最后一步：更新`state`中的`count`值。


首先需要明确一点：__React组件内无法修改`state`__。你不可以在`increment()`中写如下代码：
```js
    state.count++//这修改了state
    state.count=42//这也修改了state
```
如果所有的组件都能随意获取`state`并进行修改，Redux的加入就不是对数据流动进行了简化，而是使数据流动失去了管制。起初或许一切正常，但随着不同组件与数据源的频繁互动会使数据源变成一团乱：数据变化无法预测，并且你无法知道哪一个组件改变了数据。这里我引用本案例原教程的一句原文：
>Redux is built on the idea of immutability, because mutating global state is the road to ruin.
>Redux是基于不变性构造的，因为全局变量的滥用是一条毁灭之路。


这也正是接下来需要明确的：__`state`的更新只能在`reducer()`中进行__。这一点很便于理解：与`state`更新相关的是`action`和`reducer`。`action`作为用户定义的参数，并不具有更新`state`的能力，这意味着`action`是能力有限的。


`action`是一个JavaScript对象，顾名思义，它是对行为的描述，它告诉`reducer()`当前用户在做的是什么事，描述用户行为的是一个字段`type`（这也是action的必需字段），类型是字符串。例如，对应`increment()`的`action`可以这样写：
```js
{
    type: "INCREMENT"
}
```
接着，`reducer()`就可以对`action`进行处理，当收到"INCREMENT"时，就更新`state`，使count值更新为+1后的值。例如：
```js
function reducer(state = initialState, action) {
  if(action.type === "INCREMENT") {
    return {
      count: state.count + 1
    };
  }

  return state;
}
```
当然，考虑到`action`通常有多种取值，使用switch语块会更好一些：
```js
function reducer(state = initialState, action) {
  switch(action.type) {
    case 'INCREMENT':
      return {
        count: state.count + 1
      };
    case 'DECREMENT':
      return {
        count: state.count - 1
      };
    default:
      return state;
  }
}
```

接下来是第三点：__`state`是无法被修改的__。事实上Redux对`state`进行的更新，并不是更改其中的内容，而是通过Reducer的返回值对`state`进行替换。Reducer的返回值是一个对象，这个对象本身构成了新的`state`，而不是这个`state`的字段被修改了。这意味着你不能写这样的代码：
```js
function brokenReducer(state = initialState, action) {
  switch(action.type) {
    case 'INCREMENT':
      // NO! BAD: this is changing state!
      state.count++;
      return state;

    case 'DECREMENT':
      // NO! BAD: this is changing state too!
      state.count--;
      return state;

    default:
      // this is fine.
      return state;
  }
}
```
现在我们解决了Reducer，那么只剩一步，向Reducer发送`action`。这一步需要依赖的方法是`dispatch`,`dispatch()`方法是一个实例函数，它是`store`的一个方法，这意味着你不能通过`import {dispatch}`的方法导入一个模块，而是通过store.dispatch({type:"INCREMENT")的形式向Reducer传参。但store只能在一个文件`src/index.js`中被调用，而需要发送`action`的函数总是在其他文件。Redux的解决方案是：通过`connect`将`mapStateToProps`的返回值，和`dispatch()`方法一起传入组件的props，也就是说，在`src/Counter.js`中，我们这样处理`increment()`和`decrement()`：
```js
import React from 'react';
import { connect } from 'react-redux';

class Counter extends React.Component {
  increment = () => {
    this.props.dispatch({ type: 'INCREMENT' });
  }

  decrement = () => {
    this.props.dispatch({ type: 'DECREMENT' });
  }

  render() {
    return (
      <div>
        <h2>Counter</h2>
        <div>
          <button onClick={this.decrement}>-</button>
          <span>{this.props.count}</span>
          <button onClick={this.increment}>+</button>
        </div>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    count: state.count
  };
}

export default connect(mapStateToProps)(Counter);
```
至此，这个用例的改造就完成了。这也包含了Redux基本的应用，更多关于Redux的信息可以阅读[这里][20]。
 
---

## webpack的使用
webpack是一个前端构建工具，本项目使用webpack进行构建。webpack需要一个配置文件`webpack.config.js`。通过在这个文件中对构建和打包方式进行配置，并在`package.json`的`script`字段进行命令配置，就可以实现通过webpack进行项目构建。
webpack详细教程可见[这篇教程][21]。
本项目根目录下的webpack目录内容如下：
```js
-webpack
    -webpack.config.js//webpack配置文件
    -webpack.dev.js//NODE_ENV开发环境配置文件
    -webpack.prod.js//NODE_ENV生产环境配置文件
```
其中，webpack.dev.js和webpack.prod.js也是webpack配置的一部分。NODE_ENV是Node的系统环境变量，它们在package.json中被这样调用：
```json
"start": "NODE_ENV=development webpack-dev-server --config ./webpack/webpack.dev.js --progress --colors --content-base ./dist --host 127.0.0.1 --port 4000",
"start-dev": "npm run start",
"start-prod": "NODE_ENV=production webpack-dev-server --config ./webpack/webpack.prod.js --progress --colors --content-base ./dist --host 127.0.0.1 --port 4000",
"build-dev": "webpack --progress --config=webpack.dev.js",
"build-prod": "webpack --progress --config=webpack.prod.js",
```
即对于开发和生产环境进行不同的配置。

---

## 什么是AntDesign
Ant Design是一个UI 设计语言，是一套提炼和应用于企业级后台产品的交互语言和视觉体系。它提供了丰富的，可定制的组件。普通的网页都会包含JS，HTML，CSS三个元素，其中CSS是网页元素的风格配置文件，它定义了线条的粗细，表格的位置等，是美观问题的关键，并且难以与所有浏览器适配。使用Ant Design可以免除在UI组件的美观，适配等底层问题，而关注React等上层代码，从而大大提高开发效率。


由于Ant Design提供了大量的Demo，并且有详实易读的官方的中文说明文档与教程，有需要的读者可以自行访问[这里][22]


  [1]: https://github.com/Benjamin15122/react-redux-example
  [2]: http://javascript.ruanyifeng.com/nodejs/packagejson.html#toc2
  [3]: https://reactjs.org/docs/getting-started.html
  [4]: https://segmentfault.com/a/1190000010522782
  [5]: https://react-guide.github.io/react-router-cn/docs/Introduction.html
  [6]: https://reacttraining.com/react-router/core/api/MemoryRouter
  [7]: https://zhuanlan.zhihu.com/p/26231889
  [8]: https://github.com/ruanyf/webpack-demos#demo01-entry-file-source
  [9]: https://daveceddia.com/how-does-redux-work/
  [10]: https://nodejs.org/en/
  [11]: https://nodejs.org/en/
  [12]: http://javascript.ruanyifeng.com/nodejs/packagejson.html#toc2
  [13]: https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html
  [14]: https://reactjs.org/docs/fragments.html
  [15]: https://reactjs.org/docs/portals.html
  [16]: https://segmentfault.com/a/1190000010522782
  [17]: https://reacttraining.com/react-router/core/api/MemoryRouter
  [18]: https://zhuanlan.zhihu.com/p/26231889
  [19]: https://daveceddia.com/how-does-redux-work/
  [20]: https://daveceddia.com/refactoring-to-redux/
  [21]: https://github.com/ruanyf/webpack-demos#demo01-entry-file-source
  [22]: https://ant.design/docs/react/introduce-cn
