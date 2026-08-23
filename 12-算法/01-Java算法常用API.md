---
category: 算法
priority: P1
status: 未学习
tags:
  - Java后端
  - 面试
  - 算法
---

# Java算法常用API

## 628. ArrayList 常用方法有哪些？

**面试回答**

高频方法有 `add(e)`、`add(i,e)`、`get(i)`、`set(i,e)`、`remove(i)`、`remove(Object)`、`size()`、`isEmpty()`、`contains`、`subList` 和遍历。算法题常把它作为可变长度、支持下标访问的结果容器。

**原理与理解**

ArrayList 是可扩容数组实现。随机 `get/set` 通常为 O(1)，尾部追加摊销 O(1)，中间插入删除因移动元素通常 O(n)。`remove(1)` 对 `List<Integer>` 调用的是按下标删除，删除值 1 要写 `remove(Integer.valueOf(1))`。

**成立条件与边界**

复杂度是 ArrayList 的典型实现性质，不是所有 List 都相同。`subList` 是原列表的视图，结构性修改可能互相影响；遍历时直接结构修改可能触发 fail-fast，需用 Iterator 的约定操作。

**实际场景（算法题）**

收集树遍历结果用 `List<Integer> ans = new ArrayList<>()`；已知结果规模时可预设容量，减少扩容但不改变逻辑复杂度。

**常见追问**

- `set` 与 `add` 区别？——set 替换已有下标，add 插入或追加并改变大小。
- 删除 Integer 值为什么容易错？——`remove(int)` 与 `remove(Object)` 重载会优先匹配基本类型下标。
- ArrayList 能存 null 吗？——可以，除非业务另行限制。

**易错点**

不要把“List 按下标都是 O(1)”推广到 LinkedList，也不要在增强 for 中直接 remove。

## 629. HashMap 常用方法有哪些？

**面试回答**

常用 `put`、`get`、`getOrDefault`、`containsKey`、`remove`、`putIfAbsent`、`computeIfAbsent`、`merge`、`keySet`、`values` 和 `entrySet`。算法题中常用于频次、值到下标映射与状态记忆。

**原理与理解**

HashMap 基于键的 `hashCode/equals` 定位映射，get/put 在哈希分布良好时期望 O(1)。遍历键值对优先 `entrySet`；计数可写 `map.merge(x, 1, Integer::sum)` 或 `put(x, getOrDefault(x,0)+1)`。

**成立条件与边界**

`get(k)==null` 无法区分“键不存在”和“键存在但值为 null”，需用 containsKey。HashMap 不保证遍历顺序且非线程安全；可变对象作为键时若参与 hash/equals 的字段变化，后续可能无法正确查找。

**实际场景（算法题）**

两数之和在扫描到 nums[i] 时先查 `target-nums[i]` 是否已存在，再写入当前值到下标，避免同一元素被使用两次。

**常见追问**

- `put` 返回什么？——该键之前关联的值，原来没有通常返回 null。
- `computeIfAbsent` 适合什么？——按键惰性创建集合或缓存值，但映射函数应避免修改同一 Map。
- 平均 O(1) 是否绝对？——不是，碰撞、扩容和键实现都会影响。

**易错点**

不要通过 `map.get(k) != null` 判断键存在，也不要依赖 HashMap 遍历顺序。

## 630. HashSet 常用方法有哪些？

**面试回答**

常用 `add`、`contains`、`remove`、`size`、`isEmpty`、`clear`，以及 `addAll`、`retainAll`、`removeAll` 等集合运算。它适合去重和快速存在性判断。

**原理与理解**

HashSet 基于 HashMap，只保存元素作为键；`add(e)` 在此前不存在时返回 true。操作在哈希分布良好时期望 O(1)，元素相等性由 hashCode 与 equals 契约决定。

**成立条件与边界**

HashSet 不保证遍历顺序，允许一个 null，且非线程安全。若元素放入后修改了参与 hashCode/equals 的字段，contains/remove 可能失效；集合运算的复杂度还取决于两个集合大小和实现。

**实际场景（算法题）**

最长连续序列先把所有数放入 HashSet，只从不存在 `x-1` 的数开始向后扩展，避免对每个数重复扫描。

**常见追问**

- add 重复元素会怎样？——集合不变并返回 false。
- 需要插入顺序怎么办？——使用 LinkedHashSet；需要排序则评估 TreeSet。
- 为什么对象要同时正确实现 equals 和 hashCode？——相等对象必须落在兼容的哈希定位逻辑中。

**易错点**

“Set 无序”应理解为 HashSet 没有遍历顺序保证，不是每次输出必然随机。

## 631. Deque 常用方法有哪些？

**面试回答**

Deque 支持两端操作：`offerFirst/offerLast` 入队，`pollFirst/pollLast` 取出，`peekFirst/peekLast` 查看。作为栈可用 `push/pop/peek`，作为 FIFO 队列常用 `offerLast/pollFirst/peekFirst`；算法题通常以 ArrayDeque 实现。

**原理与理解**

每类操作有两组方法：`add/remove/get` 失败时抛异常，`offer/poll/peek` 失败时返回 false 或 null。ArrayDeque 不允许 null，因此 poll/peek 返回 null 可明确表示为空。

**成立条件与边界**

Deque 是接口，复杂度取决于实现；ArrayDeque 非线程安全，也没有固定容量语义。不要混用首尾约定，否则单调队列或 BFS 会出现方向错误。

**实际场景（算法题）**

滑动窗口最大值把下标从队尾维护为对应值单调递减，队首始终是当前窗口最大值下标；出窗口从队首删，新元素从队尾压制较小值。

**常见追问**

- 为什么推荐 ArrayDeque 代替 Stack？——API 同时支持栈/队列，且不继承 Vector 的旧设计。
- Queue 语义如何写？——offerLast、pollFirst、peekFirst。
- ArrayDeque 能放 null 吗？——不能。

**易错点**

`peek` 只查看不删除，`poll` 查看并删除；栈与队列的同一端/不同端约定要统一。

## 632. PriorityQueue 如何使用？

**面试回答**

PriorityQueue 是基于优先级堆的无界优先队列。默认按自然顺序让最小元素位于队首；`offer` 插入、`peek` 查看队首、`poll` 删除并返回队首。构造时传 Comparator 可定义优先级。

**原理与理解**

`offer/poll` 通常 O(log n)，`peek` O(1)，但按对象搜索或删除通常 O(n)。最大堆可用 `new PriorityQueue<>(Comparator.reverseOrder())`；比较整数应使用 `Integer.compare(a,b)`，避免 `a-b` 溢出。

**成立条件与边界**

PriorityQueue 不允许 null，非线程安全，迭代器也不保证按优先级排序；只有连续 poll 才按队列顺序取出。元素进入后若影响比较结果的字段变化，会破坏堆的不变量。

**实际场景（算法题）**

求最大 K 个数维护容量 K 的最小堆：元素入堆后若 size>K 就 poll，最终堆内是 K 个最大值，复杂度 O(n log k)。

**常见追问**

- 默认队首是最大还是最小？——按自然顺序是最小。
- 如何按对象字段建堆？——传 `Comparator.comparingInt(Node::weight)` 等比较器。
- 遍历 PriorityQueue 是否有序？——不保证。

**易错点**

不要用 `(a,b) -> b-a` 比较极端整数，也不要把堆内数组误认为完整排序结果。

## 633. Arrays 常用方法有哪些？

**面试回答**

Arrays 提供数组工具：`sort`、`parallelSort`、`binarySearch`、`fill`、`copyOf/copyOfRange`、`equals/deepEquals`、`toString/deepToString`、`asList` 和 `stream`。做题最常用排序、填充、复制和二分。

**原理与理解**

基本类型数组可直接 `Arrays.sort(int[])`；对象数组可传 Comparator。`binarySearch` 要求区间已按同一顺序排序，未找到时返回负值，插入点为 `-result-1`。

**成立条件与边界**

`Arrays.asList(T...)` 返回大小固定且由原数组支持的 List，可 set 但不能 add/remove；`Arrays.asList(new int[]{1,2})` 得到的是只含一个 `int[]` 的 List，而不是两个 Integer。对象排序的稳定性与基本类型排序实现也不同，不应依赖非契约细节。

**实际场景（算法题）**

把区间对象数组按起点排序用 `Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]))`；对 primitive 数组只需自然排序时直接 sort。

**常见追问**

- binarySearch 未找到返回 -1 吗？——不一定，返回 `-(insertion point)-1`。
- asList 能增删吗？——不能改变大小。
- 打印二维数组用什么？——`Arrays.deepToString`。

**易错点**

二分查找前必须按相同 Comparator 排好序；primitive 数组不能直接使用对象 Comparator 重载。

## 634. Collections 常用方法有哪些？

**面试回答**

Collections 是集合工具类，常用 `sort`、`binarySearch`、`reverse`、`rotate`、`shuffle`、`swap`、`min/max`、`frequency`、`fill`，以及 unmodifiable/synchronized 等包装方法。现代代码也可直接调用 `list.sort`。

**原理与理解**

排序和二分要求元素有自然顺序或提供同一 Comparator。`reverse` 原地修改列表，`shuffle` 打乱列表，`min/max` 按比较规则选极值；这些方法通常作用于传入集合而非返回新集合。

**成立条件与边界**

`Collections.unmodifiableList` 是不可修改视图，不代表底层列表不再变化；`synchronizedList` 也要求按文档在遍历期间手工同步。`binarySearch` 对未按相同顺序排序的列表结果未定义。

**实际场景（算法题）**

先 `list.sort(cmp)`，再用 `Collections.binarySearch(list, key, cmp)`；若只是反转输出，可根据是否允许修改原列表决定原地 reverse 或创建副本。

**常见追问**

- Collections 与 Collection 区别？——前者是工具类，后者是集合根接口之一。
- shuffle 能用于安全随机吗？——默认随机源不面向密码学用途。
- unmodifiable 是否等于 immutable？——不是，底层仍可能被其他引用修改。

**易错点**

很多方法会原地修改传入 List，做题前要确认是否允许破坏原顺序。

## 635. StringBuilder 常用方法有哪些？

**面试回答**

常用 `append`、`insert`、`delete/deleteCharAt`、`replace`、`reverse`、`charAt/setCharAt`、`length/setLength`、`substring` 和 `toString`。它是可变字符序列，适合循环拼接、就地修改与构造答案。

**原理与理解**

append/insert 会扩充内部存储并返回当前 builder，便于链式调用；toString 生成 String 快照。频繁循环使用 `s = s + part` 会产生许多中间结果，复用 StringBuilder 更容易控制总成本。

**成立条件与边界**

StringBuilder 非线程安全；共享并发修改需外部同步或重新设计所有权。单条简单的字符串 `+` 表达式通常会被编译器优化，不必机械替换；真正需要关注的是循环或大量动态拼接。索引按 UTF-16 char；reverse 会处理有效代理对，但不保证按用户感知的字素簇反转组合字符或 emoji 序列。

**实际场景（算法题）**

生成路径字符串时把进入递归前的长度保存为 oldLen，返回后 `setLength(oldLen)` 一次撤销本轮追加，比逐字符 delete 更清晰。

**常见追问**

- StringBuilder 与 StringBuffer？——前者不做同步，单线程通常优先；后者方法带同步语义。
- `substring` 返回什么？——String，而不是共享的 StringBuilder。
- reverse 能否等价处理所有“字符”？——不能直接等同按字素簇反转，题目若涉及组合字符或 emoji 序列需明确单位。

**易错点**

不要在多个线程无保护共享 StringBuilder，也不要忘记最终返回通常需要 `toString()`。

## 636. Java 如何自定义排序？

**面试回答**

Comparable 由类型实现 `compareTo` 定义自然顺序；Comparator 是外部排序策略，可传给 sort、PriorityQueue、TreeMap 等。推荐用 `Comparator.comparingInt`、`comparing`、`thenComparing` 和 `reversed` 组合规则。

**原理与理解**

比较结果小于、等于、大于 0 分别表示前者小于、等于、大于后者。比较器应满足反对称、传递和一致的零关系，否则排序可能报错或有不可预测结果。

**成立条件与边界**

不要用 `a-b`、`b-a` 比较整数，可能溢出；使用 `Integer.compare`。自然顺序与 equals 最好一致，否则 TreeSet/TreeMap 可能把 compare==0 的不同对象当作同一键，而 HashSet 仍依据 equals/hashCode。

**实际场景（算法题）**

区间先按左端点升序、再按右端点降序：`Comparator.<int[]>comparingInt(a -> a[0]).thenComparing((a,b) -> Integer.compare(b[1],a[1]))`。

**常见追问**

- Comparable 与 Comparator 区别？——自然顺序属于类型，Comparator 是可替换的外部策略。
- 多字段如何排序？——主比较器后接 thenComparing。
- null 如何处理？——显式使用 `Comparator.nullsFirst/nullsLast` 包装可处理 null 的规则。

**易错点**

“返回正数就交换”只是部分排序实现的直觉，接口契约是相对顺序；比较器不能随调用改变规则。
