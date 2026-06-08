# DVWA XSS (Reflected) – High

## Steps

- Set **Security Level = High** and open **XSS (Reflected)**.
  - `01_target_page.jpg`

- Enter the following payload in the **Name** field:

```html
<img src=x onerror=alert('XSS')>
```

- Click **Submit**.
  - `02_xss_alert_high.jpg`

## Result

- XSS successfully executed.
- Alert box appeared.

## Reason

- The application attempts to block script tags using a regular expression.
- The filter focuses on detecting the word `script`.
- Other HTML elements and event handlers such as `onerror` are not filtered.
- The browser executes JavaScript through the image error event.

## Fix

- Use context-aware output encoding.
- Sanitize user input using a whitelist approach.
- Avoid relying on regex-based blacklists.
- Implement a Content Security Policy (CSP).