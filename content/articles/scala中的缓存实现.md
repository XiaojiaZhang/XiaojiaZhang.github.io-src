Title: scala中的缓存处理
Date: 2019/3/7
Tags: scala, 缓存
Cover: images/Scala_logo.png
Summary: 如何在scala中实现简易的缓存方案提高计算效率？
Category: scala


[TOC]

### 1.缓存问题概述

缓存是指每次计算结果进行保存，再下次需要得到相同的计算结果时直接从缓存中获取，无需重复计算。缓存的使用是一种典型的以空间换时间的优化方案。在有些计算中，可能会连接多次执行相同的计算（多次调用函数其入参相同），一种有代表性的便是动态规划算法。此时使用缓存，能够有效提升计算效率。

缓存的基本思想是保存每次函数执行结果。所以缓存实现的第一个问题是如何将函数计算结果进行保存？

1. 使用何种数据类型保存缓存值？

一种简便的方式是使用映射保存每一个缓存值，其中映射的键为函数入参，值为函数计算结果。这样，每次调用时，首先从映射中查找对应的键是否有值存在，如果存在，则直接中缓存中返回结果，否则，执行函数调用，并将计算结果添加到缓存映射中。

2. 缓存值保存到何处？

由于函数调用每次都会创建一个新的函数环境，一种可能的方案是使用一个全局变量保存缓存结果。每次在函数执行时，首先从该全局变量中检查是否存在缓存值，如果不存在，则计算新的结果，并将其添加到全局变量中。然而，在scala中，并不支持类似于python的global声明实现一个全局变量的定义。此外，即便可以使用全局变量，通常也不是一种优雅的解决方案。在函数式编程理念中，**闭包**可以用于保存外部函数的状态，是一种好的解决方案。我们使用如下实例讲解基于闭包的缓存方案。

### 2.使用闭包实现缓存

如下`isPrime`函数定义了计算素数的一个简单方案：


```scala
def isPrime(num: Int): Boolean = {
  2 to (num - 1) forall (x => num % x != 0)
}
```

为了实现缓存，基于闭包方案，可以写出如下函数：


```scala
def memorizedIsPrime: Int => Boolean = {
    
  def isPrime(num: Int): Boolean = {
    2 to (num - 1) forall (x => num % x != 0)
  }

  val cache = collection.mutable.Map.empty[Int, Boolean]

  // 返回一个函数
  num =>
    cache.getOrElse(
        num, // 如果num存在，直接返回cache(num)
        {print(s"\n Calling isPrime since input ${num} hasn't seen before and caching the output")
         cache update(num, isPrime(num)) // 如果不存在，则执行isPrime计算，并更新缓存映射
         cache(num)  //返回计算结果
        })
}
```


在上例的实现中，我们将计算函数`isPrime`主体放到了`memoizedIsPrime`内部，`memoizedIsPrime`函数返回了一个函数，这个结果函数将成为我们后续进行素数与否计算的执行体。


```scala
val isPrime2 = memorizedIsPrime
```

```scala
isPrime2(10)
```
    
     Calling isPrime since input 10 hasn't seen before and caching the output

     Boolean = false




```scala
isPrime2(10)
```

    Boolean = false


为区别起见，将memoizedIsPrime返回的函数命名为isPrime2，使用该函数第一次调用计算10是否为素数，由于10不存在与cache的键中，所以执行getOrElse的第二个参数代码块，打印提示，计算结果，更新缓存映射，最终返回计算结果。第二次调用函数计算10是否为素数，由于10已经存在与缓存映射的键中，所以直接从缓存映射中查找结果并进行返回。

此处的关键是通过使用闭包，isPrime2函数能够访问并修改其上层函数中cache映射的值。

### 3.基于闭包的通用缓存方案

使用闭包的通用缓存方案处理思路即通过对原计算主体函数进行包装，返回一个新的拥有同样函数签名的函数。


```scala
def memorizedFun[K, V](f: K => V): K => V = {
    val cache = collection.mutable.Map.empty[K, V]
    
    num => cache.getOrElse(num,
                          {cache update(num, f(num))
                          cache(num)})
}
```



```scala
val isPrime3 = memorizedFun(isPrime)

```


```scala
isPrime3(10)
```
    
     Calling isPrime since input 10 hasn't seen before and caching the output

    Boolean = false


```scala
isPrime3(10)
```

    Boolean = false

在上述实现中，memorizedFun函数接受拥有一个入参的主体计算函数，基于该通用方案，我们定义了了`isPrime3`函数，调用结果显示，该函数支持缓存。

本文主要参考[Scala: Optimizing expensive functions with Memoization](https://medium.com/musings-on-functional-programming/scala-optimizing-expensive-functions-with-memoization-c05b781ae826)
