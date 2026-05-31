# DVWA Insecure CAPTCHA - High Level

## Step 1

Opened the Insecure CAPTCHA page with security level set to High.

![Target Page](screenshots/01-target-page.jpg)

## Step 2

Entered a new password and intercepted the request using Burp Suite.

![Normal Request](screenshots/02-normal-request.jpg)

## Step 3

Modified the `User-Agent` header:

```text
User-Agent: reCAPTCHA
```

![User-Agent Modified](screenshots/03-user-agent-modified.jpg)

## Step 4

Modified the CAPTCHA response value:

```text
g-recaptcha-response=hidd3n_valu3
```

and prepared the bypass request.

![Bypass Payload](screenshots/04-bypass-payload.jpg)

## Result

Forwarded the modified request and successfully changed the password.

![Password Changed](screenshots/05-password-changed.jpg)

## Reason

The application contains a hardcoded CAPTCHA bypass:

```php
if (
    $resp ||
    (
        $_POST['g-recaptcha-response'] == 'hidd3n_valu3'
        && $_SERVER['HTTP_USER_AGENT'] == 'reCAPTCHA'
    )
)
```

An attacker can manually set these values and bypass CAPTCHA validation without solving the challenge.

## Fix

* Remove hardcoded CAPTCHA bypass conditions.
* Validate CAPTCHA responses only through the official server-side verification process.
* Never trust client-controlled headers or special parameter values for security decisions.