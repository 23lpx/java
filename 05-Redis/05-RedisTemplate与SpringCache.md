---
category: Redis
priority: P0
status: 未学习
verified: 已校验
reviewed_at: 2026-08-22
version_scope:
  - Spring Framework 5.3+ 缓存抽象（默认代理模式）
  - Spring Data Redis 2.7+（RedisTemplate / RedisCache）
tags:
  - Java后端
  - 面试
  - Redis
---

# RedisTemplate与SpringCache

## 361. RedisTemplate 是什么？

**面试回答**

`RedisTemplate<K, V>` 是 Spring Data Redis 提供的命令式 Redis 操作模板。它通过 `RedisConnectionFactory` 获取连接，统一处理连接生命周期、异常转换和序列化，并按 Redis 数据类型提供类型化的操作接口。

**原理与理解**

常用入口包括 `opsForValue()`、`opsForHash()`、`opsForList()`、`opsForSet()` 和 `opsForZSet()`。配置完成后的模板可以在线程间复用；底层驱动可由 Lettuce 或 Jedis 等连接器提供，但应用通常面向 Spring Data Redis API，而不是直接依赖驱动 API。

**成立条件与边界**

模板封装不等于命令自动具备事务性。单条 Redis 命令通常原子，多条操作若要求整体原子，需要结合 Lua、Redis 事务或重新设计数据模型；序列化、超时、拓扑和驱动能力也仍要正确配置。

**实际场景（真实项目边界）**

简历能够确认项目使用了 `RedisTemplate`，但不能据此声称具体存过验证码、实现过分布式锁或采用了某个 Key/TTL；这些细节必须由源码和配置核验。

**常见追问**

- `RedisTemplate` 与 Lettuce/Jedis 是什么关系？（前者是 Spring 操作抽象，后者是可由连接工厂适配的底层驱动）
- 它配置好后能作为单例复用吗？（可以，模板会为操作获取和管理连接）

**易错点**

不要把 `RedisTemplate` 说成 Redis 客户端协议的唯一实现，也不要把“模板线程安全”误解为任意多步业务逻辑都是线程安全或原子的。

## 362. RedisTemplate 如何操作 Redis？

**面试回答**

先注入带明确泛型和序列化配置的 `RedisTemplate`，再通过 `opsForXxx()` 获取对应数据结构的操作对象。例如 String Value 使用 `opsForValue().get/set`，Hash 使用 `opsForHash().get/put`，通用 Key 操作用模板自身的 `delete`、`expire` 等方法。

**原理与理解**

一次调用通常经历“Java 参数序列化 → 连接工厂提供连接 → 执行 Redis 命令 → 结果反序列化与异常转换”。带 TTL 的 Value 可在写入时使用 `set(key, value, timeout)` 一次完成；批量往返可评估 pipeline，需要原子脚本时可通过 `execute` 调用 Lua。

**成立条件与边界**

方法名只是对 Redis 能力的映射，最终支持范围取决于 Spring Data Redis 版本、Redis 服务端和驱动。pipeline 主要减少网络往返，不保证事务原子性；先 `set` 再单独 `expire` 还可能在中间失败而留下无过期 Key。

**实际场景（项目核验项）**

项目可检查 `opsForValue`、`opsForHash`、`delete` 和脚本调用的真实使用位置，再记录实际 Key、TTL 和序列化器；不能直接沿用“菜品缓存 30 分钟”之类示例作为项目事实。

**常见追问**

- 如何一次写入 Value 和 TTL？（使用带超时参数的 `set` 重载）
- pipeline 与事务有什么区别？（pipeline 优化往返，事务/Lua处理原子语义）

**易错点**

不要把 `opsForValue()` 简单等同于只处理 Java `String`；它对应 Redis String/Value 操作，Java 类型由模板泛型和序列化器决定。

## 363. RedisTemplate 中的序列化是什么？

**面试回答**

序列化决定 Java 对象如何转换为 Redis 命令使用的字节，以及读取时如何还原。`RedisTemplate` 可以分别配置 Key、Value、Hash Key 和 Hash Value 的序列化器，读写双方必须使用兼容规则。

**原理与理解**

未覆盖默认配置的 `RedisTemplate` 多数操作使用 Java 原生序列化；`StringRedisTemplate` 的 Key 和 Value 使用 `StringRedisSerializer`。工程中也常配置 JSON，但需要明确类型信息、日期格式、字段演进和未知字段策略。

**成立条件与边界**

JSON 不天然保证更省空间，也不自动保证跨语言兼容；类型元数据可能增加体积，模型变更也可能导致旧数据无法反序列化。Java 原生反序列化不应处理不可信数据，历史数据切换格式时还需要迁移或兼容读取方案。

**实际场景（项目核验项）**

简历不能证明项目使用了 JSON 序列化。应检查 `RedisTemplate` Bean、`RedisCacheConfiguration` 和线上 Key 的真实编码，并确认手写操作与 Spring Cache 是否使用兼容的 Key/Value 格式。

**常见追问**

- 为什么 Redis 中会看到不可读的 Key 或 Value？（可能使用了 JDK 等二进制序列化）
- 更换序列化器有什么风险？（存量数据不兼容、类型恢复失败和 Key 命名变化）

**易错点**

不要只替换 Value 序列化器却忽略 Key、Hash Key 和 Hash Value，也不要把“可读 JSON”直接等同于安全、紧凑和无版本兼容问题。

## 364. Spring Cache 是什么？

**面试回答**

Spring Cache 是面向方法调用的缓存抽象，核心接口是 `Cache` 和 `CacheManager`，并提供 `@Cacheable`、`@CachePut`、`@CacheEvict` 等声明式注解。它定义缓存行为，但需要实际缓存实现负责存储。

**原理与理解**

启用缓存支持后，Spring 通常通过 AOP 代理拦截方法调用，根据缓存名和 Key 查找、写入或淘汰条目。业务代码可以少写重复的 Cache Aside 样板，但缓存的 TTL、序列化、集群一致性和并发能力仍由具体实现及配置决定。

**成立条件与边界**

注解并非写上就一定生效：需要启用缓存基础设施，并让调用经过代理。默认代理模式下，同类自调用不会被拦截，通常只应标注可被代理的公共方法；缓存抽象也不会自动处理多线程、多进程的一致性。

**实际场景（真实项目边界）**

简历能够确认项目使用了 Spring Cache，但具体缓存了哪些方法、是否由 Redis 承载、是否配置 TTL，都需要结合注解和 `CacheManager` 配置核验。

**常见追问**

- Spring Cache 是缓存产品吗？（不是，是缓存抽象，见 [[05-Redis/05-RedisTemplate与SpringCache#365. Spring Cache 本身是不是 Redis？]]）
- 为什么同类内部调用可能不生效？（默认代理模式只拦截经过代理的外部调用）

**易错点**

不要把“声明式”理解成框架自动解决缓存一致性、击穿和故障降级；这些仍是应用与缓存实现需要承担的设计问题。

## 365. Spring Cache 本身是不是 Redis？

**面试回答**

不是。Spring Cache 是 Spring Framework 的缓存抽象，Redis 是可作为后端存储的一种产品。使用 Spring Data Redis 时，通常由 `RedisCacheManager` 和 `RedisCache` 把该抽象适配到 Redis。

**原理与理解**

`CacheManager` 根据缓存名返回一个 `Cache`，具体实现再完成 `get`、`put`、`evict` 等操作。后端也可以是 Caffeine、JCache 或基于内存的实现，因此同一套注解不必绑定 Redis。

**成立条件与边界**

“面向抽象”不代表更换后端只改一行配置。不同实现对 TTL、空值、并发加载、事务感知、Key 转换和集群传播的能力不同，迁移时仍要重新验证语义与数据格式。

**实际场景（通用工程）**

若配置的是 `RedisCacheManager`，注解缓存通常落到 Redis；单元测试也可能替换为内存实现。判断实际后端应看容器中的 `CacheManager`，不能只看 `@Cacheable`。

**常见追问**

- 谁负责实际存储？（当前 `CacheManager` 创建的 `Cache` 实现）
- Spring Cache 可以使用本地缓存吗？（可以，但多实例间的数据传播语义需要另行处理）

**易错点**

不要说“Redis 实现了 Spring 的接口”；更准确的是 Spring Data Redis 提供 `RedisCacheManager`、`RedisCache` 适配 Redis。

## 366. Spring Cache 和 Redis 是什么关系？

**面试回答**

两者是“缓存抽象与一种后端适配”的关系：Spring Cache 规定应用如何声明和访问缓存，Spring Data Redis 则可以用 `RedisCacheManager` 将这些操作映射到 Redis。

**原理与理解**

以 Redis 为后端时，缓存名、方法 Key 和前缀共同决定 Redis Key，返回值按 `RedisCacheConfiguration` 序列化。默认配置与手写 `RedisTemplate` 未必相同，因此即使访问同一 Redis，也不一定能直接互读条目。

**成立条件与边界**

Spring Data Redis 当前默认的 `RedisCacheConfiguration` 会启用缓存名前缀、允许缓存空值且不设置过期时间，但 Spring Boot 或项目配置可以覆盖这些默认值。面试回答应以项目实际 `CacheManager` 配置为准。

**实际场景（项目核验项）**

核验项目时需要找到 `RedisCacheManager` 或 Boot 缓存配置，确认缓存名、前缀、TTL、空值和序列化策略；只看到 Redis 依赖不能证明 Spring Cache 正在使用 Redis。

**常见追问**

- Spring Cache 的 Key 为什么在 Redis 中带前缀？（RedisCache 默认通常以缓存名分区并加前缀）
- Spring Cache 与 RedisTemplate 是两级缓存吗？（不是，它们可能是访问同一 Redis 的不同入口）

**易错点**

不要把文档默认值当成 Spring Boot 或当前项目最终配置，自动配置与自定义 Bean 都可能改变行为。

## 367. `@Cacheable` 有什么作用？

**面试回答**

`@Cacheable` 表示先按缓存名和 Key 查询：命中时返回缓存值并跳过目标方法；未命中时执行方法，再按条件将正常返回结果写入缓存，适合结果可复用的读取方法。

**原理与理解**

它本质上是代理拦截的 get-if-absent-then-load。默认情况下，多个并发 miss 可能同时执行方法；可用 `sync = true` 请求底层缓存对同一 Key 的加载进行同步，但具体能力和范围由缓存实现决定，不能直接等同于业务分布式锁。

**成立条件与边界**

同一输入应能得到可复用的结果，并设计合理 TTL 和失效规则。默认代理模式下自调用不生效；`condition` 在调用前判断是否参与缓存，`unless` 在结果产生后决定是否拒绝写入。

**实际场景（项目核验项）**

可检查项目查询方法是否真实使用 `@Cacheable`、缓存名和 Key 表达式是什么，以及空结果是否缓存；不能仅凭“用了 Spring Cache”就声称菜品查询一定采用了该注解。

**常见追问**

- 命中缓存会执行方法吗？（通常不会，直接返回缓存结果）
- Key 怎么确定？（默认按参数生成，也可自定义，见 [[05-Redis/05-RedisTemplate与SpringCache#370. Spring Cache 如何指定缓存 Key？]]）

**易错点**

不要认为 `@Cacheable` 默认就能防止缓存击穿；Spring 缓存抽象本身不对所有并发和多进程场景提供统一加锁语义。

## 368. `@CacheEvict` 有什么作用？

**面试回答**

`@CacheEvict` 用方法调用触发缓存淘汰，可以删除指定 Key，也可以用 `allEntries = true` 清理整个缓存区域。默认在方法正常完成后淘汰；`beforeInvocation = true` 则在方法执行前淘汰。

**原理与理解**

默认后置淘汰把缓存删除与方法成功返回关联，方法抛异常时通常不删除；前置淘汰不依赖方法结果，即使后续失败也已经清理。清理整个区域时指定的 `key` 会被忽略，范围和成本必须谨慎评估。

**成立条件与边界**

“方法正常返回后”不必然等于“数据库事务已经成功提交”。若要求缓存操作在事务提交后执行，需要核验事务与缓存切面的顺序，或使用事务感知的缓存管理配置；它仍不能让数据库与 Redis 形成原子事务。

**实际场景（项目核验项）**

数据修改方法可以按依赖关系淘汰详情或列表缓存，但项目究竟使用 `@CacheEvict`、手动删除还是清空整个缓存，需要从源码确认，不能直接补成既有实现。

**常见追问**

- `beforeInvocation` 有什么差别？（前者执行方法前就删除，默认则只在正常完成后删除）
- `allEntries = true` 时 Key 是否有意义？（没有，整个缓存区域都会被清理）

**易错点**

不要说 `@CacheEvict` 能“保证绝不读到旧值”；并发读写、事务提交时机、删除失败和其他缓存入口都可能造成短暂不一致。

## 369. `@CachePut` 有什么作用？

**面试回答**

`@CachePut` 不用缓存命中跳过方法，而是始终执行目标方法，并把正常返回结果写入指定缓存，适合业务执行完成后主动刷新缓存内容。

**原理与理解**

它和 `@Cacheable` 的控制流相反：前者强制调用并 put，后者可能直接返回缓存。`@CachePut` 的 Key 可以在允许的位置引用 `#result`，但缓存 Key 必须与读取端一致，否则更新的是另一个条目。

**成立条件与边界**

Spring 官方通常不建议在同一方法同时使用 `@CachePut` 与 `@Cacheable`，因为一个要求执行、一个可能跳过，容易产生冲突。缓存写入也不与数据库更新天然原子，事务回滚、写缓存失败和并发旧值覆盖仍需设计。

**实际场景（通用工程）**

若更新方法能返回读取端所需的完整对象，可评估 `@CachePut`；若对象依赖多表重新组装或并发覆盖风险高，更新数据库后淘汰缓存通常更容易控制。

**常见追问**

- 与 `@Cacheable` 的核心区别是什么？（`@CachePut` 总执行方法，`@Cacheable` 命中时跳过）
- 为什么写入后仍可能不一致？（数据库与缓存没有天然的跨系统原子提交）

**易错点**

不要把 `@CachePut` 理解成“修改现有缓存但不执行方法”，也不要在返回值不是完整缓存对象时直接覆盖读取缓存。

## 370. Spring Cache 如何指定缓存 Key？

**面试回答**

可在缓存注解的 `key` 属性中使用 SpEL，例如 `key = "#id"`、`key = "#a0.id"`；复杂且统一的规则可以实现 `KeyGenerator`，再通过 `keyGenerator` 属性引用。`key` 与 `keyGenerator` 是互斥选择。

**原理与理解**

默认 `SimpleKeyGenerator` 的规则是：无参数使用 `SimpleKey.EMPTY`，单参数直接使用该参数，多参数组成 `SimpleKey`。参数名不可发现时可以使用 `#a0` 或 `#p0`；`#result` 只在结果已经可用的特定表达式位置使用。

**成立条件与边界**

缓存 Key 必须包含所有会影响返回结果的维度，例如租户、语言、分页和权限视图。Spring 生成的是逻辑 Key，落到 Redis 后还会经过类型转换、序列化和缓存名前缀，未必与 SpEL 文本完全相同。

**实际场景（项目核验项）**

项目需要核对注解中的 `cacheNames/value`、`key`、编译参数和 Redis 中的最终 Key，避免把示例 `#id` 当成已确认实现；多租户接口尤其不能遗漏租户维度。

**常见追问**

- 默认多参数 Key 是什么？（包含全部参数的 `SimpleKey`）
- 为什么 `#参数名` 可能不可用？（运行时无法发现参数名，可改用 `#a0/#p0` 或保留参数元数据）

**易错点**

不要只追求 Key 唯一，还要保证相同业务查询稳定地产生同一 Key；可变对象或不可靠的 `equals/hashCode` 不适合作为默认 Key。

## 371. RedisTemplate 和 Spring Cache 有什么区别？

**面试回答**

`RedisTemplate` 是面向 Redis 的命令式操作工具，适合显式控制数据结构、命令、TTL 和脚本；Spring Cache 是面向方法结果的缓存抽象，适合用统一注解或 `Cache` API 声明查、写、淘汰行为。

**原理与理解**

前者直接表达“对 Redis 做什么”，后者表达“这个方法结果如何缓存”，再由 `CacheManager` 选择后端。Spring Cache 也能配置 TTL、序列化等后端能力，但复杂命令、Lua、计数器、队列和集合操作通常不是该抽象的目标。

**成立条件与边界**

Spring Cache 不一定比 `RedisTemplate` 慢或功能弱，只是抽象粒度不同；`RedisTemplate` 也不只用于缓存。两者若共用 Redis，必须避免缓存名、Key 前缀、序列化和失效逻辑互不兼容。

**实际场景（真实项目边界）**

简历确认两者都出现过，但不能据此断言“Spring Cache 缓存菜品、RedisTemplate 存验证码或锁”。合理回答是先说明定位，再以源码核验出的真实用途举例。

**常见追问**

- 哪个更适合方法结果缓存？（通常是 Spring Cache）
- 哪个更适合 Lua 或 Redis 特有数据结构？（通常是 `RedisTemplate`）

**易错点**

不要把两者说成竞争关系或两级缓存，也不要让两种入口以不同序列化规则操作同一个物理 Key。

## 372. 为什么项目中同时使用 RedisTemplate 和 Spring Cache？

**面试回答**

因为二者解决的问题层级不同：标准的方法结果缓存可用 Spring Cache 减少样板代码；需要显式 Redis 数据结构、原子脚本、独立 TTL 或细粒度失败处理时，可使用 `RedisTemplate`。同时使用是按场景选择入口，不是重复建设。

**原理与理解**

Spring Cache 通过缓存拦截器统一处理方法级 get/put/evict，便于集中配置；`RedisTemplate` 让业务或基础设施代码直接组织 Redis 命令。二者最终可以共享连接工厂和 Redis，但各自的 Key 空间与数据契约应明确隔离。

**成立条件与边界**

能用两种工具不代表每个功能都应混用。若同一缓存既由注解又由模板维护，任何前缀、序列化、TTL 或删除范围不一致都可能产生“写得到、读不到”或漏删问题。

**实际场景（真实项目边界）**

简历只支持“项目同时使用过 RedisTemplate 与 Spring Cache”这一层事实。面试前应从源码整理各自负责的真实功能、配置和一个完整读写链路，不补造验证码、锁或特定业务缓存。

**常见追问**

- 同时使用是否代表两级缓存？（不是，可能只是两个 API 访问同一 Redis）
- 如何避免互相干扰？（划分 Key 命名空间，并统一或显式区分序列化与失效规则）

**易错点**

“注解简单、模板复杂”只是选型线索，不是绝对规则；还要考虑可测试性、可观测性、事务边界和团队维护成本。

## 373. 项目中数据修改后如何清理对应缓存？

**面试回答**

先建立数据到缓存条目的依赖关系。数据修改成功后，可用 `@CacheEvict` 淘汰对应缓存，或用 `RedisTemplate.delete` 显式删除；下次读取再从事实来源重建。存在多个派生缓存时，要按依赖清理相关条目。

**原理与理解**

详情缓存通常能按实体 ID 精确删除，列表、聚合和分页缓存可能难以枚举，可选择版本化 Key、按缓存区域失效或事件驱动更新。`@Caching` 可组合多项淘汰；`allEntries = true` 简单但影响范围和重建压力更大。

**成立条件与边界**

默认 `@CacheEvict` 只与方法正常返回关联，不等同于数据库和 Redis 原子提交。删除失败、事务最终回滚或并发旧读回填都可能造成不一致，因此还需 TTL 兜底、监控、有限重试，关键链路可评估事务提交后事件或可靠消息。

**实际场景（项目核验项）**

应从项目更新与删除方法出发，列出它们真实影响的详情、列表和聚合缓存，再核对注解 Key 与手动删除代码；简历不能证明“所有相关缓存都已删全”或已实现可靠补偿。

**常见追问**

- 为什么不能无条件清空整个缓存？（影响面大，容易带来命中率骤降和集中回源）
- 缓存删除失败怎么办？（TTL 兜底、告警与有限重试，强要求场景使用可靠事件机制）

**易错点**

不要机械回答“列表和详情都删”；只有真正依赖该数据的缓存才应失效，关键是可维护的依赖关系、事务时机和失败补偿。

## 参考资料

- [Spring Data Redis：Working with Objects through RedisTemplate](https://docs.spring.io/spring-data/redis/reference/redis/template.html)
- [Spring Data Redis：Drivers](https://docs.spring.io/spring-data/redis/reference/redis/drivers.html)
- [Spring Framework：Understanding the Cache Abstraction](https://docs.spring.io/spring-framework/reference/integration/cache/strategies.html)
- [Spring Framework：Declarative Annotation-based Caching](https://docs.spring.io/spring-framework/reference/integration/cache/annotations.html)
- [Spring Data Redis：Redis Cache](https://docs.spring.io/spring-data/redis/reference/redis/redis-cache.html)
