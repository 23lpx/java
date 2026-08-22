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

Spring MVC 是 Spring 框架中基于 MVC 设计模式构建 Web 应用的模块，负责接收请求、处理业务、返回响应，核心是 DispatcherServlet 前端控制器。

**理解**

MVC 即 Model（数据）、View（视图）、Controller（控制器）。Spring MVC 把 HTTP 请求的处理拆成一条清晰的链路：请求 → DispatcherServlet → HandlerMapping 找处理器 → Controller 处理 → 返回 ModelAndView 或数据 → 视图/响应渲染。它让 Web 开发分层清晰、可测试。

**场景**

项目里的 Controller 层就是 Spring MVC 的体现，接收前端请求、调用 Service、返回 JSON 给前端。

**常见追问**

- MVC 三个字母指什么？（Model、View、Controller）
- Spring MVC 的核心组件是什么？（DispatcherServlet）

**易错点**

Spring MVC 是 Spring 的一部分（Web 模块），不是独立框架；现在做前后端分离，View 常退化为「返回 JSON 数据」。

## 127. 一个 HTTP 请求进入 Spring MVC 后经历哪些流程？

**面试回答**

大致流程：请求先到 DispatcherServlet → 通过 HandlerMapping 找到对应的 Handler（Controller 方法）→ 经过 HandlerAdapter 执行 Handler → 返回结果（ModelAndView 或数据）→ 视图解析/消息转换渲染 → 返回响应给客户端。

**理解**

DispatcherServlet 是「总调度」，它自己不干活，把活分给各组件：HandlerMapping 负责「找谁处理」，HandlerAdapter 负责「调用」，ViewResolver/HttpMessageConverter 负责「怎么返回」。整条链路里还穿插拦截器、参数解析、异常处理等。

**场景**

项目里前端发一个 `GET /dish/list`，DispatcherServlet 找到 DishController.list()，解析参数、执行方法，返回 JSON 列表给前端。

**常见追问**

- 谁负责找处理器？（HandlerMapping）
- 参数解析和返回值转换靠什么？（HandlerAdapter 里的 ArgumentResolver 和 HttpMessageConverter）

**易错点**

DispatcherServlet 是「调度中心」不是「处理器」；记流程抓「找 → 调 → 返」三个关键环节。

## 128. DispatcherServlet 有什么作用？

**面试回答**

DispatcherServlet 是 Spring MVC 的前端控制器，作为所有请求的统一入口，负责分发请求、协调各组件完成处理，并返回响应。

**理解**

它是整个 MVC 流程的「中央调度器」。所有请求先进来，它根据 HandlerMapping 找到处理器、交给 HandlerAdapter 执行，再处理结果渲染。它本身是 Servlet，配置在 web 容器里，映射到所有请求路径。

**场景**

项目里每个请求都经过 DispatcherServlet 调度，再由它转给具体 Controller 处理。

**常见追问**

- DispatcherServlet 是 Servlet 吗？（是，继承自 HttpServlet）
- 它和 HandlerMapping 什么关系？（它用 HandlerMapping 找处理器，自己负责调度）

**易错点**

DispatcherServlet 是「入口 + 调度」，不要理解成「具体处理业务的组件」。

## 129. HandlerMapping 有什么作用？

**面试回答**

HandlerMapping 负责建立请求（URL、方法等）与处理器（Handler，通常是 Controller 方法）之间的映射，根据请求找到该由谁处理。

**理解**

它维护「请求路径 → 处理方法」的对应关系。Spring MVC 有多个 HandlerMapping 实现（如 RequestMappingHandlerMapping），启动时扫描 @RequestMapping 等注解，把路径和 Controller 方法登记下来，请求来了按匹配规则找到目标 Handler。

**场景**

项目里 `@GetMapping("/dish/list")` 标注的方法，就是被 RequestMappingHandlerMapping 登记，请求到达时被定位到。

**常见追问**

- Handler 是什么？（就是处理请求的 Controller 方法/对象）
- HandlerMapping 返回什么？（HandlerExecutionChain，包含处理器和拦截器链）

**易错点**

HandlerMapping 只负责「找到处理器」，不负责「执行」，执行是 HandlerAdapter 的事。

## 130. Controller 是如何匹配到请求的？

**面试回答**

通过 @RequestMapping 及其组合注解（@GetMapping、@PostMapping 等）声明路径和方法，启动时被 HandlerMapping 登记，请求来时按 URL + HTTP 方法匹配到对应的 Controller 方法。

**理解**

RequestMappingHandlerMapping 启动时解析注解，建立「路径 + 请求方法 → Controller 方法」的映射表。请求到达，DispatcherServlet 拿 URL 和 HTTP 方法去匹配，命中后交给 HandlerAdapter 执行。路径还支持占位符（@PathVariable）等。

**场景**

项目里 `@PostMapping("/order/submit")` 匹配前端的下单请求，`@GetMapping("/dish/{id}")` 匹配按 id 查菜品。

**常见追问**

- @RequestMapping 的 method 属性做什么用？（限定 HTTP 方法）
- 路径变量怎么匹配？（@PathVariable 配合 {id} 占位符）

**易错点**

匹配不仅看路径，还看 HTTP 方法；路径对但方法错（GET 请求打到 @PostMapping）会 405。

## 131. `@Controller` 和 `@RestController` 有什么区别？

**面试回答**

@Controller 用于标记 MVC 控制器，方法默认返回视图名；@RestController 是 @Controller + @ResponseBody 的组合，方法返回值直接作为响应体（通常是 JSON），适合前后端分离接口。

**理解**

@Controller 传统 MVC 里返回视图（页面）；如果想让 @Controller 的方法也返回 JSON，得手动在方法上加 @ResponseBody。@RestController 把这一步省了，类里所有方法都默认把返回对象序列化成 JSON 写进响应体。

**场景**

项目前后端分离，Controller 都用 @RestController，直接返回 JSON 给前端，不返回视图页面。

**常见追问**

- @ResponseBody 作用？（把返回值写入响应体，而不是当视图名解析）
- @RestController 能返回页面吗？（不直接，它是返回数据；要页面用 @Controller）

**易错点**

@RestController = @Controller + @ResponseBody，别以为它是全新的注解。

## 132. `@RequestMapping` 有什么作用？

**面试回答**

@RequestMapping 把请求（URL 路径、HTTP 方法等）映射到 Controller 的处理方法上，是 Spring MVC 最基础的映射注解。

**理解**

它可以用在类上（统一前缀）和方法上（具体路径），两者路径拼接成完整路径。通过 method 属性限定 GET/POST 等，通过 params、headers 等做更细的条件匹配。@GetMapping、@PostMapping 等是它的简写。

**场景**

项目里类上 `@RequestMapping("/admin/dish")` 统一前缀，方法上 `@GetMapping("/page")` 拼成 `/admin/dish/page`。

**常见追问**

- 类上和方法上的路径怎么组合？（拼接成完整路径）
- @RequestMapping 能限定请求方法吗？（能，method = RequestMethod.GET 等）

**易错点**

类和方法上的路径会「拼接」，不是互相覆盖；注意别少写或重复斜杠。

## 133. `@GetMapping` 和 `@PostMapping` 有什么区别？

**面试回答**

都是 @RequestMapping 的简写，@GetMapping 限定只处理 GET 请求，@PostMapping 限定只处理 POST 请求，语义更清晰。

**理解**

GET 一般用于查询、参数放 URL 里、幂等；POST 一般用于提交/新增、参数放请求体里。用对应注解能表达意图，也让匹配更明确，避免方法不匹配的请求误入。它们都支持指定路径。

**场景**

项目里查询菜品列表、按 id 查详情用 @GetMapping；新增菜品、下单用 @PostMapping。

**常见追问**

- 它们和 @RequestMapping 什么关系？（是它的快捷方式，等价于 method 属性）
- 还有其他简写吗？（@PutMapping、@DeleteMapping、@PatchMapping）

**易错点**

GET 不该用来做有副作用的操作（如新增、删除），要把 GET 幂等、POST 变更这个语义用对。

## 134. `@RequestParam` 和 `@PathVariable` 有什么区别？

**面试回答**

@RequestParam 用来接收 URL 查询参数或表单参数（如 `?id=1`）；@PathVariable 用来接收 URL 路径中的占位符（如 `/dish/{id}`）。

**理解**

@RequestParam 对应「问号后面的参数」或表单字段，可指定 name、required、defaultValue；@PathVariable 对应「路径里 {} 占位符」的值，通常用于 RESTful 风格按资源定位。两者取值的来源位置不同。

**场景**

项目里分页查询 `?page=1&pageSize=10` 用 @RequestParam；按 id 查详情 `/dish/{id}` 用 @PathVariable。

**常见追问**

- @RequestParam 的 required 默认是？（默认 true，参数缺失会报错）
- 什么时候用 @PathVariable？（路径里用 {} 占位的资源标识）

**易错点**

@PathVariable 取的是「路径占位符」，@RequestParam 取的是「查询参数」，别把 `?id=1` 和 `/{id}` 搞混。

## 135. `@RequestBody` 有什么作用？

**面试回答**

@RequestBody 把 HTTP 请求体里的内容（通常是 JSON）读取出来，反序列化成 Java 对象，绑定到方法参数上。

**理解**

POST 请求的 JSON 数据在请求体里，@RequestBody 配合 HttpMessageConverter（如 Jackson）把 JSON 字符串转成目标对象。它常用于接收前端提交的复杂对象。

**场景**

项目里新增菜品、下单时，前端把整个对象序列化成 JSON 提交，后端用 `@RequestBody DishDTO dishDTO` 接收。

**常见追问**

- @RequestBody 靠什么转换 JSON？（HttpMessageConverter，如 Jackson）
- 一个方法能有两个 @RequestBody 吗？（不能，请求体只能读一次）

**易错点**

@RequestBody 读的是「请求体」，不是查询参数；一个方法只能有一个 @RequestBody 参数。

## 136. Spring MVC 如何完成参数绑定？

**面试回答**

通过参数解析器（HandlerMethodArgumentResolver）把请求里的数据（路径变量、查询参数、请求体等）按注解和类型，转换成 Controller 方法的参数。

**理解**

HandlerAdapter 执行 Handler 前，会用一系列 ArgumentResolver 逐个处理方法参数：@PathVariable 用 PathVariableResolver、@RequestParam 用对应解析器、@RequestBody 用消息转换器等。它们从 request 里取数据、做类型转换、绑定到参数。

**场景**

项目里 Controller 方法声明了 @RequestParam、@PathVariable、@RequestBody 参数，Spring MVC 自动按注解把它们绑定好。

**常见追问**

- 参数解析的核心接口？（HandlerMethodArgumentResolver）
- 自定义参数解析器怎么做？（实现该接口并注册）

**易错点**

参数绑定不是「魔法」，是一套可扩展的解析器机制，理解这点就知道为什么能自定义。

## 137. Java 对象为什么可以自动转换成 JSON？

**面试回答**

因为返回对象时，Spring MVC 用消息转换器（HttpMessageConverter，默认是 Jackson）把 Java 对象序列化成 JSON 字符串，写入响应体。

**理解**

@RestController 或 @ResponseBody 触发返回值处理，Spring 根据 Content-Type 选择合适的 HttpMessageConverter，Jackson 的 MappingJackson2HttpMessageConverter 通过反射读取对象字段，按规则序列化成 JSON。序列化依赖 getter 或字段，还可能受注解（如 @JsonIgnore）影响。

**场景**

项目里 Controller 返回 List<Dish> 或 Result 对象，Jackson 自动转成 JSON 返回给前端。

**常见追问**

- 默认用什么库序列化？（Jackson）
- 怎么排除某个字段不序列化？（@JsonIgnore 或 @JsonIgnoreProperties）

**易错点**

对象转 JSON 靠 Jackson 这类库，不是 Spring 自己写的；序列化规则要了解字段/getter 和注解。

## 138. JSON 请求为什么可以转换成 Java 对象？

**面试回答**

因为 @RequestBody 配合消息转换器（默认 Jackson）把请求体里的 JSON 字符串反序列化成 Java 对象，再绑定到方法参数。

**理解**

请求进来时，RequestBody 对应的参数解析器读请求体，交给 Jackson 的 HttpMessageConverter，Jackson 根据目标类型反射创建对象、把 JSON 字段映射到属性。反序列化依赖无参构造 + setter/字段，规则和序列化对称。

**场景**

前端提交的 JSON 菜品数据，后端用 @RequestBody DishDTO 接收，Jackson 自动填好字段。

**常见追问**

- 反序列化需要无参构造吗？（通常需要）
- 字段名不一致怎么办？（@JsonProperty 映射）

**易错点**

JSON 转对象靠 Jackson 的「反射 + 无参构造 + setter」，字段名对不上会映射失败。

## 139. Spring MVC 如何处理返回值？

**面试回答**

方法返回后，Spring MVC 根据返回类型和注解决定怎么处理：返回视图名则视图解析，返回 @ResponseBody/对象则用消息转换器序列化成响应体。

**理解**

有 @ResponseBody（或 @RestController）时，返回值交给 HandlerMethodReturnValueHandler，用 HttpMessageConverter 把对象转成 JSON/文本写入响应；没有则把返回值当视图名交给 ViewResolver 解析。返回值处理也是一套可扩展机制。

**场景**

项目里 Controller 返回 Result<T> 对象，被统一序列化成 JSON 响应体。

**常见追问**

- 返回值处理核心接口？（HandlerMethodReturnValueHandler）
- 想统一包装返回结构怎么做？（自定义返回值处理器或统一在 Controller 里包装）

**易错点**

返回 String 时要注意：@RestController 下 String 是「响应体」，@Controller 下可能被当「视图名」，别搞混。

## 140. `Content-Type` 是什么？

**面试回答**

Content-Type 是 HTTP 头，告诉接收方「请求体/响应体里数据的格式」，常见如 application/json、text/html、application/x-www-form-urlencoded。

**理解**

它是媒体类型（MIME type）的标识，让接收方知道按什么格式解析数据。请求里标明提交数据的格式，响应里标明返回数据的格式。前后端靠它约定数据格式。

**场景**

项目里前端 POST 提交 JSON 时，请求头 Content-Type 是 application/json；后端返回 JSON 时响应头 Content-Type 也是 application/json。

**常见追问**

- application/json 表示什么？（数据是 JSON 格式）
- 表单提交用什么 Content-Type？（application/x-www-form-urlencoded 或 multipart/form-data）

**易错点**

Content-Type 是「数据格式」声明，不是「编码」；格式不对接收方会解析失败（如 415）。

## 141. `application/json` 是什么意思？

**面试回答**

表示数据格式是 JSON（JavaScript Object Notation），即「请求体/响应体里的内容是 JSON 文本」，是前后端交互最常用的数据格式。

**理解**

它是 Content-Type 的一种值，告诉接收方按 JSON 语法解析数据。后端用 @RequestBody 接收时，要求请求的 Content-Type 是 application/json，否则参数解析可能失败；返回时 Spring 也会自动带上这个头。

**场景**

项目里所有接口都用 JSON 交互：前端把对象序列化成 JSON 提交，后端返回 JSON，Content-Type 都是 application/json。

**常见追问**

- application/json 和 text/plain 什么区别？（前者是结构化 JSON，后者是纯文本）
- 发 JSON 请求不带头会怎样？（后端可能解析失败，返回 415）

**易错点**

application/json 是「媒体类型」不是「字符编码」；字符编码是另一个头（charset）。
