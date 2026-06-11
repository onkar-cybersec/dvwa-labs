# DVWA Insecure CAPTCHA - High Level

## Step 1

Opened the Insecure CAPTCHA page with security level set to High.

![Target Page](images/01-target-page.JPG)

## Step 2

Entered a new password and intercepted the request using Burp Suite.

![Normal Request](images/02-normal-request.JPG)

## Step 3

Modified the `User-Agent` header:

```text
User-Agent: reCAPTCHA
```

![User-Agent Modified](images/03-user-agent-modified.JPG)

## Step 4

Modified the CAPTCHA response value:

```text
g-recaptcha-response=hidd3n_valu3
```

and prepared the bypass request.

![Bypass Payload](images/04-bypass-payload.JPG)

## Result

Forwarded the modified request and successfully changed the password.

![Password Changed](images/05-password-changed.JPG)

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