# AWS IAM Security Audit

A lightweight Python tool that programmatically audits IAM users in an AWS account, detecting stale credentials, orphaned access keys, and console login anomalies.

## Features / Checks

| Check | Description |
|-------|-------------|
| **Console Login Staleness** | Flags users who have never logged in or haven't used the console recently |
| **Active Access Keys** | Enumerates active programmatic access keys per user |
| **Paginated Enumeration** | Handles accounts with 1,000+ IAM users via boto3 paginators |
| **Profile-Based Auth** | Uses AWS named profiles — no hardcoded credentials |

## Prerequisites

- **Python 3.8+**
- **AWS CLI** configured with a named profile that has IAM read permissions
- Minimum IAM policy for the audit profile:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:ListUsers",
        "iam:ListAccessKeys"
      ],
      "Resource": "*"
    }
  ]
}
```

## Setup

```bash
# Clone the repo
git clone https://github.com/elkana-langat/cloud-iam-audit.git
cd cloud-iam-audit

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## How to Run

The script uses the AWS named profile `auditor` by default. Make sure the profile is configured:

```bash
# Configure the audit profile (one-time)
aws configure --profile auditor

# Run the audit
python src/audit.py
```

To use a different profile, edit `profile_name` in `src/audit.py`:

```python
session = boto3.Session(profile_name='your-profile-name')
```

## Example Output

```
🚀 Starting IAM User Audit...

👤 User: admin-elkana
   - Console Last Login: 2025-02-10 08:32:15+00:00
   - ⚠️  Active Access Keys Found: 1
------------------------------
👤 User: deploy-bot
   - Console Last Login: Never (or no password)
   - ✅ No Active Access Keys
------------------------------
👤 User: intern-jane
   - Console Last Login: 2024-06-22 14:01:00+00:00
   - ⚠️  Active Access Keys Found: 2
------------------------------
```

## Security Notes

- **No hardcoded credentials.** The script authenticates via AWS CLI named profiles only.
- **Read-only operations.** The tool calls `ListUsers` and `ListAccessKeys` — it does not modify any IAM resources.
- **Never commit `.env` or AWS credential files.** The `.gitignore` excludes these by default.

## Project Structure

```
cloud-iam-audit/
├── src/
│   └── audit.py          # Main audit script
├── images/               # Screenshots of audit output
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## Limitations

- Currently audits a **single AWS account** (the one associated with the configured profile)
- Does not check **access key age** or **last-used date** — only whether keys are active
- Does not evaluate **MFA enrollment** status
- Does not analyze **attached IAM policies** for over-permissioning
- Output is terminal-only (no CSV/JSON export yet)

## Next Improvements

- [ ] Access key age analysis — flag keys older than 90 days
- [ ] MFA enrollment check per user
- [ ] Export to CSV / JSON for SIEM integration
- [ ] IAM policy analysis (detect wildcard or overly broad permissions)
- [ ] Multi-account scanning via AWS Organizations
- [ ] CLI argument for custom profile name (`--profile`)

## License

MIT — see [LICENSE](LICENSE) for details.
