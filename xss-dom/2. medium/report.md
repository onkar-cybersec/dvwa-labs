# DVWA XSS (DOM) – Medium

## Steps

- Set **Security Level = Medium** and open **XSS (DOM)**.
  - `01_target_page.jpg`

- Inject the following payload in the `default` parameter:

```html
English</option></select><img src=x onerror=alert('XSS')>
```

  - `02_xss_alert_medium.jpg`

## Result

- XSS successfully executed.
- Alert box appeared.

## Reason

- The filter only blocks `<script>` tags.
- Event handlers such as `onerror` are still allowed.
- User input is inserted into the page without proper output encoding.

## Fix

- Validate input using a whitelist of allowed values.
- Encode output before inserting it into the DOM.
- Use safe DOM methods such as `textContent`.
- Implement a Content Security Policy (CSP).