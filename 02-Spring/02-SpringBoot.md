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

Spring Boot 是基于 Spring 的框架，通过自动配置、起步依赖（Starter）和内嵌服务器，让我们能快速搭建、独立运行、开箱即用的 Spring 应用，省去大量配置。

**理解**

传统 Spring 要写一堆 XML/配置、手动搭 Tomcat、引一堆依赖，Spring Boot 用「约定优于配置」把这些都自动化了。核心能力：自动配置、Starter 依赖管理、内嵌容器、Actuator 监控等。它是 Spring 的「脚手架」，不是替代 Spring 的新框架。

**场景**

项目就是一个 Spring Boot 应用，启动类上 @SpringBootApplication，一个 main 方法就能跑起来，内嵌 Tomcat，不用单独部署。

**常见追问**

- Spring Boot 和 Spring 是什么关系？（Boot 基于 Spring，是对它的封装和简化）
- 为什么能独立运行？（内嵌 Tomcat，打成 jar 直接 java -jar 运行）

**易错点**

Spring Boot 不是新框架，是 Spring 的快速启动方案；别把「Spring Boot」和「Spring 全家桶里的某个框架」对立起来。

## 117. Spring Boot 和 Spring 有什么关系？

**面试回答**

Spring Boot 构建在 Spring 之上，是对 Spring 的封装和简化。Spring 提供 IoC、AOP 等核心能力，Spring Boot 用自动配置、Starter 让这些能力开箱即用。

**理解**

可以把 Spring 理解成「发动机」，Spring Boot 是「整车 + 一键启动」。没有 Spring Boot，Spring 也能用，但要手动配很多东西；有了 Boot，启动一个 Web 项目只要一个注解 + 一个 main 方法。

**场景**

项目里的 IoC、AOP、事务本质都来自 Spring，Spring Boot 负责帮我们把它们自动配好、简化依赖管理。

**常见追问**

- Spring Boot 能脱离 Spring 用吗？（不能，它基于 Spring）
- 学 Spring Boot 还要学 Spring 吗？（要，IoC/AOP 等原理是 Boot 的基础）

**易错点**

Boot 是 Spring 的「封装/简化」，不是「替代」，底层还是 Spring 的那套 IoC/AOP。

## 118. Spring Boot 为什么能简化开发？

**面试回答**

主要靠三点：自动配置（按依赖自动配好 Bean）、起步依赖 Starter（一键引入相关依赖并管理版本）、内嵌服务器（不用单独部署 Tomcat）。

**理解**

自动配置省去手写 Bean 配置；Starter 把「一个功能的依赖集合 + 默认版本」打包，避免依赖冲突；内嵌 Tomcat 让应用能直接运行。再加上「约定优于配置」的思想，很多东西有合理默认值，不配也能跑。

**场景**

项目里引入 `spring-boot-starter-web` 就自动配好 Spring MVC、内嵌 Tomcat、Jackson 等，几乎不用额外配置就能写接口。

**常见追问**

- 自动配置怎么实现的？（@EnableAutoConfiguration + 条件装配 @Conditional 系列）
- 什么是约定优于配置？（提供合理默认值，减少显式配置）

**易错点**

「简化」不等于「不用懂原理」，出问题还是得回到 Spring 的 IoC/AOP 去理解。

## 119. 什么是自动配置？

**面试回答**

自动配置是 Spring Boot 根据你引入的依赖和类路径情况，自动帮你创建并配置所需的 Bean，而不需要你手写配置。

**理解**

Spring Boot 通过 `@EnableAutoConfiguration` 开启自动配置，运行时读取很多 `xxxAutoConfiguration` 类，用条件注解（@ConditionalOnClass、@ConditionalOnMissingBean 等）判断「某个类在不在、Bean 有没有被用户自定义」，满足条件才装配。核心是「按需、有默认值、可被用户覆盖」。

**场景**

项目引入 MyBatis 相关 Starter 后，Spring Boot 自动配置 DataSource、SqlSessionFactory 等，不用我们手写。

**常见追问**

- 自动配置的判断条件靠什么？（@Conditional 系列注解）
- 用户自定义配置能覆盖自动配置吗？（能，@ConditionalOnMissingBean 保证用户优先）

**易错点**

自动配置不是「无脑全配」，是「条件装配」，条件不满足就不配；理解这一点就不会觉得它神秘。

## 120. 什么是 Starter？

**面试回答**

Starter 是一组依赖的集合打包，把某个功能需要的所有依赖（含版本）和自动配置集中在一起，引入一个 Starter 就能用整套功能，避免手动逐个引依赖和管版本。

**理解**

比如 `spring-boot-starter-web` 内部包含了 Spring MVC、内嵌 Tomcat、Jackson 等一堆依赖。Starter 的核心价值：①依赖聚合（省心）②版本统一（避免冲突）。命名上，官方的是 `spring-boot-starter-xxx`，第三方通常是 `xxx-spring-boot-starter`。

**场景**

项目里引入 `spring-boot-starter-web`、`spring-boot-starter-data-redis`、`spring-boot-starter-validation` 等，每个都对应一块功能的依赖集合。

**常见追问**

- Starter 和自动配置什么关系？（Starter 引入依赖，自动配置类根据这些依赖装配 Bean）
- 官方和第三方 Starter 命名区别？（官方 spring-boot-starter-xxx，第三方 xxx-spring-boot-starter）

**易错点**

Starter 本质是「依赖聚合 + 版本管理」，它不写业务逻辑，别理解成「一个功能模块的代码包」。

## 121. `@SpringBootApplication` 有什么作用？

**面试回答**

它是 Spring Boot 启动类的核心注解，标记主类，开启自动配置和组件扫描，是整个应用的入口。

**理解**

`@SpringBootApplication` 是一个组合注解，主要包含三部分：`@SpringBootConfiguration`（标记配置类）、`@EnableAutoConfiguration`（开启自动配置）、`@ComponentScan`（组件扫描）。一个注解搞定三件事，所以 main 方法里的 `SpringApplication.run(...)` 能启动整个容器。

**场景**

项目启动类上就这一个注解，main 方法调用 `SpringApplication.run` 启动应用。

**常见追问**

- 必须放在启动类上吗？（一般放在主类上，且建议放根包，便于扫描子包）
- @SpringBootApplication 能拆开写吗？（能，等价于那三个注解）

**易错点**

它是「组合注解」，不是一个单独功能；记住它 = 配置类 + 自动配置 + 组件扫描。

## 122. `@SpringBootApplication` 包含哪些主要注解？

**面试回答**

主要包含 `@SpringBootConfiguration`、`@EnableAutoConfiguration`、`@ComponentScan` 三个注解。

**理解**

@SpringBootConfiguration 本质是 @Configuration，表示这是个配置类；@EnableAutoConfiguration 开启自动配置；@ComponentScan 扫描当前包及子包的组件。三者合起来，应用就能自动发现组件、按需装配 Bean、作为容器启动。

**场景**

理解这个组合后，就知道为什么启动类放在根包、组件放子包就能被扫到。

**常见追问**

- @SpringBootConfiguration 和 @Configuration 什么关系？（前者是后者的特化，本质一样）
- @ComponentScan 默认扫哪里？（启动类所在包及其子包）

**易错点**

别漏了 @EnableAutoConfiguration 是「自动配置」的开关，没有它 Boot 的省事能力就没了。

## 123. `application.yml` 和 `application.properties` 有什么作用？

**面试回答**

都是 Spring Boot 的配置文件，用来放应用的外部化配置（端口、数据库连接、日志级别等），Boot 启动时自动读取并绑定。

**理解**

两者作用一样，只是格式不同：properties 是 `key=value` 平铺写法，yml 是缩进层级写法，更简洁、支持更自然的层级结构。Spring Boot 默认加载 `application.properties` 或 `application.yml`（也可用 yaml），也可以配合 profile 区分环境。

**场景**

项目用 application.yml 配端口、MySQL 数据源、Redis 连接、JWT 密钥、支付宝配置等。

**常见追问**

- 两者能同时存在吗？（能，properties 优先级高于 yml）
- 配置文件里的值怎么读？（@Value、@ConfigurationProperties）

**易错点**

properties 和 yml 只是「格式」不同，功能等价；注意同时存在时的优先级（properties 覆盖 yml）。

## 124. Spring Boot 如何配置不同环境？

**面试回答**

用 Profile 机制：定义多个环境配置文件，如 `application-dev.yml`、`application-prod.yml`，通过 `spring.profiles.active` 指定激活哪个环境。

**理解**

不同环境（开发、测试、生产）配置不同（数据库地址、日志级别等），把这些差异拆到各自的 profile 文件里，主配置里用 `spring.profiles.active=dev` 激活。也可以打成 jar 后用命令行参数 `--spring.profiles.active=prod` 覆盖，实现一套代码多环境部署。

**场景**

项目里用 application-dev.yml 连本地数据库、application-prod.yml 连生产库，部署时指定 active 环境。

**常见追问**

- profile 文件命名规则？（application-{profile}.yml）
- 命令行怎么指定环境？（--spring.profiles.active=prod）

**易错点**

激活环境用 `spring.profiles.active`，不是 `spring.profile.active`（少个 s 是常见拼写错误）。

## 125. Spring Boot 内嵌 Tomcat 有什么作用？

**面试回答**

内嵌 Tomcat 让应用不再需要外部安装、部署独立的 Tomcat 服务器，应用启动时内置的 Tomcat 就随之启动，直接打成 jar 包用 `java -jar` 就能运行。

**理解**

传统做法是把应用打成 war 包，放到外置 Tomcat 里。Spring Boot 把 Tomcat 作为依赖内嵌进应用，`SpringApplication.run` 时启动内嵌容器，监听端口处理请求。这样部署更简单、环境更一致（每个应用自带容器，互不影响）。

**场景**

项目开发时直接运行 main 方法就能启动服务，打出的 jar 包丢到服务器 `java -jar` 就能跑，不用单独配 Tomcat。

**常见追问**

- 能换成别的容器吗？（能，比如用 Undertow、Jetty，排除 Tomcat 引入对应依赖）
- 内嵌 Tomcat 是默认的吗？（是，spring-boot-starter-web 默认带内嵌 Tomcat）

**易错点**

内嵌 Tomcat 是「应用的一部分」，不是「外部服务器」；它让部署变简单，但本质还是那个 Servlet 容器。
