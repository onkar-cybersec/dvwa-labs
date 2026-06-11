# SQL Injection (Blind) - High

## Step 1

* Opened SQL Injection (Blind) page.
* Security level set to High.

![01_Target_Page](images/01_Target_Page.__temp__.JPG)

## Step 2

* Verified a valid user ID through the cookie mechanism.

![02_valid_user](images/02_valid_user.__temp__.JPG)

## Step 3

* Modified the `id` cookie using Burp Suite Repeater.

**Payload**

```sql
1' AND '1'='1
```

* Application returned a positive response.

![03_cookie_true](images/03_cookie_true.__temp__.JPG)

## Step 4

* Modified the `id` cookie using Burp Suite Repeater.

**Payload**

```sql
1' AND '1'='2
```

* Application returned a negative response.

![04_cookie_false](images/04_cookie_false.__temp__.JPG)

## Result

* Blind SQL Injection confirmed.
* SQL conditions were successfully injected through the cookie value.
* Application responses changed based on TRUE and FALSE conditions.

## Reason

* Cookie input is directly concatenated into the SQL query.
* No prepared statements or parameterized queries are used.

## Fix

* Use prepared statements with parameterized queries.
* Validate and sanitize cookie values.
* Implement least-privilege database permissions.
* Return generic responses that do not reveal query evaluation results.
