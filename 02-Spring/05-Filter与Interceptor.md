---
category: Spring
priority: P0
status: 未学习
tags:
  - Java后端
  - 面试
  - Spring
---

# Filter与Interceptor

## 147. Filter 是什么？

**面试回答**

Filter 是 Jakarta Servlet 规范的容器组件，可在目标 Servlet 或资源前后检查、包装或阻断请求与响应；调用 `FilterChain.doFilter` 才会把处理继续交给下一个 Filter 或目标资源。

**原理与理解**

Filter 由 Servlet 容器按 URL pattern、Servlet 名称和 dispatcher type 等规则应用。代码可在调用 chain 前处理请求，在返回后处理响应，也可用 wrapper 改写接口行为。

**成立条件与边界**

Filter 的覆盖范围由注册映射决定，并非天然“拦截所有请求和静态资源”。它不属于 Spring MVC，但通过 `DelegatingFilterProxy`、`FilterRegistrationBean` 等方式仍可与 Spring Bean 协作。

**实际场景（通用工程）**

请求关联 ID、通用头处理、请求包装或安全过滤链适合 Filter；涉及 HandlerMethod 元数据的规则更适合 MVC 组件。

**常见追问**

- 不调用 `chain.doFilter` 会怎样？——后续链不执行，当前 Filter 应负责形成响应或抛出异常。
- Filter 是单例吗？——容器通常复用实例，不能把请求状态放在实例字段中。

**易错点**

“Filter 不能注入 Spring Bean”过于绝对，关键在注册和代理方式。

## 148. Interceptor 是什么？

**面试回答**

Interceptor 通常指 Spring MVC 的 `HandlerInterceptor`，围绕已映射的 Handler 执行 `preHandle`、`postHandle` 和 `afterCompletion`，适合使用 Handler 信息做 Web 层横切处理。

**原理与理解**

DispatcherServlet 找到 `HandlerExecutionChain` 后按顺序执行前置回调，再调用 Handler；成功返回后逆序执行后置和完成回调。拦截器是 MVC 执行链机制，不是依靠 AOP 代理拦截 Controller。

**成立条件与边界**

它只作用于进入相应 HandlerMapping 的请求，异步处理还有额外生命周期。拦截器可以注册为 Spring Bean，但“能使用 Bean”不是它区别于 Filter 的绝对标准。

**实际场景（通用工程）**

根据 HandlerMethod 注解记录审计维度、建立请求上下文或执行轻量前置检查；通用认证授权优先评估 Spring Security。

**常见追问**

- Interceptor 属于哪一层？——Spring MVC Handler 执行链。
- 与 AOP 的区别？——前者围绕 Web Handler，后者围绕可代理的连接点，适用边界不同。

**易错点**

不要回答“Interceptor 和 AOP 都是动态代理”；MVC 拦截器是显式调用链。

## 149. Filter 和 Interceptor 有什么区别？

**面试回答**

Filter 由 Servlet 容器执行，围绕 Servlet/资源并可包装请求响应；Interceptor 由 Spring MVC 执行，围绕已映射 Handler 并能获取 Handler 信息。通常先进入 Filter 链，再进入 DispatcherServlet 和 Interceptor 链。

**原理与理解**

Filter 的映射可覆盖不同 Servlet、静态资源及 ERROR/ASYNC dispatch；Interceptor 的匹配基于 MVC 路径和 HandlerMapping。两者都能调用 Spring 服务，只是集成方式和上下文信息不同。

**成立条件与边界**

“Filter 范围一定更大、Interceptor 一定只拦 Controller”也需看映射：MVC 静态资源 Handler 可能被拦截，Filter 也可能只映射小范围。安全规则不宜只依赖 MVC 路径匹配，Spring 官方更建议使用 Spring Security 或 Servlet Filter chain。

**实际场景（通用工程）**

安全认证放在成熟 Filter 安全链，Handler 注解审计放 Interceptor；若项目规模较小使用 JWT Interceptor，也要明确其路径和异步边界。

**常见追问**

- 谁先执行？——一般是外层 Filter，再到 DispatcherServlet 内的 Interceptor。
- 哪个能拿到 Controller 方法？——Interceptor 在 Handler 为 HandlerMethod 时可以。

**易错点**

不要用“Filter 不能用 Spring Bean”作为核心区别。

## 150. `HandlerInterceptor` 有哪些主要方法？

**面试回答**

三个主要回调是：`preHandle` 在 Handler 调用前执行并决定是否继续；`postHandle` 在 Handler 成功执行后、视图渲染前执行；`afterCompletion` 在请求处理完成后用于收尾。

**原理与理解**

多个拦截器的 preHandle 按注册顺序执行，postHandle 与 afterCompletion 通常逆序。若某个 preHandle 返回 false，Handler 不执行，已经成功通过的前序拦截器会收到完成回调，返回 false 的当前拦截器不会因此自动收到自己的 afterCompletion。

**成立条件与边界**

`@ResponseBody` 场景中响应可能在 HandlerAdapter 内已写出，postHandle 往往太晚，响应体修改应使用 `ResponseBodyAdvice`。异步请求需关注 `AsyncHandlerInterceptor` 和再次 dispatch。

**实际场景（项目核验项）**

若项目在 preHandle 写入 ThreadLocal，应核对实际在哪个回调或 Filter 的 finally 中清理，并覆盖拒绝、异常和异步路径。

**常见追问**

- preHandle 返回 false 后谁负责响应？——当前拦截器或前置组件应设置状态/响应体。
- 三个方法都是抽象的吗？——现代接口提供默认实现，可按需覆盖。

**易错点**

“preHandle 返回 false 后所有 afterCompletion 都不执行”不准确，要区分已通过的前序拦截器。

## 151. `preHandle()` 在什么时候执行？

**面试回答**

DispatcherServlet 已找到 Handler、准备由 HandlerAdapter 调用它之前，会按顺序执行拦截器的 `preHandle`；返回 true 继续，返回 false 中断当前 Handler 链。

**原理与理解**

此时可访问 request、response 和 Handler，因此能读取头、判断 HandlerMethod 元数据或建立请求上下文。它不是请求最早阶段，外层 Filter 已经执行。

**成立条件与边界**

返回 false 不会自动生成 401 或 JSON，拦截器必须正确设置响应或抛出可处理异常。异步请求可能发生再次 dispatch，逻辑要避免重复副作用。

**实际场景（通用工程）**

认证失败时设置 401 并停止链路；认证成功时只建立最小身份上下文，把资源级授权留给更合适的安全或业务层。

**常见追问**

- 多个 preHandle 的顺序？——按配置顺序。
- 此时 Controller 已实例化吗？——Handler 已解析，但目标方法尚未执行。

**易错点**

preHandle 不是 Servlet 请求的绝对起点，也不应把所有业务规则塞进去。

## 152. `postHandle()` 在什么时候执行？

**面试回答**

`postHandle` 在 Handler 正常返回后、DispatcherServlet 渲染视图前逆序执行，可调整 `ModelAndView` 等 MVC 模型信息。

**原理与理解**

如果 Handler 抛出异常，正常 postHandle 链通常不会执行，异常会转入异常解析流程。对于 `@ResponseBody` 和 `ResponseEntity`，响应可能已经由消息转换器写出。

**成立条件与边界**

因此 postHandle 不适合统一修改 REST 响应体；可使用 `ResponseBodyAdvice`、返回值处理器或明确响应 DTO。异步 Handler 启动后，初始线程也不会按同步请求的简单时序完成全部回调。

**实际场景（通用工程）**

服务端视图可以在 postHandle 补充公共模型；REST API 的统一包装和头处理使用专门扩展点。

**常见追问**

- Controller 异常时会调用吗？——通常不会。
- 与 afterCompletion 的差异？——后者更晚，并接收处理阶段异常信息。

**易错点**

“Controller 后、响应前”只是简化说法，响应体模式下数据可能已经写出。

## 153. `afterCompletion()` 在什么时候执行？

**面试回答**

同步请求中，Handler 链和可能的视图渲染完成后，会逆序调用已成功通过 preHandle 的拦截器 `afterCompletion`，并传入处理阶段可能存在的异常。

**原理与理解**

它适合清理请求上下文和记录最终耗时。若某拦截器自己的 preHandle 返回 false，它不会收到自己的完成回调；此前已返回 true 的拦截器会被触发清理。

**成立条件与边界**

异常参数可能为 null，即使最终产生错误响应；异常也可能已被 Resolver 处理。Servlet 异步处理时，完成回调在后续 dispatch 完成后发生，不能依赖原线程的 ThreadLocal 自动延续。

**实际场景（项目核验项）**

项目已确认使用 ThreadLocal 传递登录上下文；需核对清理是否覆盖正常、拒绝、异常和异步分支，必要时用 Filter 的 `try-finally` 建立更完整边界。

**常见追问**

- 它一定执行吗？——只对已成功通过前置回调且流程能完成的拦截器有保证，进程终止等仍不保证。
- 能否仅靠异常参数判断最终状态？——不能，还要结合响应状态和异常解析结果。

**易错点**

“只要 preHandle 放行就绝对执行”忽略了异步、进程故障和容器边界。

## 154. 为什么 JWT 登录校验适合放在拦截器？

**面试回答**

在简单 Spring MVC 应用中，JWT 校验是 Controller 前的重复逻辑，Interceptor 能统一读取请求、匹配 Handler 和建立身份上下文，避免每个接口手写；但生产级通用认证更适合 Spring Security 的 Filter chain。

**原理与理解**

校验不仅是解码，还应限制允许算法并验证签名、有效期以及系统要求的 issuer、audience 等 Claims。校验成功后只保存必要身份信息，授权仍需按资源和操作判断。

**成立条件与边界**

Spring 官方指出 MVC Interceptor 并非理想的通用安全层，因为路径匹配可能与 Controller 映射产生差异。还要处理密钥轮换、注销/撤销策略、时钟偏差、日志脱敏和 ThreadLocal 清理。

**实际场景（真实项目边界）**

项目已确认使用 JWT、双拦截器与 ThreadLocal 建立登录上下文；具体算法、Claims、有效期、撤销和清理回调仍属于核验项，不能在面试中虚构。

**常见追问**

- 为什么不在每个 Controller 校验？——重复、容易遗漏且协议逻辑侵入业务。
- 为什么生产更偏向 Spring Security？——它提供成熟的认证、授权、异常和安全链集成。

**易错点**

“能解析出 userId”不代表 Token 可信，必须先完成加密学与语义校验。

## 155. 为什么登录接口必须放行？

**面试回答**

如果登录接口用于未认证主体提交凭据并换取 Token，它就不能要求先携带该 Token，否则会形成认证前置死循环；应把它配置为最小公开端点。

**原理与理解**

公开只表示无需已有登录态，不表示无保护。登录接口仍需凭据校验、速率限制、防爆破、审计和安全错误提示；注册、验证码、找回密码是否公开由产品策略决定。

**成立条件与边界**

白名单必须使用与路由一致的精确匹配并经过测试，避免 `/admin/**` 等保护范围被错误排除。刷新 Token、登出和健康检查也要分别设计，不应全部笼统放行。

**实际场景（项目核验项）**

核对项目实际登录路径和 `excludePathPatterns` 配置，只描述仓库中确实存在的放行项；不要凭经验补写注册、找回密码等接口。

**常见追问**

- 放行是否等于匿名成功？——不是，登录处理器仍要验证凭据。
- 如何验证白名单安全？——用集成测试覆盖匿名允许、保护路径拒绝和相似路径绕过。

**易错点**

“登录、注册、验证码都必须放行”不是普遍规则。

## 156. Interceptor 如何获取请求头中的 Token？

**面试回答**

在 `preHandle` 中通过 `HttpServletRequest.getHeader` 读取约定请求头。标准 Bearer 用法通常是 `Authorization: Bearer <token>`，解析前要验证认证方案和格式，再交给 JWT 验证组件。

**原理与理解**

HTTP 头名大小写不敏感，但值格式有契约。验证失败通常返回 401；已认证但权限不足通常是 403。Token 不应写入普通日志或错误响应。

**成立条件与边界**

自定义 `token` 头也能工作，但互操作性、代理策略和安全中间件支持通常不如 Authorization。仅 Base64 解码 Payload、只检查过期或信任前端传来的用户 ID 都不安全。

**实际场景（项目核验项）**

项目已确认使用 JWT 拦截器，但具体头名、Bearer 前缀、算法、Claims 和错误码需以代码为准；确认后再形成可背诵的项目答案。

**常见追问**

- Token 缺失与权限不足如何区分？——前者通常 401，后者通常 403。
- 能否在日志中打印 Token 排查？——不应记录完整凭据，可记录脱敏标识和追踪 ID。

**易错点**

获取字符串只是第一步，验签和 Claims 校验才建立可信身份。

## 157. 为什么管理端和用户端可以使用两个拦截器？

**面试回答**

当管理端与用户端确实具有不同凭据、Claims、错误协议或路径边界时，拆成两个拦截器能隔离认证域；若只是权限不同，也可以共用认证并在授权层按角色或权限判断。

**原理与理解**

双拦截器需要明确互斥或有意叠加的路径、执行顺序、上下文类型和白名单。管理权限不能仅由 URL 前缀决定，最终仍应校验可信 Claims 或服务端权限数据。

**成立条件与边界**

“管理端多校验一个管理员标记”只是可能实现。两个拦截器会增加重复逻辑和路径配置风险，生产系统可考虑多个 Spring Security FilterChain 或统一认证、细粒度授权。

**实际场景（真实项目边界）**

项目已确认存在管理端、用户端两个 JWT 拦截器并配合 ThreadLocal；各自路径、Token 来源和权限差异仍要以代码为准，不使用臆测的类名与字段。

**常见追问**

- 两个链路如何防止串用 Token？——验证各自 issuer/audience/密钥或认证域，并测试跨端拒绝。
- 什么时候不必拆？——认证方式相同、只需按权限授权时可共用认证组件。

**易错点**

拆分的依据是安全域和职责，不是看到 `/admin` 与 `/user` 就机械复制代码。
