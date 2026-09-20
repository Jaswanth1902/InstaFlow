# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

Security is paramount in InstaFlow. Because InstaFlow interacts directly with session authentication and direct messaging:

1. **Zero Secret Leakage**: Never commit `.env` or session tokens (`sessionid`, `ds_user_id`, `csrftoken`) to version control.
2. **Subprocess Isolation**: All background commands strictly enforce `creationflags=0x08000000` (`CREATE_NO_WINDOW`) to prevent focus stealing or shell exposure.
3. **DWEL Anti-Loop Protection**: Infinite bot-to-bot ping pong loops are systematically intercepted via local action tracking.

To report security issues, please contact: `jaswanthreddy1537@gmail.com`.
