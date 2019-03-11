Title: 谈谈样例类
Date: 2019/3/11
Category: scala
tags: scala
Cover: images/Scala_logo.png
Summary: Scala提供了功能强大的模式匹配方法，为了更加便捷的使用模式匹配，scala专门定制了样例类，本文将讲述样例类如何使模式匹配的编写变的更容易

## 谈谈样例类 Case Class

Scala提供了功能强大的模式匹配方法，如果之前有接触过模式匹配，你很可能已经和样例类打过交道了，这篇文章我们将详细讨论样例类如何帮助我们编写更简洁的模式匹配

我们首先观察一个样例类的使用例子：


```scala
case class Fruit(name: String, price: Double)
```


此处，我们定义了一个样例类Fruit，它包含一个String类型的name字段和一个Double类型的price字段


```scala
val fruits = Seq(Fruit("apple", 3.5), Fruit("banana", 4.8))
```


此处，定义一个序列类型的fruits变量保存了两个水果实例


```scala
for(fruit <- fruits) fruit match {
    case Fruit("apple", price) => println("the price of apple is " + price)
    case Fruit(_, _) => println("other fruit!")
}
```

    the price of apple is 3.5
    other fruit!

此处，我们使用模式匹配处理定义的fruits序列，如果该水果是苹果，我们打印出包含其价格的提示语句，如果是其他类型的水果，则直接打印"other fruit!"

以上便是一个使用样例类进行模式匹配的短小但完整的实例，仔细分析以上三处代码，你能发现样例类为我们编写模式匹配提供了哪些遍历吗？

第一处：使用样例类，参数列表中的参数都隐式地获得了一个`val`修饰符，由于scala中参数列表的参数并不会自动成为自动，仅当其包含`val`或`var`修饰符时其才会自动转为字段，因此样例类的第一个优点是帮助我们自动创建参数列表的对应类字段。如果不使用样例类，我们可能需要像如下这样书写：


```scala
class Fruit2(val name: String, val price: Double)

class Fruit3(namestr: String, pricenum: Double) {
    val name = namestr
    val price = pricenum
}
```


第二处：样例类为我们提供的便捷不止一处，看一下这条语句 `val fruits = Seq(Fruit("apple", 3.5), Fruit("banana", 4.8))`，有没有发现什么不一样的地方？是在类实例化的地方！当我们构建苹果和香蕉两个实例的时候，我们使用的是`Fruit("apple", 3.5)`和`Fruit("banana", 4.8)`，而不是常见的`new Fruit("apple", 3.5)`与`new Fruit("apple", 3.5)`。如果你已经了解过有关伴生对象`apply`方法的有关知识，应该对此不会陌生，当我们写下 `Fruit("apple", 3.5)`的时候，我们实际上调用了`Fruit`类伴生对象的`apply`方法，该方法接受name和price两个参数的值，返回一个类实例。事实上使用`Seq(……)`的形式定义序列变量也是调用了其伴生对象的`apple`方法。结合第一点，如果不借助样例类，我们可能需要采用如下的定义形式：


```scala
class Fruit4(val name: String, val price: Double) 
object Fruit4 {
    def apply(name: String, price: Double) = new fruit2(name, price)
}
```

第三处：第三处是样例类提供的用于模式匹配的核心功能。当使用`case Fruit("apple", price)`形式的模式匹配时，通常称其为构造方法模式，因为该模式匹配的是类构造方法所对应的参数，例如类构造方法的第一个字段将与常量”apple“进行比较，第二个字段直接赋值给price变量。你可能觉得上述的写法是自然而然的，似乎并不需要借助样例类提供的便利，实则不然，构造方法模式的实现需要类定义了`unapply`方法，而样例类就为我们已经为我们定义了该方法。

> 通常称定义了`unapply`方法的类为提取器，实际上`unapply`方法可以根据实际需要有多种形式，构造方法模式只是`unapply`的一种实现，如下形式unapply接受的并不是一个Email对象，而是一个普通字符串


```scala
class Email(val name: String, val domain: String)
object Email {
    def apply(name: String, domain: String) = name + "@" + domain
    def unapply(email: String) = {
      val res = email.split("@")
        Some((res(0), res(1)))
    }
}
```

如果没有样例类，我们可能需要实现如下形式的定义：


```scala
class Fruit5(val name: String, val price: Double)
object Fruit5 {
    def apply(name: String, price: Double) = new Fruit5(name, price)
    
    def unapply(fruit: Fruit5) = Some((fruit.name, fruit.price))
}
```

以上，我们讨论了case class 样例类如何通过三个方面帮助我们简化模式匹配的编写，最重要的是第三点，case class 帮我们实现了`unapply`方法，case class还提供了其他有用的方法，例如`copy`方法，感兴趣的朋友可参阅相关介绍。
