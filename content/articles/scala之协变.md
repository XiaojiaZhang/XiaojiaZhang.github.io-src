Title: Scala类型系统之协变正确定义
Date: 2019/4/22
tags: Scala
Cover: images/Scala_logo.png
Summary:

[TOC]



scala类型参数型变包括协变、逆变与不变。本文主要总结协变类型定义中存在的常见问题。

### 1. 协变类型基础

对于一个拥有类型参数的泛型类型或泛型特质，我们可以在定义通过指定类型参数的型变符号来说明该泛型类型的型变类型。通过在类型参数前添加`+`号，可以声明当前泛型类型为协变的。例如，定义如下协变队列：


```scala
class Queue[+T]
val x: Queue[Any] = new Queue[Int]
```


由于`Int`是`Any`的子类，且`Queue`为协变类型，因此`Queue[Int]`是`Queue[Any]`的子类。可以将一个`Queue[Int]`类型的对象赋值给`Queue[Any`类型的变量。

### 2.   协变定义中常见错误

假设我们需要对当前队列添加一个用于入队的方法，考虑使用`List`作为保存队列元素的集合，每次入队后返回一个新的队列。对Queue类的初步设计可能如下：


```scala
class Queue[+T](val data: List[T] = List()){
    def put(x: T) = new Queue[T](x::data)
}
```

    cmd4.sc:2: covariant type T occurs in contravariant position in type T of value x
        def put(x: T) = new Queue[T](x::data)
                ^Compilation Failed


    Compilation Failed


对上述类定义代码进行编译，编译结果报错：协变类型T出现在需要逆变类型的变量x处。事实上，一旦泛型参数类型作为方法参数类型出现，包含这个泛型参数的类或特质就不能以这个类型参数做协变。上述类定义中，T作为方法参数类型出现，且T作为协变类型参数出现，因此违背了协变类定义规则。对协变定义规则的深入理解有助于理解型变约束的合理性。

假设上述代码可以正确编译通过，我们便能够正确执行如下语句：

```scala
class QueueInt(val data: List[Int] = List()) extends Queue[Int] {
    import math.sqrt
    override def put(x: Int) = new QueueInt(sqrt(x)::data) 
}
//由于Queue是协变类型，因此此条语句成立
val x: Queue[Any] = new Queue[Int]
// 由于String是Any的子类，因此此条语句成立
x.put("abc")
```

但上述第二条语句显然不应该成立，我们无法对一个字符串型变量进行开方，这正是协变定义中编译失败的原因。

### 3. 协变类型正确定义

处理协变类型方法定义错误的一种方式是添加类型下界约束


```scala
class Queue[+T](val data: List[T]=List()) {
     def put[A >: T](x: A) = new Queue[A](x::data)
     override def toString: String = data.toString
}
```


为便于展示，我们重写Queue类的toString方法，该方法直接打印列表元素。将`put`方法的参数类型修改为类型参数T的父类（包括T），此时可以向其中添加类型A的元素，返回的队列元素类型将是原有元素与新加入元素类型的最近父类，如下例所示：


```scala
val x = new Queue[Int]
val y = x.put("abc")
```

Queue[Int] = List()
    
Queue[Any] = List(abc)



可以看到，向`Queue[Int]`类型的队列添加`String`类型的元素后，返回一个`Queue[Any]`类型的队列，因为`Any`是`Sting`与`Int`的最近公共父类。

### 4. 协变类型的特例


```scala
class Test[+T](init: T) {
    var x = init
}
```

    cmd11.sc:2: covariant type T occurs in contravariant position in type T of value x_=
        var x = init
            ^Compilation Failed


    Compilation Failed


在上述协变类型定义包含一个可变字段x，尝试对代码进行编译，提示在可变变量定义中存在协变定义错误。实际上这只是我们在前一节提到的协变类型方法的参数类型不能与类型参数一致的一个特例。

当在scala中定义一个可变对象时，自动会生成两个方法，一个是get方法`def x: T`，一个是set方法`def x_=(y: T)`。由于set方法包含类型参数，因此无法协变定义失败。

为了解决这一问题，通常可以将可变对象访问级别设置为对象内部可见性：


```scala
class Test[+T](init: T){
    private[this] var x = init
}
```


使用`private`关键字结合限定词`this`使得x只能在对象内被访问，由于不存在从对象外部访问的可能性，因此之前讨论的型变可能引发的尅型错误也不会存在，即便此时我们的set方法参数类型仍然与类型参数相同，编译器也能正确编译通过。
