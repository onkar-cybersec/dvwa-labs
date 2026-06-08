# DVWA XSS (Stored) – Medium

## Steps

- Set **Security Level = Medium** and open **XSS (Stored)**.
  - `01_target_page.jpg`

- Configure Burp Suite and enable **Proxy → Intercept**.

- Enter the following values in the form:

**Name**
```text
test
```

**Message**
```text
test
```

- Click **Sign Guestbook** and intercept the request in Burp.

- Modify:

```text
txtName=test
```

to:

```html
txtName=<ScRiPt>alert(1)</ScRiPt>
```

- Forward the request.
  - `02_xss_alert_medium.jpg`

## Result

- XSS successfully executed.
- Alert box appeared.
- Payload was stored in the guestbook.

## Reason

- The application removes only the exact lowercase string `<script>`.
- Mixed-case script tags bypass the filter.
- The Name field length restriction can be bypassed using Burp Suite.
- Stored content is rendered without proper output encoding.

## Fix

- Use output encoding such as `htmlspecialchars()` when displaying stored data.
- Avoid blacklist-based filtering.
- Validate input using a whitelist approach.
- Implement a Content Security Policy (CSP).