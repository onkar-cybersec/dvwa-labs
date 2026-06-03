# Weak Session IDs - Medium

## Step 1

* Opened Weak Session IDs page.
* Security level set to Medium.

**Screenshot:** `01_target_page.jpg`

## Step 2

* Generated a session ID.
* Observed a timestamp-based cookie value.

**Value**

```text
dvwaSession=1780396107
```

**Screenshot:** `02_timestamp_session_id_1.jpg`

## Step 3

* Generated another session ID.
* Observed the value changed according to the current time.

**Value**

```text
dvwaSession=1780396199
```

**Screenshot:** `03_timestamp_session_id_2.jpg`

## Step 4

* Generated another session ID and verified the value continued following the current timestamp.

**Value**

```text
dvwaSession=1780396276
```

**Screenshot:** `04_predicted_timestamp_session_id.jpg`

## Result

* Session IDs were predictable.
* Session values were based on the current Unix timestamp.
* Future session IDs could be estimated from the current time.

## Reason

* Session IDs are generated using PHP's `time()` function.
* No randomness or cryptographic protection is used.

## Fix

* Use cryptographically secure random session IDs.
* Regenerate session IDs after authentication.
* Avoid timestamp-based session generation.
* Use secure framework-managed session handling.
