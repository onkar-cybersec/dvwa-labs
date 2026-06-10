# DVWA - Authorisation Bypass (Medium)

## Steps

- Logged in as a non-admin user (`gordonb`).
- Attempted to access the Authorisation Bypass page directly.
  - Screenshot: `01_target_page.JPG`

- Intercepted the request using Burp Suite and sent it to Repeater.
- Modified the request target to:

  ```http
  GET /DVWA/vulnerabilities/authbypass/get_user_data.php HTTP/1.1
  ```

- Sent the request and observed the response.
  - Screenshot: `02_burp_api_bypass.JPG`

## Result

The application blocked direct access to the page and returned:

```text
Unauthorised
```

However, the backend endpoint `get_user_data.php` remained accessible and returned user information, including the admin account.

## Reason

The page implements an authorization check:

```php
if (dvwaCurrentUser() != "admin") {
    print "Unauthorised";
    http_response_code(403);
    exit;
}
```

However, the backend API endpoint only restricts access on **High** and **Impossible** security levels:

```php
if ((dvwaSecurityLevelGet() == "high" ||
     dvwaSecurityLevelGet() == "impossible") &&
     dvwaCurrentUser() != "admin") {
    print json_encode(array(
        "result" => "fail",
        "error" => "Access denied"
    ));
    exit;
}
```

As a result, non-admin users can directly access the API endpoint and retrieve protected data.

## Fix

Apply authorization checks to every backend endpoint handling sensitive data.

```php
if (dvwaCurrentUser() != "admin") {
    http_response_code(403);
    exit("Access Denied");
}
```

Do not rely solely on page-level restrictions. Enforce authorization on all server-side API requests.