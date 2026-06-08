# DVWA XSS (Stored) – Low

## Steps

- Set **Security Level = Low** and open **XSS (Stored)**.
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
  - `02_xss_alert.jpg`

## Result

- XSS successfully executed.
- Alert box appeared.
- The payload was stored in the guestbook.
- The payload executes whenever the page is viewed.

## Reason

- User input is stored without HTML encoding.
- The application only escapes SQL special characters.
- Stored data is rendered as HTML by the browser and executed.

## Fix

- Encode output before displaying stored content.
- Validate and sanitize user input.
- Use `htmlspecialchars()` when rendering guestbook entries.
- Implement a Content Security Policy (CSP).