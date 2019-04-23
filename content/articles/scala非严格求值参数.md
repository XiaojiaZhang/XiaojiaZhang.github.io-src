Title: Scala：非严格求值(non-strictness)参数
Date: 2019/4/23
tags: Scala
Cover: images/Scala2.jpg
Summary:


[TOC]



### 1. 非严格求值

非严格求值是函数的一种属性，称一个函数是非严格求值的意思是这个函数可以选择不对它的一个或多个参数求值。相反，一个严格求值的函数总是对它的参数求值。严格求值函数在大部分编程语言中是一种常态。并且大部分编程语言也只支持严格求值。在Scala中除非明确声明，否则任何函数都是严格求值的。


```scala
def add(x: Int, y: Int) = {
    println("run...")
    x + y
}
```


```scala
add(12, sys.error("failure"))
```


    java.lang.RuntimeException: failure
      scala.sys.package$.error(package.scala:30)
      ammonite.$sess.cmd6$Helper.<init>(cmd6.sc:1)
      ammonite.$sess.cmd6$.<init>(cmd6.sc:7)
      ammonite.$sess.cmd6$.<clinit>(cmd6.sc:-1)


在上面的例子中，我们定义了一个简单的计算两个整数之和的函数，由于默认参数为严格求值，因此当执行函数调用时，函数将在函数体执行之前，先计算传入的实参，然后尝试将其赋值给形参。由于我们传入`sys.error("failure")`给形参y，因此函数在第一步计算实参时变引发异常，导致函数调用失败。

如果参数y是一个非严格求值参数，函数调用会有什么不一样的结果呢？非严格求值参数只有在函数体执行中需要时才进行计算求值。因此即使传入`sys.error("failure")`给参数y，在调用涉及到形参y的语句之前，函数都不会抛出异常。由于scala支持函数作为参数，因此可以使用空参数函数来实现非严格求值。


```scala
def add(x: Int, y: () => Int) = {
    println("run...")
    x + y()
}
```


将参数y定义为一个接受空参数返回整数值的函数，在函数体中可以通过调用该函数得到整数值。此时y仍然是一个严格求值参数，但由于其是一个函数，调用add函数时，并不涉及到y函数的实际调用，基于此我们可以模仿出与非严格求值参数一样的运行方式。尝试对该add函数调用。


```scala
add(1, () => sys.error("failure"))
```

    run...



    java.lang.RuntimeException: failure
      scala.sys.package$.error(package.scala:30)
      ammonite.$sess.cmd8$Helper.$anonfun$res8$1(cmd8.sc:1)
      scala.Function0.apply$mcI$sp(Function0.scala:39)
      ammonite.$sess.cmd7$Helper.add(cmd7.sc:3)
      ammonite.$sess.cmd8$Helper.<init>(cmd8.sc:1)
      ammonite.$sess.cmd8$.<init>(cmd8.sc:7)
      ammonite.$sess.cmd8$.<clinit>(cmd8.sc:-1)


函数调用结果和我们预期一样，第一条`println`函数调用由于不涉及参数y因此被成功执行，只有当第一次执行y的调用时，函数才抛出异常。

### 2. 传名参数

由于非严格求值函数的重要性，scala提供了一种简洁的语法用于声明函数参数为非严格求值的，有时称其为传名参数(by-name)。这种语法便是在前一节空参数函数的形式上直接去掉括号`()`，使用这种方法定义的非严格求值参数，由于其参数类型不再是函数，因此我们直接在函数体中使用参数名称而不是通过函数调用的形式。


```scala
def add(x: Int, y: => Int) = {
    print("run...")
    x + y
}
```



```scala
add(1, 2)
```

    run...

3


实际上，传名参数的执行原理于第一节中的空参数函数形式完全一致，scala只是提供了更简洁的语法。由此不难发现一个问题，即如果函数体中涉及到多次对传名参数的使用，每次都会涉及对空参数函数的隐式调用。如果该非严格求值参数的计算开销较大，则会对函数执行效率产生不小影响。


```scala
def add(x: Int, y: => Int) = {
    println("run...")
    println(x + y)
    x + y
}
```


```scala
add(1, {Thread.sleep(3000); println("calculate y"); 2})
```

    run...
    calculate y
    3
    calculate y



3



add函数中涉及到两处对传名参数y的引用，每次引用y都需要重新计算其参数值。在我们的调用中，y的计算过程包括线程休眠3秒钟，输出调试信息以及返回y。两次引用意味着线程总共要休眠6秒钟。

对于计算开销较大的传名参数，可以考虑对其结果进行缓存，只在第一次使用时进行计算，其后引用直接返回缓存结果。scala提供了`lazy`关键字用于定义一个缓存结果。

def add(x: Int, y: => Int) = {
    lazy val y1 =  y
    println("run...")
    println(x + y1)
    x + y1
}应用


```scala
add(1, {Thread.sleep(3000); println("calculate y"); 2})
```

    run...
    calculate y
    3



3



我们定义了一个y1变量用于缓存y的参数值。观察函数输出结果，首先定义变量y1的过程并不涉及到对参数y的求值，这可以从`run...`语句先于`calculate y`打印进行验证，只有当第一次真正引用y1变量时，才会计算参数y的值。而在后续引用y1变量时，由于其结果已经被缓存，因此不会重复计算，这可以从`calculate y`只打印了一次得到验证。

### 3. 传名参数在并发编程中的应用

scala中Future对象支持异步计算。由于需要在不同的线程中进行计算。Future对象使用Future特质伴生对象的`apply`方法进行定义，方法签名如下：

```scala
def apply[T](body: => T)(implicit executor: ExecutionContext): Future[T]
```

该方法包括两个参数，第二个参数为用于执行计算的上下文执行环境，为[隐式参数]({filename}Scala隐式系统之隐式参数.md)。第一个参数为一个类型为T的传名参数。由于对body参数的求值需要异步进行，因此该参数必须被设置为传名参数，实现非严格求值。可以使用如下语句定义一个Future[Int]对象


```scala
// 导入类型为ExecutionContext的隐式值
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future
val x:Future[Int] = Future {
    Thread.sleep(3000)
    1 + 2
}
```

