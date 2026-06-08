# DVWA XSS (Stored) – High

## Steps

- Set **Security Level = High** and open **XSS (Stored)**.
  - `01_target_page.jpg`

- Configure Burp Suite and enable **Proxy → Intercept**.

- Enter the following values:

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
txtName=<img src=x onerror=alert(1)>
```

- Forward the request.
  - `02_xss_alert_high.jpg`

## Result

- XSS successfully executed.
- Alert box appeared.
- Payload was stored in the guestbook.
- The payload executes whenever the stored entry is viewed.

## Reason

- The application uses a regex filter focused on blocking script tags.
- HTML elements such as `<img>` are still allowed.
- JavaScript executes through the `onerror` event handler.
- The Name field restriction can be bypassed using Burp Suite.

## Fix

- Encode output using `htmlspecialchars()` before displaying stored content.
- Avoid blacklist and regex-based filtering.
- Use a whitelist approach for allowed input.
- Implement a Content Security Policy (CSP).