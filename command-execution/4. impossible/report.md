 ; ls# Command Injection - Impossible

## Step 1
Set DVWA Security Level to **Impossible**.

## Step 2
Entered a valid IP address (`8.8.8.8`) and confirmed that the application executed the ping command normally.

## Step 3
Attempted command injection using the payload:

8.8.8.8 ; ls

## Step 4
The application rejected the input and displayed the error:

ERROR: You have entered an invalid IP.

## Step 5
Reviewed the source code using the **View Source** feature.

## Result
Command injection attack was not successful.

## Reason
The application implements strict input validation by:

- Splitting the input into four IP octets.
- Verifying that each octet is numeric using `is_numeric()`.
- Ensuring exactly four octets exist using `sizeof($octet) == 4`.
- Rejecting any input that contains command separators or additional characters.
- Using Anti-CSRF token validation to protect requests.

Because the payload contains non-numeric characters (`; ls`), validation fails before the system command is executed.

## Conclusion
The Impossible security level effectively prevents command injection through strict allowlist validation and request protection mechanisms.

## Fix

Already Implemented:

- Strict input validation
- Allowlist-based IP verification
- Anti-CSRF protection
- Rejection of malformed input before command execution

## Screenshots

![Normal Ping Request](images/01.normal.JPG)

![Injection Attempt Blocked](images/02.Fail.JPG)

![Source Code Review](images/03.source code.JPG)