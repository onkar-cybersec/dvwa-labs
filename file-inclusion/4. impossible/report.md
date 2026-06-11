# DVWA File Inclusion - Impossible

## Step 1
Open the DVWA File Inclusion page and set the security level to Impossible.

![Target Page](images/01-target-page.__temp__.JPG)

## Step 2
Verify that an approved file loads correctly.

```text
?page=file1.php
```

![Normal File Load](images/02-normal-file1.__temp__.JPG)

## Step 3
Attempt Local File Inclusion using a file wrapper payload.

```text
?page=file:///etc/passwd
```

The application rejects the request.

![File Wrapper Blocked](images/03-file-wrapper-blocked.__temp__.JPG)

## Step 4
Attempt Local File Inclusion using directory traversal.

```text
?page=../../../../../../etc/passwd
```

The application rejects the request.

![Traversal Blocked](images/04-traversal-blocked.__temp__.JPG)

## Result
The File Inclusion vulnerability could not be exploited. All unauthorized file access attempts were blocked.

## Reason
The application uses a strict allowlist and only permits approved files:

```text
include.php
file1.php
file2.php
file3.php
```

Any value outside this allowlist is rejected before file inclusion occurs.

## Fix
Already Implemented:
- Strict allowlist validation.
- Validation of all user input.
- Prevention of arbitrary file inclusion.
- Restriction of file access to approved application resources.