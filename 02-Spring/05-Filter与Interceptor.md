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

Filter 是 Java Servlet 规范里的过滤器，在请求进入 Servlet 之前、响应返回客户端之前，对请求和响应做预处理和后处理，如编码、登录态、日志。

**理解**

Filter 是 Web 容器（Servlet 容器）层面的组件，不属于 Spring。它基于「过滤链」，多个 Filter 按顺序依次执行。因为它工作在容器层，比 Spring MVC 更靠前，适合处理通用、与具体 Controller 无关的逻辑（字符编码、CORS 等）。

**场景**

项目里可以用 Filter 做字符编码过滤、统一日志、跨域处理等。

**常见追问**

- Filter 是 Spring 的吗？（不是，是 Servlet 规范的一部分）
- Filter 链怎么执行？（按注册顺序逐个调用，最后才到目标 Servlet/请求）

**易错点**

Filter 在 Servlet 容器层、拦截范围更大；别把它和 Spring 的拦截器混为一谈。

## 148. Interceptor 是什么？

**面试回答**

Interceptor 是 Spring MVC 提供的拦截器，在 Handler（Controller 方法）执行前后做拦截处理，如登录校验、权限判断、日志。

**理解**

Interceptor 是 Spring MVC 层的组件，通过实现 HandlerInterceptor 接口，在 preHandle（执行前）、postHandle（执行后）、afterCompletion（渲染完成后）三个阶段插入逻辑。它比 Filter 更贴近业务，能拿到 Handler 信息，也能使用 Spring 容器的 Bean。

**场景**

项目里用拦截器做 JWT 登录校验：在 preHandle 里校验 token，把用户信息存 ThreadLocal，放行或拦截。

**常见追问**

- Interceptor 属于哪个层？（Spring MVC 层）
- 和 AOP 有关系吗？（都基于代理思想，但 Interceptor 针对 Web 请求，AOP 更通用）

**易错点**

Interceptor 是 Spring MVC 的，Filter 是 Servlet 容器的，层级不同。

## 149. Filter 和 Interceptor 有什么区别？

**面试回答**

主要区别在层级和范围：Filter 属于 Servlet 容器层，在请求进入 Spring MVC 前就拦截，能拦所有请求（含静态资源）；Interceptor 属于 Spring MVC 层，只拦进入 DispatcherServlet 后、到 Controller 的请求，且能使用 Spring 的 Bean。

**理解**

执行顺序上，Filter 先于 Interceptor。Filter 更底层、范围更大，但拿不到 Controller 方法等 Spring 上下文信息；Interceptor 更贴近业务，能获取 Handler、能注入 Spring Bean，适合做登录校验、权限这类业务拦截。两者定位不同，常配合使用。

**场景**

项目里 Filter 做通用编码/跨域，Interceptor 做 JWT 登录校验和用户信息注入（ThreadLocal）。

**常见追问**

- 执行顺序？（Filter 先执行，再进 Interceptor，再到 Controller）
- 登录校验放哪更合适？（业务相关的放 Interceptor 更合适，能拿 Handler 和 Bean）

**易错点**

记清楚「层级不同、范围不同、先后不同」，Filter 更底层更宽，Interceptor 更贴近业务。

## 150. `HandlerInterceptor` 有哪些主要方法？

**面试回答**

主要有三个：preHandle（执行前）、postHandle（执行后、视图渲染前）、afterCompletion（整个请求处理完成后，含渲染）。

**理解**

preHandle 返回 true 才继续往下走（放行），返回 false 则中断请求；postHandle 在 Handler 执行完、视图渲染前调用；afterCompletion 在视图渲染完成、请求结束后调用，常用于清理资源。三个方法配合能覆盖请求的前、中、后。

**场景**

项目里拦截器实现 preHandle 做 token 校验，afterCompletion 里清理 ThreadLocal，防止内存泄漏。

**常见追问**

- preHandle 返回 false 会怎样？（中断请求，后面的拦截器和 Controller 都不执行）
- afterCompletion 一定执行吗？（preHandle 成功放行后才执行）

**易错点**

preHandle 的返回值决定是否放行，别忽略这个布尔值的作用。

## 151. `preHandle()` 在什么时候执行？

**面试回答**

在请求到达 Controller 方法之前执行，是拦截器的第一道关卡，返回 true 放行、返回 false 拦截。

**理解**

DispatcherServlet 找到 Handler 后、调用 Controller 前，先执行所有拦截器的 preHandle。它适合做「前置校验」：校验通过放行，不通过直接返回（如未登录返回 401）。多个拦截器的 preHandle 按注册顺序执行。

**场景**

项目里 JWT 拦截器在 preHandle 里解析并校验 token，失败直接返回「未登录」，不放行到 Controller。

**常见追问**

- preHandle 里能拿到请求信息吗？（能，参数里有 HttpServletRequest/Response）
- 多个拦截器的 preHandle 顺序？（按注册顺序）

**易错点**

preHandle 是「Controller 执行前」，不是「请求最开始」（Filter 比它更早）。

## 152. `postHandle()` 在什么时候执行？

**面试回答**

在 Controller 方法执行完之后、视图渲染之前执行，此时业务已处理完，但响应还没最终渲染。

**理解**

postHandle 能拿到 Handler 执行的结果（ModelAndView，前后端分离时可能是 null），可以在响应给客户端前做额外处理。注意：如果 Controller 抛异常，postHandle 通常不会执行。

**场景**

前后端分离项目里 postHandle 用得较少，更多逻辑放在 preHandle（校验）和 afterCompletion（清理）。

**常见追问**

- postHandle 能改响应吗？（能拿到 ModelAndView，可做修改）
- Controller 抛异常 postHandle 还执行吗？（通常不执行）

**易错点**

postHandle 在「视图渲染前」，不是「整个请求结束后」；异常时它可能不执行。

## 153. `afterCompletion()` 在什么时候执行？

**面试回答**

在整个请求处理完成后执行（包括视图渲染之后），无论中间是否发生异常（只要 preHandle 放行了），常用于资源清理。

**理解**

它是请求生命周期的最后一步，适合做收尾工作：释放 ThreadLocal、关闭资源、记录耗时等。它和 postHandle 的区别是：postHandle 在渲染前且异常时不执行；afterCompletion 在渲染后、且只要 preHandle 成功就执行（异常也会进 afterCompletion）。

**场景**

项目里在 afterCompletion 里 remove 掉 ThreadLocal 里的用户信息，避免线程复用导致信息串号或内存泄漏。

**常见追问**

- afterCompletion 和 postHandle 区别？（时机更晚，且异常时也会执行）
- 为什么用它清 ThreadLocal？（保证每次请求结束后都清理）

**易错点**

afterCompletion 是「清理资源」的最佳位置；它的执行条件是 preHandle 放行成功。

## 154. 为什么 JWT 登录校验适合放在拦截器？

**面试回答**

因为登录校验是「进入 Controller 前」的通用逻辑，拦截器能在 Controller 执行前统一拦截，且能拿到请求信息、注入 Spring Bean、按路径放行，比在每个接口里手写校验更统一。

**理解**

JWT 校验不依赖某个具体业务方法，是横切在 Controller 前的一道闸。拦截器 preHandle 恰好是这个位置：能读请求头取 token、能调用 Service 查用户、能通过 path 匹配决定哪些接口放行。相比 Filter，它更能拿到 Handler 信息和 Spring 上下文；相比 AOP，它更贴合 Web 请求场景。

**场景**

项目里写一个 JwtTokenInterceptor 实现 preHandle 校验 token，把用户 id 存 ThreadLocal，配置拦截路径并放行登录接口。

**常见追问**

- 为什么不放 Filter？（Filter 也能做，但拿不到 Spring 的 Bean 和 Handler 信息，业务校验放拦截器更方便）
- 拦截器里怎么放行登录接口？（配置 excludePathPatterns 或 preHandle 里判断路径）

**易错点**

登录校验放拦截器是「统一 + 贴近业务」的选择，不是唯一方案；要能说清为什么比在每个接口手写或放 Filter 更合适。

## 155. 为什么登录接口必须放行？

**面试回答**

因为登录接口是「获取 token」的入口，用户此时还没有 token，如果拦截器不放过登录接口，用户永远无法登录，形成死循环。

**理解**

登录校验的逻辑是「没有合法 token 就拦截」，而登录接口本身的作用就是「用账号密码换 token」，调用时用户天然没有 token。所以必须把登录、注册这类「获取凭证」的接口配置为放行，否则所有人都会被拦在门外。

**场景**

项目里拦截器配置 excludePathPatterns 把 `/user/login`、`/user/register` 放行，其余接口都要带 token。

**常见追问**

- 还有哪些接口需要放行？（注册、找回密码、验证码等无需登录的接口）
- 怎么放行？（excludePathPatterns 配置，或 preHandle 里判断白名单路径）

**易错点**

登录接口不放行会导致「无法登录」，这是拦截器配置的经典坑。

## 156. Interceptor 如何获取请求头中的 Token？

**面试回答**

通过 preHandle 方法参数里的 HttpServletRequest 对象，调用 `request.getHeader("Authorization")`（或自定义头名）拿到 token。

**理解**

preHandle 的参数里有 HttpServletRequest，可以直接读请求头。常见约定是 `Authorization: Bearer <token>` 或自定义头如 `token`。拿到后做解析、校验（验签、过期时间），再决定放行还是返回 401。

**场景**

项目里前端把 JWT 放在请求头的 token 字段，拦截器 `request.getHeader("token")` 取出来解析校验。

**常见追问**

- Authorization 头格式？（常是 Bearer 加空格加 token）
- 拿到 token 后干什么？（解析验签、查用户、存 ThreadLocal）

**易错点**

token 放哪个头是前后端约定的，取的时候头名要一致；注意 Bearer 前缀和空格的处理。

## 157. 为什么管理端和用户端可以使用两个拦截器？

**面试回答**

因为管理端和用户端校验规则不同（用户端验用户身份，管理端还验管理员权限），拆成两个拦截器可以让职责清晰、按不同路径分别拦截，互不干扰。

**理解**

用户端拦截器只校验「是不是合法登录用户」；管理端拦截器在用户校验基础上还要校验「是不是管理员」，甚至可能校验不同来源（如用户端 token 和管理端 token 分开）。拆开后各自配置拦截路径，逻辑清晰、便于维护。

**场景**

项目里用户端接口走 JwtTokenUserInterceptor，管理端接口走 JwtTokenAdminInterceptor，分别配置 /user/** 和 /admin/** 路径。

**常见追问**

- 两个拦截器的校验差异？（用户端验登录，管理端额外验管理员身份）
- 拆开有什么好处？（职责单一、路径清晰、便于各自扩展）

**易错点**

拆两个拦截器是「按业务职责和路径」拆分，不是为了拆而拆；关键是两者的校验逻辑确实不同。
