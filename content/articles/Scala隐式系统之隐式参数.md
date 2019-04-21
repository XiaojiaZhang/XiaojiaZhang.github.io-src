Title: Scala隐式系统之隐式参数
Date: 2019/4/21
tags: Scala
Cover: images/Scala_logo.png
Summary:

scala隐式系统包括隐式转换和隐式参数两大部分，本文我们先来聊聊隐式参数。

隐式参数用法：编译器会使用隐式参数提供整个最后一组柯里化的参数列表。例如当最后一组柯里化参数被定义为隐式参数树，隐式参数可能会`someCall(a)`替换为`someCall(a)(b)`,或者将`new Some(a)`替换为`new Some(a)(b)`以及将`some(a)`替换为`some(a)(b, c, d)`，当时也可以显示提供隐式参数列表所需要的参数。乍看上去，隐式参数似乎与默认参数有点类似，这也是我自己在一开始学习隐式参数时所疑惑的地方，接下来我们一起对隐式参数一探究竟。

### 1. 隐式参数 VS 默认参数

隐式参数与默认参数类似的一点是都位于参数列表的最后，但默认参数并不需要将函数参数柯里化。看如下例子：


```scala
def defaultParam(first: String, second: String="world"): String = first + second

defaultParam("Hello ")
```

"Hello world"




```scala
def implicitParam(first: String)(implicit second: String): String = first + second
implicit val second = "World"
implicitParam("Hello")
```

"HelloWorld"



以上是对默认参数与隐式参数的一个简单比较，默认参数通过在参数列表中提供默认值实现，隐式参数则在参数列表中使用关键字`implicit`定义，当调用函数隐式参数的函数时，编译器会在当前作用域内查找可用的同类型隐式值，使用该隐式值填充隐式参数列表。

由于默认参数需要在参数列表中制定，默认参数只能是某一种给定的类型，默认参数也只能提供一个默认值。不同于默认参数，隐式参数可以为泛型参数，基于泛型的隐式参数可以有多个隐式值，这也是隐式参数相对于默认参数最显著的差异。因此，隐式参数对与泛型函数尤其有用。接下来我们来看一个使用隐式参数的实际案例。

### 2. 在泛型函数中使用隐式参数

我们准备定义一个用于寻找列表最大值的方法，该方法接收两个参数，一为目标列表，二为用于比较列表元素大小的方法，此处将该参数定义为`Ordering`特质。对于基本类型的列表，例如整型列表、字符串列表等，scala标准库提供了隐式的排序方法，如`Ordering[Int]`、`Ordering[String]`，因此我们想使用隐式参数来简化函数调用，这样在查找基本类型列表最大值时，我们可以不必显示给定比较大小的特质。我们的函数定义如下：


```scala
def maxListImpParm[T](elements: List[T])(implicit ordering: Ordering[T]): T = elements match {
    case List() => throw new IllegalArgumentException("empty List")
    case List(x) => x
    case x::rest =>
        val maxRest = maxListImpParm(rest)(ordering)
        if (ordering.gt(x, maxRest)) x
        else maxRest
}
```




```scala
maxListImpParm(List(3, 5, 7, 2))
maxListImpParm(List("Bob", "Ana", "Selina"))
```

7

"Selina"



由于scala提供了隐式的`Ordering[Int]`以及`Ordering[String]`,因此上述代码语句可以执行成功。


```scala
case class Score(value: Double)

implicit object ScoreComp extends Ordering[Score] {
    import math.ceil
    def compare(x: Score, y: Score): Int = ceil(x.value - y.value).toInt
}

maxListImpParm(List(Score(67), Score(89.3), Score(55)))
```


Score(89.3)



对于自定义类型，也可以通过引入隐式的`Ordering[Score]`特质实现最大值的查找。

 ### 3. 基于隐式参数的上下文界定

在上面查找列表最大值的例子中，在递归调用函数也可以省略掉隐式参数。因此，代码可以简化为如下：


```scala
def maxListImpParm[T](elements: List[T])(implicit ordering: Ordering[T]): T = elements match {
    case List() => throw new IllegalArgumentException("empty List")
    case List(x) => x
    case x::rest =>
        val maxRest = maxListImpParm(rest)
        if (ordering.gt(x, maxRest)) x
        else maxRest
}
```



我们将递归调用`maxListImpParm(rest)(ordering)`改成了`maxListParm(rest)`，此时缺失的参数`ordering`将通过同样的隐式参数查找规则查找。

还有一种方法可以去掉对ordering的第二处调用`ordering.gt(x, maxReset)`，这涉及到标准库中定义的如下方法：


```scala
def implicitly[T](implicit t: T) = t
```


`implicitly`泛型函数中唯一的参数被设置为隐式参数，因此可以直接通过`implicitly[T]`的形式进行调用，此时编译器会查找是否存在隐式的类型为T的变量，如果存在，则返回该变量。因此，`maxListImpParm`可进一步写为如下形式：


```scala
def maxListImpParm[T](elements: List[T])(implicit ordering: Ordering[T]): T = elements match {
    case List() => throw new IllegalArgumentException("empty List")
    case List(x) => x
    case x::rest =>
        val maxRest = maxListImpParm(rest)
        if (implicitly[Ordering[T]].gt(x, maxRest)) x
        else maxRest
}
```

我们使用`implicitly[Ordering[T]]`代替了`ordering`参数名称，此时方法体中不涉及隐式参数的参数名称。由于这个模式经常出现，scala提供了上下文界定来让我们进一步简化函数签名，`maxListImpParm`可写为如下形式：


```scala
def maxListImpParm[T: Ordering](elements: List[T]): T = elements match {
    case List() => throw new IllegalArgumentException("empty List")
    case List(x) => x
    case x::rest =>
        val maxRest = maxListImpParm(rest)
        if (implicitly[Ordering[T]].gt(x, maxRest)) x
        else maxRest
}

maxListImpParm(List(Score(67), Score(89.3), Score(55)))
```

Score(89.3)



上下文界定是一种简化的方法，编译器会将其翻译为对等的包含有一个隐式参数的方法签名，即：
`def maxListImpParm[T: Ordering](elements: List[T]): T`等价于`def maxListImpParm[T](elements: List[T])(implicit AnyName: Ordering[T])`。

由于隐式参数的名称不会出现在方法体中，因此我们可以使用上下文界定简化方法签名。同样，当使用上下文界定时，如果需要获取隐式参数，我们需要使用`implicitly[T]`获取类型为T的隐式参数。
