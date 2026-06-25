# Dubbo Interface Documentation

Use this reference when documenting Apache Dubbo facade, provider, or consumer interfaces.

## Search Patterns

Start with:

```bash
rg -n "(@DubboService|@DubboReference|@Reference|@Service|interface .*Facade|interface .*Service|org\\.apache\\.dubbo|com\\.alibaba\\.dubbo)" <project-root> -g '*.java'
```

Also inspect `pom.xml`, `build.gradle`, `application*.yml`, `application*.properties`, and `bootstrap*.yml` for artifact, registry, group, version, timeout, retries, and protocol settings.

## Provider Contract

Extract:

- Interface FQN, module/artifact, source file, and package.
- Provider implementation class and annotation (`@DubboService`, XML, Spring `@Service` exporting through config, or other local pattern).
- Method signatures, parameter DTOs, return DTOs, checked/unchecked exceptions, and business exception type.
- Version, group, timeout, retries, protocol, registry, and serialization settings when explicit.
- Whether the method is idempotent, read-only, writes data, sends messages, or calls downstream services.

## Consumer Contract

Include a consumer example when possible:

```java
@DubboReference(version = "1.0.0")
private ExampleFacade exampleFacade;
```

If the code uses Maven modules, include the likely dependency:

```xml
<dependency>
  <groupId>...</groupId>
  <artifactId>...</artifactId>
  <version>...</version>
</dependency>
```

Mark dependency coordinates as inferred when they come from module names rather than resolved build metadata.

## DTO And Return Rules

- Document request DTO fields with type, requiredness, default, format, enum values, and example.
- Document return DTO fields and wrapper objects separately.
- For `Boolean`, `String`, `List<T>`, and nullable returns, state exact success, empty, and null semantics if visible in implementation or docs.
- For exceptions, name the thrown type and business code/message source when visible.

## Output Shape

Use these sections unless the user asks for a different format:

1. Interface overview
2. Consumer dependency and reference configuration
3. Method list
4. Per-method request DTO
5. Per-method response DTO
6. Exceptions and business rules
7. Java invocation examples
8. Source locations

When creating a dedicated skill for a Dubbo interface, put exact FQN, facade name, method names, DTO names, and project name in the skill description so it triggers reliably.
