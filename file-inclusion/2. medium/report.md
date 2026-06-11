# DVWA File Inclusion - Medium

## Step 1
Open the DVWA File Inclusion page and set the security level to Medium.

![Target Page](images/01-target-page.JPG)

## Step 2
Verify that the application loads the default page correctly.

```text
?page=include.php
```

![Normal Include](images/02-normal-include.JPG)

## Step 3
Use a directory traversal bypass payload.

```text
?page=....//....//....//....//....//....//etc/passwd
```

![LFI Payload URL](images/03-lfi-payload-url.JPG)

## Step 4
Observe that the contents of `/etc/passwd` are displayed.

![LFI Success](images/04-lfi-success-passwd.JPG)

## Result
Successfully bypassed the application's filter and accessed a local system file.

## Reason
The application attempts to remove `../` sequences but can be bypassed using crafted payloads such as `....//`, which become valid traversal sequences after processing.

## Fix
- Do not include files directly from user input.
- Use a strict allowlist of approved files.
- Normalize file paths before validation.
- Restrict access to approved directories only.