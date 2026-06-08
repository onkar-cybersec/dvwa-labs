# DVWA XSS (Stored) – Impossible

## Steps

- Set **Security Level = Impossible** and open **XSS (Stored)**.
  - `01_target_page.jpg`

- Enter the following values:

**Name**
```text
test
```

**Message**
```html
<script>alert('XSS')</script>
```

- Click **Sign Guestbook**.
  - `02_payload_encoded.jpg`

## Result

- XSS execution failed.
- No alert box appeared.
- The payload was displayed as encoded text.

## Reason

- The application uses `htmlspecialchars()` on both the Name and Message fields.
- Special HTML characters are encoded before storage/display.
- The browser treats the payload as text rather than executable code.
- Anti-CSRF token validation is also implemented.
- PDO prepared statements are used for database operations.

## Fix

- Continue using `htmlspecialchars()` for output encoding.
- Maintain Anti-CSRF token validation.
- Continue using prepared statements.
- Implement a Content Security Policy (CSP) as an additional defense layer.