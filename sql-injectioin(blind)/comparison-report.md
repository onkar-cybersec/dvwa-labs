# SQL Injection (Blind) Comparison Report

## Low

* User input is directly concatenated into the SQL query.
* TRUE condition (`1' AND '1'='1`) returned a positive response.
* FALSE condition (`1' AND '1'='2`) returned a negative response.
* Blind SQL Injection successfully exploited.
* Database information could be inferred through boolean responses.

## Medium

* Application switched from GET to POST.
* `mysqli_real_escape_string()` was implemented.
* Numeric SQL expressions could still be injected.
* Burp Suite Repeater was used to modify the POST parameter.
* Blind SQL Injection successfully exploited.

## High

* User input moved from parameters to cookies.
* SQL query still used unsanitized cookie data.
* Burp Suite Repeater was used to modify the `id` cookie.
* TRUE and FALSE conditions produced different responses.
* Blind SQL Injection successfully exploited through cookie manipulation.

## Impossible

* Input validated using `is_numeric()`.
* Input converted using `intval()`.
* Prepared statements with bound parameters were implemented.
* Anti-CSRF protection was enabled.
* Injection payloads failed and did not affect the query.
* Blind SQL Injection was not exploitable.

## Conclusion

* Low: Vulnerable.
* Medium: Vulnerable despite escaping functions.
* High: Vulnerable through cookie-based input.
* Impossible: Secure due to input validation, parameterized queries, and CSRF protection.
