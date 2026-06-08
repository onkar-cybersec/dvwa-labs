# DVWA XSS (Stored) – Comparison Report

## Low

### Vulnerability

- User input is stored without HTML encoding.
- Only SQL-related escaping is applied.

### Payload

```html
<script>alert('XSS')</script>
```

### Outcome

- JavaScript executed successfully.
- Alert box appeared.
- Payload was stored and executed whenever the page was viewed.

---

## Medium

### Vulnerability

- Message field is protected using `strip_tags()` and `htmlspecialchars()`.
- Name field only removes the exact lowercase `<script>` string.

### Payload

```html
<ScRiPt>alert(1)</ScRiPt>
```

### Bypass

- Burp Suite was used to bypass the Name field length restriction.

### Outcome

- JavaScript executed successfully.
- Alert box appeared.
- Payload was stored in the guestbook.

---

## High

### Vulnerability

- Regex-based filtering attempts to block script tags.
- Other HTML elements and event handlers remain allowed.

### Payload

```html
<img src=x onerror=alert(1)>
```

### Bypass

- Burp Suite was used to bypass the Name field length restriction.

### Outcome

- JavaScript executed through the `onerror` event.
- Alert box appeared.
- Payload was stored in the guestbook.

---

## Impossible

### Protection

- `htmlspecialchars()` is applied to both Name and Message fields.
- Anti-CSRF token validation is implemented.
- PDO prepared statements are used.

### Payload

```html
<script>alert('XSS')</script>
```

### Outcome

- No alert box appeared.
- Payload was displayed as encoded text.
- XSS execution failed.

---

## Conclusion

| Level | Result |
|---------|---------|
| Low | Vulnerable |
| Medium | Vulnerable |
| High | Vulnerable |
| Impossible | Not Vulnerable |

- Low stores and renders user input without output encoding.
- Medium relies on weak blacklist filtering that can be bypassed.
- High blocks script tags but remains vulnerable through HTML event handlers.
- Impossible properly encodes output and prevents stored XSS execution.
- Output encoding (`htmlspecialchars()`) is the primary control that prevents exploitation.