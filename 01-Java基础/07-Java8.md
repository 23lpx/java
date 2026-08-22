---
category: Java
priority: P0
status: 未学习
tags:
  - Java后端
  - 面试
  - Java
---

# Java8

## 88. Lambda 表达式是什么？

**面试回答**

Lambda 是 Java 8 引入的匿名函数的简洁写法，用 `参数 -> 方法体` 表示，代替原来写匿名内部类的繁琐代码。

**理解**

它本质是一个「函数式接口」的实例。原来实现一个接口要 new 一个匿名内部类写一堆样板代码，Lambda 直接 `(x, y) -> x + y` 搞定。它让代码更简洁，尤其是配合 Stream 和集合操作。

**场景**

项目里 `list.forEach(dish -> System.out.println(dish.getName()))`、`Comparator.comparing(d -> d.getPrice())` 都用 Lambda 简化代码。

**常见追问**

- Lambda 和匿名内部类区别？（Lambda 更简洁，只能用于函数式接口）
- Lambda 能捕获外部变量吗？（能，但变量必须 effectively final）

**易错点**

Lambda 只能用在「函数式接口」上，一个接口有多个抽象方法就不能用 Lambda 表示。

## 89. 什么是函数式接口？

**面试回答**

只有一个抽象方法的接口就是函数式接口，可以用 Lambda 表达式实现，通常加 `@FunctionalInterface` 注解标注。

**理解**

Lambda 的本质就是函数式接口的实例，所以接口必须有且只有一个抽象方法，编译器才能推断 Lambda 对应哪个方法。`@FunctionalInterface` 注解不是必须的，但加上能让编译器帮你检查，防止多加了抽象方法。Java 内置了很多，如 `Runnable`、`Comparator`、`Function`、`Predicate`。

**场景**

Stream 的 `filter` 参数是 `Predicate`（函数式接口），传 `dish -> dish.getStatus() == 1` 这个 Lambda 就能直接匹配。

**常见追问**

- 函数式接口可以有 default 方法吗？（可以，default/static 方法不算抽象方法）
- 常见函数式接口有哪些？（Function、Predicate、Consumer、Supplier）

**易错点**

「只有一个抽象方法」是核心，default 和 static 方法不影响；有多个抽象方法就不是函数式接口，不能写 Lambda。

## 90. Stream 是什么？

**面试回答**

Stream 是 Java 8 提供的对集合、数组做「流式」处理的 API，支持链式地过滤、映射、聚合等操作，代码更简洁。

**理解**

Stream 不是数据结构，它不存数据，而是一系列操作的流水线。操作分两类：中间操作（filter、map、sorted，返回新 Stream，惰性）和终止操作（forEach、collect、count，触发真正执行）。只有调用终止操作，整条流水线才会跑。

**场景**

项目里 `dishList.stream().filter(...).map(...).collect(Collectors.toList())` 链式处理菜品列表，替代一堆 for 循环。

**常见追问**

- Stream 存数据吗？（不存，是对数据源的流水线操作）
- 中间操作和终止操作区别？（中间操作惰性，终止操作触发执行）

**易错点**

Stream 本身不是集合，是「操作管道」；忘记调用终止操作时，中间操作不会执行。

## 91. Stream 和普通集合遍历有什么区别？

**面试回答**

普通遍历用 for/foreach 手动控制流程，命令式；Stream 用声明式链式 API 描述「做什么」，中间操作惰性执行，代码更简洁、可读性更高。

**理解**

普通 for 循环要自己写「怎么取、怎么判、怎么存」；Stream 声明式地写「过滤什么、映射什么、收集成什么」，逻辑更清晰。Stream 还能并行处理（parallelStream），而普通遍历是串行。不过 Stream 在简单场景下不一定比 for 快，选择时看可读性和场景。

**场景**

多条件筛选、映射、统计时用 Stream 一行搞定，比嵌套 for 循环清楚得多。

**常见追问**

- Stream 一定比 for 快吗？（不一定，简单遍历 for 可能更快）
- Stream 怎么并行？（parallelStream 或 parallel()）

**易错点**

Stream 的优势是「可读性和声明式」，不是「一定更快」，别把性能当 Stream 的唯一卖点。

## 92. `filter()` 有什么作用？

**面试回答**

`filter()` 是 Stream 的中间操作，按条件过滤元素，只保留满足条件的元素，返回一个新的 Stream。

**理解**

`filter` 接收一个 `Predicate`（返回 boolean 的 Lambda），对每个元素判断，true 保留、false 丢弃。它是惰性的，不会立即执行，要配合终止操作（如 collect）才生效。

**场景**

项目里 `dishList.stream().filter(d -> d.getStatus() == 1).collect(...)` 过滤出「起售状态」的菜品。

**常见追问**

- filter 返回什么？（新的 Stream）
- filter 会改原集合吗？（不会）

**易错点**

filter 是「中间操作」，不调用终止操作不会真正过滤，很多新手写了 filter 没 collect 以为没生效。

## 93. `map()` 有什么作用？

**面试回答**

`map()` 是中间操作，把流里的每个元素「转换」成另一个元素，返回转换后的新 Stream，常用于提取字段或类型转换。

**理解**

`map` 接收一个 `Function`（输入一个元素、输出另一个元素），一对一映射，元素个数不变。比如把 `List<Dish>` 映射成 `List<Long>`（提取 id）。

**场景**

项目里 `dishList.stream().map(Dish::getId).collect(Collectors.toList())` 提取所有菜品 id。

**常见追问**

- map 和 flatMap 区别？（map 一对一，flatMap 把嵌套结构拍平）
- map 会改变元素数量吗？（不会，一对一映射）

**易错点**

map 是「转换每个元素」，元素个数不变；要拍平嵌套集合用 flatMap，别搞混。

## 94. `forEach()` 有什么作用？

**面试回答**

`forEach()` 是终止操作，遍历流中的每个元素并执行指定操作，常用于打印、消费、累加等副作用。

**理解**

`forEach` 接收 `Consumer`，对流里每个元素执行一次操作，并触发整条流水线执行。它是终止操作，调用后流就结束、不能再复用。

**场景**

项目里 `list.forEach(System.out::println)` 打印，或 `list.forEach(item -> total += item.getPrice())` 做累加。

**常见追问**

- forEach 是中间还是终止操作？（终止）
- forEach 能改元素本身吗？（能改对象内部状态，但不推荐在 forEach 里改集合结构）

**易错点**

forEach 是终止操作，调用后流就不能再用了；不要在 forEach 里增删集合元素（会抛异常）。

## 95. Stream 会修改原集合吗？

**面试回答**

不会。Stream 操作是基于原集合生成新的流和结果，不修改原集合本身。

**理解**

Stream 是函数式的、不可变的操作：filter、map 等都返回新 Stream，collect 生成新集合，原集合内容不变。这也符合「无副作用」的设计，多个 Stream 操作可以安全复用同一个数据源。

**场景**

项目里对流做过滤、映射后 collect 到新 List，原来的 dishList 不受影响。

**常见追问**

- 如果原集合被外部改了，Stream 会怎样？（遍历中修改可能抛 ConcurrentModificationException）
- 怎么拿到处理后的结果？（用 collect 收集成新集合）

**易错点**

Stream 不修改原集合，但要拿结果必须用 collect 等终止操作收集，否则看不到任何变化。

## 96. Optional 是什么？解决什么问题？

**面试回答**

Optional 是 Java 8 的容器类，用来包装「可能为 null」的值，避免直接返回 null 导致空指针，让调用方显式处理空值。

**理解**

传统写法方法可能返回 null，调用方忘了判空就 NPE。Optional 把「值可能不存在」这个信息显式化：`Optional.ofNullable(x)` 包装，`orElse(默认值)`、`isPresent()`、`ifPresent()`、`map()` 等安全处理。它不消除 null，而是逼你面对 null。

**场景**

项目里按 id 查询可能查不到，返回 `Optional<Dish>`，调用方用 `orElseThrow(...)` 抛业务异常，比返回 null 更清晰。

**常见追问**

- Optional 能完全避免 NPE 吗？（不能，滥用 Optional.of 传 null 仍会 NPE）
- Optional 用在哪些场景？（方法返回值，一般不用于字段或方法参数）

**易错点**

Optional 是「返回值」场景的优化，不建议到处用（字段、方法参数）；`Optional.of(null)` 依然会抛 NPE。
