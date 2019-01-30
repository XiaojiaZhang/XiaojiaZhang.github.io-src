Title: Python数据分组
Date: 2019/1/30
Tags: python, 函数式编程
Cover: images/python_logo.svg
Summary: 如何使用python语言对数据进行分组？
Category: python


问题描述：我们需要对一组数据按照某种规则进行分组，如何利用python实现？

[TOC]


## 1. 使用`itertools`模块中的`groupby`函数实现数据分组

假定有如下一组随机数据，我们需要根据其能否被1,2,3,4,5分别整除对齐进行分组，该如何实现？


```python
from random import randrange
data = [randrange(100) for _ in range(20)]
data
```

    [45, 38, 46, 81, 19, 13, 72, 60, 64, 67, 94, 54, 75, 4, 39, 45, 25, 7, 21, 75]



首先我们定义一个用来计算其分组指标的函数：


```python
from typing import Callable
key_fun: Callable[[int], int] = lambda val: val%5
```

可以使用`key_fun`函数计算每个元素的整除数：


```python
[key_fun(val) for val in data]
```

    [0, 3, 1, 1, 4, 3, 2, 0, 4, 2, 4, 4, 0, 4, 4, 0, 0, 2, 1, 0]



实现了分组指标函数后，我们便可以考虑对数据进行分组了，python`itertools`模块提供了`groupby`函数用于实现数据的分组：


```python
from itertools import groupby
groups = groupby(data, key=key_fun)
for type_, group in groups:
    print(type_, tuple(group))
```

    0 (45,)
    3 (38,)
    1 (46, 81)
    4 (19,)
    3 (13,)
    2 (72,)
    0 (60,)
    4 (64,)
    2 (67,)
    4 (94, 54)
    0 (75,)
    4 (4, 39)
    0 (45, 25)
    2 (7,)
    1 (21,)
    0 (75,)


结果似乎有些奇怪，为什么会出现这么多的分组？事实上，`groupby`函数的运行方式可能并不像我们想象中的那样。

`groupby`函数执行时，会顺次遍历每一个元素，如果当前元素与前一元素的分组指标不相同，便会创建一个新的分组，这也就解释了为什么我们的分组结果中会有超过5组结果。理解这一运作原理后，很容易想到，要想实现我们想要的分组结果，首先需要根据分组指标对数据进行排序，使同一分组的数据聚集在一处，然后使用`groupby`函数进行分类，如下所示：


```python
groups = groupby(sorted(data, key=key_fun), key=key_fun)
for key, group in groups:
    print(key, tuple(group))
```

    0 (45, 60, 75, 45, 25, 75)
    1 (46, 81, 21)
    2 (72, 67, 7)
    3 (38, 13)
    4 (19, 64, 94, 54, 4, 39)


结果和我们预期的相一致。`itertools`模块`groupby`函数最大的不便就是需要对数据进行预先排序，这对于拥有较多元素的序列数据是一个比较耗时的操作，因此下一节我们想要实现不要排序的直接分组。

## 2. 基于分组指标直接对数据进行分组

我们的基本实现思想时使用字典保存分组，对于一组数据，顺次遍历所有元素，根据其分组指标将其添加到对应的分组结果中，具体实现如下：


```python
from typing import Iterable, Iterator, Tuple, List, Dict, TypeVar, Callable
from collections import defaultdict
val = TypeVar("val") # 表示待分组数据类型
K_ = TypeVar("K_") #表示分组指标类型

def group_by(data: Iterable[val],
             key: Callable[[val], K_]
            )-> Iterator[Tuple[K_, Iterator[val]]]:
    groups: Dict[K_, List[val]] = defaultdict(list)
    
    for item in data:
        groups[key(item)].append(item)
    
    for type_ in groups:
        yield type_, iter(groups[type_])
```


```python
for type_, group in group_by(data, key_fun):
    print(type_, tuple(group))
```

    0 (45, 60, 75, 45, 25, 75)
    3 (38, 13)
    1 (46, 81, 21)
    4 (19, 64, 94, 54, 4, 39)
    2 (72, 67, 7)


以上便是我们实现的无需排序的分组方式。

## 3. `itertools`模块中`groupby`函数为什么不直接提供无需预先排序的分组方式？

事实上，`itertools`模型中`groupby`函数所提供的分组方式在某种程度上为我们计算游程提供了很大的便捷。何为”游程“？游程指具有相同符号的序列。当我们想要计算一组数据所有游程的长度时，便可使用`groupby`函数。


```python
sample_data = [randrange(2) for _ in range(20)]
sample_data
```




    [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]



假定有如上一组序列数据，我们想要计算每组游程的长度，根据游程的定义，第一组游程为1，第二组游程为0，第三组游程为1，1，等等，由于`groupby`函数每当当前分组指标与前一组分组指标不同时变化创建新的分组，因此其每一个分组恰好对应一组游程。


```python
[(val, len(tuple(group))) for val, group in groupby(sample_data)]
```




    [(1, 1),
     (0, 1),
     (1, 2),
     (0, 4),
     (1, 2),
     (0, 2),
     (1, 2),
     (0, 1),
     (1, 1),
     (0, 1),
     (1, 2),
     (0, 1)]



如上我们便计算得到了每一组游程的长度，由于`groupby`函数返回的分组数据是一个迭代器对象，迭代器对象不支持求长度操作，因此为了计算每个游程的长度，需要先将其转化为一个序列数据。
