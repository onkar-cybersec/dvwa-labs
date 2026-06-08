# DVWA CSP Bypass - Medium

## Steps

- Opened CSP Bypass at Medium security level.
  - Screenshot: `01_target_medium.jpg`

- Entered the payload:

```html
<script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(1)</script>
```

- Clicked **Include**.
  - Screenshot: `02_medium_alert.jpg`

## Result

- Alert box executed successfully.
- CSP protection was bypassed.

## Reason

- User input is inserted directly into the page without filtering.
- The CSP nonce is hardcoded in the source code.
- An attacker can reuse the exposed nonce value to execute arbitrary JavaScript.

## Fix

- Generate a unique random nonce for every request.
- Do not hardcode nonce values.
- Encode or sanitize user input before rendering.
- Avoid placing raw user input directly into HTML output.