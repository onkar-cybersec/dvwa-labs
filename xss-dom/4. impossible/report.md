# DVWA XSS (DOM) – Impossible

## Steps

- Set **Security Level = Impossible** and open **XSS (DOM)**.
  - `01_target_page.jpg`

- Test the payload that worked on High:

```text
http://localhost/DVWA/vulnerabilities/xss_d/?default=English#<script>alert('XSS')</script>
```

  - `02_payload_blocked.jpg`

## Result

- XSS execution failed.
- No alert box appeared.
- The payload was rendered as text and not executed by the browser.

## Reason

- Client-side protection sanitizes or encodes data obtained from the URL fragment.
- Untrusted input is not inserted into the DOM in an executable context.
- The application prevents JavaScript execution even when a malicious fragment is supplied.

## Fix

- Continue treating all data from `location.hash` as untrusted.
- Use safe DOM APIs such as `textContent` instead of `innerHTML`.
- Encode user-controlled data before rendering it.
- Maintain a strong Content Security Policy (CSP).