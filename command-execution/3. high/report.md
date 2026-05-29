# Command Injection - High

## Step 1

Tested valid input and observed normal ping output.

Input used:

```text
127.0.0.1
```

## Step 2

Attempted basic command injection using semicolon payload.

Payload used:

```text
127.0.0.1;whoami
```

## Step 3

The payload failed because the High security level removed the semicolon from the input.

After filtering, the payload became invalid:

```text
127.0.0.1whoami
```

Possible observed error:

```text
ping: 127.0.0.1whoami: Name or service not known
```

In some cases, the page may show no output because the failed command does not return useful standard output.

## Step 4

Tested bypass payload using pipe operator without a space.

Payload used:

```text
127.0.0.1|whoami
```

## Result

Command injection was successful using the bypass payload.

## Reason

The application blocks common command separators such as semicolon, but the blacklist does not properly block the pipe operator when used without a space.

The failed payload was:

```text
127.0.0.1;whoami
```

The successful bypass payload was:

```text
127.0.0.1|whoami
```

## Impact

An attacker may be able to execute operating system commands through the vulnerable input field.

## Fix

* Use strict allowlist validation for IP addresses
* Avoid passing user input directly to system commands
* Avoid using `shell_exec()` with untrusted input
* Use safer built-in functions where possible
* Run the web server with low privileges

## Conclusion

DVWA Command Injection High blocks basic payloads, but command injection is still possible using a blacklist bypass.

## Screenshots

![Normal Attempt](images/01-normal.JPG)
![Failed Payload](images/02-failed.JPG)
![Successful Bypass](images/03-bypass.JPG)
