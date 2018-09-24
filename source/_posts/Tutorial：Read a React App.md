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
 - 

---

## 运行项目

方法一：
 1. 确保安装[Node.js][9]最新版本
 2. 命令行进入项目根目录执行以下指令：
```
npm install
npm start
```
方法二：（由于不可描述的原因，推荐使用本方法）
 1. 确保安装[Node.js][10]最新版本
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
package.json的详细说明可见[这里][11]。
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
本项目的React代码文件后缀为.ts，即我们使用的是TypeScript。由于TypeScript支持JavaScript语法，并且代码中并没有过多涉及TypeScript特有的语法（你可以直接复制粘贴代码到.js文件中运行），因此本教程不对TypeScript做过多解释。TypeScript的教程可以在[这里][12]查看。

---

## Render机制

 1. ReactDOM
 DOM（Document Object Model，文档对象模型）定义了访问HTML和XML文档的标准。HTML是用来描述网页的语言。DOM描述了HTML文档的访问顺序，一般组织为一个DOM树，描述了不同的HTML元素之间的关系，浏览器通过DOM树知道网页应当如何被渲染。
我们已经知道通过定义一个React元素可以在屏幕展示想要看到的东西，如：
```
const element = <h1>Hello, world</h1>;
```
但不同于浏览器的DOM元素，React元素只是一个对象。React元素包含页面展示内容的描述信息，ReactDOM的职能是依据React元素对DOM树进行更新，使得DOM树内容与React元素定义的内容一致。
为了举例说明ReactDOM如何将React元素映射到DOM树，我们定义一个HTML标签：
```
<div id="root"></div>
```
它是一个DOM元素，可以通过document.getElementById('root')来获取。
假设需要将element元素插入这个标签，ReactDOM需要进行如下操作：
```
ReactDOM.render(element, document.getElementById('root'));
```
以本项目根目录下src/index.tsx的代码片段为例：
```
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
__React中，创建元素并传入ReactDOM.reader()是唯一更新UI的方法__。
 2. Render
render()方法是一个组件类唯一必要的方法。render()方法会在渲染当前组件时被调用。当render()组件被调用时，它会检测this.props和this.state，并返回以下结果中的一种：

React元素：一般由JSX创建。例如`<div />`和`<MyApp />`，ReactDOM会将它们分别渲染为DOM节点和用户自定义组件。
数组和fragments：你可以用render()方法通过这种方式返回多个组件。fragments在本项目中并未涉及，详见它的[说明文档][13]。
Portals：你可以通过这种方式将当前组件渲染到其他DOM子树中，本项目中并未涉及，详见它的[说明文档][14]。
字符串和数字：它们会被渲染为DOM的文本节点。
布尔类型和null：它们不会被渲染。多数情况下它们是为了支持`return test && <Child />`，其中`test`是布尔类型。

render()方法必须是纯函数，它不改变组件的状态，它们每次被调用时都返回同样的结果，并且render()不与浏览器进行直接交互。
 3. React渲染过程
React有效提高了网页性能，它通过自身的render机制实现了这一点。React渲染页面的过程大致可以描述为：在页面打开时，调用render函数构建一颗DOM树，在state/props发生改变时，render函数会被再次调用渲染出另外一棵树。接着，React会用两棵树进行对比，找到需要更新的地方批量改动。
实际的比较过程和算法有一定复杂性，如果你对这一过程感兴趣，我们推荐阅读[这篇文章][15]。

---

## 路由
当浏览网页时，每个页面会有一个URL，当URL变化时，网页内容也会切换。当我们创建一个较为复杂的应用，它通常都会包含诸多页面。假设当前有一个具有两个页面的应用App，两个页面分别是About和Inbox。如果我们要指定两个URL`/about`，`/inbox`，使得点击后分别跳转到About和inbox页面，React通常这样写：
```
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
```
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
```
<Switch>
  <Route exact path="/login" component={LoginPage}></Route>
  <AuthorizedRoute path="/" component={HomePage}></AuthorizedRoute>
</Switch>
```
其中`<Switch />`是一个React Router库的组件，它类似于C++或是Java中的Switch语块。它在对路由进行匹配时，会顺次匹配自己的子元素`<Route />`，并对第一次匹配到的`<Route />`中的component进行渲染。
而`<AuthorizedRoute />`则是一个自定义组件，它继承了`<Route />`。
React Router的各类工具有很多，篇幅所限不一一列举。
关于React Router的API说明可见[这里][16]。

---

## 模块化
模块化主要是解决代码分割、作用域隔离、模块之间的依赖管理以及发布到生产环境时的自动化打包与处理等多个方面的问题。通俗地讲就是将代码划分为多个独立的片段，一个模块只有通过特定的模块化方案才能调用另一个模块的内容。随着代码库增长，不使用模块化方案将很容易导致命名冲突等问题。

熟悉Java和C++或其他支持模块化语言的用户应当对本项目中的import和export有基本的理解。本项目使用的模块化方案为ES6（ECMAScript2015）方案，它主要的import和export语法示例如下：
```
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
```
//exports
module.exports = foo;

//imports
const a = require("../b.js");
```
想要对JavaScript模块化的发展和各种方案有所了解的读者可以阅读[这篇专栏][17]。

---

## Redux简介


---

## webpack的使用
webpack是一个前端构建工具，本项目使用webpack进行构建。webpack需要一个配置文件`webpack.config.js`。通过在这个文件中对构建和打包方式进行配置，并在`package.json`的`script`字段进行命令配置，就可以实现通过webpack进行项目构建。
webpack详细教程可见[这篇教程][18]。
本项目根目录下的webpack目录内容如下：
```
-webpack
    -webpack.config.js//webpack配置文件
    -webpack.dev.js//NODE_ENV开发环境配置文件
    -webpack.prod.js//NODE_ENV生产环境配置文件
```
其中，webpack.dev.js和webpack.prod.js也是webpack配置的一部分。NODE_ENV是Node的系统环境变量，它们在package.json中被这样调用：
```
    "start": "NODE_ENV=development webpack-dev-server --config ./webpack/webpack.dev.js --progress --colors --content-base ./dist --host 127.0.0.1 --port 4000",
    "start-dev": "npm run start",
    "start-prod": "NODE_ENV=production webpack-dev-server --config ./webpack/webpack.prod.js --progress --colors --content-base ./dist --host 127.0.0.1 --port 4000",
    "build-dev": "webpack --progress --config=webpack.dev.js",
    "build-prod": "webpack --progress --config=webpack.prod.js",
```
即对于开发和生产环境进行不同的配置。

---

## 什么是AntDesign



  [1]: https://github.com/Benjamin15122/dc-ui
  [2]: http://javascript.ruanyifeng.com/nodejs/packagejson.html#toc2
  [3]: https://reactjs.org/docs/getting-started.html
  [4]: https://segmentfault.com/a/1190000010522782
  [5]: https://react-guide.github.io/react-router-cn/docs/Introduction.html
  [6]: https://reacttraining.com/react-router/core/api/MemoryRouter
  [7]: https://zhuanlan.zhihu.com/p/26231889
  [8]: https://github.com/ruanyf/webpack-demos#demo01-entry-file-source
  [9]: https://nodejs.org/en/
  [10]: https://nodejs.org/en/
  [11]: http://javascript.ruanyifeng.com/nodejs/packagejson.html#toc2
  [12]: https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html
  [13]: https://reactjs.org/docs/fragments.html
  [14]: https://reactjs.org/docs/portals.html
  [15]: https://segmentfault.com/a/1190000010522782
  [16]: https://reacttraining.com/react-router/core/api/MemoryRouter
  [17]: https://zhuanlan.zhihu.com/p/26231889
  [18]: https://github.com/ruanyf/webpack-demos#demo01-entry-file-source