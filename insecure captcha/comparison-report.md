# DVWA Insecure CAPTCHA - Comparison Report

## Low

* CAPTCHA validation occurs only during the first step.
* Password change is performed in a separate request.
* Final request can be submitted directly using `step=2`.
* CAPTCHA protection bypassed successfully.

## Medium

* CAPTCHA status is stored in a hidden form field.
* Application trusts the client-controlled parameter `passed_captcha=true`.
* Parameter can be modified through Burp Suite.
* Password changed successfully without proper server-side validation.

## High

* Application contains a hardcoded CAPTCHA bypass.
* Request modified to use:

```text
User-Agent: reCAPTCHA
g-recaptcha-response=hidd3n_valu3
```

* CAPTCHA validation bypassed successfully.
* Password changed without solving the challenge.

## Impossible

* Validates CAPTCHA on the server side.
* Requires the correct current password.
* Enforces Anti-CSRF token validation.
* Uses prepared statements for database operations.
* No hardcoded bypasses or client-side trust.

## Conclusion

Security improves at each level. Low relies on a flawed multi-step process, Medium trusts a client-controlled parameter, and High contains a hardcoded backdoor. Impossible correctly implements server-side CAPTCHA validation, password verification, and CSRF protection, preventing the bypass techniques used in the previous levels.
