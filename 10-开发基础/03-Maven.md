---
category: 开发基础
priority: P1
status: 未学习
tags:
  - Java后端
  - 面试
  - 开发工具
---

# Maven

## 561. Maven 是什么？

**面试回答**

Maven 是 Java 项目的构建和依赖管理工具，通过一个 pom.xml 配置项目信息、依赖、构建插件，用统一命令完成编译、测试、打包、发布等构建过程。

**理解**

Maven 解决「项目构建标准化」：以前每个项目手动下 jar 包、写不同构建脚本，混乱。Maven 用「约定优于配置」——统一目录结构（src/main/java 等）、统一生命周期（编译、测试、打包）、用 pom.xml 声明依赖，Maven 自动下载依赖并执行构建。

**场景**

项目用 Maven 管理依赖、统一构建，团队每个人用相同的 pom.xml 和构建流程，保证一致性。

**常见追问**

- Maven 干什么？（构建 + 依赖管理）
- 核心配置文件？（pom.xml）

**易错点**

Maven 两个核心能力「依赖管理」和「构建」都要答到；它靠 pom.xml 和统一生命周期工作。

## 562. Maven 解决什么问题？

**面试回答**

解决依赖管理和构建标准化问题：不用手动下载、管理 jar 包及其传递依赖，统一项目的构建流程（编译、测试、打包），让不同环境、不同人构建结果一致。

**理解**

手动管理 jar 的问题：要自己下载、版本冲突、依赖它的其他 jar（传递依赖）要自己找。Maven 只需在 pom.xml 声明依赖，它自动下载、处理传递依赖和版本。构建方面，Maven 用统一生命周期和插件，一条命令完成编译测试打包，规范了流程。

**场景**

项目里不用往 lib 里手动塞 jar，pom 声明依赖即可；CI 里 `mvn package` 一条命令打出可部署的包。

**常见追问**

- 解决哪两大问题？（依赖管理、构建标准化）
- 手动管 jar 有什么问题？（下载麻烦、版本冲突、传递依赖难找）

**易错点**

Maven 的价值是「自动依赖管理 + 标准化构建」，不只是「下载 jar 包」。

## 563. `pom.xml` 是什么？

**面试回答**

pom.xml 是 Maven 项目的核心配置文件（Project Object Model），描述项目的基本信息、依赖、插件、构建配置等，Maven 根据它来下载依赖和执行构建。

**理解**

pom 是「项目说明书」：里面声明 groupId/artifactId/version（坐标）、依赖列表（dependencies）、构建插件（plugins）、打包方式等。Maven 读到 pom，就知道这个项目要哪些依赖、怎么构建。它是 Maven 项目的入口和灵魂。

**场景**

项目里在 pom.xml 里加 Spring Boot 等依赖、配置打包插件，Maven 据此构建项目。

**常见追问**

- pom 是什么？（项目对象模型，核心配置）
- pom 里声明什么？（依赖、插件、坐标等）

**易错点**

pom.xml 是「Maven 项目的核心配置」，依赖、构建都靠它；groupId/artifactId/version 是它的坐标三要素。

## 564. dependency 是什么？

**面试回答**

dependency 是 pom.xml 里声明的「依赖」，表示项目要用到某个第三方库（jar），通过 groupId、artifactId、version 三个坐标唯一定位，Maven 会自动下载它及它的传递依赖。

**理解**

一个 dependency 就是一个「我要用哪个库」的声明，用坐标三要素定位：groupId（组织/公司）、artifactId（项目/模块名）、version（版本）。Maven 根据坐标去仓库下载对应 jar，并自动处理它依赖的其他 jar（传递依赖）。

**场景**

项目里要连 MySQL，就在 pom 加 mysql-connector-java 的 dependency，Maven 自动下载驱动 jar。

**常见追问**

- 定位一个依赖靠什么？（groupId、artifactId、version 三坐标）
- 传递依赖是什么？（依赖的依赖，Maven 自动拉）

**易错点**

dependency 用「坐标三要素」唯一定位；它还能自动带出「传递依赖」，这是 Maven 依赖管理的核心。

## 565. Maven 本地仓库是什么？

**面试回答**

本地仓库是 Maven 在本机存放已下载 jar 包的目录（默认 ~/.m2/repository），下载过的依赖缓存在这里，之后再用直接从本地取，不用重复下载。

**理解**

Maven 第一次下载某个 jar 后，会存到本地仓库；下次项目再用同样的坐标，直接从本地仓库拿，快且离线可用。本地仓库是「依赖缓存」，避免了每次都去远程下载，也方便多个项目共享同一份 jar。

**场景**

项目第一次构建会下载依赖到本地 ~/.m2/repository，之后构建直接复用，速度快。

**常见追问**

- 本地仓库默认在哪？（~/.m2/repository）
- 它干嘛？（缓存已下载的 jar）

**易错点**

本地仓库是「依赖缓存目录」；第一次下载后复用，不必每次联网下载。

## 566. Maven 的依赖是怎么下载的？

**面试回答**

Maven 根据 pom 里的依赖坐标，先去本地仓库找，找到直接用；找不到就按配置的远程仓库（默认中央仓库 Maven Central）顺序去下载，下载后缓存到本地仓库，供以后使用。

**理解**

下载顺序：本地仓库 → 远程仓库（中央仓库、私服等）。先在本地 ~/.m2 找，有就直接用；没有就去远程仓库（默认 Maven Central，公司常用私服 Nexus）下载，下完存本地。私服通常配置在 settings.xml 或 pom 里，能加速、缓存、管理内部依赖。

**场景**

项目配置了公司私服镜像，依赖先从私服拉取，没有再从中央仓库下载，速度更快。

**常见追问**

- 先找哪里？（本地仓库，再远程）
- 公司一般配什么加速？（私服 Nexus 镜像）

**易错点**

下载顺序是「本地 → 远程」；公司常用「私服」加速和统一管理，别只知道中央仓库。

## 567. Maven 常见生命周期有哪些？

**面试回答**

Maven 有三大生命周期：clean（清理）、default（构建，含编译测试打包部署）、site（生成站点文档）。日常最常用的是 default 里的几个阶段：compile、test、package、install、deploy。

**理解**

生命周期是「一串有序的阶段」，执行后面的阶段会自动先执行前面的。default 生命周期核心阶段：validate（校验）→ compile（编译）→ test（跑测试）→ package（打包）→ verify → install（装本地仓库）→ deploy（发布远程仓库）。执行 `mvn package` 会先自动 compile、test 再打包。

**场景**

项目里 `mvn package` 自动完成编译+测试+打包；`mvn install` 再额外装到本地仓库。

**常见追问**

- 三大生命周期？（clean、default、site）
- 执行 package 会自动跑什么？（先 compile、test）

**易错点**

生命周期阶段「有序」，执行靠后的会先跑前面的；常用 compile/test/package/install 要分清。

## 568. `clean` 是做什么的？

**面试回答**

clean 是 Maven 的清理命令，删除之前构建产生的输出（如 target 目录），让项目回到干净状态，下次构建重新开始。

**理解**

每次构建会在 target 目录生成编译产物（class 文件、jar 包等）。clean 就是把这些构建产物清掉。常用 `mvn clean package` 组合：先清理旧的构建结果，再重新编译打包，避免旧文件残留影响构建结果。

**场景**

项目里打包前用 `mvn clean package`，先清掉旧的 target 再重新构建，保证产物干净正确。

**常见追问**

- clean 清什么？（target 等构建产物）
- 常和什么组合？（clean package，先清后构建）

**易错点**

clean 是「清理构建产物（target）」，不是删除源码；常和 package 组合用。

## 569. `package` 是做什么的？

**面试回答**

package 是 Maven 的打包命令，把项目编译、测试后打成可分发的包（如 jar 或 war），输出到 target 目录。

**理解**

package 会先自动执行前面阶段（compile、test），然后把代码和资源打包成 jar（普通 Java 项目）或 war（Web 项目）。打包方式由 pom 的 packaging 决定。执行 `mvn package` 后，target 目录会出现可部署的包。

**场景**

项目里 `mvn package` 打出 jar 包，部署到服务器运行。

**常见追问**

- package 产出什么？（jar/war，在 target 目录）
- 打包类型由谁定？（pom 的 packaging）

**易错点**

package 是「编译+测试+打包」，会自动跑前面的阶段；产物在 target 目录。

## 570. `install` 是做什么的？

**面试回答**

install 是把项目打包后安装到本地仓库（~/.m2/repository），让本机其他项目可以作为依赖引用这个项目。

**理解**

install 比 package 多一步：package 只把包放 target；install 还把包复制到本地仓库，并按坐标归档。这样本机的其他项目就能在 pom 里声明这个依赖、引用它。它常用于「多个项目之间有依赖」的情况。

**场景**

项目里某个公共模块开发完，`mvn install` 装到本地仓库，其他项目就能引用这个模块。

**常见追问**

- install 和 package 区别？（install 多一步：装到本地仓库）
- 装到哪？（本地仓库 ~/.m2/repository）

**易错点**

install = package + 安装到本地仓库；它让「本机其他项目」能依赖这个项目，不是发布到远程。

## 571. 什么是 Maven 依赖冲突？

**面试回答**

依赖冲突指项目中不同的依赖引入了同一个库的不同版本，Maven 需要从中选一个，可能选错导致运行时类找不到或行为异常（比如方法不存在、NoSuchMethodError）。

**理解**

比如 A 依赖了 guava 30，B 依赖了 guava 20，项目同时引入 A、B，就出现两个版本的 guava。Maven 用「就近原则」等策略选一个版本，但可能选到和代码不匹配的版本，运行时报 NoSuchMethodError 等问题。解决：用 dependencyManagement 统一版本、用 exclusions 排除、或看依赖树 mvn dependency:tree 定位。

**场景**

项目里引入多个 starter 时可能出现版本冲突，用 `mvn dependency:tree` 查依赖树、用 exclusions 排除冲突版本。

**常见追问**

- 冲突怎么产生？（同一库不同版本被间接引入）
- 怎么排查？（mvn dependency:tree）
- 怎么解决？（统一版本、exclusions 排除）

**易错点**

依赖冲突的典型表现是「NoSuchMethodError/ClassNotFound」；用 dependency:tree 定位、exclusions 排除、dependencyManagement 统一版本解决。
