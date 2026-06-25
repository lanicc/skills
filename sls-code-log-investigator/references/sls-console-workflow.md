# SLS Console Workflow

Use this file when operating the Aliyun SLS web console through Browser or Chrome automation.

## Login

- Prefer an existing authenticated browser session.
- If login is required, pause for user-provided authentication or let the user complete the login flow.
- Do not store account passwords, MFA seeds, cookies, or tokens in this skill.
- Do not repeat credentials or secrets in investigation summaries.

## Navigation

1. Open the Aliyun Simple Log Service console.
2. Select region `华东1（杭州）`.
3. Open the mapped project and logstore from `environments.md`.
4. Select the expected time window before searching.
5. Filter by container/service when the UI supports it.
6. Run the narrowest query first.

## Query Operation

- Start with an exact id or exact fixed phrase.
- Inspect a raw log line, not only the table summary.
- Copy the decisive fields: timestamp, container, logger/class, trace id, business ids, and message.
- Re-run the query in adjacent services when a trace id or business id appears.
- Widen the time range only after checking environment, logstore, and container selection.

## Browser Automation Notes

- Use text snapshots to locate project, logstore, time range, query editor, and search buttons.
- Prefer form fill tools for query/time fields.
- When the UI virtualizes log rows, open the raw detail view for each decisive row.
- If a search appears stale, reload or clear the query field before re-running.
- Capture screenshots only when layout or UI state affects the diagnosis.
