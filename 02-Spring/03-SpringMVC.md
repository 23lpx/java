---
category: Spring
priority: P0
status: 未学习
tags:
  - Java后端
  - 面试
  - Spring
---

# SpringMVC

## 126. Spring MVC 是什么？

**面试回答**

Spring MVC 是 Spring Framework 基于 Servlet API 的 Web MVC 框架，以 `DispatcherServlet` 为前端控制器，提供请求映射、参数绑定、校验、异常解析、视图渲染和 HTTP 消息转换等能力。

**原理与理解**

它把 Web 请求协调拆给 `HandlerMapping`、`HandlerAdapter`、参数解析器、返回值处理器、`ViewResolver` 和 `HttpMessageConverter` 等扩展点。Controller 负责协议适配，业务规则通常下沉到 Service。

**成立条件与边界**

Spring MVC 属于 Servlet 阻塞式技术栈，不等于 Spring WebFlux。前后端分离时通常写响应体而非服务器端页面，但 View 并没有“退化成 JSON”，JSON 走的是消息转换分支。

**实际场景（通用工程）**

REST 接口由 Controller 接收 HTTP 输入、调用用例服务并返回 `ResponseEntity` 或响应对象，框架完成协商和序列化。

**常见追问**

- 核心入口是什么？——`DispatcherServlet`。
- MVC 三部分是什么？——Model、View、Controller；在 REST 场景仍应区分模型与协议控制层。

**易错点**

不要回答“Spring MVC 负责处理业务”；它主要负责 Web 请求分派和协议适配。

## 127. 一个 HTTP 请求进入 Spring MVC 后经历哪些流程？

**面试回答**

在请求匹配到 `DispatcherServlet` 后，它通过 `HandlerMapping` 获得 `HandlerExecutionChain`，选择 `HandlerAdapter`，执行拦截器前置逻辑、参数解析和 Controller；随后由返回值处理器写响应体或生成 `ModelAndView`，异常则交给 `HandlerExceptionResolver`，最后完成渲染和清理回调。

**原理与理解**

`RequestMappingHandlerAdapter` 内部组合参数解析器、数据绑定、校验、消息转换器和返回值处理器。REST 返回值可能在 HandlerAdapter 执行期间直接写入响应，不一定产生 View。

**成立条件与边界**

Filter 位于 Servlet 链更外层；异步请求会退出原线程并可能再次 dispatch，不能把所有请求背成一次线程内的固定直线。

**实际场景（通用工程）**

JSON 请求先按映射定位方法，再由消息转换器反序列化并校验，业务返回对象后经内容协商选择转换器写回。

**常见追问**

- 谁负责找 Handler？——`HandlerMapping`。
- 谁真正调用 Controller？——合适的 `HandlerAdapter`。

**易错点**

不要漏掉拦截器、异常解析和返回值处理，也不要说 Controller 必然返回 `ModelAndView`。

## 128. DispatcherServlet 有什么作用？

**面试回答**

`DispatcherServlet` 是 Spring MVC 的前端控制器，统一协调 Handler 查找、适配执行、异常处理、视图解析和响应完成，但不承载具体业务逻辑。

**原理与理解**

它继承 Servlet 基础类，由 Servlet 容器按映射接收请求，并委托给配置在 `WebApplicationContext` 中的 MVC 策略组件。不同 Handler 类型可由不同 Adapter 执行。

**成立条件与边界**

并非服务器上的“所有请求”必然经过它：Filter、其他 Servlet、容器默认资源和 servlet mapping 会影响路径。静态资源若由 MVC 的资源 Handler 处理，则仍可进入其映射链路。

**实际场景（通用工程）**

API 路径映射到 DispatcherServlet 后，框架负责找到 Controller 和转换返回值，业务 Service 对 Servlet API 保持低耦合。

**常见追问**

- 它是 Servlet 吗？——是。
- 为什么需要 HandlerAdapter？——让 DispatcherServlet 以统一方式调用不同 Handler 模型。

**易错点**

“统一入口”是相对其 Servlet 映射而言，不是整个 Web 容器的绝对第一站。

## 129. HandlerMapping 有什么作用？

**面试回答**

`HandlerMapping` 根据当前请求查找 Handler，并返回包含 Handler 与拦截器链的 `HandlerExecutionChain`；注解式 Controller 常由 `RequestMappingHandlerMapping` 处理。

**原理与理解**

映射条件不只包含 URL，还可包含 HTTP 方法、请求参数、请求头、`consumes` 和 `produces` 等。启动时框架注册映射，运行时选择最匹配项。

**成立条件与边界**

Handler 不一定是 Controller 方法；资源处理器等也可成为 Handler。HandlerMapping 只负责选择，不负责参数绑定或方法执行。

**实际场景（通用工程）**

同一路径可按 GET、POST 或媒体类型映射到不同方法；冲突映射应在启动或匹配阶段暴露，而不是靠代码顺序选择。

**常见追问**

- 返回的只有 Handler 吗？——通常是 `HandlerExecutionChain`，还包含适用拦截器。
- 多个 Mapping 如何使用？——DispatcherServlet 按已配置顺序查找能够处理请求的映射器。

**易错点**

不要把映射规则缩成“路径到方法”的单一 Map。

## 130. Controller 是如何匹配到请求的？

**面试回答**

`RequestMappingHandlerMapping` 读取类和方法上的 `@RequestMapping` 及组合注解，形成路径、HTTP 方法、参数、请求头和媒体类型等条件；请求必须满足组合后的条件才能命中 HandlerMethod。

**原理与理解**

类级条件提供共享范围，方法级条件进一步缩小。路径变量在匹配后提取，参数与请求体随后由 HandlerAdapter 解析。

**成立条件与边界**

路径正确但 HTTP 方法不匹配通常对应 405；请求媒体类型不受支持可能是 415，响应媒体类型无法满足 `Accept` 可能是 406。实际结果还受异常处理和容器配置影响。

**实际场景（通用工程）**

`@RequestMapping("/orders")` 配合 `@GetMapping("/{id}")` 形成查询映射；写操作用相应 HTTP 语义和 `consumes` 约束 JSON。

**常见追问**

- 为什么同一路径能有多个方法？——其他映射条件不同。
- 模糊匹配冲突怎么办？——框架按具体度规则选择，无法消歧时报告歧义。

**易错点**

Controller 匹配不仅看 URL 与注解名称。

## 131. `@Controller` 和 `@RestController` 有什么区别？

**面试回答**

`@Controller` 声明 MVC Controller；`@RestController` 组合了 `@Controller` 与类级 `@ResponseBody`，因此其处理方法默认把返回值作为响应体，而不是按视图名解释。

**原理与理解**

最终行为仍由返回值类型和 `HandlerMethodReturnValueHandler` 决定。`@ResponseBody` 返回值通常交给 `HttpMessageConverter`；普通 Controller 可以返回视图名、`ModelAndView`，也可在单个方法上加 `@ResponseBody`。

**成立条件与边界**

`@RestController` 不等于“返回值一定是 JSON”：字符串、字节、JSON 或其他格式取决于返回类型、可用转换器和内容协商。特殊返回类型也有自己的处理器。

**实际场景（通用工程）**

前后端分离 API 常使用 `@RestController`；服务端页面使用 `@Controller` 与模板视图，两者也可在同一应用并存。

**常见追问**

- `@ResponseBody` 做什么？——经返回值处理器把结果写入 HTTP 响应体。
- REST Controller 能返回 `ResponseEntity` 吗？——可以，并能明确状态和响应头。

**易错点**

“RestController 自动转 JSON”只在存在合适 JSON 转换器且协商选择它时成立。

## 132. `@RequestMapping` 有什么作用？

**面试回答**

`@RequestMapping` 在类或方法上声明请求映射条件，包括路径、HTTP 方法、参数、请求头、可消费媒体类型和可生产媒体类型；`@GetMapping` 等是针对方法的组合注解。

**原理与理解**

类级映射定义共享条件，方法级映射通常进一步缩小范围。`value` 与 `path` 是别名，`consumes` 对应请求 `Content-Type`，`produces` 参与响应内容协商。

**成立条件与边界**

条件组合并非简单字符串拼接的全部语义；同一元素上不要堆叠多个 `@RequestMapping` 期待全部生效。路径尾斜杠、大小写和路径匹配策略也可能因配置与版本不同。

**实际场景（通用工程）**

类上声明 `/orders`，方法上用 `@PostMapping(consumes="application/json")` 限定创建接口接受的表示格式。

**常见追问**

- 能否限制请求头？——可以使用 `headers` 条件。
- `produces` 与 `Content-Type` 什么关系？——它描述可生成的响应媒体类型，并与客户端 `Accept` 协商。

**易错点**

不要只把 `@RequestMapping` 记作 URL 注解。

## 133. `@GetMapping` 和 `@PostMapping` 有什么区别？

**面试回答**

它们分别是限定 GET 和 POST 的 `@RequestMapping` 组合注解。差异首先是 HTTP 方法语义：GET 应是安全且幂等的读取；POST 用于由目标资源处理表示，常见于创建、命令或非幂等操作。

**原理与理解**

映射注解只限制方法并提供条件，不决定参数必须放在哪里。GET 仍有请求头和查询参数，POST 也可有查询参数；请求体是否解析由方法参数与媒体类型决定。

**成立条件与边界**

POST 不等于“新增”，GET 也不是因“参数在 URL”才用于查询。缓存、重试、预取和安全工具依赖 HTTP 语义，不能用 GET 执行扣款、删除等副作用。

**实际场景（通用工程）**

查询订单使用 GET；提交订单命令可使用 POST，并通过幂等键额外处理重复提交，而不是假设 POST 天然幂等。

**常见追问**

- 还有哪些组合注解？——`@PutMapping`、`@PatchMapping`、`@DeleteMapping`。
- 方法不匹配会怎样？——通常形成 405 响应。

**易错点**

不要回答“GET 参数只能放 URL、POST 参数只能放请求体”。

## 134. `@RequestParam` 和 `@PathVariable` 有什么区别？

**面试回答**

`@RequestParam` 读取 Servlet 请求参数，常来自查询字符串、表单或 multipart 字段；`@PathVariable` 读取已匹配路径模板中的变量。前者多表达筛选/选项，后者多标识资源路径的一部分。

**原理与理解**

两者都支持类型转换、名称和 required 语义。`@RequestParam` 可给默认值，给出默认值也会隐含非必需；`@PathVariable` 必须对应映射模板中的变量。

**成立条件与边界**

URL 设计是接口契约而非注解强制：复杂筛选可以使用查询对象，资源 ID 也不应因放进路径就跳过权限和存在性校验。

**实际场景（通用工程）**

`GET /orders/{id}` 用路径变量定位订单，`?status=PAID&page=1` 用请求参数筛选和分页。

**常见追问**

- `@RequestParam(required)` 默认值？——默认 true，除非使用可选形式或默认值等。
- 能获取多个同名参数吗？——可绑定为集合、数组或 MultiValueMap。

**易错点**

Servlet request parameter 不只等于“问号后的参数”。

## 135. `@RequestBody` 有什么作用？

**面试回答**

`@RequestBody` 让 Spring MVC 通过 `HttpMessageConverter` 读取 HTTP 请求体，并按声明类型和请求媒体类型反序列化为方法参数。

**原理与理解**

框架根据目标类型和 `Content-Type` 选择能读取的转换器；JSON 常由 Jackson 转换器处理。配合 `@Valid`/`@Validated` 可在转换后触发 Bean Validation。

**成立条件与边界**

请求体不只可以是 JSON，也可能是文本、字节或 XML，取决于转换器。一个请求通常只设计一个 Body 参数；流读取、重复读取和大请求体还受 Servlet 与安全限制。

**实际场景（通用工程）**

创建订单接口接收 JSON DTO，显式限制 `consumes`，校验结构后再把 DTO 转为业务命令，避免直接绑定持久化实体。

**常见追问**

- 解析失败常见原因？——媒体类型不支持、JSON 语法或类型不匹配、转换器缺失。
- 与 `@RequestParam` 的区别？——前者读取消息体，后者读取请求参数。

**易错点**

`@RequestBody` 不负责鉴权或业务校验，也不是“只用于 POST JSON”。

## 136. Spring MVC 如何完成参数绑定？

**面试回答**

`HandlerAdapter` 通过一组 `HandlerMethodArgumentResolver` 解析方法参数；简单请求参数和模型属性还会使用 `WebDataBinder`、`ConversionService`，请求体则委托 `HttpMessageConverter`。

**原理与理解**

不同解析器支持 `@PathVariable`、`@RequestParam`、`@ModelAttribute`、`@RequestBody`、请求头以及 Servlet 原生对象。解析后可执行类型转换、数据绑定和校验。

**成立条件与边界**

不是所有参数都经过 JSON 转换，也不是所有绑定失败都抛同一种异常。字段白名单、日期格式、集合大小和嵌套深度需要控制，避免 over-binding 与资源消耗。

**实际场景（通用工程）**

分页查询用查询对象绑定并限制最大页大小；JSON 命令用 DTO + Bean Validation，自定义用户上下文可通过专用 ArgumentResolver 提供。

**常见追问**

- 如何自定义参数解析？——实现 `HandlerMethodArgumentResolver` 并注册。
- 参数绑定和业务校验相同吗？——不同，绑定解决数据到类型，业务校验判断规则。

**易错点**

“参数绑定靠反射”过于粗糙，核心是可扩展的解析、转换与绑定链路。

## 137. Java 对象为什么可以自动转换成 JSON？

**面试回答**

在 `@ResponseBody` 或 `ResponseEntity` 等响应体分支中，返回值处理器通过内容协商选择可写的 `HttpMessageConverter`；若 Jackson 转换器可用且选择 JSON，它用配置好的 `ObjectMapper` 序列化对象。

**原理与理解**

转换器选择受返回类型、`Accept`、`produces` 和已注册媒体类型影响。Jackson 的属性发现、命名、日期、空值和注解规则都可定制。

**成立条件与边界**

Spring MVC 不保证所有对象都能序列化，也不保证一定使用 Jackson。循环引用、懒加载代理、不可访问属性和不受信任类型都可能产生问题，响应 DTO 比直接暴露实体更稳定。

**实际场景（通用工程）**

Controller 返回明确的响应 DTO，统一配置时间和枚举格式，并用接口测试锁定 JSON 契约。

**常见追问**

- 如何忽略字段？——可用 Jackson 注解或专用 DTO，后者更能隔离领域模型。
- 谁设置 Content-Type？——选中的消息转换器与返回值处理链。

**易错点**

不是“Spring 用反射自动转 JSON”一句话就能覆盖转换器选择和 ObjectMapper 配置。

## 138. JSON 请求为什么可以转换成 Java 对象？

**面试回答**

`@RequestBody` 参数解析器选择支持 `application/json` 和目标类型的消息转换器，Jackson 转换器再根据 `ObjectMapper` 配置把 JSON 反序列化为 Java 对象。

**原理与理解**

Jackson 可使用构造器、`@JsonCreator`、record 组件、setter 或字段等多种创建和赋值方式；字段名、未知属性、泛型类型与日期格式都会影响结果。

**成立条件与边界**

“必须有无参构造 + setter”不成立。转换成功也只说明结构可绑定，仍需 Bean Validation、业务校验和授权；未知字段是否报错取决于 ObjectMapper 配置。

**实际场景（通用工程）**

请求 DTO 明确声明允许字段和校验规则，接口测试覆盖缺字段、未知字段、类型错误和超大载荷。

**常见追问**

- 字段名不同怎么办？——使用稳定 DTO 或 `@JsonProperty` 等映射配置。
- 泛型对象如何保留类型？——Spring 根据方法参数的泛型类型信息传给转换器。

**易错点**

JSON 到对象不是“序列化的完全对称过程”，构造和可写属性规则可能不同。

## 139. Spring MVC 如何处理返回值？

**面试回答**

Controller 返回后，`HandlerMethodReturnValueHandler` 根据注解和类型选择处理方式：写响应体、设置状态与头、填充 Model、返回视图、启动异步处理等。

**原理与理解**

`@ResponseBody`、`HttpEntity`/`ResponseEntity` 通常经 `HttpMessageConverter` 写出；视图分支形成 `ModelAndView` 后由 `ViewResolver` 与 View 渲染。异常由 HandlerExceptionResolver 链处理。

**成立条件与边界**

返回 String 在 `@RestController` 中通常是响应体，在普通 `@Controller` 中可能是视图名，但仍受方法注解和返回值处理器影响。统一包装响应可使用显式 DTO 或 `ResponseBodyAdvice`，需避免重复包装和文件流等特殊类型。

**实际场景（项目核验项）**

项目已确认存在统一响应结构；还应核对是 Controller 显式返回、Advice 包装还是其他机制，再描述其状态码和异常映射。

**常见追问**

- 如何自定义响应状态？——使用 `ResponseEntity`、`@ResponseStatus` 或异常映射。
- 响应对象何时转 JSON？——响应体处理分支选中 JSON 转换器时。

**易错点**

Controller 返回对象不等于框架必然返回 200 JSON。

## 140. `Content-Type` 是什么？

**面试回答**

`Content-Type` 表示当前 HTTP 消息体的媒体类型，并可携带该媒体类型定义的参数，例如某些文本类型的字符集；请求和响应都可以使用它。

**原理与理解**

服务端依据请求 `Content-Type` 选择读取转换器，依据客户端 `Accept`、处理方法的 `produces` 和可用转换器协商响应类型。前者描述“我发送的是什么”，后者描述“我希望接收什么”。

**成立条件与边界**

Content-Type 不是通用“文件格式保证”，声明与实际内容不一致仍会解析失败。请求类型不支持通常对应 415，无法生成可接受响应通常对应 406。

**实际场景（通用工程）**

发送 JSON 时设置 `Content-Type: application/json`，下载文件时返回准确媒体类型和内容处置头，并限制可接受的上传类型与大小。

**常见追问**

- 表单常见类型？——`application/x-www-form-urlencoded` 和 `multipart/form-data`。
- `Accept` 与它的区别？——Accept 面向期望的响应表示。

**易错点**

不要把 Content-Type 与 Content-Encoding、字符编码或 Accept 混为一谈。

## 141. `application/json` 是什么意思？

**面试回答**

`application/json` 是注册的 JSON 媒体类型，表示消息体使用 JSON 文本语法；它常作为请求 Content-Type 或响应协商结果。

**原理与理解**

Spring MVC 在有可用 JSON 转换器时可读取或写出该类型。客户端发送 `Accept: application/json` 表达希望得到 JSON，服务端实际响应仍由映射条件、协商与转换器共同决定。

**成立条件与边界**

不带该 Content-Type 不一定总返回 415，取决于端点 `consumes`、参数类型和可用转换器；反之，写了头也不能让非法内容变成 JSON。标准 `application/json` 没有定义 charset 参数，JSON 在网络交换中通常使用 UTF-8。

**实际场景（通用工程）**

接口契约同时约定媒体类型、字段语义、错误结构和版本策略，并通过契约测试验证，而不是只检查一个请求头。

**常见追问**

- 与 `text/plain` 的区别？——媒体类型和处理语义不同，后者不是结构化 JSON 契约。
- JSON 头正确但解析失败为什么？——内容语法、字段类型或转换配置仍可能错误。

**易错点**

`application/json` 只声明表示类型，不保证内容合法、字段可信或业务有效。
