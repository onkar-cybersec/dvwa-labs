# SQL Injection – DVWA (Low Security)

## Step 1 – Open the Target Page

* Navigated to the SQL Injection module in DVWA.
* Verified that the Security Level was set to Low.

**Screenshot:** 01_Target_Page.jpg

---

## Step 2 – Perform a Normal Query

* Entered User ID `1`.
* Submitted the request.
* The application returned the corresponding user information.

**Screenshot:** 02_Normal_Query.jpg

---

## Step 3 – Verify SQL Injection

* Entered the payload:

  ```sql
  1' OR '1'='1
  ```
* Submitted the request.
* The application returned multiple records, confirming that user input was directly injected into the SQL query.

**Screenshot:** 03_SQLi_Verification.jpg

---

## Step 4 – Discover Column Count

* Tested the following payloads:

  ```sql
  1' ORDER BY 1#
  ```

  ```sql
  1' ORDER BY 2#
  ```

  ```sql
  1' ORDER BY 3#
  ```
* The application generated an error when testing column 3.

**Screenshot:** 04_Column_Count_Discovery.jpg

---

## Step 5 – Confirm Valid Column Count

* Executed:

  ```sql
  1' ORDER BY 2#
  ```
* The application responded normally without any error.
* Determined that the query contains 2 columns.

**Screenshot:** 05_Valid_Column_Count.jpg

---

## Step 6 – Test UNION-Based SQL Injection

* Executed:

  ```sql
  1' UNION SELECT 1,2#
  ```
* The values `1` and `2` appeared in the output.
* Confirmed that both columns are reflected and can be used for data extraction.

**Screenshot:** 06_Union_Select_Test.jpg

---

## Result

The SQL Injection vulnerability was successfully exploited. The application accepted malicious SQL input and allowed modification of the original query. UNION-based SQL Injection was achieved, demonstrating that database information could potentially be extracted.

---

## Reason

The application directly inserts user input into the SQL query without validation or parameterized statements.

Vulnerable query:

```php
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";
```

User input is concatenated directly into the SQL statement, allowing attackers to inject arbitrary SQL commands.

---

## Fix

* Use parameterized queries (Prepared Statements).
* Validate and sanitize user input.
* Implement allow-list input validation.
* Disable detailed database error messages.
* Apply the principle of least privilege to database accounts.
* Conduct regular security testing and code reviews.
