---
title: 'React简易教程'
date: 2018-09-19 15:51:50
description: 本教程的内容是实现一个小游戏。实现这个小游戏过程中需要学习的技术是实现任何React应用的基础，通过实现这个小游戏，你会对React有更好的理解。

---


本教程的内容是实现一个小游戏。实现这个小游戏过程中需要学习的技术是实现任何React应用的基础，通过实现这个小游戏，你会对React有更好的理解。

---

## 前言

本教程分为以下几个部分：

- 搭建环境：配置实现小游戏的环境
- React简介：讲解React的核心元素：conmponents，props，state
- 游戏编写：讲解React开发中最常见的一些技术

在你阅读教程时，你可以复制粘贴教程中的代码来一步步实现游戏。但我们更推荐你把代码手工敲一遍，这样更有助于加强肌肉记忆和对React开发的理解。

### 游戏简介

本教程将会使用React开发一个有交互的井字棋游戏。


你可以从[这里][1]看到游戏的最终实现。如果这个代码你完全看不懂，或是不明白代码中的语法，那么本教程可以帮助你理解React和它的语法。


我们希望你在继续阅读本教程之前先仔细观察游戏的最终实现，你会发现棋盘右侧有一个带序号的列表，它随着游戏进行而更新，记录了棋盘每一步的变化。


如果你已经对井字棋游戏非常熟悉了，那么你可以关闭游戏并继续阅读本教程。我们将从一个简单的React应用开始做起。下一步我们将先搭建React的开发环境，使你可以开始编写React应用。


### 预备知识
我们会假设你已经熟悉HTML和JavaScript，但实际上即使你只掌握了不同于前两者的编程语言，也足以跟进本教程。我们还假设你已经对于函数（functions），对象（objects），数组（arrays），你至少需要理解类（classes）的概念。

如果你需要复习一下JavaScript，我们推荐你在继续阅读本教程之前先行阅读[这篇教程][2]。注意，我们使用了JavaScript最近版本（ES6）的特性。在这篇教程中，我们将使用函数指针（arrow functions），类（classes），let和const声明。你可以通过[Babel REPL][3]来检查ES6代码会编译成什么。

--- 
## 搭建环境
有两种方式实现本教程，你可以选择在浏览器上编写代码或是使用本地开发环境编写代码。

### 选项1：在浏览器编写代码
这个环境搭建最为简单。
第一步，在新标签页打开[这个链接][4]。页面会展示一个空的井字棋棋盘和它对应的React代码。我们将对这部分代码进行编辑。


你现在可以跳过另一个环境搭建教程，并进入<a href="#react">React简介</a>。

### 选项2：本地开发环境搭建
这个部分是可选的，本教程无须搭建本地环境，在浏览器编写也可以完成。

#### 在命令行输入以下指令后你可以用指定的代码编辑器搭建本地开发环境

以下搭建工作量比选项一大，但完成后你可以自行选择编辑器来完成教程代码编写。以下是操作步骤：

1. 确保你已经安装了[Node.js][5]的最新版本
2. 依照[创建React应用教程][6]新建一个React项目
   
``` bash
npm install -g create-react-app
create-react-app my-app

```

1. 删除已新建项目中src/下的所有文件（注意不要删除目录）
   
``` bash
cd my-app
rm -f src/*
```

1. 在src/下添加index.css，并输入[这些CSS代码][7]
2. 在src/下添加index.js，并输入[这些JS代码][8]
3. 在src/index.js的开头添加如下代码
   
``` js
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
```

现在项目根目录下运行`npm start`，并用浏览器打开`http://localhost:3000`，应该可以看见一个空的井字棋棋盘。

我们推荐你的编辑器使用[这个高亮方案][9]。

#### 搭建环境问题

在配置环境时出错，可以访问[这些资源][10]。特别是[Reactiflux社区][11]是一个解决问题的有效途径。

---

## React简介

#### React是什么

React是一个声明式，高效，灵活的JavaScript库，它可以用于实现用户接口。它使你可以通过少量，独立的代码（称为“Component”）来组成复杂的UI。


React有一定不同种类的组件（Component），我们将首先介绍`React.Component`。

``` js
class ShoppingList extends React.Component {
    render() {
        return (
            <div className="shopping-list">
                <h1>Shopping List for {this.props.name}</h1>
                <ul>
                    <li>Instagram</li>
                    <li>WhatsApp</li>
                    <li>Oculus</li>
                </ul>
            </div>
        );
    }
}

// Example usage: <ShoppingList name="Mark" />
```

我们立刻接触到了这些像XML一样的标签。通过组件（Component），我们可以告诉React需要在屏幕上显示什么。当数据变化时，React会高效地重新渲染（render）组件。

这里的ShoppingList是一个**React component class**，或者说**React component type**。一个组件接受参数，参数名为props（properties的缩写）。组件的返回值是通过render方法渲染的一个有层次的视图结构（a hierarchy of views）。

`render`方法返回一个对屏幕展示内容的说明。React接受render传入的说明并展示渲染成果。特别的是，`render`方法返回的是一个React元素（element），是一种轻量级的渲染说明。大部分的React开发人员会使用一种特殊的语法“JSX”，它可以使得渲染说明的结构便于书写。例如`<div />`标签将会被编译器翻译成React.createElement('div')。以上的代码片段等价于如下React代码：

``` js
return  React.createElement('div', {className: 'shopping-list'},
        React.createElement('h1', /* ... h1 children ... */),
        React.createElement('ul', /* ... ul children ... */)
);
```

[点击这里查看完整扩展后的React代码][12]


如果你对于createElement()方法的工作原理感到好奇，可以通过[API说明文档][13]来了解其中的细节，它在本教程中无须使用，我们会全程使用JSX。


JSX拥有JavaScript的全部功能。你可以在JSX的括号里添加任何JavaScript代码。每一个React元素都是一个JavaScript对象，你可以在程序中通过变量来存储或是遍历React元素。


ShoppingList组件仅会渲染一些React自带的DOM元素，例如`<div />`和`<li />`。你也可以编写自定义组件进行渲染。例如现在我们可以通过插入<ShoppingList />来渲染整个shopping list。每个React元素都会被封装，并且相互独立，这种设计允许设计者通过简单的组件来构建复杂的UI。

#### 阅读初始代码（starter code）

如果你选择在浏览器查看代码，在新标签页打开[这个链接][14]。
如果你选择在本地查看代码，只要在你的项目文件夹（搭建环境时创建的）中打开`src/index.js`即可。


这些代码是我们即将构造的应用的基础代码，我们已经提供了CSS，你只需要关注React学习和井字棋游戏的编写。


在阅读代码时你会发现代码中有三个React组件：

- Square
- Board
- Game

Square组件渲染一个`<button>`，代表棋盘的一个正方形格子。Board组件渲染9个正方形格子。Game组件渲染了拥有多个placeholder的棋盘，在后面的教程中我们将要修改这部分代码。当前代码中没有组件之间的通信和互动。


#### 通过props传递数据

例如我们现在需要从Board组件向Square组件传递一些数据。


在Board代码中的`renderSquare`方法内，更改原代码，向Square传入一个`value`参数。

``` js
class Board extends React.Component {
    renderSquare(i) {
        return <Square value={i} />;
}
```

在Square代码中，把`{/* TODO */}`更改为`{this.props.value}`，这样Square的`render`方法就可以展示value值。

``` js
class Square extends React.Component {
    render() {
        return (
            <button className="square">
                {this.props.value}
            </button>
        );
    }
}
```

之前的渲染效果：
![原棋盘][15]


更改后，你可以在棋盘的每个格子（Square）中看到一个数字：
![更改后棋盘][16]


[点击此处查看完整代码][17]


现在你已经实现了从父组件（Board）向子组件（Square）传递数据了。props的传递本质上就是信息在React应用中的传递，也就是数据在父组件和子组件之间的传递。


#### 编写可响应操作的组件

现在我们需要在点击棋盘上的格子时，在格子里显示一个“X”标记。


第一步，按照如下代码修改Square组件中`render()`函数的返回值里的button标签。

``` js
class Square extends React.Component {
    render() {
        return (
                <button className="square" onClick={function() { alert('click'); }}>
                    {this.props.value}
                </button>
            );
    }
}
```

现在如果我们点击一个棋盘上的方格，我们将会得到一个alert消息。


__注意__：为了简便书写和避免[这种令人混乱的写法][18]，本教程将在编写所有的事件处理函数时使用[箭头函数][19]。

``` js
class Square extends React.Component {
    render() {
        return (
            <button className="square" onClick={() => alert('click')}>
                {this.props.value}
            </button>
        );
    }
}
```

注意这一句：`onClick={() => alert('click')}`，它将一个函数作为参数传入props中的onClick。它只会在单击后被触发，如果你忘记写`()=>`而是写成了`onClick={alert('click')}`。那么每当这个组件被重新渲染时，alert就会被触发，这是一个很常见的错误。

下一步，我们需要被点击的Square组件“记住”自己被点击了，并用一个“X”标记来填充自己。为此，我们需要使用__state__。

React组件可以通过在构造器中设置`this.state`来配置并使用__state__属性。我们可以在Square组件的构造器中对`this.state`中定义一个value字段，来储存Square的当前状态，并通过点击来改变它。

首先我们需要给Square组件添加一个构造器，来初始化__state__：

``` js
class Square extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: null,
        };
    }

    render() {
        return (
            <button className="square" onClick={() => alert('click')}>
                {this.props.value}
            </button>
        );
    }
}
```

__注意__：在JavaScript类中，只要自身是一个子类，则总是需要在构造器的开头使用super(props)调用，因此所有拥有构造器的React组件类都需要在构造器的开头使用super(props)调用。


现在我们需要修改Square的`render`方法来展示Square被点击后的状态变化。

- 在`<button>`标签中把`this.props.value`改成`this.state.value`
- 把事件处理函数中的`()=>alert()`改成`() => this.setState({value: 'X'})`
- 出于可读性考虑，将className和onClick函数分成两行书写

做了以上修改后，Square组件的`render()`方法返回的`<button>`标签内容如下：

``` js
class Square extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: null,
        };
    }

    render() {
        return (
            <button
            className="square"
            onClick={() => this.setState({value: 'X'})}
            >
                {this.state.value}
            </button>
        );
    }
}
```

通过在`render()`函数的onClick中调用`this.setState`方法，我们使得这个组件每次`<button>`被点击时都会重新渲染。在重新渲染后，Square的value值就会变成‘X’，当你点击任意一个Square组件，棋盘上对应位置都会出现一个‘X’。

当你在一个组件的`render()`方法中调用`setState`，它的所有子组件也会被重新渲染。

[点击此处阅读完整代码][20]

---

[1]: https://codepen.io/gaearon/pen/gWWZgR?editors=0010
[2]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/A_re-introduction_to_JavaScript
[3]: https://babeljs.io/repl/#?presets=react&code_lz=MYewdgzgLgBApgGzgWzmWBeGAeAFgRgD4AJRBEAGhgHcQAnBAEwEJsB6AwgbgChRJY_KAEMAlmDh0YWRiGABXVOgB0AczhQAokiVQAQgE8AkowAUAcjogQUcwEpeAJTjDgUACIB5ALLK6aRklTRBQ0KCohMQk6Bx4gA
[4]: https://codepen.io/gaearon/pen/oWWQNa?editors=0010
[5]: https://nodejs.org/en/
[6]: https://reactjs.org/docs/create-a-new-react-app.html#create-react-app
[7]: https://codepen.io/gaearon/pen/oWWQNa?editors=0100
[8]: https://codepen.io/gaearon/pen/oWWQNa?editors=0010
[9]: http://babeljs.io/docs/en/editors/
[10]: https://reactjs.org/community/support.html
[11]: https://discordapp.com/invite/0ZcbPKXt5bZjGY5n
[12]: https://babeljs.io/repl/#?presets=react&code_lz=DwEwlgbgBAxgNgQwM5IHIILYFMC8AiJACwHsAHUsAOwHMBaOMJAFzwD4AoKKYQgRlYDKJclWpQAMoyZQAZsQBOUAN6l5ZJADpKmLAF9gAej4cuwAK5wTXbg1YBJSswTV5mQ7c7XgtgOqEETEgAguTuYFamtgDyMBZmSGFWhhYchuAQrADc7EA
[13]: https://reactjs.org/docs/react-api.html#createelement
[14]: https://codepen.io/gaearon/pen/oWWQNa?editors=0010
[15]: https://reactjs.org/static/tictac-empty-1566a4f8490d6b4b1ed36cd2c11fe4b6-a9336.png
[16]: https://reactjs.org/static/tictac-numbers-685df774da6da48f451356f33f4be8b2-be875.png
[17]: https://codepen.io/gaearon/pen/aWWQOG?editors=0010
[18]: https://yehudakatz.com/2011/08/11/understanding-javascript-function-invocation-and-this/
[19]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions
[20]: https://codepen.io/gaearon/pen/VbbVLg?editors=0010
