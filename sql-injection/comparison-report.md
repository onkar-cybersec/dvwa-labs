# SQL Injection – DVWA Security Level Comparison

## Low

* User input is directly concatenated into the SQL query.
* No input validation or parameterized queries are used.
* SQL Injection payloads execute successfully.
* Column enumeration using `ORDER BY` is possible.
* UNION-based SQL Injection is successful.

**Outcome:** Vulnerable

---

## Medium

* Input is processed using `mysqli_real_escape_string()`.
* User selection is submitted through a POST request.
* Request manipulation using Burp Suite bypasses client-side restrictions.
* SQL Injection payloads execute successfully.
* UNION-based SQL Injection is successful.

**Outcome:** Vulnerable

---

## High

* Input is stored in a session variable.
* Query uses `LIMIT 1` and generic error messages.
* Session value is still inserted directly into the SQL query.
* Payload `1' OR '1'='1` successfully alters query logic.

**Outcome:** Vulnerable

---

## Impossible

* Input is validated using `is_numeric()`.
* User input is converted using `intval()`.
* Prepared statements and parameter binding are implemented.
* SQL Injection payloads fail.
* Query structure cannot be modified by user input.

**Outcome:** Not Vulnerable

---

## Conclusion

* Low Security: SQL Injection successfully exploited.
* Medium Security: SQL Injection successfully exploited after intercepting and modifying the request.
* High Security: SQL Injection successfully exploited through session-based input handling.
* Impossible Security: SQL Injection prevented through input validation and prepared statements.

The vulnerability exists in Low, Medium, and High security levels, while the Impossible security level properly mitigates SQL Injection attacks.
