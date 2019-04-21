Title: 闭包
Date: 2019/4/19
tags: Scala, python
Cover: images/programming.png
Summary:

[TOC]

在函数定义中，函数定义体中可能包括自由变量与绑定变量两种变量类型。绑定变量是指通过函数参数显示传入的变量，自由变量则是指在函数引用范围类但不是函数参数的变量。在函数每次执行时，都需要重新捕获函数体中涉及的自由变量。因此，对包括自由变量的函数，即使每次使用相同的参数进行调用，由于可能捕获不同的自由变量，因此可能产生不同的调用结果。闭包这一术语即指函数调用时，捕获自由变量从而闭合函数的动作。

## 1. 编译型语言中的闭包

### 1.1 闭包基础

对于编译型语言，函数定义中使用的自由变量必须已经被创建，且可以在函数体中进行访问， 否则编译无法通过。使用scala语言展示这一规则。


```scala
def add(b: Int): Int = a + b
```

    cmd0.sc:1: not found: value a
    def add(b: Int): Int = a + b
                           ^Compilation Failed


    Compilation Failed



```scala
val a = 1
def add(b: Int): Int = a + b
```


在第一个函数定义中，由于变量a尚未定义，因此编译错误，无法找到变量a。在第二个函数定义中，由于自由变量a可以在函数体中访问到，因此编译通过。

关于闭包一个理解要点是函数会在每一次运行时捕获其所包含的自由变量，因此函数的实际执行效果不取决于其定义时自由变量的状态，而取决与其实际运行时自由变量的状态。在上一个例子中，add函数自由变量被定义为一个`val`不可变变量，因此对于相同的输入参数，函数调用结果均不变。但如果自由变量是`var`变量，或一个可变的`val`变量，则调用结果可能不同。


```scala
var first = "hello"
def concate(second: String): String = first + second

concate(" world")
first = "bad"
concate(" world")
```

"hello world"

"bad world"



由于自由变量second是`var`变量，因此当自由变量引用发生变化时，相同输入参数的函数调用返回不同的调用结果。


```scala
import collection.mutable
val num = mutable.Buffer(1, 5, 3)
def expand(x: Int): Int = num.max * x
expand(3)
num += (8)
expand(3)
```

15

24


在上例中，尽管自由变量num是`val`变量，但由于其是可变变量，因此当更改其元素内容时，相同输入参数的函数调用返回了不同的调用结果。

### 1.2 嵌套函数中的闭包

闭包最常见的应用便是嵌套函数定义。在一些情况下，对于主函数的功能需求，我们可能在函数体内定义一个辅助函数。基于闭包技术，辅助函数无需重复定义一个参数用于表示其需要引用主函数参数，而是可以直接在其函数体内引用主函数的参数。


```scala
def outer(x: List[Int]) = {
    def inner(f: Int => Boolean): List[Int] = x.filter(f)
    inner(_ % 2 == 0)
}

outer(List(1, 2, 3))
```


List(2)



内层函数inner可直接引用外层函数的参数x作为自由变量，当内层函数调用时，闭包可捕获到外层函数的参数x。



## 2 解释型语言闭包

### 2.1 基础

区别于编译型语言，在解释型语言中，函数定义中的自由变量在函数定义时无需已经被定义，仅需保证在函数调用时，可捕获到相应的自由变量即可，使用python对解释型语言中的闭包机制进行将讲解。


```python
def concate(y = " world"):
    return x + y
```


```python
x = "hello"
concate()
```

    'hello world'

```python
x = "bad"
concate()
```

    'bad world'

同样，基于闭包机制，函数的具体执行结果并不取决于其定义时自由变量的状态，而取决于其实际调用时自由变量状态。

### 2.2 基于闭包机制的函数柯里化

python语言并不直接支持函数柯里化，不过可以基于闭包间接实现这一技巧。


```python
def curry(first):
    def inner(second):
        def inner2(third):
            return first + second + third
        return inner2
    return inner
```


```python
curry("python: ")("hello")(" world")
```

    'python: hello world'

使用三层嵌套函数实现对含有三个参数函数的柯里化。在inner2函数定义体中，first, second均为自由变量，使用闭包机制可向上分别捕获到inner和curry各自传入的参数。
