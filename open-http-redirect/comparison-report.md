# Open HTTP Redirect - Comparison Report

## Low

* No validation is applied to the `redirect` parameter.
* Any external URL is accepted.
* The server responds with a `302 Found` redirect to the attacker-controlled destination.

**Result:** Vulnerable

## Medium

* The application blocks URLs containing `http://` or `https://`.
* The filter is bypassed using a protocol-relative URL:

```text
//google.com
```

**Result:** Vulnerable

## High

* The application only checks whether `info.php` exists somewhere in the URL.
* External URLs containing `info.php` bypass the validation:

```text
https://google.com/info.php
```

**Result:** Vulnerable

## Impossible

* The application only accepts numeric redirect IDs.
* Approved IDs are mapped server-side to predefined destinations.
* User-controlled URLs are rejected.

**Result:** Not vulnerable

## Conclusion

Low, Medium, and High are vulnerable because they allow user-controlled redirect destinations through weak or incomplete validation. Impossible fixes the issue by replacing user-controlled URLs with server-side destination mapping.
