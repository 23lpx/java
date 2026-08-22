---
category: Redis
priority: P0
status: 未学习
tags:
  - Java后端
  - 面试
  - Redis
---

# RedisTemplate与SpringCache

## 361. RedisTemplate 是什么？

**面试回答**

RedisTemplate 是 Spring Data Redis 提供的操作 Redis 的模板类，封装了对 Redis 各种数据类型的操作方法，让 Java 代码能方便地读写 Redis。

**理解**

它屏蔽了 Redis 底层连接的细节，提供 `opsForValue`（String）、`opsForHash`（Hash）、`opsForList`、`opsForSet`、`opsForZSet` 等操作入口，配合序列化器把 Java 对象和 Redis 里的数据互相转换。是 Java 操作 Redis 最常用的工具。

**场景**

项目里用 RedisTemplate 手动读写缓存、存验证码、实现分布式锁等。

**常见追问**

- RedisTemplate 怎么操作不同数据类型？（opsForValue/opsForHash 等）
- 和 Jedis/Lettuce 什么关系？（RedisTemplate 底层用这些客户端连接 Redis）

**易错点**

RedisTemplate 是「操作模板/封装」，不是 Redis 本身；它需要配置序列化器，否则可能存成难读的二进制。

## 362. RedisTemplate 如何操作 Redis？

**面试回答**

通过注入 RedisTemplate，调用 `opsForValue()`、`opsForHash()` 等方法获取对应类型的操作对象，再调用 set/get/hget 等方法读写数据。

**理解**

典型用法：`redisTemplate.opsForValue().set(key, value, ttl, TimeUnit.SECONDS)` 存 String，`redisTemplate.opsForValue().get(key)` 取；Hash 用 `opsForHash().put/get`；列表、集合、有序集合同理。它把 Redis 命令映射成 Java 方法调用。

**场景**

项目里 `redisTemplate.opsForValue().set("dish:info:" + id, dish, 30, TimeUnit.MINUTES)` 存菜品缓存，get 取缓存。

**常见追问**

- 存带 TTL 的数据怎么做？（set(key, value, timeout, TimeUnit)）
- 序列化不配置会怎样？（可能存成 JDK 序列化的二进制，可读性差）

**易错点**

RedisTemplate 通过「opsForXxx() 取操作对象再调方法」来操作；注意序列化配置，否则数据难读、跨语言不友好。

## 363. RedisTemplate 中的序列化是什么？

**面试回答**

序列化是指把 Java 对象和 Redis 里存储的字节数据互相转换的规则，RedisTemplate 通过配置 Serializer 决定 key、value 以什么格式存储。

**理解**

Redis 存的是二进制，Java 对象要存进去必须先序列化成字节，取出来再反序列化。常见序列化器：JDK 序列化（默认，但可读性差、占空间）、StringRedisSerializer（字符串）、GenericJackson2JsonRedisSerializer / Jackson2JsonRedisSerializer（JSON，可读性好）。项目通常用 JSON 序列化。

**场景**

项目里给 RedisTemplate 配置 JSON 序列化器，让缓存里存的是可读的 JSON，而不是 JDK 二进制。

**常见追问**

- 默认序列化是什么？（JDK 序列化，可读性差）
- 为什么改用 JSON 序列化？（可读、跨语言、省空间）

**易错点**

序列化是「对象 ↔ 字节」的转换规则；默认 JDK 序列化可读性差，生产常配 JSON 序列化，这是面试易问点。

## 364. Spring Cache 是什么？

**面试回答**

Spring Cache 是 Spring 提供的一套缓存抽象（注解 + 接口），用 @Cacheable、@CacheEvict、@CachePut 等注解声明缓存行为，具体用哪个缓存（Redis、本地缓存等）由底层实现决定。

**理解**

Spring Cache 定义的是「缓存的标准接口和注解」，不是具体缓存。它把「哪些方法要缓存、什么时候清缓存」用注解声明出来，底层通过 CacheManager 对接真正的缓存产品（Redis、Caffeine、ConcurrentMap 等）。好处是「与具体缓存解耦」，换缓存实现不改业务代码。

**场景**

项目里在 Service 方法上加 @Cacheable 缓存菜品，底层 CacheManager 用的是 Redis 实现。

**常见追问**

- Spring Cache 是缓存产品吗？（不是，是缓存抽象，见 [[05-Redis/05-RedisTemplate与SpringCache#365. Spring Cache 本身是不是 Redis？]]）
- 它靠什么对接具体缓存？（CacheManager）

**易错点**

Spring Cache 是「缓存抽象/规范」，不是「具体缓存」；它本身不做缓存，靠 CacheManager 接真正的缓存产品。

## 365. Spring Cache 本身是不是 Redis？

**面试回答**

不是。Spring Cache 是缓存抽象层，只提供注解和接口，本身不是任何具体缓存；Redis 是它「可以选择对接」的一种缓存实现。

**理解**

Spring Cache 不绑定 Redis，你可以让它对接 Redis、本地 Caffeine、甚至内存 Map。它只定义「缓存怎么做」（@Cacheable 等注解），「缓存放哪」由你配置的 CacheManager 决定。所以「Spring Cache = Redis」是误解，准确说是「Spring Cache + Redis 实现」的组合。

**场景**

项目里 Spring Cache 的底层实现配置成了 Redis（用 RedisCacheManager），但换个实现（如本地缓存）注解代码都不用改。

**常见追问**

- Spring Cache 能对接哪些缓存？（Redis、Caffeine、Ehcache、ConcurrentMap 等）
- 怎么决定用哪个缓存？（配置对应的 CacheManager）

**易错点**

这是必须纠正的常见错误：Spring Cache 是「抽象」，Redis 是「实现」，两者不是一回事。

## 366. Spring Cache 和 Redis 是什么关系？

**面试回答**

Spring Cache 是缓存抽象，Redis 是具体的缓存实现；Spring Cache 定义「怎么用缓存」（注解和接口），Redis 通过实现 CacheManager 接口作为「实际存储」被接入。

**理解**

关系类似「接口」和「实现」：Spring Cache 提供统一 API（Cache、CacheManager 接口 + 注解），Redis 是这个 API 的一个实现（RedisCacheManager + RedisCache）。业务代码面向 Spring Cache 注解编程，底层具体是 Redis 还是别的，由配置决定，实现了缓存技术与业务解耦。

**场景**

项目里业务代码用 Spring Cache 注解，底层接 Redis 做实际存储；若将来换本地缓存，只改配置不改代码。

**常见追问**

- 谁实现谁？（Redis 实现 Spring Cache 的 CacheManager 接口）
- 解耦体现在哪？（换缓存实现不用改业务代码）

**易错点**

Spring Cache 与 Redis 是「抽象与实现」的关系，不是「同一个东西」，更不是「两级缓存」。

## 367. `@Cacheable` 有什么作用？

**面试回答**

@Cacheable 用在方法上，表示「先查缓存，命中直接返回，未命中才执行方法并把结果写入缓存」，常用于读操作。

**理解**

执行被 @Cacheable 标注的方法前，Spring Cache 先按 key 查缓存：命中就跳过方法体直接返回缓存值；未命中才真正执行方法，把返回值按配置存入缓存。它让「缓存读」变成注解声明，不用手写 if-else 查缓存逻辑。

**场景**

项目里查询菜品的方法加 @Cacheable，第一次查库并缓存，后续直接命中缓存。

**常见追问**

- 命中缓存会执行方法吗？（不会，直接返回缓存）
- key 怎么定？（默认按参数，可自定义，见 [[05-Redis/05-RedisTemplate与SpringCache#370. Spring Cache 如何指定缓存 Key？]]）

**易错点**

@Cacheable 的核心是「先查缓存，命中则不执行方法」；它针对「读」场景，写场景要用 @CacheEvict/@CachePut。

## 368. `@CacheEvict` 有什么作用？

**面试回答**

@CacheEvict 用在方法上，表示方法执行后删除指定缓存，常用于数据更新、删除后清掉对应缓存，保证缓存不过期存旧值。

**理解**

数据变更后，相关缓存要失效。@CacheEvict 在方法执行后（或 beforeInvocation 时）删除指定 key 或整个缓存，让下次读取重新加载最新数据。它对应「更新库后删缓存」的写场景。

**场景**

项目里修改菜品的方法加 @CacheEvict，删除对应菜品缓存，下次查询重新加载最新数据。

**常见追问**

- @CacheEvict 删什么？（指定 key，或 allEntries=true 清整个缓存）
- 和 @Cacheable 什么关系？（一个写时删、一个读时存，配合使用）

**易错点**

@CacheEvict 是「写后删缓存」，对应「更新库 + 删缓存」模式；allEntries=true 能清空整个缓存。

## 369. `@CachePut` 有什么作用？

**面试回答**

@CachePut 用在方法上，表示「无论如何都执行方法，并把返回值更新到缓存」，用于既执行方法又同步更新缓存的场景。

**理解**

和 @Cacheable 不同：@Cacheable 命中缓存就不执行方法，@CachePut 总是执行方法、然后用返回值刷新缓存。它适合「既要完成操作、又要让缓存立刻更新」的场景，常用于更新操作后主动更新缓存（而非删除）。

**场景**

项目里更新菜品的方法若想「更新库后同步更新缓存」，可用 @CachePut，但实际更常用 @CacheEvict 删缓存。

**常见追问**

- @CachePut 和 @Cacheable 区别？（CachePut 总是执行并更新缓存，Cacheable 命中就不执行）
- 为什么项目更常用 @CacheEvict？（删缓存更简单、避免并发覆盖）

**易错点**

@CachePut 是「总是执行 + 刷新缓存」，和 @Cacheable 的「命中就不执行」相反，别搞混。

## 370. Spring Cache 如何指定缓存 Key？

**面试回答**

用 @Cacheable 等的 key 属性指定，支持 SpEL 表达式，如 `key = "#id"`、`key = "#dish.id"`，也可以用 keyGenerator 自定义生成规则。

**理解**

默认 key 是基于方法参数的某种规则生成，可能不够精确或易冲突。用 key 属性 + SpEL 能明确指定：`#参数名` 引用参数、`#p0`/`#a0` 引用第一个参数、`#result` 引用返回值（@CachePut）。也可以用 keyGenerator 统一生成。

**场景**

项目里缓存菜品用 `@Cacheable(key = "#id")`，按菜品 id 作为缓存 key。

**常见追问**

- key 属性用什么表达式？（SpEL）
- 复杂 key 怎么做？（key = "#a + ':' + #b" 拼接，或自定义 keyGenerator）

**易错点**

指定 key 用 SpEL，注意 `#参数名` 的写法；key 设计不好会导致缓存冲突或失效。

## 371. RedisTemplate 和 Spring Cache 有什么区别？

**面试回答**

RedisTemplate 是「手动操作 Redis」的工具类，代码里显式写 set/get，灵活可控但代码量大；Spring Cache 是「声明式缓存抽象」，用注解自动缓存，简洁但与具体缓存解耦，灵活性稍弱。

**理解**

RedisTemplate 面向「具体 Redis」，你精确控制每一步（key、value、TTL、序列化），适合复杂缓存逻辑（如分布式锁、验证码、精细控制）；Spring Cache 面向「抽象缓存」，用注解声明「缓存/清缓存」，由框架自动处理，适合简单、标准的缓存场景（如方法结果缓存）。两者不冲突，可搭配使用。

**场景**

项目里简单的方法级缓存用 Spring Cache 注解，需要精细控制（锁、验证码、自定义过期）用 RedisTemplate。

**常见追问**

- 谁更灵活？（RedisTemplate 更灵活，精细控制）
- 谁更简洁？（Spring Cache 注解更简洁）

**易错点**

RedisTemplate「手动、精细、绑 Redis」vs Spring Cache「声明、自动、抽象」；两者是「工具」和「抽象层」的区别，不是同类竞争关系。

## 372. 为什么项目中同时使用 RedisTemplate 和 Spring Cache？

**面试回答**

因为两者定位不同、各有所长：Spring Cache 注解适合「简单的方法级缓存」，写起来简洁；RedisTemplate 适合「需要精细控制」的场景（自定义 key/TTL、分布式锁、验证码等）。配合使用能兼顾简洁和灵活。

**理解**

Spring Cache 是「声明式」，一个注解搞定方法缓存，但粒度粗、不易做复杂逻辑；RedisTemplate 是「命令式」，能做任意精细操作，但每个缓存都要手写。实际项目里：常规查询缓存用 Spring Cache 省事；验证码、分布式锁、特殊 TTL、复杂数据结构用 RedisTemplate 精确控制。两者互补，不是二选一。

**场景**

项目里菜品/套餐的简单查询缓存用 Spring Cache 注解；验证码、分布式锁等用 RedisTemplate 手动实现。

**常见追问**

- 什么用 Spring Cache？（简单、标准的方法级缓存）
- 什么用 RedisTemplate？（需要精细控制 TTL/锁/结构的场景）

**易错点**

同时用两者不是「做了两级缓存」，而是「不同场景用不同工具」；Spring Cache 和 RedisTemplate 最终都可能操作同一个 Redis，别理解成两层缓存。

## 373. 项目中数据修改后如何清理对应缓存？

**面试回答**

数据修改后，用 @CacheEvict 注解删除对应缓存 key（或整个缓存），或手动用 RedisTemplate 删除相关 key，让缓存失效、下次读时重新加载。

**理解**

清理缓存的关键是「改数据 → 让相关缓存失效」。用 Spring Cache 就在写方法上加 @CacheEvict 指定 key；用 RedisTemplate 就显式 delete 相关 key。要注意「删干净」——一个数据可能对应多个缓存 key（如列表缓存和详情缓存），都要清理，否则部分缓存还是旧值。

**场景**

项目里修改菜品后，用 @CacheEvict 删除该菜品详情缓存，同时手动清理包含该菜品的列表缓存，保证都失效。

**常见追问**

- 列表缓存和详情缓存都要删吗？（是，避免部分旧值残留）
- 删失败怎么办？（配合 TTL 兜底）

**易错点**

清理缓存要「删全」：一个数据可能有多处缓存（列表、详情），漏删会导致部分旧数据；TTL 是最后兜底。
