---
name: java-interface-access-docs
description: Generate or update integration-documentation skills for Java/Spring HTTP APIs and Apache Dubbo facade/RPC interfaces from local project source code and existing Markdown docs. Use when Codex needs to document Controller endpoints, request/response DTOs, headers, Result wrappers, Dubbo service methods, @DubboReference dependencies, consumer setup, sample curl/JSON payloads, or create reusable Codex skills from project HTTP/Dubbo access documents.
---

# Java Interface Access Docs

Use this skill to turn local Java project interfaces into reliable integration docs or narrow API-specific skills. Prefer source-backed facts over memory: locate the Controller/facade, DTOs, wrappers, annotations, configuration, and existing docs before writing.

## Workflow

1. Identify the target project root. If the user does not specify one, start from the current repository and nearby `docs/`, `api/`, `web/`, `controller/`, `facade/`, and `*-api` modules.
2. Run the scanner for a first-pass inventory:

```bash
python3 <skill-dir>/scripts/scan_java_interfaces.py --root <project-root> --format markdown
```

Use `--keyword <term>` to narrow by endpoint path, class name, method name, DTO, or business word.

3. Read the relevant source files and existing Markdown docs. Do not rely only on scanner output; it is an index, not the contract.
4. Choose the documentation path:
   - For HTTP/Spring endpoints, read [references/http.md](references/http.md).
   - For Dubbo facade or RPC interfaces, read [references/dubbo.md](references/dubbo.md).
   - For final document/skill structure, read [references/output-template.md](references/output-template.md).
5. Produce a concise, source-cited integration doc or create a dedicated skill when the interface is reused often. For dedicated skills, keep `SKILL.md` short and put full contracts in `references/<interface-name>.md` when the contract is long.

## Evidence Rules

- Preserve exact Java package names, class names, method signatures, endpoint paths, header names, wrapper types, enum values, config keys, and source file paths.
- Separate observed facts from inference. Mark unclear requiredness, default values, or error codes as "needs verification" instead of guessing.
- Trace wrapper behavior such as `Result<T>`, `Response<T>`, `BaseResult`, or custom Dubbo result DTOs to the concrete fields callers see.
- Inspect DTO validation annotations, field comments, enum constants, builder defaults, controller assignments, and service-level overwrites before declaring client-facing fields.
- Include both provider contract and consumer instructions when documenting Dubbo: dependency artifact, interface FQN, version/group/url if present, and `@DubboReference` example.

## Creating API-Specific Skills

When converting one stable interface into a reusable skill:

1. Name the skill after the interface or endpoint, for example `example-search-api` or `example-facade-api`.
2. In frontmatter `description`, include the exact trigger strings: class FQN, method name, endpoint path, DTO names, and project name.
3. Keep the body to a short pointer plus critical quick facts if the contract is large.
4. Put full request/response tables, examples, behavior notes, and source locations in `references/<api>.md`.
5. Validate with `quick_validate.py`.

## Output Standard

Return or write documentation that lets a caller integrate without re-reading the service code:

- Interface identity: project/module, class, method, path or Dubbo FQN.
- Invocation contract: HTTP method/path/headers/body or Dubbo dependency/reference/method signature.
- Request schema: fields, types, requiredness, defaults, examples.
- Response schema: wrapper, success shape, business data, null/empty behavior.
- Error/exception behavior: business codes, thrown exceptions, fallback behavior.
- Side effects and dependencies: persistence, remote calls, async tasks, config keys.
- Examples: curl/JSON for HTTP; Java consumer snippet for Dubbo.
- Source map: exact files and relevant classes/methods used as evidence.
