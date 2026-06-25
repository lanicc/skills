# Skills

这个仓库包含 3 个用于本地开发和排查流程的 Codex skill。

## Skill 概览

| Skill | 用途 | 典型场景 |
| --- | --- | --- |
| `git-branch-management` | 按项目规则创建、重命名和记录 Git 分支。 | 开始需求、微调优化或缺陷修复分支，并同步维护 `git-branchs.md`。 |
| `java-interface-access-docs` | 基于 Java/Spring HTTP 接口和 Apache Dubbo 接口源码生成接入文档。 | 文档化 Controller 接口、DTO、响应包装、Dubbo facade、消费方示例，或创建接口专用 skill。 |
| `sls-code-log-investigator` | 从代码中提取日志检索线索，并在阿里云 SLS 中追踪问题链路。 | 通过日志关键词、TraceID、业务 ID、部署版本或异常链路排查测试/生产问题。 |


## 目录结构

```text
.
├── git-branch-management/
│   └── SKILL.md
├── java-interface-access-docs/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── scripts/
└── sls-code-log-investigator/
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── scripts/
```

## Skill 说明

### `git-branch-management`

用于根据任务类型选择合适的分支前缀，并生成统一格式的分支名：

- `feature/yyyyMMdd_requirement-short-name`：新需求或较大的用户可见能力。
- `develop/yyyyMMdd_adjustment-short-name`：小优化、微调、清理或低风险改动。
- `bugfix/yyyyMMdd_bug-short-name`：缺陷、回归、错误行为或失败流程修复。

该 skill 还会维护仓库根目录下的 `git-branchs.md`，为每个分支记录中文说明。

### `java-interface-access-docs`

用于把 Java 项目源码转换成可信的接口接入文档。它会辅助扫描 Spring MVC 映射、Dubbo 服务/引用、DTO、响应包装、注解、校验规则和已有 Markdown 文档。

常见产出包括：

- HTTP 接口契约。
- Dubbo facade 接口契约。
- 请求和响应字段表。
- 错误、异常和副作用说明。
- Curl、JSON 或 Java 消费方示例。
- 每个结论对应的源码位置证据。

### `sls-code-log-investigator`

用于从代码到日志完成问题排查。它会从源码中提取稳定的日志检索线索，再指导在 SLS 中查询、跳转和重建调用链路。

适合处理：

- 使用 `EagleEye-TraceID`、业务 ID、请求 ID 或精确报错文本检索日志。
- 从代码中提取日志关键词、异常类名、接口路径和固定状态值。
- 沿着上下游服务追踪一次请求。
- 比对 `APPLICATION VERSION` 等部署标记。
- 输出包含观察事实、链路路径、结论和不确定性的简洁排查记录。

## 隐私说明

这些 skill 面向本地源码和内部日志使用。提交或共享生成结果前，应避免包含：

- 凭据、token、cookie 或 session 数据。
- 不应外部共享的真实生产环境标识。
- 包含用户数据的原始日志片段。
- 私有代码库中的源码片段，除非该仓库本身允许保存这些内容。

仓库中的示例环境和服务标识使用 `example-*` 这类泛化名称。
