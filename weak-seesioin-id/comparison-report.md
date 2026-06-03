# Weak Session IDs Comparison Report

## Low

* Session IDs were sequential.
* Values increased as `1, 2, 3, 4...`.
* Future session IDs could be accurately predicted.
* Vulnerable.

## Medium

* Session IDs were generated using `time()`.
* Values reflected the current Unix timestamp.
* Future session IDs could be estimated from the current time.
* Vulnerable.

## High

* Session IDs were generated using MD5 hashes.
* Underlying values were sequential integers.
* Hashes such as `MD5(1)`, `MD5(2)`, `MD5(3)` were predictable.
* Vulnerable.

## Impossible

* Session IDs were generated using random data and SHA1.
* No observable pattern existed between generated values.
* Secure and HttpOnly cookie flags were enabled.
* Not vulnerable.

## Conclusion

* Low: Vulnerable due to sequential session IDs.
* Medium: Vulnerable due to timestamp-based session IDs.
* High: Vulnerable because predictable values were only hashed.
* Impossible: Secure because session identifiers are generated using random data and protected cookie settings.
