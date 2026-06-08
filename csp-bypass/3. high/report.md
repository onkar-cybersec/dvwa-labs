# DVWA CSP Bypass - High

## Steps

- Opened CSP Bypass at High security level.
  - Screenshot: `01_target_high.jpg`

- Clicked **Solve the sum** and observed the JSONP request execute successfully.
  - Screenshot: `02_high_normal_result.jpg`

- Opened:

```text
http://localhost/DVWA/vulnerabilities/csp/source/jsonp.php?callback=alert
```

- The application returned:

```javascript
alert({"answer":"15"})
```

  - Screenshot: `03_high_jsonp_callback.jpg`

## Result

- CSP protection was bypassed using the JSONP endpoint.
- Arbitrary JavaScript execution was possible through the `callback` parameter.

## Reason

- The CSP policy only allows scripts from the same origin:

```http
Content-Security-Policy: script-src 'self';
```

- The application loads JavaScript from:

```javascript
source/jsonp.php?callback=solveSum
```

- The `callback` parameter is user-controllable.
- Replacing `solveSum` with `alert` causes the server to return:

```javascript
alert({"answer":"15"})
```

- Because the script originates from the same domain, CSP allows it to execute.

## Fix

- Do not use unrestricted JSONP endpoints.
- Validate callback names against a strict whitelist.
- Prefer CORS with JSON responses instead of JSONP.
- Remove support for arbitrary callback functions.
- Apply input validation before reflecting callback parameters.