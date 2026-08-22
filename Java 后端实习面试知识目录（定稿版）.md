# P0：Java 基础

## 一、面向对象
1. Java 面向对象的三大特性是什么？
2. 封装、继承、多态分别是什么？
3. 什么是方法重载？什么是方法重写？
4. 重载和重写有什么区别？
5. 接口和抽象类有什么区别？
6. Java 为什么不支持类的多继承？
7. 一个类可以实现多个接口吗？
8. `this` 和 `super` 有什么区别？
9. `static` 修饰变量、方法分别有什么特点？
10. `final` 可以修饰哪些内容？分别有什么作用？
11. Java 是值传递还是引用传递？
12. 成员变量和局部变量有什么区别？
13. 基本数据类型和引用数据类型有什么区别？
14. Java 有哪些基本数据类型？
15. 自动装箱和拆箱是什么？
16. Integer 和 int 有什么区别？
17. Integer 缓存是什么？

## 二、Object
18. `==` 和 `equals()` 有什么区别？
19. Object 默认的 `equals()` 比较什么？
20. 为什么重写 `equals()` 通常要重写 `hashCode()`？
21. `equals()` 相同，`hashCode()` 一定相同吗？
22. `hashCode()` 相同，`equals()` 一定相同吗？
23. `hashCode()` 有什么作用？
24. `toString()` 有什么作用？

## 三、String
25. String 为什么是不可变的？
26. String 不可变有什么好处？
27. String、StringBuilder、StringBuffer 有什么区别？
28. 为什么循环拼接字符串推荐 StringBuilder？
29. `"abc"` 和 `new String("abc")` 有什么区别？
30. `new String("abc")` 会创建几个对象？
31. 什么是字符串常量池？
32. String 的 `equals()` 是怎么比较的？
33. String 为什么适合作为 HashMap 的 Key？
34. StringBuilder 为什么比 String 频繁拼接效率高？

## 四、泛型
35. Java 泛型是什么？
36. 为什么需要泛型？
37. 泛型有什么好处？
38. 泛型类、泛型方法分别是什么？
39. `<?>` 是什么意思？
40. `<? extends T>` 和 `<? super T>` 有什么区别？
41. 什么是泛型擦除？

## 五、集合基础
42. Java 常用集合有哪些？
43. List、Set、Map 有什么区别？
44. Collection 和 Collections 有什么区别？
45. ArrayList 和 LinkedList 有什么区别？
46. ArrayList 的底层数据结构是什么？
47. ArrayList 为什么随机访问快？
48. ArrayList 为什么中间插入、删除较慢？
49. ArrayList 容量不足时会发生什么？
50. ArrayList 是线程安全的吗？
51. LinkedList 的底层数据结构是什么？
52. LinkedList 插入一定比 ArrayList 快吗？
53. HashSet 为什么可以去重？
54. HashSet 底层是怎么实现的？
55. HashSet 和 HashMap 有什么关系？
56. Iterator 是什么？
57. Iterator 和普通 for 循环有什么区别？
58. 什么是 ConcurrentModificationException？
59. 为什么 foreach 遍历集合时修改集合可能报错？
60. Comparable 和 Comparator 有什么区别？

## 六、HashMap
61. HashMap 的底层数据结构是什么？
62. Java 8 中 HashMap 为什么使用数组 + 链表 + 红黑树？
63. HashMap 的 `put()` 流程是什么？
64. HashMap 的 `get()` 流程是什么？
65. 什么是 Hash 冲突？
66. HashMap 如何解决 Hash 冲突？
67. HashMap 为什么同时需要 `hashCode()` 和 `equals()`？
68. HashMap 默认初始容量是多少？
69. HashMap 默认负载因子是多少？
70. 为什么负载因子默认是 0.75？
71. HashMap 什么时候扩容？
72. HashMap 为什么把容量设计成 2 的幂？
73. HashMap 链表什么时候转换成红黑树？
74. 为什么链表过长后要转换成红黑树？
75. HashMap 为什么线程不安全？
76. HashMap 可以存 null Key 和 null Value 吗？
77. HashMap 和 Hashtable 有什么区别？
78. HashMap 和 ConcurrentHashMap 有什么区别？

## 七、异常
79. Java 异常体系是怎样的？
80. Error 和 Exception 有什么区别？
81. Checked Exception 和 RuntimeException 有什么区别？
82. `throw` 和 `throws` 有什么区别？
83. `try-catch-finally` 的执行顺序是什么？
84. finally 一定会执行吗？
85. finally 中存在 return 会怎样？
86. 如何自定义业务异常？
87. 项目中为什么通常要定义统一业务异常？

## 八、Java 8 常用特性
88. Lambda 表达式是什么？
89. 什么是函数式接口？
90. Stream 是什么？
91. Stream 和普通集合遍历有什么区别？
92. `filter()` 有什么作用？
93. `map()` 有什么作用？
94. `forEach()` 有什么作用？
95. Stream 会修改原集合吗？
96. Optional 是什么？解决什么问题？

# P0：Spring

## 九、Spring 基础
97. Spring 是什么？
98. Spring 最核心的两个特性是什么？
99. 什么是 IoC？
100. IoC 解决了什么问题？
101. 什么是 DI？
102. IoC 和 DI 有什么关系？
103. 什么是 Spring Bean？
104. Bean 是怎么交给 Spring 管理的？
105. `@Component`、`@Service`、`@Controller`、`@Repository` 有什么区别？
106. `@Autowired` 有什么作用？
107. 字段注入和构造器注入有什么区别？
108. `@Configuration` 有什么作用？
109. `@Bean` 有什么作用？
110. `@ComponentScan` 有什么作用？
111. `@Value` 有什么作用？
112. Spring Bean 默认是单例吗？
113. 单例 Bean 一定线程安全吗？
114. Spring Bean 有哪些常见作用域？
115. Spring Bean 生命周期大致是什么？

## 十、Spring Boot
116. Spring Boot 是什么？
117. Spring Boot 和 Spring 有什么关系？
118. Spring Boot 为什么能简化开发？
119. 什么是自动配置？
120. 什么是 Starter？
121. `@SpringBootApplication` 有什么作用？
122. `@SpringBootApplication` 包含哪些主要注解？
123. `application.yml` 和 `application.properties` 有什么作用？
124. Spring Boot 如何配置不同环境？
125. Spring Boot 内嵌 Tomcat 有什么作用？

## 十一、Spring MVC
126. Spring MVC 是什么？
127. 一个 HTTP 请求进入 Spring MVC 后经历哪些流程？
128. DispatcherServlet 有什么作用？
129. HandlerMapping 有什么作用？
130. Controller 是如何匹配到请求的？
131. `@Controller` 和 `@RestController` 有什么区别？
132. `@RequestMapping` 有什么作用？
133. `@GetMapping` 和 `@PostMapping` 有什么区别？
134. `@RequestParam` 和 `@PathVariable` 有什么区别？
135. `@RequestBody` 有什么作用？
136. Spring MVC 如何完成参数绑定？
137. Java 对象为什么可以自动转换成 JSON？
138. JSON 请求为什么可以转换成 Java 对象？
139. Spring MVC 如何处理返回值？
140. `Content-Type` 是什么？
141. `application/json` 是什么意思？

## 十二、参数校验
142. 为什么后端需要参数校验？
143. `@Valid` 有什么作用？
144. `@NotNull`、`@NotBlank`、`@NotEmpty` 有什么区别？
145. 参数校验失败后如何统一处理？
146. 为什么不能完全依赖前端校验？

## 十三、Filter 与 Interceptor
147. Filter 是什么？
148. Interceptor 是什么？
149. Filter 和 Interceptor 有什么区别？
150. `HandlerInterceptor` 有哪些主要方法？
151. `preHandle()` 在什么时候执行？
152. `postHandle()` 在什么时候执行？
153. `afterCompletion()` 在什么时候执行？
154. 为什么 JWT 登录校验适合放在拦截器？
155. 为什么登录接口必须放行？
156. Interceptor 如何获取请求头中的 Token？
157. 为什么管理端和用户端可以使用两个拦截器？

## 十四、AOP
158. 什么是 AOP？
159. AOP 解决什么问题？
160. 哪些场景适合使用 AOP？
161. 什么是横切关注点？
162. 什么是 JoinPoint？
163. 什么是 Pointcut？
164. 什么是 Advice？
165. 常见的通知类型有哪些？
166. 什么是 Aspect？
167. Spring AOP 底层大致如何实现？
168. JDK 动态代理和 CGLIB 有什么区别？
169. Spring 什么情况下使用 JDK 动态代理？
170. Spring 什么情况下使用 CGLIB？
171. 为什么 Spring 事务可以通过 AOP 实现？

## 十五、反射
172. Java 反射是什么？
173. 反射可以在运行时做什么？
174. 获取 Class 对象有哪些方式？
175. Method 对象是什么？
176. Field 对象是什么？
177. `Method.invoke()` 有什么作用？
178. 反射有什么优点？
179. 反射有什么缺点？
180. 项目的 AutoFill 为什么需要反射？
181. 为什么不直接调用实体类 setter？

## 十六、Spring 事务
182. 什么是数据库事务？
183. 事务的 ACID 四大特性是什么？
184. 什么是原子性？
185. 什么是一致性？
186. 什么是隔离性？
187. 什么是持久性？
188. `@Transactional` 有什么作用？
189. 什么是 Spring 声明式事务？
190. Spring 声明式事务大致是怎么实现的？
191. 为什么 `@Transactional` 通常加在 Service 层？
192. Spring 默认哪些异常会触发回滚？
193. Checked Exception 默认会回滚吗？
194. `rollbackFor` 有什么作用？
195. 把异常 catch 住为什么可能导致事务不回滚？
196. 同一个类内部调用另一个事务方法为什么可能失效？
197. private 方法上的 `@Transactional` 为什么通常不生效？
198. 什么是事务传播行为？
199. `Propagation.REQUIRED` 是什么意思？
200. 项目中为什么主表和子表写入需要放在同一个事务中？

# P0：MyBatis

## 十七、MyBatis
201. MyBatis 是什么？
202. MyBatis 和 JDBC 有什么关系？
203. Mapper 接口有什么作用？
204. Mapper 接口没有实现类为什么可以执行？
205. MyBatis Mapper 动态代理是什么？
206. MyBatis 注解方式和 XML 方式有什么区别？
207. `#{}` 和 `${}` 有什么区别？
208. 为什么 `#{}` 可以降低 SQL 注入风险？
209. `${}` 为什么存在 SQL 注入风险？
210. `${}` 一般在什么场景使用？
211. 什么是 MyBatis 动态 SQL？
212. `<if>` 有什么作用？
213. `<where>` 有什么作用？
214. `<set>` 有什么作用？
215. `<foreach>` 有什么作用？
216. 如何通过 `<foreach>` 实现批量插入？
217. 什么是主键回填？
218. MyBatis 如何获取 MySQL 自增主键？
219. 为什么项目中的子表插入需要主键回填？
220. 什么是 MyBatis 一级缓存？
221. 什么是 MyBatis 二级缓存？
222. 一级缓存和二级缓存有什么区别？
223. PageHelper 是什么？
224. PageHelper 大致如何实现分页？

# P0：MySQL

## 十八、SQL 基础
225. SQL 的执行顺序是什么？
226. `WHERE` 和 `HAVING` 有什么区别？
227. `GROUP BY` 有什么作用？
228. `ORDER BY` 有什么作用？
229. `LIMIT` 如何实现分页？
230. INNER JOIN 是什么？
231. LEFT JOIN 是什么？
232. INNER JOIN 和 LEFT JOIN 有什么区别？
233. 什么是子查询？
234. `COUNT(*)` 和 `COUNT(column)` 有什么区别？
235. `COUNT(*)` 和 `COUNT(1)` 有什么区别？
236. `DELETE`、`TRUNCATE`、`DROP` 有什么区别？
237. UNION 和 UNION ALL 有什么区别？
238. 深分页为什么可能比较慢？

## 十九、MySQL 表设计
239. 什么是主键？
240. 什么是唯一索引？
241. 主键和唯一索引有什么区别？
242. 为什么一张表通常需要主键？
243. 为什么很多业务表使用自增主键？
244. `char` 和 `varchar` 有什么区别？
245. NULL 和空字符串有什么区别？
246. 数据库三大范式是什么？
247. 为什么实际业务中有时会适当冗余字段？
248. 什么是反范式设计？

## 二十、MySQL 索引
249. 什么是数据库索引？
250. 索引为什么能提高查询速度？
251. 索引有什么缺点？
252. 索引是不是越多越好？
253. InnoDB 为什么使用 B+Tree？
254. 为什么不用普通二叉树？
255. 为什么不用 Hash 作为主要索引结构？
256. B+Tree 为什么能减少磁盘 IO？
257. B+Tree 为什么适合范围查询？
258. 什么是聚簇索引？
259. InnoDB 主键索引叶子节点保存什么？
260. 什么是二级索引？
261. 二级索引叶子节点保存什么？
262. 什么是回表？
263. 什么是覆盖索引？
264. 覆盖索引为什么可以提高查询效率？
265. 什么是联合索引？
266. 什么是最左匹配原则？
267. 联合索引 `(a,b,c)` 哪些查询可以使用索引？
268. 常见的索引失效场景有哪些？
269. `like '%xxx'` 为什么可能导致索引失效？
270. 对索引列使用函数为什么可能导致索引失效？
271. 隐式类型转换为什么可能导致索引失效？
272. 什么是 EXPLAIN？
273. EXPLAIN 中 `type` 表示什么？
274. EXPLAIN 中 `key` 表示什么？
275. EXPLAIN 中 `rows` 表示什么？
276. EXPLAIN 中 `Extra` 有哪些常见信息？

## 二十一、MySQL 事务
277. MySQL 有哪些事务隔离级别？
278. 什么是脏读？
279. 什么是不可重复读？
280. 什么是幻读？
281. READ COMMITTED 和 REPEATABLE READ 有什么区别？
282. InnoDB 默认事务隔离级别是什么？
283. 什么是 MVCC？
284. MVCC 主要解决什么问题？
285. MVCC 为什么能提高数据库并发性能？
286. 什么是 Read View？
287. 什么是 undo log？
288. undo log 有什么作用？
289. 什么是 redo log？
290. redo log 有什么作用？
291. 什么是 binlog？
292. redo log 和 binlog 有什么区别？

## 二十二、MySQL 锁
293. 为什么数据库需要锁？
294. 什么是共享锁？
295. 什么是排他锁？
296. 什么是行锁？
297. 什么是表锁？
298. 行锁和表锁有什么区别？
299. 什么是悲观锁？
300. 什么是乐观锁？
301. 乐观锁通常如何实现？
302. 什么是数据库死锁？
303. MySQL 为什么会产生死锁？
304. 如何降低死锁发生概率？

# P0：Redis

## 二十三、Redis 基础
305. Redis 是什么？
306. Redis 为什么适合做缓存？
307. Redis 为什么快？
308. Redis 是完全单线程的吗？
309. Redis 单线程为什么还能这么快？
310. 什么是 IO 多路复用？
311. Redis 常见的五种基本数据类型是什么？
312. String 适合哪些场景？
313. Hash 适合哪些场景？
314. List 适合哪些场景？
315. Set 适合哪些场景？
316. ZSet 适合哪些场景？
317. 什么是 TTL？
318. 为什么缓存通常要设置 TTL？
319. Redis 中 Key 应该如何设计？

## 二十四、Redis 过期与内存管理
320. Redis 中的数据过期后会立即删除吗？
321. Redis 有哪些过期删除策略？
322. 什么是惰性删除？
323. 什么是定期删除？
324. 为什么 Redis 不只使用一种删除策略？
325. Redis 内存满了怎么办？
326. 什么是内存淘汰策略？
327. Redis 有哪些常见的内存淘汰策略？
328. LRU 是什么？
329. LFU 是什么？

## 二十五、Redis 缓存
330. 什么是 Cache Aside 模式？
331. 查询 Redis + MySQL 的基本流程是什么？
332. 什么是 Cache Hit？
333. 什么是 Cache Miss？
334. Cache Miss 后为什么要把数据库数据写回 Redis？
335. 数据库数据发生修改后缓存怎么办？
336. 为什么通常删除缓存而不是更新缓存？
337. 为什么 Redis 和 MySQL 可能出现数据不一致？
338. 先更新数据库再删除缓存有什么问题？
339. 先删除缓存再更新数据库有什么问题？
340. 如何降低缓存和数据库不一致的概率？
341. 什么是延迟双删？
342. 什么是缓存预热？

## 二十六、缓存穿透、击穿、雪崩
343. 什么是缓存穿透？
344. 缓存穿透是如何产生的？
345. 缓存穿透为什么会给数据库造成压力？
346. 如何解决缓存穿透？
347. 缓存空值如何解决缓存穿透？
348. 什么是布隆过滤器？
349. 布隆过滤器为什么存在误判？
350. 什么是缓存击穿？
351. 缓存击穿通常发生在什么场景？
352. 什么是热点 Key？
353. 如何解决缓存击穿？
354. 互斥锁如何解决缓存击穿？
355. 什么是逻辑过期？
356. 什么是缓存雪崩？
357. 缓存雪崩通常是怎么产生的？
358. 如何解决缓存雪崩？
359. TTL 加随机值有什么作用？
360. 缓存穿透、击穿、雪崩有什么区别？

## 二十七、RedisTemplate 与 Spring Cache
361. RedisTemplate 是什么？
362. RedisTemplate 如何操作 Redis？
363. RedisTemplate 中的序列化是什么？
364. Spring Cache 是什么？
365. Spring Cache 本身是不是 Redis？
366. Spring Cache 和 Redis 是什么关系？
367. `@Cacheable` 有什么作用？
368. `@CacheEvict` 有什么作用？
369. `@CachePut` 有什么作用？
370. Spring Cache 如何指定缓存 Key？
371. RedisTemplate 和 Spring Cache 有什么区别？
372. 为什么项目中同时使用 RedisTemplate 和 Spring Cache？
373. 项目中数据修改后如何清理对应缓存？

## 二十八、Redis 持久化
374. Redis 为什么需要持久化？
375. RDB 是什么？
376. AOF 是什么？
377. RDB 和 AOF 有什么区别？
378. RDB 有什么优缺点？
379. AOF 有什么优缺点？
380. Redis 重启后如何恢复数据？

# P0：Web 与认证

## 二十九、Cookie、Session、JWT
381. Cookie 是什么？
382. Session 是什么？
383. Cookie 和 Session 有什么区别？
384. Token 是什么？
385. JWT 是什么？
386. JWT 由哪三个部分组成？
387. Header 中通常保存什么？
388. Payload 中通常保存什么？
389. Signature 有什么作用？
390. JWT 为什么可以实现无状态认证？
391. JWT 中的数据是加密的吗？
392. 为什么 JWT 中不能存密码等敏感信息？
393. JWT 被修改以后服务端怎么发现？
394. JWT 如何判断是否过期？
395. JWT 和 Session 有什么区别？
396. JWT 有什么优点？
397. JWT 有什么缺点？
398. 如何让 JWT 主动失效？
399. 项目中用户登录后的 JWT 完整流程是什么？

## 三十、ThreadLocal
400. ThreadLocal 是什么？
401. ThreadLocal 解决什么问题？
402. 为什么项目中用 ThreadLocal 保存 userId / empId？
403. 为什么不直接从 Controller 一直传 userId？
404. ThreadLocal 的 `set()`、`get()`、`remove()` 分别做什么？
405. ThreadLocal 如何实现线程之间的数据隔离？
406. ThreadLocal 是线程安全工具吗？
407. 为什么 ThreadLocal 使用完需要 `remove()`？
408. Tomcat 线程池为什么会产生 ThreadLocal 数据残留风险？
409. ThreadLocal 为什么可能造成内存泄漏？
410. 多个用户请求会不会读取到彼此的 userId？

## 三十一、HTTP
411. HTTP 是什么？
412. HTTP 请求由哪些部分组成？
413. HTTP 响应由哪些部分组成？
414. HTTP Header 是什么？
415. HTTP Body 是什么？
416. GET 和 POST 有什么区别？
417. PUT 和 POST 有什么区别？
418. PUT 和 PATCH 有什么区别？
419. 什么是 HTTP 方法幂等？
420. 哪些 HTTP 方法通常具有幂等性？
421. HTTP 为什么是无状态协议？
422. 200 表示什么？
423. 400 表示什么？
424. 401 和 403 有什么区别？
425. 404 表示什么？
426. 500 表示什么？
427. HTTP 和 HTTPS 有什么区别？
428. HTTPS 为什么更安全？

# P0：项目业务

## 三十二、统一响应与全局异常处理
429. 为什么后端需要统一响应结构？
430. 统一响应体一般包含哪些字段？
431. 什么是全局异常处理？
432. `@RestControllerAdvice` 有什么作用？
433. `@ExceptionHandler` 有什么作用？
434. `@ControllerAdvice` 和 `@RestControllerAdvice` 有什么区别？
435. 为什么不在每个 Controller 里写 try-catch？
436. 什么是业务异常？
437. 数据库异常为什么不应该直接返回前端？
438. 唯一约束异常如何转换成友好提示？

## 三十三、订单与关联数据
439. 为什么订单表和订单明细表要拆开？
440. 什么是一对多关系？
441. 为什么新增主表后再新增子表？
442. 为什么需要先拿到主表 ID？
443. 主键回填在关联数据写入中有什么作用？
444. 为什么子表数据适合批量插入？
445. 批量插入相比循环单条插入有什么优势？
446. 为什么主表和子表必须放在同一事务中？
447. 为什么订单不能只保存 addressBookId？
448. 什么是订单地址快照？
449. 为什么地址快照属于合理的数据冗余？
450. 数据冗余一定是不好的设计吗？
451. 为什么历史订单不能跟随地址簿变化？

## 三十四、第三方支付
452. 支付宝 Precreate 是什么？
453. Precreate 为什么适合扫码支付？
454. 支付二维码是怎么得到的？
455. 用户扫码支付后的完整流程是什么？
456. 什么是支付宝异步通知？
457. 为什么不能只相信前端返回的支付成功？
458. 为什么支付结果需要服务端确认？
459. 什么是 RSA 验签？
460. 为什么支付回调必须验签？
461. 如果不验签会有什么风险？
462. `out_trade_no` 是什么？
463. 商户订单号和支付宝交易号有什么区别？
464. 什么是接口幂等？
465. 为什么支付回调必须保证幂等？
466. 支付宝为什么可能重复发送回调？
467. 项目中如何保证支付回调幂等？
468. 为什么更新订单前先检查支付状态？
469. `TRADE_SUCCESS` 是什么意思？
470. `TRADE_FINISHED` 是什么意思？
471. 支付成功但本地订单状态更新失败怎么办？

# P1：JVM

## 三十五、JVM 基础
472. JVM 是什么？
473. JDK、JRE、JVM 有什么区别？
474. JVM 运行时内存区域有哪些？
475. 哪些区域是线程私有的？
476. 哪些区域是线程共享的？
477. Java 堆中主要存放什么？
478. Java 栈中主要存放什么？
479. 堆和栈有什么区别？
480. 程序计数器有什么作用？
481. 方法区和元空间是什么？
482. `new` 一个 Java 对象大致经历什么过程？
483. 什么情况下可能发生 StackOverflowError？
484. 什么情况下可能发生 OutOfMemoryError？

## 三十六、GC 与类加载
485. GC 是什么？
486. 为什么 Java 需要 GC？
487. 如何判断一个对象是否可以被回收？
488. 什么是可达性分析？
489. 什么是强引用、软引用、弱引用？
490. 什么是类加载？
491. Java 类加载过程有哪些阶段？
492. 什么是双亲委派机制？
493. 为什么需要双亲委派？

# P1：Java 并发基础

## 三十七、线程基础
494. 什么是进程？
495. 什么是线程？
496. 进程和线程有什么区别？
497. Java 创建线程有哪些常见方式？
498. `start()` 和 `run()` 有什么区别？
499. Java 线程有哪些状态？
500. `sleep()` 和 `wait()` 有什么区别？
501. 什么是线程上下文切换？
502. 什么叫线程安全？
503. 为什么会出现线程安全问题？

## 三十八、锁与线程池
504. `synchronized` 是什么？
505. `synchronized` 可以锁什么？
506. `volatile` 是什么？
507. `volatile` 能保证原子性吗？
508. `synchronized` 和 `volatile` 有什么区别？
509. 什么是死锁？
510. 死锁产生的四个必要条件是什么？
511. 什么是线程池？
512. 为什么要使用线程池？
513. 线程池相比频繁创建线程有什么优势？
514. ThreadPoolExecutor 有哪些核心参数？
515. corePoolSize 是什么？
516. maximumPoolSize 是什么？
517. workQueue 是什么？
518. 拒绝策略是什么？
519. 常见拒绝策略有哪些？
520. Tomcat 为什么使用线程池处理请求？
521. ConcurrentHashMap 和 HashMap 有什么区别？
522. Java 8 ConcurrentHashMap 大致如何保证线程安全？

# P1：计算机网络

## 三十九、TCP 与网络
523. TCP 和 UDP 有什么区别？
524. TCP 为什么是可靠协议？
525. TCP 三次握手过程是什么？
526. 为什么 TCP 建立连接需要三次握手？
527. TCP 四次挥手过程是什么？
528. 为什么关闭连接通常需要四次挥手？
529. 什么是 TIME_WAIT？
530. DNS 是什么？
531. 浏览器输入 URL 后大致发生了什么？

# P1：Java Web 开发常识

## 四十、DTO、VO、Entity
532. Entity 是什么？
533. DTO 是什么？
534. VO 是什么？
535. DTO、VO、Entity 有什么区别？
536. 为什么不建议直接把 Entity 返回给前端？
537. 为什么需要参数校验？
538. 分页接口通常需要哪些参数？
539. 什么是接口幂等？
540. 哪些接口需要考虑幂等？
541. 重复提交订单可能产生什么问题？

## 四十一、日志
542. Java 项目为什么需要日志？
543. 常见日志级别有哪些？
544. DEBUG、INFO、WARN、ERROR 有什么区别？
545. SLF4J 是什么？
546. Logback 是什么？
547. SLF4J 和 Logback 是什么关系？
548. 为什么生产环境不推荐使用 `System.out.println()`？
549. 如何通过日志排查接口异常？

# P1：开发工具

## 四十二、Git
550. Git 的基本提交流程是什么？
551. `git add` 是做什么的？
552. `git commit` 是做什么的？
553. `git push` 是做什么的？
554. `git pull` 是做什么的？
555. `git fetch` 和 `git pull` 有什么区别？
556. Git 分支有什么作用？
557. `merge` 是什么？
558. Git 冲突是什么？
559. 遇到代码冲突一般怎么处理？
560. `git reset` 和 `git revert` 有什么区别？

## 四十三、Maven
561. Maven 是什么？
562. Maven 解决什么问题？
563. `pom.xml` 是什么？
564. dependency 是什么？
565. Maven 本地仓库是什么？
566. Maven 的依赖是怎么下载的？
567. Maven 常见生命周期有哪些？
568. `clean` 是做什么的？
569. `package` 是做什么的？
570. `install` 是做什么的？
571. 什么是 Maven 依赖冲突？

## 四十四、Linux
572. `ls` 有什么作用？
573. `cd` 有什么作用？
574. `pwd` 有什么作用？
575. 如何查看文件内容？
576. 如何实时查看日志？
577. 如何搜索日志中的关键字？
578. 如何查看当前运行的 Java 进程？
579. 如何查看端口占用？
580. 如何结束一个进程？
581. `chmod` 是什么？
582. Linux 文件权限分别表示什么？

# P2：了解即可

## 四十五、Redis 进阶
583. Redis 主从复制是什么？
584. 为什么需要主从复制？
585. Redis Sentinel 是什么？
586. Redis Cluster 是什么？
587. 什么是 Redis 分布式锁？
588. 为什么 `SETNX` 可以实现简单分布式锁？
589. 简单的 `SETNX` 分布式锁存在哪些问题？
590. Redisson 是什么？

## 四十六、Java 并发进阶
591. CAS 是什么？
592. CAS 有什么问题？
593. AQS 是什么？
594. ReentrantLock 是什么？
595. synchronized 和 ReentrantLock 有什么区别？
596. 什么是 Java 内存模型 JMM？
597. 什么是可见性？
598. 什么是原子性？
599. 什么是有序性？

## 四十七、MySQL 进阶
600. 什么是 Gap Lock？
601. 什么是 Next-Key Lock？
602. MySQL 如何处理幻读？
603. 什么是索引下推？
604. 什么是 Buffer Pool？
605. 什么是两阶段提交？

## 四十八、中间件与分布式基础
606. 什么是消息队列？
607. 为什么需要消息队列？
608. 消息队列可以解决哪些问题？
609. Kafka 是什么？
610. RabbitMQ 是什么？
611. 什么是 RPC？
612. Dubbo 是什么？
613. 什么是微服务？
614. Spring Cloud 是什么？
615. Nacos 是什么？
616. 什么是服务注册与发现？
617. 什么是限流？
618. 什么是熔断？
619. 什么是分布式事务？
620. CAP 理论是什么？

## 四十九、部署基础
621. Docker 是什么？
622. Docker 解决什么问题？
623. 镜像和容器有什么区别？
624. Nginx 是什么？
625. Nginx 常见用途有哪些？
626. 什么是反向代理？
627. 什么是负载均衡？

# 独立准备：算法与手撕代码

## 五十、Java 算法常用 API
628. ArrayList 常用方法有哪些？
629. HashMap 常用方法有哪些？
630. HashSet 常用方法有哪些？
631. Deque 常用方法有哪些？
632. PriorityQueue 如何使用？
633. Arrays 常用方法有哪些？
634. Collections 常用方法有哪些？
635. StringBuilder 常用方法有哪些？
636. Java 如何自定义排序？

## 五十一、算法基础
637. 数组常见题型有哪些？
638. 链表常见题型有哪些？
639. 栈和队列常见题型有哪些？
640. Hash 表常见题型有哪些？
641. 二分查找的基本写法是什么？
642. 双指针常见场景有哪些？
643. 滑动窗口常见场景有哪些？
644. BFS 的基本写法是什么？
645. DFS 的基本写法是什么？
646. 回溯的基本模板是什么？
647. 二叉树常见遍历方式有哪些？
648. 堆通常解决什么问题？
649. 动态规划的基本思路是什么？