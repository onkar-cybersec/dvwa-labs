# DVWA XSS (Reflected) – Comparison Report

## Low

### Vulnerability

- No input validation or output encoding.
- User input is reflected directly into the page.

### Payload

```html
<script>alert('XSS')</script>
```

### Outcome

- JavaScript executed successfully.
- Alert box appeared.

---

## Medium

### Vulnerability

- Application removes only the exact lowercase `<script>` string.
- Filtering is case-sensitive.

### Payload

```html
<ScRiPt>alert('XSS')</ScRiPt>
```

### Outcome

- JavaScript executed successfully.
- Alert box appeared.

---

## High

### Vulnerability

- Application uses a regex filter targeting script tags.
- Other HTML elements and event handlers remain allowed.

### Payload

```html
<img src=x onerror=alert('XSS')>
```

### Outcome

- JavaScript executed through the `onerror` event.
- Alert box appeared.

---

## Impossible

### Protection

- User input is encoded using `htmlspecialchars()`.
- Anti-CSRF token validation is implemented.

### Payload

```html
<script>alert('XSS')</script>
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

- Low reflects user input directly and allows script execution.
- Medium relies on weak case-sensitive filtering that is easily bypassed.
- High blocks script tags but remains vulnerable through HTML event handlers.
- Impossible uses output encoding and token validation, preventing reflected XSS execution.