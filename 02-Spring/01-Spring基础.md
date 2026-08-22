---
category: Spring
priority: P0
status: 未学习
tags:
  - Java后端
  - 面试
  - Spring
---

# Spring基础

## 97. Spring 是什么？

**面试回答**

Spring 是一个开源的 Java 应用开发框架，核心是 IoC（控制反转）和 AOP（面向切面编程），用来简化企业级应用开发。它还提供了一整套生态，比如 Spring MVC 做 Web、Spring Boot 快速启动、Spring Cloud 做微服务。

**理解**

Spring 本质是一个「对象容器」，帮你管理对象的创建、依赖注入和生命周期，让你不用自己 new 对象、手动维护对象之间的关系。它的核心思想是解耦——把对象之间的依赖关系从硬编码里抽出来，交给框架管理。

**场景**

项目里几乎所有组件（Controller、Service、Mapper）都由 Spring 管理，通过注解声明依赖，Spring 自动注入，不用我们手动装配。

**常见追问**

- Spring 和 Spring Boot 什么关系？（Spring Boot 是 Spring 的脚手架，用自动配置和起步依赖简化 Spring 项目搭建）
- Spring 全家桶有哪些？（Spring MVC、Spring Boot、Spring Cloud、Spring Data 等）

**易错点**

Spring 不是「只能做 Web」，它是一个通用框架；别把 Spring 和 Spring Boot 混为一谈。

## 98. Spring 最核心的两个特性是什么？

**面试回答**

IoC（控制反转）和 AOP（面向切面编程）。IoC 负责对象的创建和依赖管理，AOP 负责把横切逻辑（如事务、日志）从业务代码中抽离。

**理解**

IoC 解决「对象怎么创建、依赖怎么注入」的问题，AOP 解决「公共逻辑怎么不侵入业务」的问题。两者都服务于同一个目标：解耦，让代码更清晰、易维护、易测试。

**场景**

项目里 @Autowired 注入依赖体现 IoC；@Transactional 事务、@AutoFill 公共字段填充体现 AOP。

**常见追问**

- AOP 底层是什么？（动态代理）
- 两者分别解决什么问题？（对象管理、横切关注点）

**易错点**

别把 IoC 和 AOP 说成两个互不相关的东西，它们都是「解耦」的手段。

## 99. 什么是 IoC？

**面试回答**

IoC 是控制反转，把「对象的创建和依赖管理」的控制权从程序员手里交给 Spring 容器，程序员不再手动 new 对象，而是由容器负责创建并注入依赖。

**理解**

传统方式是你自己 new 对象、手动 set 依赖；IoC 后，你只需声明需要什么，容器负责装配。控制权「反转」了——从「你主动创建」变成「容器主动给你」。这样对象之间的耦合降低，替换实现更容易。

**场景**

Service 里需要 Mapper，不用 new，只需 @Autowired 声明，Spring 就注入。

**常见追问**

- 「控制反转」反转的是什么？（对象创建和依赖获取的控制权）
- IoC 容器是什么？（Spring 里就是 ApplicationContext / BeanFactory）

**易错点**

IoC 不是「不用 new 了」这么简单，核心是「控制权转移 + 依赖解耦」。

## 100. IoC 解决了什么问题？

**面试回答**

解决对象之间的耦合问题。以前对象自己创建依赖，导致类之间强耦合、难替换、难测试；IoC 把依赖交给容器管理，类之间松耦合，便于扩展和单元测试。

**理解**

比如 Service 直接 new 一个具体的 Dao 实现，想换实现就得改代码。IoC 让 Service 只依赖接口，具体实现由容器注入，换实现只改配置或注解。这就是「面向接口编程」落地的基础。

**场景**

项目里 Service 依赖 Mapper 接口，不关心具体是 MyBatis 还是别的实现，测试时还能注入 mock 对象。

**常见追问**

- 解耦具体体现在哪？（依赖接口而非实现，容器统一装配）
- 对测试有什么好处？（容易替换成 mock 对象）

**易错点**

IoC 的主要价值是「解耦」，不是为了少写几行 new。

## 101. 什么是 DI？

**面试回答**

DI 是依赖注入，是 IoC 的一种实现方式：容器在创建对象时，把对象依赖的其他对象自动注入进去，而不是对象自己去获取。

**理解**

依赖注入有几种方式：构造器注入、字段注入、setter 注入。Spring 通过 @Autowired 等方式完成注入。DI 让「依赖」由外部提供，而不是内部创建。

**场景**

Controller 依赖 Service，通过构造器注入或 @Autowired 字段注入，Spring 自动把 Service 实例传进去。

**常见追问**

- DI 有哪几种方式？（构造器注入、setter 注入、字段注入）
- IoC 和 DI 是一个东西吗？（DI 是 IoC 的具体实现）

**易错点**

DI 只是 IoC 的一种实现，别把两者完全等同。

## 102. IoC 和 DI 有什么关系？

**面试回答**

IoC 是思想/设计原则，DI 是实现这个思想的具体手段。Spring 通过 DI 来完成 IoC 的「控制反转」。

**理解**

IoC 说「控制权要反转」，但怎么反转？DI 就是答案——通过注入依赖，把对象的创建和依赖获取交给容器。所以常说「IoC 是目的，DI 是手段」，它们通常一起出现。

**场景**

Spring 容器用 DI 帮我们把 Service 注入 Controller，实现了 IoC 的解耦。

**常见追问**

- 除了 DI，IoC 还有别的实现吗？（依赖查找 Dependency Lookup，如 getBean）
- 为什么总把 IoC/DI 一起说？（因为 Spring 主要用 DI 实现 IoC）

**易错点**

别把两者完全等同，IoC 是思想、DI 是具体实现。

## 103. 什么是 Spring Bean？

**面试回答**

Spring Bean 就是由 Spring 容器创建并管理的对象。凡是被 Spring 实例化、装配、管理的对象，都叫 Bean。

**理解**

Bean 是 Spring 容器里的基本单元。一个类被 @Component 等注解标记或通过 @Bean 声明后，Spring 会创建它的实例放进容器，之后需要时通过注入获取。Bean 和普通 new 出来的对象的区别在于：Bean 的生命周期由容器管理。

**场景**

项目里的 DishController、DishService、DishMapper 都是 Bean，由 Spring 统一管理。

**常见追问**

- 怎么定义一个 Bean？（@Component 系列注解、@Bean 方法、XML 配置）
- Bean 和 JavaBean 一样吗？（不一样，JavaBean 是规范，Spring Bean 是容器管理的对象）

**易错点**

Bean 不一定非要用 @Bean 注解，@Component 等也能让对象成为 Bean。

## 104. Bean 是怎么交给 Spring 管理的？

**面试回答**

通过声明让 Spring 知道要管理它：用 @Component/@Service/@Controller/@Repository 等注解标记类，配合 @ComponentScan 扫描，或者用 @Bean 方法、@Configuration 显式注册。

**理解**

Spring 启动时会扫描指定包下带这些注解的类，为它们创建 Bean 定义，然后实例化放进容器（IoC 容器）。之后通过 @Autowired 等注入。核心三步：声明（注解）→ 扫描（@ComponentScan）→ 注册（容器管理）。

**场景**

项目启动类上的 @SpringBootApplication 内部包含 @ComponentScan，默认扫描启动类所在包及子包，自动把 @Service、@Controller 等注册为 Bean。

**常见追问**

- @SpringBootApplication 和 @ComponentScan 什么关系？（前者内含 @ComponentScan）
- 不在扫描范围的包能被管理吗？（不能，得手动配置扫描路径或用 @Bean）

**易错点**

光加 @Service 不够，还要保证它在 @ComponentScan 的扫描范围内，否则不会成为 Bean。

## 105. `@Component`、`@Service`、`@Controller`、`@Repository` 有什么区别？

**面试回答**

它们作用一样，都是把类声明为 Spring Bean；区别只是语义分层，便于阅读和按层处理异常、切面等。

**理解**

@Component 是通用注解；@Service 表示业务层、@Controller 表示控制层、@Repository 表示数据访问层。这三个本质是 @Component 的「特化」别名。@Repository 还有额外作用：Spring 会把数据访问层的异常翻译成 Spring 的 DataAccessException。

**场景**

项目里 Controller 用 @RestController（含 @Controller）、Service 用 @Service、Mapper 用 MyBatis 的 @Mapper，分层清晰。

**常见追问**

- 它们能互换吗？（功能上基本能，但语义和个别增强不同）
- @Repository 的特殊之处？（异常翻译）

**易错点**

说「功能完全不同」是错的，它们本质都是 @Component；区别主要是语义和个别增强。

## 106. `@Autowired` 有什么作用？

**面试回答**

@Autowired 是 Spring 的依赖注入注解，容器会自动把匹配类型的 Bean 注入到被标注的字段、构造器或方法上。

**理解**

默认按类型（byType）注入，如果同类型有多个 Bean，再结合 @Qualifier 或 @Primary 指定。它是 Spring 最常用的注入方式。

**场景**

Controller 里 @Autowired 注入 Service，Service 里 @Autowired 注入 Mapper。

**常见追问**

- @Autowired 和 @Resource 什么区别？（@Autowired 按类型，Spring 提供；@Resource 默认按名称，JSR-250 提供）
- 多个同类型 Bean 怎么办？（@Qualifier 或 @Primary）

**易错点**

@Autowired 默认按类型注入，不是按名称；找不到唯一 Bean 会报错。

## 107. 字段注入和构造器注入有什么区别？

**面试回答**

字段注入直接在字段上 @Autowired，写法简洁但依赖不透明、难测试、可能有 NPE 或循环依赖问题；构造器注入通过构造方法传依赖，依赖明确、不可变，官方推荐。

**理解**

构造器注入让依赖在构造时就确定，对象创建后依赖就是完整的，且字段可声明 final，更不可变；字段注入依赖通过反射赋值，对象可以先创建出来（字段可能为空）。构造器注入还能在启动时暴露循环依赖问题。

**场景**

项目里推荐用构造器注入（或 Lombok 的 @RequiredArgsConstructor），依赖明确；字段注入常见于简单 Controller 场景。

**常见追问**

- 为什么推荐构造器注入？（依赖明确、可 final、易测试）
- 字段注入有什么问题？（依赖不透明，不利于单元测试，NPE 风险）

**易错点**

别以为字段注入和构造器注入完全没差别，构造器注入在可测试性和不可变性上更好。

## 108. `@Configuration` 有什么作用？

**面试回答**

@Configuration 标记一个类为配置类，表示这个类里会定义 Bean，通常配合 @Bean 使用，等价于早期的 XML 配置文件。

**理解**

@Configuration 类本身也是一个 @Component（会被注册为 Bean），Spring 会处理类里 @Bean 方法，把返回的对象注册到容器。它通过 CGLIB 代理保证 @Bean 方法调用返回的是容器里的单例（而不是每次 new）。

**场景**

项目里用配置类声明一些第三方 Bean（如 RestTemplate、自定义拦截器、RedisTemplate 配置）。

**常见追问**

- @Configuration 和 @Component 什么关系？（@Configuration 是 @Component 的特化）
- @Configuration 里的 @Bean 方法直接调用会怎样？（返回容器里的单例，因为有 CGLIB 代理）

**易错点**

@Configuration 里 @Bean 方法互相调用能保证单例，靠的是 CGLIB 代理；普通 @Component 类里的 @Bean 没有这个保证。

## 109. `@Bean` 有什么作用？

**面试回答**

@Bean 用在方法上，把这个方法的返回值注册成一个 Spring Bean，方法名默认就是 Bean 的名字，常用于注册第三方类或需要自定义初始化逻辑的对象。

**理解**

有些类不是你自己写的（如 RestTemplate、连接池、Jackson 的 ObjectMapper），没法直接加 @Component，就用 @Bean 方法在配置类里返回一个实例交给 Spring 管理。它更灵活，能自定义构造过程。

**场景**

项目里配置 RestTemplate、RedisTemplate、对象映射器时用 @Bean。

**常见追问**

- @Bean 和 @Component 区别？（@Bean 作用于方法、注册第三方类；@Component 作用于类）
- @Bean 的 Bean 名字默认是什么？（方法名）

**易错点**

@Bean 用在「方法」上，@Component 用在「类」上，别搞混。

## 110. `@ComponentScan` 有什么作用？

**面试回答**

@ComponentScan 指定 Spring 扫描哪些包，把包下带 @Component 等注解的类注册为 Bean。

**理解**

Spring 不会自动扫描所有包，需要 @ComponentScan 告诉它扫描范围。@SpringBootApplication 内部包含了 @ComponentScan，默认扫描启动类所在包及其子包，所以项目里组件放在启动类同包或子包下才能被扫到。

**场景**

项目里所有 @Service、@Controller 都放在启动类所在包的子包里，自动被扫描注册。

**常见追问**

- 默认扫描范围？（启动类所在包及其子包）
- 想扫描别的包怎么办？（@ComponentScan(basePackages = "...") 或 @SpringBootApplication(scanBasePackages=...)）

**易错点**

组件放错包（不在扫描范围内）不会被注册，这是常见 bug。

## 111. `@Value` 有什么作用？

**面试回答**

@Value 用于给 Bean 字段注入配置值，支持从配置文件（application.yml/properties）读取，或直接写字面量、表达式。

**理解**

`@Value("${server.port}")` 从配置读值，`@Value("${key:默认值}")` 可给默认值。它简化了从配置文件取值的操作，但适合简单值（字符串、数字等），复杂配置对象更适合用 @ConfigurationProperties。

**场景**

项目里用 @Value 读一些单值配置，比如支付宝回调地址、JWT 过期时间等。

**常见追问**

- @Value 和 @ConfigurationProperties 区别？（@Value 单值，@ConfigurationProperties 批量绑定复杂对象）
- @Value 能读对象吗？（不适合，复杂结构用 @ConfigurationProperties）

**易错点**

@Value 适合简单值；读复杂配置（多字段、层级）用 @ConfigurationProperties 更合适。

## 112. Spring Bean 默认是单例吗？

**面试回答**

是，Spring 容器里的 Bean 默认是单例（singleton），同一个 Bean 名字在整个容器里只有一个实例，每次注入拿到的都是同一个对象。

**理解**

单例是 Spring 默认作用域。容器启动时创建实例，之后复用，节省内存、提高性能。这跟 GoF 单例模式不完全一样——Spring 的「单例」是「每个容器每个 Bean 一个实例」，不是 JVM 全局唯一。

**场景**

项目里的 Service、Controller 都是单例，多个请求共享同一个实例。

**常见追问**

- 为什么默认单例？（性能、复用，大多数 Bean 无状态）
- 单例是 JVM 全局唯一吗？（不是，是「每容器每 Bean 名一个实例」）

**易错点**

Spring 单例 ≠ 设计模式单例（JVM 唯一），是「每容器每 Bean 名一个实例」。

## 113. 单例 Bean 一定线程安全吗？

**面试回答**

不一定。Spring 只保证 Bean 是单例（共享同一实例），不保证线程安全；单例 Bean 如果有可变状态且被多线程修改，就会有线程安全问题。

**理解**

单例只是「共享实例」，线程安全要看 Bean 有没有共享的可变状态。无状态 Bean（如 Service 方法内只用局部变量）天然线程安全；如果 Bean 里有可变成员变量（如一个计数器字段）被多线程读写，就会出问题。所以要让单例 Bean 线程安全，通常是保持无状态设计，或对共享状态加锁/用 ThreadLocal。

**场景**

项目里的 Service 大多是无状态的（依赖的 Mapper 也是无状态），所以单例没线程安全问题；但如果有成员变量存请求数据就危险，这也是为什么用 ThreadLocal 存用户信息而不是存成员变量。

**常见追问**

- 怎么让单例 Bean 线程安全？（无状态设计、ThreadLocal、锁、换作用域）
- 无状态是什么意思？（Bean 不持有可变实例字段）

**易错点**

别把「单例」等同于「线程安全」；核心看有没有共享可变状态。

## 114. Spring Bean 有哪些常见作用域？

**面试回答**

常见的有 singleton（单例，默认）、prototype（原型，每次获取新建实例）；Web 环境下还有 request（每个请求一个）、session（每个会话一个）、application（每个 Web 应用一个）等。

**理解**

singleton 容器里只有一个实例；prototype 每次注入/获取都 new 一个；request/session/application 是 Web 应用中的作用域，生命周期跟随请求/会话/应用。多数业务 Bean 用默认 singleton，需要每次新建的用 prototype。

**场景**

项目里绝大多数 Bean 是默认 singleton；个别需要每次新建（比如有状态对象、每次独立的临时对象）才用 prototype。

**常见追问**

- singleton 和 prototype 区别？（一个实例 vs 每次新建）
- prototype 的 Bean 谁负责销毁？（容器不负责完整生命周期，需自己处理）

**易错点**

prototype Bean 的销毁回调 Spring 不完全管理，别以为所有作用域都有完整生命周期回调。

## 115. Spring Bean 生命周期大致是什么？

**面试回答**

大致是：实例化 → 属性填充（依赖注入）→ 各种 Aware 接口回调 → 初始化前（BeanPostProcessor）→ 初始化（InitializingBean / @PostConstruct）→ 初始化后（AOP 代理）→ 使用 → 销毁（DisposableBean / @PreDestroy）。

**理解**

简化记忆：创建对象 → 注入依赖 → 初始化 → 使用 → 销毁。Spring 提供很多扩展点，常见的是 @PostConstruct（初始化时执行）和 @PreDestroy（销毁前执行）。AOP 代理也在这个流程里（初始化后生成代理对象）。

**场景**

项目里可以用 @PostConstruct 做初始化逻辑（如加载缓存），@PreDestroy 做清理；AOP（事务、@AutoFill）也是在 Bean 初始化后通过代理实现的。

**常见追问**

- @PostConstruct 和构造方法哪个先？（构造方法先，@PostConstruct 在依赖注入完成后）
- BeanPostProcessor 是什么？（Bean 初始化前后的扩展点，AOP 就是靠它）

**易错点**

记住顺序——先实例化、再注入、再初始化；@PostConstruct 在依赖注入之后才执行。
