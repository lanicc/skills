# SLS Environment Mapping

Use this file when selecting Aliyun SLS project, logstore, and container before querying logs.

## Shared Anchors

- Region: `华东1（杭州）`
- Version marker keyword: `APPLICATION VERSION`
- Cross-service correlation key: `EagleEye-TraceID`

## Test Environment

- Project: `k8s-log-cf194c581f4c848d8a051abe4c1b2a8de`
- Logstore: `test-app-log`

Known containers:

- Board service: `test-zstt-cleanrender-comments`
- GK service: `test-zstt-jzx-graphickites-comments`
- jzx-home-tutoring: `test-zstt-jzx-home-tutoring`
- jzx-artcManager: `test-zstt-jzx-artcmanager`
- jzx-ai-dual-mentor: `test-zstt-ai-dual-mentor`
- ai-agents: `test-zstt-ai-agents`
- Lecture component: `test-zstt-lecture-component`
- Question component: `test-zstt-question-component`

## Production Gray

- Project: `k8s-log-c292481d697254c0cb6272d5a74f3c5c1`
- Logstore: `prod-app-log`

Known containers:

- Question component: `prod-zstt-question-component-new`
- jzx-home-tutoring: `prod-zstt-jzx-home-tutoring-new`
- jzx-artcManager: `prod-zstt-jzx-artcmanager-new`
- jzx-ai-dual-mentor: `prod-zstt-ai-dual-mentor-new`
- ai-agents: `prod-zstt-ai-agents-new`
- Wrong-question service: `prod-zstt-poseidon-new`

## Production Formal

- Project: `k8s-log-c292481d697254c0cb6272d5a74f3c5c1`
- Logstore: `prod-app-log`

Known containers:

- Question component: `prod-zstt-question-component-base`
- jzx-home-tutoring: `prod-zstt-jzx-home-tutoring-base`
- jzx-artcManager: `prod-zstt-jzx-artcmanager-base`
- jzx-ai-dual-mentor: `prod-zstt-ai-dual-mentor-base`
- ai-agents: `prod-zstt-ai-agents-base`
- Wrong-question service: `prod-zstt-poseidon-base`

## Service Traversal Hint

Start from the service named by the user when available. Otherwise prefer:

1. `jzx-home-tutoring` for application flow failures.
2. `jzx-artcmanager` for request ingress, routing, session, or channel issues.
3. `ai-agents`, lecture component, or question component when logs show downstream calls or callback waits.
