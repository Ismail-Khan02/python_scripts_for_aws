import boto3
import json

# Initialize the Secrets Manager client
sm_client = boto3.client('secretsmanager')

def get_secret_value(secret_name):
    """
    Retrieves the SecretString from AWS Secrets Manager.
    """
    try:
        response = sm_client.get_secret_value(
            SecretId=secret_name
        )
        
        # Check if the secret is a plain string or a JSON object
        if 'SecretString' in response:
            secret = response['SecretString']
            try:
                # If it's a JSON string, load it into a Python dictionary
                return json.loads(secret)
            except json.JSONDecodeError:
                # Otherwise, return the plain string
                return secret
        else:
            # Handle binary secrets (not common for simple credentials)
            print("Warning: Secret is in binary format. Returning byte data.")
            return response['SecretBinary']

    except sm_client.exceptions.ResourceNotFoundException:
        print(f"Error: Secret '{secret_name}' not found.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    # --- Example 1: Retrieval (Common use in Lambda/EC2 applications) ---
    DB_SECRET_NAME = 'prod/db/credentials' # << Replace with your secret name
    
    db_credentials = get_secret_value(DB_SECRET_NAME)
    
    if db_credentials:
        print(f"## Retrieved Secret: {DB_SECRET_NAME} ##")
        # Assuming the secret is JSON: {"username": "user", "password": "pwd"}
        if isinstance(db_credentials, dict):
            print(f"Username: {db_credentials.get('username', 'N/A')}")
            # NEVER print the password in real code!
            print("Password: ***(Hidden for Security)***") 
        else:
            print(f"Secret Value: {db_credentials}")

    # --- Example 2: Rotation (The core logic for a custom rotation Lambda) ---
    # This is often packaged as a standalone Lambda function
    print("\n## Custom Rotation Logic Outline ##")
    print("A Python script for rotation handles three stages:")
    print("1. **create_secret**: Generates a new random password.")
    print("2. **set_secret**: Updates the database/service with the new password.")
    print("3. **finish_secret**: Moves the new password to the 'current' version.")

if __name__ == "__main__":
    main()