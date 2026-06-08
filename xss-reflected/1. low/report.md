# DVWA XSS (Reflected) – Low

## Steps

- Set **Security Level = Low** and open **XSS (Reflected)**.
  - `01_target_page.jpg`

- Enter the following payload in the **Name** field:

```html
<script>alert('XSS')</script>
```

- Click **Submit**.
  - `02_xss_alert.jpg`

## Result

- XSS successfully executed.
- Alert box appeared.

## Reason

- User input is reflected directly into the page without validation or output encoding.
- The browser interprets the injected script and executes it.

## Fix

- Validate and sanitize user input.
- Encode output before displaying user-controlled data.
- Implement a Content Security Policy (CSP).
- Use frameworks/functions that automatically escape HTML output.