# File Inclusion Comparison (DVWA)

## Low

* No input validation
* Local File Inclusion successful
* Sensitive files accessible

## Medium

* Filters `../` sequences
* Filter bypass possible
* LFI still successful

## High

* Filename pattern validation
* `file://` wrapper bypass
* LFI still successful

## Impossible

* Strict allowlist
* Unauthorized files blocked
* LFI prevented

## Conclusion

As security increases, additional protections are introduced. However, Low, Medium, and High remain vulnerable through different bypass techniques. Only the Impossible level effectively prevents File Inclusion attacks through strict allowlist validation.
