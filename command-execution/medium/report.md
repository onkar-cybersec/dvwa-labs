# Command Injection - Medium

## Step 1
Tested payload: 127.0.0.1; ls

## Step 2
Observed that ";" and other operators were blocked.

## Step 3
Tried alternative payload: 127.0.0.1 & ls

## Step 4
Successfully executed system command using single "&" operator.

## Result
Command injection vulnerability still exists and can be bypassed.

## Reason
Input filtering is incomplete and does not block all command separators.

## Fix
- Strict input validation
- Allowlist approach
- Avoid direct system command execution

## Screenshots

![Failed](images/failed.jpg)
![Bypass](images/bypass.jpg)
![Execution](images/whoami.jpg)