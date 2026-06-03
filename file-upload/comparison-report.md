# DVWA File Upload - Comparison Report

## Low

* No validation on uploaded files.
* PHP web shell uploaded directly.
* Command execution achieved as `www-data`.

## Medium

* Checks client-supplied MIME type.
* MIME type changed in Burp Suite to `image/jpeg`.
* PHP web shell uploaded and executed successfully.

## High

* Validates extension and image content using `getimagesize()`.
* PHP payload embedded inside a valid PNG image.
* Upload succeeded, but PHP code was not executed.

## Impossible

* Validates extension, MIME type, file size, image content, and CSRF token.
* Re-encodes uploaded images and renames files with random hashes.
* PHP payload removed during processing; command execution not possible.

## Conclusion

Security improves at each level. Low and Medium are vulnerable to unrestricted file upload leading to command execution. High prevents direct execution but still accepts image-based payloads. Impossible provides effective protection through multiple validation layers and image re-encoding.
