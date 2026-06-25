# SLS Environment Mapping

Use this file when selecting Aliyun SLS project, logstore, and container before querying logs.

## Shared Anchors

- Region: `华东1（杭州）`
- Version marker keyword: `APPLICATION VERSION`
- Cross-service correlation key: `EagleEye-TraceID`

## Test Environment

- Project: `example-test-sls-project`
- Logstore: `example-test-logstore`

Known containers:

- Gateway service: `test-example-gateway`
- Application service: `test-example-application`
- Routing service: `test-example-routing`
- Worker service: `test-example-worker`
- Agent service: `test-example-agent`
- Content component: `test-example-content-component`
- Question component: `test-example-question-component`

## Production Gray

- Project: `example-prod-sls-project`
- Logstore: `example-prod-logstore`

Known containers:

- Gateway service: `prod-example-gateway-gray`
- Application service: `prod-example-application-gray`
- Routing service: `prod-example-routing-gray`
- Worker service: `prod-example-worker-gray`
- Agent service: `prod-example-agent-gray`
- Content component: `prod-example-content-component-gray`
- Question component: `prod-example-question-component-gray`

## Production Formal

- Project: `example-prod-sls-project`
- Logstore: `example-prod-logstore`

Known containers:

- Gateway service: `prod-example-gateway-formal`
- Application service: `prod-example-application-formal`
- Routing service: `prod-example-routing-formal`
- Worker service: `prod-example-worker-formal`
- Agent service: `prod-example-agent-formal`
- Content component: `prod-example-content-component-formal`
- Question component: `prod-example-question-component-formal`

## Service Traversal Hint

Start from the service named by the user when available. Otherwise prefer:

1. `example-application` for application flow failures.
2. `example-routing` for request ingress, routing, session, or channel issues.
3. `example-agent`, content component, or question component when logs show downstream calls or callback waits.
