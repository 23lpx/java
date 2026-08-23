---
category: Spring
priority: P0
status: 未学习
tags:
  - Java后端
  - 面试
  - Spring
---

# SpringBoot

## 116. Spring Boot 是什么？

**面试回答**

Spring Boot 是用于创建独立运行、面向生产的 Spring 应用的项目。它通过自动配置、Starter、外部化配置、可执行归档和运维特性降低搭建成本，但核心容器、MVC、事务等能力仍来自 Spring Framework。

**原理与理解**

Boot 根据类路径、已有 Bean 和配置属性进行条件化装配，并提供经过协调的依赖版本和常用默认值。`SpringApplication` 负责准备环境、创建并刷新应用上下文，Web 应用还可随应用启动嵌入式服务器。

**成立条件与边界**

“约定优于配置”不等于零配置；自动配置只在条件满足时生效，也可能被显式排除或定制。Actuator、特定服务器和数据访问组件都要有对应依赖，不能视为 Boot 必然自带。

**实际场景（通用工程）**

一个 MVC 服务可通过 Boot 管理依赖、加载配置并打包为可执行 JAR；具体使用 Tomcat、Jetty 还是外部容器要以依赖和部署方式为准。

**常见追问**

- Boot 与 Spring Framework 的关系？——Boot 组织和自动配置 Spring 生态能力，不替代 Framework。
- 为什么可以独立运行？——应用可携带嵌入式服务器并由 `SpringApplication` 启动。

**易错点**

不要把 Spring Boot 简化成“脚手架”或“内嵌 Tomcat”；它还定义了配置、依赖和运行约定。

## 117. Spring Boot 和 Spring 有什么关系？

**面试回答**

Spring Framework 提供 IoC、AOP、事务和 Web 等基础能力；Spring Boot 以这些能力为基础，通过自动配置、依赖管理和运行约定简化应用创建与部署。

**原理与理解**

Boot 本身也使用 Spring 的配置类、条件注解和应用上下文。业务 Bean 最终仍由 Spring 容器管理，MVC 请求仍由 Spring MVC 处理，Boot 主要负责选择合理的默认装配并提供扩展点。

**成立条件与边界**

Boot 不是对 Spring API 的简单二次封装，也不是所有 Spring 项目的必需品。传统 Spring 应用可以不使用 Boot，Boot 应用也必须理解容器、代理和事务等基础契约。

**实际场景（通用工程）**

引入 Web Starter 后，Boot 根据依赖配置 MVC 基础设施；Controller、Service 的注入和生命周期仍遵守 Spring Framework 规则。

**常见追问**

- Boot 能脱离 Spring Framework 吗？——其核心应用模型建立在 Spring 之上。
- 为什么还要学习 Spring？——排查条件装配、Bean 冲突和代理边界都依赖这些知识。

**易错点**

“Spring 是发动机、Boot 是整车”只能辅助记忆，不能替代对两者职责的准确说明。

## 118. Spring Boot 为什么能简化开发？

**面试回答**

主要因为自动配置减少样板装配，Starter 聚合常用依赖，Boot 的 BOM/依赖管理协调版本，外部化配置统一环境差异，嵌入式服务器与可执行归档简化运行和部署。

**原理与理解**

类路径出现某项技术且应用没有提供冲突配置时，相关自动配置才可能生效；配置属性允许在不改代码的情况下调整默认值。构建插件可把应用及依赖组织为可执行归档。

**成立条件与边界**

Starter 负责依赖聚合，版本协调主要来自 Boot 的 dependency management/BOM，不能把两者混为一谈。默认值只适合常见场景，连接池、线程、超时和安全配置仍需按生产负载验证。

**实际场景（通用工程）**

开发者引入合适的 Web 与 Validation Starter 后即可获得常用基础设施，再通过配置属性调整端口、序列化和校验行为。

**常见追问**

- 自动配置依据什么？——类路径、Bean、属性、应用类型等条件。
- 简化是否意味着无需排查依赖？——不是，仍要查看条件报告和依赖树。

**易错点**

不要回答“Starter 自带所有代码并管理版本”；它通常只是依赖描述符。

## 119. 什么是自动配置？

**面试回答**

自动配置是 Spring Boot 根据运行环境和应用已声明内容，有条件地注册一组合理默认 Bean 的机制；应用可以通过配置、显式 Bean 或排除项进行定制。

**原理与理解**

`@EnableAutoConfiguration` 会导入候选自动配置类。现代 Boot 的候选通常列在 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`，配置类再通过 `@ConditionalOnClass`、`@ConditionalOnMissingBean`、`@ConditionalOnProperty` 等判断是否生效。

**成立条件与边界**

“用户配置优先”是常见 back-off 设计，不是所有自动配置都由 `@ConditionalOnMissingBean` 控制，也不保证同名 Bean 可以任意覆盖。应查看具体自动配置和 Condition Evaluation Report。

**实际场景（通用工程）**

类路径存在数据源实现且属性完整时，Boot 可能配置数据源；应用显式提供相应 Bean 后，部分默认配置会退让，具体以条件为准。

**常见追问**

- 如何知道某项配置为何没生效？——查看条件评估报告、启动日志和对应自动配置源码。
- 能否排除自动配置？——可以使用注解属性或配置项排除指定类。

**易错点**

自动配置不是扫描所有 JAR 后“无脑创建 Bean”，而是一组可审查的条件化配置。

## 120. 什么是 Starter？

**面试回答**

Starter 是面向某类功能的一组依赖描述，使应用只声明一个入口依赖就能获得常见库组合；官方 Starter 通常命名为 `spring-boot-starter-*`。

**原理与理解**

Starter 的 POM/模块主要声明传递依赖，本身往往没有业务实现。自动配置可以和 Starter 一起发布，但两者职责不同：前者决定如何装配，后者帮助把相关类库放入类路径。

**成立条件与边界**

依赖版本由 Boot 的 BOM 或父工程等依赖管理机制协调，不是 Starter 单独“锁死”。第三方命名有推荐惯例但不是强制标准，仍要检查其兼容版本、自动配置入口和维护质量。

**实际场景（通用工程）**

Web、Validation、Data Redis 等 Starter 可减少逐项声明依赖；若不需要默认服务器，可排除传递依赖并选择其他实现。

**常见追问**

- Starter 和自动配置是什么关系？——常配套但不等同：一个聚合依赖，一个注册默认 Bean。
- 自定义 Starter 需要什么？——依赖描述、可选自动配置及清晰的属性和 back-off 契约。

**易错点**

Starter 不是“功能代码包 + 版本管理 + 自动配置”三者必然合一。

## 121. `@SpringBootApplication` 有什么作用？

**面试回答**

`@SpringBootApplication` 是常用的主配置组合注解，表示 Boot 配置类、启用自动配置并从该类所在包开始组件扫描；应用通常把它标在传给 `SpringApplication.run` 的主类上。

**原理与理解**

它组合了 `@SpringBootConfiguration`、`@EnableAutoConfiguration` 和 `@ComponentScan`，同时带有用于避免重复扫描特定配置类的过滤规则。`SpringApplication.run` 才负责实际引导应用上下文。

**成立条件与边界**

注解本身不是 JVM 入口，真正入口仍是 `main` 或其他启动机制。它也不要求类名必须叫 Application；扫描范围、自动配置排除和代理模式均可定制。

**实际场景（通用工程）**

把主配置类放在稳定的根包能覆盖常见业务子包；跨模块组件应显式导入或调整扫描，而不是依赖偶然目录结构。

**常见追问**

- 能否拆开写三个注解？——可以，但组合注解提供了 Boot 的常用约定和别名属性。
- 为什么建议放根包？——默认组件扫描以它所在包为基准。

**易错点**

不要说“加上注解 main 方法就自动产生”；启动调用和组合注解各有职责。

## 122. `@SpringBootApplication` 包含哪些主要注解？

**面试回答**

主要是 `@SpringBootConfiguration`、`@EnableAutoConfiguration` 和 `@ComponentScan`：分别标识 Boot 主配置、导入自动配置、发现应用组件。

**原理与理解**

`@SpringBootConfiguration` 元标注 `@Configuration`，并帮助测试等基础设施定位主配置；`@EnableAutoConfiguration` 导入候选自动配置；`@ComponentScan` 注册扫描到的 stereotype 组件。

**成立条件与边界**

“主要包含”不等于源码只有这三个元注解，它还包含继承、文档化等元数据和别名配置。`@ComponentScan` 只负责应用组件发现，自动配置候选不是靠普通组件扫描加载。

**实际场景（通用工程）**

遇到 Bean 未注册时先区分：是应用组件未被扫描，还是自动配置条件不成立，两者排查路径不同。

**常见追问**

- `@SpringBootConfiguration` 和 `@Configuration` 的区别？——前者建立在后者之上，并提供 Boot 主配置语义。
- 自动配置来自组件扫描吗？——不是，由 `@EnableAutoConfiguration` 的导入机制加载。

**易错点**

不要把三种机制归纳成“都负责扫描 Bean”。

## 123. `application.yml` 和 `application.properties` 有什么作用？

**面试回答**

它们是 Spring Boot 默认识别的外部配置文件格式，用于提供应用属性；属性还可来自环境变量、系统属性、命令行、配置树等，并按属性源优先级合并。

**原理与理解**

properties 使用键值形式，YAML 适合表达层次结构，最终都会进入 `Environment`。应用可通过 `@ConfigurationProperties`、`@Value` 或 `Environment` 读取，后加载或高优先级来源可覆盖较低优先级值。

**成立条件与边界**

不能只背“properties 一定覆盖 yml”而忽略文件位置、导入和属性源顺序；官方也建议同一位置尽量只选一种格式。敏感凭据不应提交进仓库，YAML 也不适用于 `@PropertySource`。

**实际场景（项目核验项）**

可核对项目实际使用的配置文件、环境变量和密钥来源；只确认存在某项配置时，不扩写其生产环境值或发布流程。

**常见追问**

- 如何绑定一组配置？——优先使用可校验的 `@ConfigurationProperties`。
- 命令行属性能覆盖文件吗？——通常可以，具体遵守 Boot 的属性源顺序。

**易错点**

配置文件不是唯一来源，写在其中也不代表该值最终生效。

## 124. Spring Boot 如何配置不同环境？

**面试回答**

可使用 Spring Profile 隔离 Bean 和配置片段，并结合外部化配置在部署时选择活动 Profile，例如通过环境变量或命令行设置 `spring.profiles.active`。

**原理与理解**

`application-{profile}.properties/yaml` 等 profile-specific 文件会在对应 Profile 激活时参与合并；`@Profile` 可限制组件或配置类。Profile group 和 include 可组合多个能力集合。

**成立条件与边界**

Profile 不是密钥管理或发布系统。`spring.profiles.active`、`default` 等只能放在允许的位置，不能在自身已受 Profile 条件控制的文档里再次激活 Profile。生产环境选择不应硬编码在制品中。

**实际场景（通用工程）**

同一制品通过部署环境提供数据库地址、日志级别和活动 Profile；敏感项从密钥设施注入，而不是复制一份带明文密码的 prod 文件。

**常见追问**

- Profile 文件命名？——常见为 `application-{profile}.yml` 或 properties。
- 如何在命令行激活？——例如 `--spring.profiles.active=prod`。

**易错点**

“一套代码多环境”不等于把所有生产机密都写进 Profile 文件。

## 125. Spring Boot 内嵌 Tomcat 有什么作用？

**面试回答**

在 Servlet Web 应用选择 Tomcat 依赖时，Boot 可把服务器作为应用依赖并随应用上下文启动，使服务能以可执行 JAR 运行，无需把 WAR 手工部署到外部 Tomcat。

**原理与理解**

Boot 创建并配置嵌入式 WebServer，注册 Servlet、Filter 等组件并管理服务器生命周期。端口、连接和线程等通过配置或定制器调整，构建插件负责生成可执行归档。

**成立条件与边界**

嵌入式服务器不一定是 Tomcat，也可以选择 Jetty 等；WebFlux 还可能使用不同服务器。Boot 也支持传统 WAR 部署，因此“Boot 项目必然是内嵌 Tomcat + JAR”不成立。

**实际场景（通用工程）**

本地可直接运行主类，部署时运行同一 JAR；生产环境仍需配置优雅停机、超时、资源上限、反向代理和健康检查。

**常见追问**

- 能替换 Tomcat 吗？——可以调整 Starter 的传递依赖并引入受支持服务器。
- 内嵌是否等于无需运维配置？——不是，服务器参数和容量仍需验证。

**易错点**

“自带服务器”描述的是依赖和生命周期模式，不代表服务器能力消失或无需调优。
