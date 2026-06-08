# DVWA CSP Bypass - Impossible

## Steps

- Opened Impossible level.
  - Screenshot: `01_target_impossible.jpg`

- Clicked **Solve the sum**.
  - Screenshot: `02_impossible_normal_result.jpg`

- Tested:

```text
jsonp_impossible.php?callback=alert
```

- Callback was ignored.
  - Screenshot: `03_impossible_callback_ignored.jpg`

## Result

- CSP bypass failed.

## Reason

- Callback function is hardcoded:

```javascript
solveSum({"answer":"15"})
```

- User cannot control the function name.

## Fix

- Avoid user-controlled JSONP callbacks.
- Use fixed callbacks or JSON+CORS.