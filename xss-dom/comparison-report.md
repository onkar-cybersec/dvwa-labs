# DVWA XSS (DOM) – Comparison Report

## Low

### Vulnerability

- No input validation or filtering is implemented.
- User input is inserted directly into the DOM.

### Bypass

```html
<script>alert('XSS')</script>
```

### Outcome

- JavaScript executed successfully.
- Alert box appeared.

---

## Medium

### Vulnerability

- Application blocks only `<script>` tags.
- Other HTML elements and event handlers remain allowed.

### Bypass

```html
English</option></select><img src=x onerror=alert('XSS')>
```

### Outcome

- JavaScript executed through the `onerror` event.
- Alert box appeared.

---

## High

### Vulnerability

- Application uses a whitelist for accepted language values.
- URL fragment (`#`) is not validated by the server.

### Bypass

```text
#<script>alert('XSS')</script>
```

### Outcome

- Client-side JavaScript processed the fragment.
- Alert box appeared.

---

## Impossible

### Protection

- URL fragment data is sanitized/encoded before being inserted into the DOM.
- Untrusted input is not executed.

### Test Payload

```text
#<script>alert('XSS')</script>
```

### Outcome

- No alert box appeared.
- Payload was displayed as text.
- XSS execution failed.

---

## Conclusion

| Level | Result |
|---------|---------|
| Low | Vulnerable |
| Medium | Vulnerable |
| High | Vulnerable |
| Impossible | Not Vulnerable |

- Low allows direct script execution.
- Medium blocks only `<script>` tags and can be bypassed with event handlers.
- High validates the parameter but remains vulnerable through the URL fragment.
- Impossible properly handles untrusted input and prevents DOM-based XSS execution.