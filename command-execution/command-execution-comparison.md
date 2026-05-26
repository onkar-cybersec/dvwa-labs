# Command Injection Comparison (DVWA)

## Low
- No input validation
- Command injection successful
- System commands executed directly

## Medium
- Basic filtering implemented
- Some payloads blocked
- Injection still possible using alternative separators

## High
- Strong input validation
- Malicious input rejected
- Injection attempts unsuccessful

## Impossible
- Strict allowlist validation
- Each IP octet must be numeric
- Anti-CSRF protection implemented
- Command injection completely prevented

## Conclusion
As the security level increases, the application applies stronger input validation and security controls. Low and Medium levels remain vulnerable to command injection, while High significantly reduces the attack surface. The Impossible level effectively prevents command injection through strict IP validation and additional security mechanisms.