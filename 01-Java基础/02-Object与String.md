---
category: Java
priority: P0
status: 未学习
tags:
  - Java后端
  - 面试
  - Java
---

# Object与String

## 18. `==` 和 `equals()` 有什么区别？

**面试回答**

`==` 是运算符，基本类型比较值，引用类型比较地址；`equals()` 是 Object 的方法，默认比较地址，但很多类（如 String、Integer）重写了它，用来比较内容。

**理解**

`==` 对引用类型比较的是两个引用是否指向同一个对象；`equals` 的行为取决于类是否重写。没有重写 `equals` 的类，`equals` 和 `==` 效果一样。所以我们常说的「equals 比内容」其实只对重写过 `equals` 的类成立。

**场景**

比较两个字符串内容用 `"a".equals(b)` 而不是 `==`；比较订单 id 用 `Objects.equals(a, b)` 更安全（避免 NPE）。

**常见追问**

- 什么时候 `==` 和 `equals` 结果一样？（没重写 equals 时）
- String 的 `==` 和 equals 什么时候不同？（见 [[02-Object与String#29. `"abc"` 和 `new String("abc")` 有什么区别？]]）

**易错点**

别把 `equals` 无条件说成「比较内容」，只有重写了 `equals` 的类才比内容，默认还是比地址。

## 19. Object 默认的 `equals()` 比较什么？

**面试回答**

Object 默认的 `equals()` 就是比较两个引用是否指向同一个对象，等价于 `==`。

**理解**

Object 里 `equals` 的实现就是 `return (this == obj)`，比的是地址。所以自定义类如果不重写 `equals`，两个内容完全相同的对象用 `equals` 比较也会返回 false。这也是为什么实体类、自定义类型要按业务字段重写 `equals`（和 `hashCode`）。

**场景**

项目中如果两个订单对象字段完全一样，但没重写 `equals`，`order1.equals(order2)` 是 false，因为它们不是同一个对象；需要按「订单 id」判断相等时就要重写。

**常见追问**

- 为什么 Object 不直接比较内容？（Object 不知道子类有哪些字段，无法定义「内容相等」）
- 重写 equals 要注意什么？（自反、对称、传递、一致，且要重写 hashCode）

**易错点**

Object 的 equals 默认比地址，不是比内容；这是新手最常见的误解。

## 20. 为什么重写 `equals()` 通常要重写 `hashCode()`？

**面试回答**

因为 Java 约定：两个对象 `equals` 相等，`hashCode` 必须相等。如果只重写 `equals` 不重写 `hashCode`，会破坏这个约定，导致对象放进 HashMap/HashSet 后行为异常。

**理解**

HashMap 先按 `hashCode` 定位桶，再用 `equals` 在桶内比较。如果两个 `equals` 相等的对象 `hashCode` 不同，它们会散列到不同桶，HashMap 就找不到已经存在的 key，出现「明明 equals 相等却判重失败、get 取不到值」的问题。所以重写 equals 必须同步重写 hashCode。

**场景**

项目中把实体对象放进 HashSet 去重，或作为 HashMap 的 key 时，如果实体重写了 equals 没重写 hashCode，去重会失效。用 Lombok 的 `@EqualsAndHashCode` 或 IDE 生成，能保证两者一起重写。

**常见追问**

- 只重写 hashCode 不重写 equals 行吗？（不违反约定，但哈希碰撞时最终靠 equals 判断，可能仍判不相等，逻辑不一致）
- 重写 hashCode 的依据是什么？（equals 用到的字段都要参与 hashCode 计算）

**易错点**

「equals 相等 hashCode 必须相等」是约定不是自动实现的，只重写一个就会出问题，这是面试高频陷阱。

## 21. `equals()` 相同，`hashCode()` 一定相同吗？

**面试回答**

按照 Java 约定，一定相同。如果两个对象 equals 相等但 hashCode 不同，说明违背了约定，代码有 bug。

**理解**

这是 Java 规范强制要求的：equals 相等是 hashCode 相等的充分条件。正常实现下，equals 用到的字段都参与了 hashCode 计算，所以 equals 相等的两个对象，这些字段值相同，算出的 hashCode 必然相同。反过来不成立，见 [[02-Object与String#22. `hashCode()` 相同，`equals()` 一定相同吗？]]。

**场景**

重写实体的 equals 时，用相同的字段集合去实现 hashCode，就能保证这个约定。

**常见追问**

- 如果违反会怎样？（HashMap/HashSet 会出问题，见 [[02-Object与String#20. 为什么重写 `equals()` 通常要重写 `hashCode()`？]]）

**易错点**

这句话只在「正确重写」的前提下成立；如果代码写错了，equals 相等 hashCode 也可能不等。

## 22. `hashCode()` 相同，`equals()` 一定相同吗？

**面试回答**

不一定。hashCode 相同只能说明它们被散列到同一个位置，可能是哈希碰撞，两个对象内容不一定相等。

**理解**

hashCode 本质是把对象映射到一个 int，不同的对象完全可能算出相同的 hashCode（哈希碰撞），就像不同的东西可能映射到同一个编号。此时还需要用 equals 进一步判断是否真正相等。所以 hashCode 相同是 equals 相等的「必要不充分条件」。

**场景**

HashMap 的同一个桶里可能挂着一串 hashCode 相同但内容不同的对象，最终靠 equals 逐个比较来定位目标。

**常见追问**

- hashCode 不同，equals 一定不同吗？（按约定，是，因为 equals 相等 hashCode 必相等，逆否命题成立）

**易错点**

别把「hashCode 相同」当成「对象相等」，哈希碰撞是正常现象，最终要靠 equals 定论。

## 23. `hashCode()` 有什么作用？

**面试回答**

返回对象的哈希码，主要用于哈希表（HashMap、HashSet）里快速定位元素，把对象散列到对应的桶，减少 equals 比较的次数。

**理解**

如果没有 hashCode，HashMap 要把新 key 和所有已有 key 逐一 equals 比较，效率是 O(n)。有了 hashCode，先算出桶位置，只和同一桶里的少量元素比较，平均接近 O(1)。所以 hashCode 是「先粗筛、再精判」，大幅提升查找效率。

**场景**

HashMap 的 `put`/`get` 第一步就是算 key 的 hashCode 定位桶，这正是 hash 结构的核心（详见 [[05-HashMap]]）。

**常见追问**

- hashCode 是怎么算出来的？（默认和对象内存地址相关，重写后通常按字段计算）
- hashCode 返回 int，范围有限会冲突吗？（会，这就是哈希碰撞）

**易错点**

hashCode 不是「对象地址」，它只是一个按规则算出来的 int；默认实现和地址有关，但重写后就和地址无关了。

## 24. `toString()` 有什么作用？

**面试回答**

返回对象的字符串表示，默认是「类名@十六进制 hashCode」，重写后可以输出更有意义的字段信息，方便打印和日志排查。

**理解**

`toString` 属于 Object 方法，默认实现信息量很少。重写后打印对象、拼接字符串、记录日志时会自动调用它。很多框架（如 Lombok 的 `@Data`）会帮我们自动生成，把字段拼成可读字符串。日志里能快速看到对象内容，排查问题很有用。

**场景**

项目里给实体加 `@Data` 后，`log.info("订单信息: {}", order)` 能打印出订单各字段，而不是一坨看不懂的 `Order@1a2b3c`。

**常见追问**

- 默认 toString 长什么样？（类名@十六进制 hashCode）
- 什么时候会自动调用 toString？（println、字符串拼接、日志占位符）

**易错点**

打印对象时 Java 会自动调 toString，所以排查问题看不到字段时，先检查实体有没有重写 toString。

## 25. String 为什么是不可变的？

**面试回答**

String 底层用 `private final char[]`（JDK9 后是 byte[]）存字符，数组是 `final` 且不对外暴露修改方法，所有「修改」操作其实都返回一个新 String 对象，原对象不变。

**理解**

两个关键点：字段是 `final`，加上 String 类本身不提供任何能改数组内容的方法（`substring`、`replace` 等都是返回新对象）。`final` 保证引用不能指向新数组，private 和没有 setter 保证数组内容不被外部改。所以 String 一旦创建就不可变。

**场景**

项目里字符串常量、JSON key、配置项都依赖 String 不可变的特性，可以被放心共享。

**常见追问**

- String 真的是 final 数组吗？（JDK8 是 `char[]`，JDK9 优化成 `byte[]`，但都是 final 且不暴露）
- 反射能改 String 吗？（能，但属于非常规操作，正常场景不可变）

**易错点**

「修改」String 不是改原对象，而是生成新对象；说 String 不可变要落到「final 数组 + 无修改方法」上，别只说「final 修饰」。

## 26. String 不可变有什么好处？

**面试回答**

一是可以做字符串常量池，相同字符串复用节省内存；二是天然线程安全，多个线程共享不需要加锁；三是 hashCode 可以被缓存，作为 HashMap key 时查找快；四是安全性好，不容易被意外篡改。

**理解**

不可变意味着对象状态不变，所以可以放心共享和缓存。常量池复用让 `"abc"` 只存一份；线程安全让 String 在多线程环境无副作用；hashCode 只算一次就能缓存，作为 HashMap key 时性能好；在类加载、网络连接等场景，String 作为参数不会被中途改掉，更安全。

**场景**

项目里大量重复的字符串（如状态码字符串、Redis key 前缀）能复用常量池；String 作为 Redis key、Map key 都依赖它稳定可靠。

**常见追问**

- 不可变为什么线程安全？（对象状态不变，多个线程读到的永远一致）
- 不可变有没有缺点？（频繁拼接会产生大量临时对象，所以有 StringBuilder）

**易错点**

不可变的「线程安全」是相对的，指的是 String 本身状态不变，而不是说用 String 写的所有逻辑都线程安全。

## 27. String、StringBuilder、StringBuffer 有什么区别？

**面试回答**

String 不可变，每次修改生成新对象；StringBuilder 和 StringBuffer 可变，修改在原有对象上进行。StringBuffer 是线程安全的（方法加了 synchronized），StringBuilder 线程不安全但更快。

**理解**

三者的核心差别是「可变性」和「线程安全」。StringBuilder 和 StringBuffer 都维护一个可扩容的字符数组，append 时原地追加；区别是 StringBuffer 每个方法都加了 `synchronized`，多线程下安全但性能略低。日常单线程拼接用 StringBuilder 就够了。

**场景**

项目里在 for 循环拼 SQL 条件、拼 Redis key 时用 StringBuilder；StringBuffer 基本只在明确需要线程安全时用，实际很少见。

**常见追问**

- 三者的性能排序？（单线程拼接：StringBuilder > StringBuffer > String）
- StringBuffer 为什么线程安全？（方法加 synchronized）

**易错点**

StringBuilder 线程不安全不等于「不能用于多线程」，只是说并发修改同一实例会有问题；没有共享场景就放心用 StringBuilder。

## 28. 为什么循环拼接字符串推荐 StringBuilder？

**面试回答**

因为 String 不可变，循环里每次 `+` 拼接都会创建一个新对象，产生大量中间对象、频繁 GC，效率低；StringBuilder 在同一个字符数组上追加，只产生一个对象。

**理解**

`String s = s + "x"` 每次都是「新对象 = 旧内容 + x」，循环 N 次就产生 N 个中间 String，既浪费内存又拖慢速度。StringBuilder 内部数组容量不够时自动扩容，但整体只在末尾追加，不产生多余对象。所以循环拼接场景要显式用 StringBuilder。

**场景**

项目里批量生成 SQL 的 values、拼接口参数时，用 `StringBuilder sb = new StringBuilder(); for (...) sb.append(...);` 而不是在循环里用 `+`。

**常见追问**

- 那普通的 `+` 拼接就一定慢吗？（少量、非循环拼接编译器会优化成 StringBuilder，影响不大）
- `+` 在循环里为什么不能优化？（每次迭代都新建，编译器无法跨迭代复用）

**易错点**

「+ 一定慢」是绝对化说法；非循环的少量拼接，编译器已经优化，直接 `+` 没问题，重点是循环拼接。

## 29. `"abc"` 和 `new String("abc")` 有什么区别？

**面试回答**

`"abc"` 是字符串字面量，会去字符串常量池找，存在就复用，不存在就创建并放入常量池；`new String("abc")` 一定在堆上创建一个新对象，即使常量池已有 "abc" 也不复用。

**理解**

字面量方式先查常量池，命中直接返回池中对象，所以 `"abc" == "abc"` 是 true；`new String("abc")` 强制在堆上 new 新对象，所以 `"abc" == new String("abc")` 是 false。用 `intern()` 可以手动把 new 的对象放入常量池并返回池中引用。

**场景**

比较字符串内容一律用 `equals`，不要用 `==`，否则字面量和 new 出来的对象比较会得到意外结果。

**常见追问**

- `intern()` 是干什么的？（把字符串放入常量池，返回池中引用）
- 为什么字面量能复用？（常量池机制，见 [[02-Object与String#31. 什么是字符串常量池？]]）

**易错点**

`"abc" == new String("abc")` 是 false，因为一个在常量池、一个在堆；这类 `==` 比较题要看清是字面量还是 new。

## 30. `new String("abc")` 会创建几个对象？

**面试回答**

如果常量池里还没有 "abc"，会创建两个对象：一个在常量池（"abc" 字面量），一个在堆上（new 出来的 String）；如果常量池已有 "abc"，只创建一个对象（堆上的那个）。

**理解**

`new String("abc")` 里的字面量 "abc" 本身会触发常量池创建（若没有），然后 new 关键字又在堆上创建一个独立对象。所以第一个场景是 2 个，第二个场景是 1 个。（JDK7 后常量池也移到堆中，但「两个对象」这个结论不变，只是位置概念调整了。）

**场景**

这是经典的考察对象创建次数的题，本质是考常量池和 new 的区别，理解 [[02-Object与String#29. `"abc"` 和 `new String("abc")` 有什么区别？]] 就够。

**常见追问**

- 常量池没有 "abc" 时，两个对象分别在哪儿？（一个在常量池，一个在堆）
- `String s = "a" + "b"` 创建几个对象？（编译期常量折叠成 "ab"，只在常量池创建 1 个）

**易错点**

这个题的答案依赖「常量池是否已有」，不要张口就说固定是 2 个；要分情况回答。

## 31. 什么是字符串常量池？

**面试回答**

字符串常量池是 JVM 里专门存放字符串字面量的一块区域，用于复用字符串，相同内容的字符串只存一份，避免重复创建。

**理解**

当代码里出现 `"abc"` 字面量时，JVM 先查常量池，有就直接返回引用，没有才创建并放入。它的位置经历过变化：JDK7 之前常量池在方法区（永久代），JDK7 之后移到堆里，这样更方便被 GC 回收。它之所以能复用，前提就是 String 不可变（见 [[02-Object与String#25. String 为什么是不可变的？]]）。

**场景**

项目里大量重复的状态字符串、Redis key 前缀如果都走字面量，会复用常量池，节省内存。

**常见追问**

- 常量池在哪？（JDK7 前方法区，JDK7 后堆）
- 怎么主动把字符串放进常量池？（调 intern()）

**易错点**

常量池不是只存 String，还有 Class 常量池等概念，别混淆；这里说的是「字符串常量池」。

## 32. String 的 `equals()` 是怎么比较的？

**面试回答**

String 重写了 `equals`，先比较两个引用是否相同（`==`），相同直接返回 true；否则判断是不是 String 类型，再逐个字符比较内容是否一致。

**理解**

大致流程：先 `this == obj` 快速判断同一个对象；再判断 obj 是不是 String 的实例；然后把两个字符串转成字符数组，先比长度、再逐个字符比较，全部相同才返回 true。所以 String 的 equals 比较的是「内容」，而不是地址。

**场景**

判断两个字符串相等（如比较订单号、手机号）一律用 `equals`，不要用 `==`。

**常见追问**

- String 的 equals 和 == 区别？（equals 比内容，== 比地址）
- equals 是线程安全的吗？（String 不可变，equals 只读不写，安全）

**易错点**

`"abc".equals(str)` 比 `str.equals("abc")` 更安全，前者能避免 str 为 null 时的 NPE。

## 33. String 为什么适合作为 HashMap 的 Key？

**面试回答**

因为 String 不可变，hashCode 稳定且可以缓存，作为 key 时哈希值不会中途变化，能正确定位和查找；同时它重写了 equals 和 hashCode，能正确比较。

**理解**

HashMap 依赖 key 的 hashCode 定位桶。如果 key 可变，hashCode 会变，放进 Map 后就找不到原来的位置了。String 不可变，hashCode 只算一次并缓存，后续不会变，所以是最理想的 key。此外 String 的 equals/hashCode 实现符合规范（见 [[02-Object与String#20. 为什么重写 `equals()` 通常要重写 `hashCode()`？]]）。

**场景**

项目里用字符串做 Map 的 key（如状态码映射、Redis key），都依赖 String 这个特性；反过来，用可变对象当 key 会出 bug。

**常见追问**

- 用可变对象当 key 会怎样？（hashCode 变化，get 取不到值）
- String 的 hashCode 是缓存的吗？（是，第一次算完缓存起来）

**易错点**

String 适合当 key 的根本原因是「不可变 + hashCode 缓存 + 正确重写 equals/hashCode」，别只说「不可变」一个点。

## 34. StringBuilder 为什么比 String 频繁拼接效率高？

**面试回答**

String 每次拼接都创建新对象，频繁操作会产生大量临时对象、触发 GC；StringBuilder 内部是一个可扩容的字符数组，拼接就是在数组末尾追加，不产生中间对象。

**理解**

StringBuilder 内部维护一个 `char[]`（容量不足时自动扩容，一般翻倍），`append` 直接往数组里写，最后 `toString` 才生成一个 String 对象。所以 N 次拼接，String 是 O(N) 个对象，StringBuilder 基本是 1 个（不含扩容）。这是「可变 vs 不可变」在性能上的直接体现。

**场景**

循环拼接 SQL、拼 Redis key、生成日志摘要等场景都用 StringBuilder。

**常见追问**

- StringBuilder 扩容机制？（容量不足时扩容，通常按 2 倍增长）
- StringBuilder 比 StringBuffer 快在哪？（少了 synchronized 开销）

**易错点**

StringBuilder 优势体现在「频繁拼接」，单次拼接两者差别不大，别把结论绝对化。
