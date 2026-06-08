# DVWA XSS (DOM) – High

## Steps

- Set **Security Level = High** and open **XSS (DOM)**.
  - `01_target_page.jpg`

- Inject the payload in the URL fragment:

```text
http://localhost/DVWA/vulnerabilities/xss_d/?default=English#<script>alert('XSS')</script>
```

  - `02_xss_alert_high.jpg`

## Result

- XSS successfully executed.
- Alert box appeared despite the whitelist protection.

## Reason

- The application whitelists the `default` parameter and redirects invalid values.
- The payload is placed after the `#` fragment, which is not sent to the server.
- Client-side JavaScript reads the fragment and inserts it into the page, resulting in DOM-based XSS.

## Fix

- Do not use untrusted data from `location.hash` without validation.
- Encode user-controlled data before inserting it into the DOM.
- Use safe DOM APIs such as `textContent` instead of `innerHTML`.
- Implement a Content Security Policy (CSP).