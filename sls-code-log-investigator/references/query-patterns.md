# Query Patterns

Use this file when concrete SLS search pivots or diagnosis output structure are needed.

## Entry Patterns

### Exact Trace

Use when `EagleEye-TraceID` is known.

- Query the exact trace id in the most likely container first.
- Confirm one valid hit.
- Re-run the same trace in upstream and downstream containers.
- Sort hits by timestamp to identify the first failure transition.

### Exact Error Token

Use when an exception class, fixed log message, endpoint, or callback topic is known.

Examples:

- `NullPointerException`
- `/callback`
- `timeout`
- exact enum, delegate, controller, or process key from source code

After the first hit, pivot to the trace id and business ids found in that line.

### Version And Deployment Suspicion

Use when the issue begins after a release or restart.

- Search `APPLICATION VERSION`.
- Inspect startup logs around the incident window.
- Compare old/new pods and gray/base containers.
- Check whether failing requests all land on the same version or container set.

### No-result Fallback

If a query returns no results, check in this order:

1. Correct environment.
2. Correct logstore.
3. Correct container filter.
4. Tight but valid time range.
5. Identifier spelling and exact case.
6. Whether the request failed upstream before entering the current service.

## Diagnosis Template

```text
Environment: test / prod-gray / prod-formal
Time window: 2026-06-05 14:00-14:10 CST
Entry query: exact keyword, id, or trace used

Observed facts:
- 14:02:11 service-a accepted request with trace xxx.
- 14:02:12 service-b called downstream service with bizId yyy.
- 14:02:42 downstream returned timeout / no matching callback log was found.

Trace path:
- client -> service-a -> service-b -> downstream

Conclusion:
- The first confirmed failure appears in downstream, not in service-b.

Next step:
- Inspect downstream dependency logs for the same trace or callback id.
```

## Repository-specific Anchors

- `APPLICATION VERSION`
- `EagleEye-TraceID`
- `example-application`
- `example-routing`
- `example-worker`
- `example-agent`

For Java-side failures, search the exact class, delegate, process key, controller path, or log message from the codebase before broadening to generic terms.
