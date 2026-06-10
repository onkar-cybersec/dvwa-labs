# DVWA - Authorisation Bypass (Low)

## Steps

- Accessed the **Authorisation Bypass** page as a non-admin user.
  - Screenshot: `01_target_page.JPG`

- Modified the user **Bob** to **Bob_Test** and clicked **Update**.
  - Screenshot: `02_user_modified.JPG`

## Result

A non-admin user was able to access an admin-only page and successfully modify user information.

## Reason

The application only hides the **Authorisation Bypass** menu item from non-admin users:

```php
if( dvwaCurrentUser() == "admin" ) {
    $menuBlocks['vulnerabilities'][] = array(
        'id' => 'authbypass',
        'name' => 'Authorisation Bypass',
        'url' => 'vulnerabilities/authbypass/'
    );
}
```

This is not a real authorization control. The page remains accessible through direct URL access, allowing unauthorized users to perform privileged actions.

## Fix

Implement server-side authorization checks before granting access to the page or processing updates.

```php
if (dvwaCurrentUser() !== "admin") {
    die("Access Denied");
}
```

Verify authorization on every sensitive request rather than relying on hidden links or client-side restrictions.