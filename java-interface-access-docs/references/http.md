# HTTP Interface Documentation

Use this reference when documenting Spring MVC or similar HTTP endpoints.

## Search Patterns

Start with:

```bash
rg -n "(@RequestMapping|@GetMapping|@PostMapping|@PutMapping|@DeleteMapping|@PatchMapping|@RequestBody|@RequestParam|@PathVariable|@RequestHeader|Result<|Response<)" <project-root> -g '*.java'
```

Narrow by business keyword, endpoint path, controller class, DTO name, or log phrase.

## Facts To Extract

- Controller class, package, source file, class-level mapping, method-level mapping, and final path.
- HTTP method and content type. If `@RequestMapping` has no method, state that the code does not constrain it.
- Method signature with annotations on each parameter.
- Headers from `@RequestHeader`, interceptors, filters, gateway conventions, or constants.
- Request body DTO and query/path parameter DTOs.
- Response wrapper and concrete generic type.
- Service/facade method called by the controller, especially when it mutates request fields.
- Auth/session/user context sources such as thread locals, interceptors, cookies, or tokens.

## DTO Field Rules

For each request/response DTO, inspect:

- Field declarations, inherited fields, comments, `@ApiModelProperty`, `@Schema`, `@JsonProperty`, `@JSONField`, validation annotations, and enum constants.
- Default values and constructor/builder assignments.
- Controller/service code that sets or overwrites fields before downstream calls.
- Serialization caveats such as capitalized Java fields, ignored fields, date formats, or JSON strings embedded in string fields.

Do not mark a field required only because a business flow needs it. Prefer:

- `Yes`: validation annotation, explicit null/blank check, or unavoidable dereference before any fallback.
- `Usually yes`: common successful flow requires it but alternate flows exist.
- `No`: optional, backend-injected, response-only, or used only by special branches.
- `Needs verification`: unclear from available code.

## Output Shape

Use these sections unless the user asks for a different format:

1. Endpoint overview
2. Headers
3. Request body/query/path parameters
4. Response body
5. Behavior and side effects
6. Error cases
7. Request/response examples
8. Source locations

For curl examples, include only non-secret headers and placeholder hosts.
