# Output Template

Use this template for generated integration docs or skill reference files. Remove sections that are not relevant.

```markdown
# <Interface Or Endpoint Name> 接入文档

## 接口概述

- 项目/模块: `<module>`
- 类型: HTTP / Dubbo
- 入口: `<controller#method>` or `<facade FQN#method>`
- 源码位置: `<path>`
- 功能: <one sentence>

## 调用方式

### HTTP

- Method: `POST`
- Path: `/example/path`
- Content-Type: `application/json`
- Headers:

| Header | Required | Type | Meaning |
| --- | --- | --- | --- |

### Dubbo

- Interface: `<fully.qualified.Interface>`
- Method: `<method signature>`
- Version/group: `<value or not configured>`
- Consumer reference:

```java
@DubboReference(...)
private ExampleFacade exampleFacade;
```

## 入参

`<RequestDTO>`

| Field | Required | Type | Example | Meaning |
| --- | --- | --- | --- | --- |

## 出参

`<ResponseDTO or wrapper>`

| Field | Type | Meaning |
| --- | --- | --- |

## 行为说明

- <business rule>
- <side effect>

## 异常与错误码

| Case | Code/Exception | Meaning |
| --- | --- | --- |

## 示例

```json
{}
```

## 证据来源

- `<path>:<class or method>`
```

## Skill Reference Pattern

For a dedicated API skill, use a short `SKILL.md`:

```markdown
---
name: <api-skill-name>
description: Use when Codex needs the exact local API contract for <FQN/path/method>, including request/response DTOs, examples, behavior, and source locations in <project>.
---

# <API Name>

Use this skill to answer questions or generate integration code for `<FQN/path/method>`.

Read `references/<api-name>.md` for the full contract, examples, behavior notes, and source locations.
```
