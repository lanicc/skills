---
name: sls-code-log-investigator
description: Investigate production or test issues by deriving log keywords from the current codebase, querying Aliyun SLS in a real browser session, following EagleEye-TraceID or business identifiers across services, and producing a concrete diagnosis. Use when Codex needs to troubleshoot online behavior, search SLS logs, inspect request chains, correlate Java/application logs, analyze exceptions, callbacks, timeouts, deployments, or verify whether a symptom appears in Aliyun Simple Log Service.
---

# SLS Code Log Investigator

Use this skill to start from source-code log anchors and end with a defensible SLS-based diagnosis. Work like an operator: identify exact keywords in the project, query the right SLS environment, pivot from one hit to the full trace, and separate observed facts from inference.

## Workflow

### 1. Build Search Seeds From Code

Extract the strongest anchor before opening SLS:

- Exact user-provided error, `EagleEye-TraceID`, `bizId`, `requestId`, `userId`, callback id, task id, or occurrence time.
- Code-derived anchors: logger messages, exception classes, controller paths, RPC method names, enum names, process keys, callback topics, and fixed status strings.
- Service hints from module names, package names, container names, or deployment names.

When the user gives only a symptom, run:

```bash
python3 <skill-dir>/scripts/extract_log_seeds.py --root <repo> --keyword "<symptom-or-domain-word>"
```

Use `--json` when another script or tool needs structured output. Prefer exact fixed phrases over generic natural-language terms.

### 2. Select Environment And Service

Read [references/environments.md](references/environments.md) when the target environment, project, logstore, or container is not already clear.

Choose the narrowest likely scope:

1. Environment: test, production gray, or production formal.
2. Time range: start with the user's incident window or 5-15 minutes around the observed time.
3. Container/service: start from the service named by the user or inferred from the code anchor.
4. Logstore/project: use the environment mapping, then verify the selected container exists.

### 3. Query SLS In Browser

Use the Browser or Chrome plugin when available so the investigation happens in an authenticated Aliyun console session. Read [references/sls-console-workflow.md](references/sls-console-workflow.md) for the browser steps.

Search from narrow to wide:

1. Exact trace id or business id.
2. Exact fixed log message, exception class, endpoint path, callback topic, or RPC method.
3. Deployment marker such as `APPLICATION VERSION`.
4. Broader fallback terms derived from source code.

Do not mix many loose terms in the first query. Confirm one relevant hit, then pivot using identifiers in that hit.

### 4. Reconstruct The Chain

For each relevant hit, capture:

- Timestamp, service/container, log level, logger/class, and message.
- `EagleEye-TraceID` and any request/business identifiers.
- Upstream/downstream service names and request/response state.
- Whether the line is a direct failure, retry, timeout, fallback, or cleanup log.

Use `EagleEye-TraceID` as the default cross-service correlation key. If no trace id appears, pivot on the most selective business id and exact timestamp.

Read [references/query-patterns.md](references/query-patterns.md) for concrete query and pivot patterns.

### 5. Diagnose

Classify the failure before writing the conclusion:

- No logs: wrong environment, wrong container, wrong time range, request never arrived, or logging gap.
- Logs stop mid-chain: timeout, async break, missing callback, or message not consumed.
- Upstream generic failure: inspect downstream services for the first real stack trace or rejection.
- Deployment-related issue: compare `APPLICATION VERSION`, pod/container, and failure start time.
- Retry/duplicate issue: compare repeated identifiers, timestamps, and status transitions.

Do not claim root cause from a single isolated line when a multi-service chain is plausible.

## Output

Return a concise incident note:

1. Scope: environment, time window, project/logstore, service/container.
2. Entry query: exact keyword, id, or trace used.
3. Evidence: decisive log fields or short log excerpts.
4. Trace path: services traversed in timestamp order.
5. Conclusion: directly observed root cause or most likely cause.
6. Uncertainty and next action: missing query, code fix, config check, retry, or logging gap.

Preserve exact identifiers that support the diagnosis. Do not expose credentials, tokens, or login secrets in the final answer.
