# DVWA - Authorisation Bypass Comparison

| Level | Result | Status |
|---------|---------|---------|
| Low | Non-admin users can directly access and modify admin-only functionality. | Vulnerable |
| Medium | Page access is blocked, but backend API endpoints remain accessible. | Vulnerable |
| High | Page access and backend API endpoints are protected. | Secure |
| Impossible | Full authorization enforcement on both page and API endpoints. | Secure |

## Low

### Observation

The application only hides the Authorisation Bypass menu option from non-admin users.

### Impact

A non-admin user can directly browse to the vulnerable URL and modify protected user information.

### Result

Authorization bypass successful.

---

## Medium

### Observation

The main page implements authorization checks and returns:

```text
Unauthorised
```

However, backend API endpoints remain accessible.

### Impact

A non-admin user can directly access:

```text
get_user_data.php
```

and retrieve protected user information.

### Result

Authorization bypass successful through direct API access.

---

## High

### Observation

Authorization checks are enforced on both the page and backend API endpoint.

### Impact

Requests from non-admin users receive:

```json
{"result":"fail","error":"Access denied"}
```

### Result

Authorization bypass prevented.

---

## Impossible

### Observation

Complete server-side authorization enforcement is applied to all protected resources.

### Impact

Non-admin users cannot access the page or backend API endpoints.

### Result

Authorization bypass prevented.

---

## Conclusion

The vulnerability evolves from a complete lack of authorization enforcement at Low, to partial protection at Medium, where backend endpoints remain exposed. High and Impossible correctly implement server-side authorization controls on both application pages and API endpoints, preventing unauthorized access to sensitive functionality and user data.