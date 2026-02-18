import boto3
import datetime
from botocore.exceptions import ClientError

# 1. SETUP: Connect to AWS using the 'auditor' profile we created earlier.
# This ensures we don't accidentally use your personal/root keys.
session = boto3.Session(profile_name='auditor')
iam = session.client('iam')

def audit_users():
    print("🚀 Starting IAM User Audit...\n")
    
    try:
        # 2. GET USERS: We use a 'Paginator'. 
        # Why? If an account has 1,000+ users, a standard call only returns the first 100.
        # A paginator automatically fetches ALL pages of results.
        paginator = iam.get_paginator('list_users')
        
        for page in paginator.paginate():
            for user in page['Users']:
                username = user['UserName']
                
                # 3. ANALYZE: Check for Stale Console Access
                # 'PasswordLastUsed' is only present if the user has a console password.
                password_last_used = user.get('PasswordLastUsed', 'Never (or no password)')
                
                # 4. ANALYZE: Check for Access Keys (API Keys)
                # We need a separate API call to list keys for each user.
                keys_response = iam.list_access_keys(UserName=username)
                active_keys = [k['AccessKeyId'] for k in keys_response['AccessKeyMetadata'] if k['Status'] == 'Active']
                
                # 5. REPORT: Print findings to the console
                print(f"👤 User: {username}")
                print(f"   - Console Last Login: {password_last_used}")
                
                if active_keys:
                    print(f"   - ⚠️  Active Access Keys Found: {len(active_keys)}")
                else:
                    print(f"   - ✅ No Active Access Keys")
                
                print("-" * 30)

    except ClientError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    audit_users()