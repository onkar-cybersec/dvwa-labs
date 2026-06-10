# API Security – Comparison Report

## Low

### Vulnerability

API Versioning Exposure

### Finding

Older API version (`v1`) exposed sensitive information that was hidden in the newer version (`v2`).

### Evidence

```text
/v1/user
```

returned password hashes:

```json
{
  "id": 1,
  "name": "tony",
  "level": 0,
  "password": "hash..."
}
```

### Impact

An attacker can access deprecated API versions and retrieve sensitive information such as password hashes.

---

## Medium

### Vulnerability

Privilege Escalation Through Parameter Manipulation

### Finding

The API trusted client-controlled parameters and allowed modification of the user's privilege level.

### Evidence

Original request:

```json
{
  "name":"test"
}
```

Modified request:

```json
{
  "name":"test",
  "level":0
}
```

Response:

```json
{
  "id": 2,
  "name": "test",
  "level": 0
}
```

### Impact

An attacker can elevate privileges and gain administrator access.

---

## High

### Vulnerability

Command Injection

### Finding

User input was passed directly into a system command.

### Vulnerable Code

```php
exec("ping -c 4 " . $target, $output, $ret_var);
```

### Evidence

Payload:

```json
{
  "target":"127.0.0.1; false"
}
```

Response:

```json
{
  "status":"Connection failed"
}
```

### Impact

An attacker can execute operating system commands on the server.

---

## Impossible

### Protection

OAuth 2.0 Authentication

### Finding

The application requires authenticated API access using OAuth 2.0 and no exploitable vulnerability was identified.

### Security Improvements

* Strong authentication requirements
* Protected API access
* Reduced exposure of sensitive functionality
* Improved authorization controls

### Impact

Unauthorized users cannot directly interact with protected API functionality without valid authentication.

---

# Conclusion

| Level      | Vulnerability           | Risk      |
| ---------- | ----------------------- | --------- |
| Low        | API Versioning Exposure | Medium    |
| Medium     | Privilege Escalation    | High      |
| High       | Command Injection       | Critical  |
| Impossible | OAuth 2.0 Protection    | Mitigated |

The API Security module demonstrates how insecure API design can evolve from information disclosure (Low), to privilege escalation (Medium), to full command execution (High). The Impossible level mitigates these issues by implementing stronger authentication and access control mechanisms through OAuth 2.0.
