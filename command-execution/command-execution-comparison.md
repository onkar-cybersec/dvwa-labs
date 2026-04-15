# Command Injection Comparison (DVWA)

## Low

* No input validation
* Commands like `;`, `&&`, `|` work easily
* Full command execution possible
* Very easy to exploit

## Medium

* Basic filtering applied
* Some operators like `;` blocked
* Bypass possible using alternative operators (e.g., `&`)
* Vulnerability still exists due to incomplete filtering

## High

* Strong input validation (IP format enforced)
* Only numeric values allowed
* Command injection not possible
* Proper mitigation implemented

## Conclusion

As security level increases, the application moves from no validation to strict allowlist validation.

Low and Medium levels are vulnerable due to lack of proper input handling, while High level effectively prevents command injection through strict validation.
