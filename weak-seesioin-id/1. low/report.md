# Weak Session IDs - Low

## Step 1

* Opened Weak Session IDs page.
* Security level set to Low.

![01_target_page](images/01_target_page.__temp__.JPG)

## Step 2

* Generated a session ID.
* Observed the cookie value.

**Value**

```text
dvwaSession=1
```

![02_session_id_1](images/02_session_id_1.__temp__.JPG)

## Step 3

* Generated another session ID.
* Observed the cookie value increment.

**Value**

```text
dvwaSession=2
```

![03_session_id_2](images/03_session_id_2.__temp__.JPG)

## Step 4

* Generated a third session ID.
* Observed the cookie value increment.

**Value**

```text
dvwaSession=3
```

![04_session_id_3](images/04_session_id_3.__temp__.JPG)

## Step 5

* Predicted the next session ID before generating it.
* Prediction was successful.

**Predicted Value**

```text
dvwaSession=4
```

**Screenshot:** `05_predicted_session_id.jpg`

## Result

* Session IDs were predictable.
* Future session IDs could be accurately guessed.

## Reason

* Session IDs are generated sequentially.
* The application increments the value by one for each request.
* No randomness is used in session generation.

## Fix

* Use cryptographically secure random session IDs.
* Regenerate session IDs after authentication.
* Avoid predictable or sequential session values.
* Use secure session management mechanisms provided by the framework.
