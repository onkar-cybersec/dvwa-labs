# DVWA XSS (Reflected) – Medium

## Steps

- Set **Security Level = Medium** and open **XSS (Reflected)**.
  - `01_target_page.jpg`

- Enter the following payload in the **Name** field:

```html
<ScRiPt>alert('XSS')</ScRiPt>
```

- Click **Submit**.
  - `02_xss_alert_medium.jpg`

## Result

- XSS successfully executed.
- Alert box appeared.

## Reason

- The application removes only the exact lowercase string `<script>`.
- Mixed-case script tags are not filtered.
- Browsers treat `<ScRiPt>` as a valid script tag and execute it.

## Fix

- Perform case-insensitive filtering if using blacklists.
- Prefer output encoding instead of keyword filtering.
- Validate and sanitize user input.
- Implement a Content Security Policy (CSP).