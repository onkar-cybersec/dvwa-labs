# DVWA XSS (Reflected) – Impossible

## Steps

- Set **Security Level = Impossible** and open **XSS (Reflected)**.
  - `01_target_page.jpg`

- Enter the following payload in the **Name** field:

```html
<script>alert('XSS')</script>
```

- Click **Submit**.
  - `02_payload_encoded.jpg`

## Result

- XSS execution failed.
- No alert box appeared.
- The payload was displayed as text.

## Reason

- The application uses `htmlspecialchars()` to encode special HTML characters.
- The browser treats the payload as text instead of executable code.
- An Anti-CSRF token is also validated before processing the request.

## Fix

- Continue using context-aware output encoding such as `htmlspecialchars()`.
- Validate all user input.
- Keep Anti-CSRF protection enabled.
- Implement a Content Security Policy (CSP) as an additional defense layer.