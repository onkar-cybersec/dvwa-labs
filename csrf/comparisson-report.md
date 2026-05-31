# CSRF Comparison (DVWA)

## Low

* No CSRF protection
* Password change request accepted directly
* Attack successful

## Medium

* Referer validation implemented
* Invalid referer blocked
* Protection bypassed by manipulating the Referer header

## High

* Anti-CSRF token implemented
* Requests without a valid token rejected
* CSRF attack unsuccessful

## Impossible

* Anti-CSRF token required
* Current password verification required
* CSRF attack effectively prevented

## Conclusion

As the security level increases, stronger protections are introduced against CSRF attacks. Low and Medium levels remain vulnerable due to weak or bypassable defenses, while High and Impossible levels use Anti-CSRF tokens to prevent unauthorized requests. The Impossible level further strengthens protection by requiring the user's current password before allowing sensitive actions.
