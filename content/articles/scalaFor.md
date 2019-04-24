Title: 翻译for推导式
Date: 2019/4/24
tags: Scala
Cover: images/russianDoll.jpg
Summary:

[TOC]


如果你有Scala集合的使用经验，那么你很大可能上已经使用过了集合操作的`map`、`flatMap`、`foreach`、`filter`等方法，你也很大可能上使用过for表达式对集合进行遍历操作。不同与其他语言的for循环，scala的for循环实际上只是一种语法糖，所有对集合遍历的for推导式均可被翻译为对原始集合使用`map`、`flatMap`、`foreach`、`withFilter`四种方法的调用组合。本文对scala中for推导式所涉及的不同情形如何翻译为对应的集合操作方法进行详细总结。

### 1. for推导式基础

根据是否返回结果，for表达式可分为两种。如果需要返回对集合元素操作后的结果，需要使用`yield`函数，如果只是以副作用(side effect)的形式对集合元素进行遍历，不返回任何结果，则像正常形式书写具有副作用的语句即可。

for推导式结构可分为两大部分，第一部分的可能操作包括：构建生成器、对集合元素进行过滤（使用if语句）、对集合元素进行模式匹配（模式匹配也可视作某种形式的过滤）、基于集合元素构建中间变量。第二部分包括的可能操作包括交出对集合元素进行转换后的新元素或执行具有副作用的语句。

for推导式的通用形式如下：
```scala
// 1.交出yield代码块最后结果
for {...} yield {...}
// 2.以副作用形式执行执行第二个代码块中的语句
for {...} {...}
```

### 2. 翻译for推导式

首先我们讨论交出新集合的for推导式，即形如`for {...} yield {...}`的for推导式。

#### 2.1 直接单个生成器的for表达式

```scala
for (x <- expr) yield expr2
```
这样的for推导式会被翻译为对集合调用`map`方法：
```scala
expr map {x => expr2}
```

#### 2.2 翻译包括多个生成器的for表达式

```scala
for (x <- expr; y <- expr2) yield expr3
```
这种包括两个及其以上生成器的for推导式会被翻译为对集合调用`flatMap`方法和`map`方法，其中除最后一个生成器之外的生成器均调用`flatMap`方法，最后一个生成器会被翻译为对`map`方法的调用：
```scala
expr flatMap {x => expr map {y => expr3}}
```

#### 2.3 翻译包括一个过滤器的for表达式

此处为便于理解，我们只关注包括单个生成器和过滤器的for表达式

```scala
for (x <- expr; if expr2) yield expr3
```
此处，if表达式会被翻译为对集合`withFilter`方法的调用，`withFilter`与`filter`方法作用类似，即根据布尔表达式结果对集合元素进行过滤，不同的是，`withFilter`方法返回结果是惰性求值的，这有助于提高性能。翻译结果如下：
```scala
expr withFilter (x => expr2) map {x => expr3}
```

#### 2.4 翻译包括模式匹配的for表达式

for表达式的一个特别便捷之处便是其允许对集合元素进行模式匹配提取我们感兴趣的部分。对于不符合给定模式的集合元素，for表达式会先对其过滤，仅对符合给定模式的元素做进一步变化。此处列出仅包括一个生成器的且对集合元素进行模式匹配的for表达式。
```scala
for (pat <- expr1) yield expr2
```
使用pat表示制定的元素模式，翻译后的for推导式如下：
```scala
expr withFilter {
    case pat => true
    case _ => false
} map {case pat => expr2}
```

如果制定的模式为单个变量或元组时，由于所有的元素都符合这中简单模式，因此不需要执行`withFilter`方法，直接翻译为对`map`方法的调用：
```scala
expr map {case pat => expr2}
```

#### 2.5 翻译包括生成中间变量的for表达式

在一些集合处理中，我们可能需要根据集合的元素生成中间变量，形式如下：
```scala
for (x <- expr1; y = expr2) yield expr3
```
由于expr2一般是一个与x相关的表达式，因此我们首先需要构建出一组同时包括(x, y)元组的集合，对上述for表达式的初步翻译如下：
```scala
for ((x, y) <- for(x <- expr1) yield (x, expr2)) yield expr3
```
此时，该for推导式仅由生成器构成（和一个元组模式匹配），继续翻译：
```scala
expr1 map {x => (x, expr2)} map {case (x, y) => expr3}
```

____________________________________

前面我们讨论了返回新集合的for推导式可能的几种形式。对于仅以副作用形式执行的for推导式，由于不需要交出值，因此对集合`map`和`flatMap`方法的调用都会被翻译为对`foreach`方法的调用。此处，我们展示几种简单的形式。

#### 2.6 包含多个生成器的for表达式

```scala
for (x <- expr1; y <- expr2) body
```
该for表达式会被翻译为如下形式：
```scala
expr1 foreach{x => expr2 foreach (y => body)}
```

#### 2.7 包含过滤器的for表达式
```scala
for (x <- expr1; if expr2; y <- expr3) body
```
上述expr2为一个关于x的布尔表达式，首先会根据该布尔表达式对expr1生成器进行过滤，随后执行嵌套`foreach`方法，翻译如下：
```scala
expr1 withFilter(x => expr2) foreach{x=> expr3 foreach {y => body}}
```

#### 2.8 同时包含模式匹配和中间变量定义的for表达式

最后，让我们来点稍微复杂的，一个同时包含模式匹配和变量定义的for表达式
```scala
for (pat <- expr1; y <- expr3; z = expr4) body
```
首先根据模式匹配对expr1生成器进行过滤，随后对变量定义进行翻译，由于涉及变量定义，因此我们需要使用`map`方法生成一组新的集合：
```scala
expr1 withFilter {
    case pat => true
    case _ => false
} foreach {case pat => expr3 map {y => (y, z)} foreach (case(y, z) => body)}
```

### 3. for表达式应用场景

当理解了for推导式可以翻译为对集合`map`,`flatMap`,`foreach`,`withFilter`方法的调用后，我们便可以尝试进一步发挥for表达式的威力。任何定义了以上四种方法的对象对可以使用for表达式来简化对方法的调用，使逻辑更为清楚。除了严格意义上的集合，scala中还包括其他多种支持for表达式的对象，因为它们都定义了这四种方法。scala`Option`类和`Future`类都定义了这四种方法，它们可以被视作具有单元素的集合。你很可能已经了过了`Option`类，`Option`包括两个子类，分别为单例对象`None`和`Some`类。None用于表示当前对象没有有意义的值，Some则用于包裹一个有意义的值。

Option类的map方法和flatMap简单逻辑如下：
```scala
object Option[T] {
    def map(f: T => A): Option[A] = this match {
        case None => None
        case Some(x) => Some(f(x))
    }
    
    def flatMap(f: T => Option[A]) => this match {
        case None => None
        case Some(x) => f(x)
    }
}
```

map方法接受一个函数，如果当前对象为None，则直接返回None，如果为Some类，则对其包括的值应用f函数并返回一个some类对象。flatMap与之类似，不过其接收一个返回Option类的函数。

在实际应用场景中，对函数参数为Option类的函数可能存在这样一种需求，如果存在一个即其以上的参数为None，则函数直接返回None。如果所有参数都为Some类型，则对这些参数进行进行处理。
假设当前函数逻辑结构如下：
```scala
def processOption[A, B, C](x: Option[A], y: Option[B]):Option[C] = {
    // 判断参数完整性
    if(一个及以上参数为None)
        None
    else
        Some(对参数进行处理)
}
```
使用for推导式可简化我们对参数完整性的判断：
```scala
def processOption[A, B, C](x: Option[A], y: Option[B]): Option[C] = {
    for (a <- A; b <- B) yield  Some(对参数进行处理)
```

### 4. 总结

总结一下，本文中，我们首先讲解了scala中for推导式的基础结构，第二节我们对for推导式不同情形如何翻译为对集合方法的调用进行详细解释，第三节我们展示了for推导式如何简化我们对Option对象的操作。
