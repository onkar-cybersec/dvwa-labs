# DVWA CSP Bypass - Comparison Report

## Low

- Allowed external scripts from trusted domains.
- Included malicious script from `cdn.jsdelivr.net`.
- CSP bypass successful.

## Medium

- User input rendered directly into the page.
- CSP nonce was hardcoded in source code.
- Reused nonce to execute JavaScript.
- CSP bypass successful.

## High

- CSP allowed only same-origin scripts.
- Application used JSONP with a user-controlled callback.
- Changed callback to `alert`.
- CSP bypass successful.

## Impossible

- CSP allowed only same-origin scripts.
- JSONP callback was hardcoded to `solveSum`.
- User-supplied callback parameter ignored.
- CSP bypass failed.

## Conclusion

- **Low:** Weak domain allowlist trust.
- **Medium:** Hardcoded nonce exposed.
- **High:** JSONP callback injection.
- **Impossible:** Fixed callback prevents JSONP abuse and blocks the bypass.