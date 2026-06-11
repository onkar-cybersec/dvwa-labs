# DVWA File Inclusion - High

## Step 1
Open the DVWA File Inclusion page and set the security level to High.

![Target Page](images/01-target-page.__temp__.JPG)

## Step 2
Verify that the application loads an approved file normally.

```text
?page=file1.php
```

![Normal File Load](images/02-normal-file1.__temp__.JPG)

## Step 3
Test a file wrapper payload.

```text
?page=file:///etc/passwd
```

![File Wrapper Payload](images/03-file-wrapper-payload.__temp__.JPG)

## Step 4
Observe that the contents of `/etc/passwd` are displayed.

![LFI Success](images/04-lfi-success-passwd.__temp__.JPG)

## Result
Successfully exploited a Local File Inclusion vulnerability using a file wrapper payload.

## Reason
The application only checks whether the supplied value starts with `file` or matches an approved filename. The `file://` wrapper satisfies this validation and allows arbitrary local file inclusion.

## Fix
- Use a strict allowlist of approved files.
- Do not allow user-controlled file paths.
- Normalize file paths before validation.
- Disable unnecessary PHP wrappers.
- Restrict access to approved application resources.