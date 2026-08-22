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

常用：add（添加）、get（按下标取）、set（按下标改）、remove（删除）、size（大小）、isEmpty（判空）、contains（是否包含）、indexOf（找下标）、clear（清空）。

**理解**

ArrayList 是动态数组，按下标操作快（get/set O(1)），中间插入删除慢（要移动元素 O(n)）。算法题里常用它存结果、做线性遍历。常用方法：add(e) 末尾加、add(i,e) 指定位置插、get(i)、set(i,e)、remove(i)/remove(o)、size()、contains(o)、indexOf(o)。

**场景**

算法题里用 `List<Integer> list = new ArrayList<>()` 存遍历结果，用 get(i) 按下标访问、add 追加。

**常见追问**

- 按下标取元素？（get(i)）
- 它底层是什么？（动态数组）

**易错点**

ArrayList 按下标 get/set 快，中间插入删除慢（数组特性）；别和 LinkedList 混。

## 629. HashMap 常用方法有哪些？

**面试回答**

常用：put（存键值对）、get（按键取值）、containsKey（是否含键）、remove（删除）、size、isEmpty、keySet（所有键）、values（所有值）、entrySet（所有键值对）。

**理解**

HashMap 是哈希表，put/get 平均 O(1)，用于「按键快速查找」。算法题里常用于统计频率、存映射、去重判断。常用：put(k,v)、get(k)（不存在返回 null）、getOrDefault(k,默认值)、containsKey(k)、remove(k)、size()。遍历用 keySet 或 entrySet。

**场景**

算法题「两数之和」用 HashMap 存「值→下标」，O(1) 查找补数；「统计字符频率」用 HashMap 计数。

**常见追问**

- 取不到值时返回什么？（null，可用 getOrDefault 给默认）
- 遍历用？（keySet 或 entrySet）

**易错点**

HashMap 的 get 不存在返回 null（别和 put 的旧值混淆）；getOrDefault 是高频好用方法。

## 630. HashSet 常用方法有哪些？

**面试回答**

常用：add（添加）、remove（删除）、contains（是否包含）、size、isEmpty、clear，以及 addAll、removeAll 等集合运算。

**理解**

HashSet 是「不允许重复元素」的集合，基于 HashMap 实现，add/contains 平均 O(1)。算法题里核心用途是「去重」和「快速判断元素是否存在」。常用：add(e)（已存在返回 false）、contains(e)、remove(e)、size()。

**场景**

算法题「判断链表是否有环/重复元素」用 HashSet 记录访问过的元素，contains 快速查重。

**常见追问**

- HashSet 特点？（元素不重复）
- 判断存在用？（contains）

**易错点**

HashSet 核心是「去重 + O(1) 查存在」；add 已存在元素会返回 false 且不加入。

## 631. Deque 常用方法有哪些？

**面试回答**

Deque 是双端队列，两端都能进出。常用：addFirst/offerFirst（头部加）、addLast/offerLast（尾部加）、removeFirst/pollFirst（头部取）、removeLast/pollLast（尾部取）、peekFirst/peekLast（看头尾）。可当栈用，也可当队列用。

**理解**

Deque 是「双端队列」接口，ArrayDeque 是常用实现。算法题里它很万能：当栈用（push/pop 或 addFirst/removeFirst）、当队列用（addLast/removeFirst）、当双端队列用。offer/poll/peek 系列在失败时返回特殊值（不抛异常），remove/add 系列失败抛异常，做题常用 offer/poll/peek。

**场景**

算法题「用栈实现队列」「滑动窗口最大值」都用 Deque；Java 里替代 Stack 用 `Deque<Integer> stack = new ArrayDeque<>()`。

**常见追问**

- 双端队列是什么？（两端都能进出）
- 当栈用什么方法？（push/pop，或 addFirst/removeFirst）

**易错点**

Deque 既能当栈又能当队列；Java 推荐用 ArrayDeque 代替老旧的 Stack（Stack 基于 Vector、性能差）。

## 632. PriorityQueue 如何使用？

**面试回答**

PriorityQueue 是优先队列（堆），元素按优先级自动排序，默认是最小堆（队头是最小元素）；用 add/offer 入队、poll 取出并移除队头、peek 只看队头。可传 Comparator 自定义优先级。

**理解**

PriorityQueue 底层是二叉堆，队头是「优先级最高」的元素，默认自然顺序（最小堆，poll 出最小值）。构建大顶堆可传 `(a,b) -> b-a` 或 `Comparator.reverseOrder()`。算法题常用于「Top K」问题（找最大/最小 K 个）、合并 K 个有序链表、求中位数等。

**场景**

算法题「求最大的 K 个元素」用小顶堆：维护大小为 K 的优先队列，遍历时把大的留下，最后堆里就是 Top K。

**常见追问**

- 默认是什么堆？（最小堆，队头最小）
- 怎么变最大堆？（传 Comparator.reverseOrder() 或 (a,b)->b-a）

**易错点**

PriorityQueue 默认「最小堆」（poll 出最小），要最大堆得传反向 Comparator；别默认以为队头最大。

## 633. Arrays 常用方法有哪些？

**面试回答**

常用：sort（排序）、binarySearch（二分查找）、fill（填充）、copyOf（复制）、equals（比较）、toString（转字符串）、asList（转 List）。

**理解**

Arrays 是操作数组的工具类，算法题高频用 sort 和 asList。sort 对数组排序（可传 Comparator）；binarySearch 在「已排序」数组里二分查找；fill 全部填充某值；copyOf 复制数组；toString 打印数组（直接打印数组是地址，要用这个）；asList 把数组转成 List（注意返回的是定长 List，不能增删）。

**场景**

算法题里 `Arrays.sort(nums)` 排序，`Arrays.toString(arr)` 打印数组调试，`Arrays.fill(arr, 0)` 初始化。

**常见追问**

- 数组排序用？（Arrays.sort）
- 怎么打印数组？（Arrays.toString）

**易错点**

Arrays.asList 返回的 List 不能增删（定长）；打印数组用 toString，直接 print 数组是地址。

## 634. Collections 常用方法有哪些？

**面试回答**

常用：sort（对 List 排序）、reverse（反转）、max/min（最大最小）、shuffle（打乱）、swap（交换）、binarySearch（二分）、frequency（出现次数）。

**理解**

Collections 是操作「集合（Collection）」的工具类，和 Arrays 对应。sort 对 List 排序（可传 Comparator）；reverse 反转；max/min 求极值；shuffle 随机打乱；frequency 统计某元素出现次数。算法题常用 sort、reverse、max/min。

**场景**

算法题里 `Collections.sort(list)` 对 List 排序、`Collections.reverse(list)` 反转、`Collections.max(list)` 求最大。

**常见追问**

- 对 List 排序用？（Collections.sort）
- 和 Arrays 区别？（Collections 管集合，Arrays 管数组）

**易错点**

Collections 操作「集合」、Arrays 操作「数组」，别混；对 List 排序用 Collections.sort。

## 635. StringBuilder 常用方法有哪些？

**面试回答**

常用：append（追加）、insert（插入）、delete/deleteCharAt（删除）、reverse（反转）、toString（转 String）、charAt、length、setCharAt。

**理解**

StringBuilder 是可变的字符串，频繁拼接字符串时用它避免 String 拼接产生大量中间对象（String 是不可变的）。算法题里常用来拼接结果、反转字符串、构建字符串。常用：append(str)、insert(i,str)、reverse()、deleteCharAt(i)、toString()。

**场景**

算法题拼接结果字符串用 StringBuilder，反转字符串用 `sb.reverse()`，比 String 反复拼接高效。

**常见追问**

- 为什么用 StringBuilder？（可变，拼接高效）
- 反转字符串？（reverse）

**易错点**

频繁拼接用 StringBuilder 而不是 String（String 不可变、拼接产生大量对象）；它是「可变字符串」。

## 636. Java 如何自定义排序？

**面试回答**

两种方式：①实现 Comparable 接口（重写 compareTo，定义对象的自然顺序）；②用 Comparator 比较器（重写 compare，在 sort 时传入），Comparator 更灵活，算法题更常用。

**理解**

Comparable：让类自己实现 compareTo，定义「默认怎么比」，类内部定死一种顺序。Comparator：外部传一个比较器，定义「这次怎么比」，可以在不同场景用不同规则，不侵入原类。算法题常用 `Arrays.sort(arr, (a,b) -> a-b)` 或 `Collections.sort(list, Comparator)`，用 Lambda 写比较规则。

**场景**

算法题里 `Arrays.sort(intervals, (a,b) -> a[0]-b[0])` 按区间起点排序；对自定义对象排序用 Comparator 指定规则。

**常见追问**

- 两种方式？（Comparable 内部实现、Comparator 外部比较器）
- 算法题常用哪种？（Comparator + Lambda）

**易错点**

Comparable 是「类自己比」、Comparator 是「外部指定规则」；Lambda `(a,b)->a-b` 是升序，`b-a` 是降序，别记反。
