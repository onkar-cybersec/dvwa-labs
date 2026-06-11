# DVWA File Inclusion - Low

## Step 1
Open the DVWA File Inclusion page and set the security level to Low.

![Target Page](images/01-target-page.JPG)

## Step 2
Load the default page using the following parameter:

```text
?page=include.php
```

![Normal Include](images/02-normal-include.JPG)

## Step 3
Modify the `page` parameter to perform Local File Inclusion.

```text
?page=../../../../../../etc/passwd
```

![LFI Payload URL](images/03-lfi-payload-url.JPG)

## Step 4
Observe that the contents of `/etc/passwd` are displayed in the browser.

![LFI Success](images/04-lfi-success-passwd.JPG)

## Result
Successfully accessed the contents of `/etc/passwd`, confirming a Local File Inclusion vulnerability.

## Reason
The application directly includes files based on user-controlled input without validating or restricting file paths, allowing directory traversal and arbitrary file access.

## Fix
- Use a strict allowlist of permitted files.
- Block directory traversal sequences such as `../`.
- Validate and sanitize user input.
- Use server-side file mappings instead of user-controlled paths.