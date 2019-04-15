Title: 程序设计决策: 如何处理程序运行可能出现的异常？
Date: 2019/3/23
Cover: images/programming.png
tags: 编程设计
Summary:



在我们编写程序时，涉及大量的决策，不同地决策产生了不同的编码方案，不同决策之间也存在好坏之分。今天讨论的是关于如何处理程序运行时可能出现的异常。内容节选自[数据结构与抽象 Java语言描述](https://item.jd.com/12094507.html)一书。

我们编写的某一方法可能需要在满足特定条件的前提下才能正常工作。当方法的调用方在不满足该条件调用方法时，方法应该如何报告其可能出现的异常给调用方呢？

考虑我们正在使用Java语言设计一个实现抽象数据结构栈的类，该类当中包含两个方法：`pop`和`top`，其中`pop`方法弹出栈顶元素，`top`方法查看栈顶元素但不弹出。这两个方法均假设当前栈不为空，当栈为空的情况下调用该方法时，方法应该作何处理呢？

我们考虑这类方法可能的三种行为：
1. 方法假定其被调用时，栈不为空。即增加一个能保证该假设的前置条件。
2. 方法返回null。
3. 方法抛出一个栈为空的异常。

第一种行为适用于类中的私有方法，因为它们仅被同一类的其他方法调用。所以，作为设计类的程序员，私有方法仅会被你作为其他方法的助手方法使用，你应当能够保证该方法的前置条件在调用之前是满足的。即私有方法能够确信其将会被可信任的代码所调用。因此不会引发异常。

在栈的设计中，`pop`和`top`方法是公有方法而非私有方法，因此我们不能够信任客户遵从这些方法所需要的前置条件来正确调用该方法。所以第一种行为不是可行的选择，公有方法必须假定调用者可能在栈为空的情况下直接调用该方法。

如果我们执行第二种行为，返回一个特殊值，例如`null`用于表示当前栈为空的情况下调用返回的特殊结果。只要`null`不是栈中的合法项，我们就可以使用它来表示当前栈为空时的调用结果。但通常我们需要允许`null`作为合法值出现在栈中，因此使用`null`作为返回值将具有二义性，不额外检查当前栈是否为空，调用方不知道`null`是合法数据项还是在栈为空情况下返回的特殊项。

如此，我们只剩下第三种方案，即显示地抛出异常。采用这种设计，`null`被允许作为栈中的合法项。