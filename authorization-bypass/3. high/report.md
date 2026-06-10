# DVWA - Authorisation Bypass (High)

## Steps

- Accessed the Authorisation Bypass page as an administrator.
  - Screenshot: `01_target_page.JPG`

- Logged in as a non-admin user (`smithy`) and attempted direct access to the protected page through Burp Repeater.
  - Screenshot: `02_unauthorised_access.JPG`

- Modified the request to access the backend endpoint:

  ```http
  GET /DVWA/vulnerabilities/authbypass/get_user_data.php HTTP/1.1
  ```

- Sent the request and reviewed the response.
  - Screenshot: `03_api_access_denied.JPG`

## Result

Direct access to the page was denied with:

```text
Unauthorised
```

Direct access to the backend API endpoint was also denied with:

```json
{"result":"fail","error":"Access denied"}
```

The authorization bypass vulnerability could not be exploited.

## Reason

Authorization checks are enforced on both the page and backend API endpoints. Non-admin users are prevented from accessing protected functionality and sensitive user data.

## Fix

No additional remediation required for this security level. Continue enforcing server-side authorization checks on all protected pages and API endpoints.