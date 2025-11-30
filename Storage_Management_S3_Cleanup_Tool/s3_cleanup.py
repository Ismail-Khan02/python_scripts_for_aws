import boto3
from datetime import datetime, timedelta, timezone

# --- Configuration ---
BUCKET_NAME = 'your-devops-artifact-bucket'  # << CHANGE THIS TO YOUR BUCKET
DAYS_OLD = 30  # Files older than 30 days will be deleted
# ---------------------

s3 = boto3.client('s3')

def cleanup_s3_bucket():
    """
    Deletes objects from an S3 bucket that are older than the specified number of days.
    """
    
    # Calculate the cutoff date (30 days ago)
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_OLD)
    
    print(f"Starting cleanup for bucket: {BUCKET_NAME}")
    print(f"Deleting objects older than: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S UTC')}")

    objects_to_delete = {'Objects': []}
    
    try:
        # Paginator helps handle buckets with a large number of objects
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME)

        for page in pages:
            if 'Contents' not in page:
                continue

            for obj in page['Contents']:
                # The 'LastModified' time is timezone-aware
                if obj['LastModified'] < cutoff_date:
                    objects_to_delete['Objects'].append({'Key': obj['Key']})
                    print(f"   -> Found old object: {obj['Key']} (Last Modified: {obj['LastModified']})")

        if objects_to_delete['Objects']:
            print(f"\nAttempting to delete {len(objects_to_delete['Objects'])} objects...")
            
            # The delete_objects API call
            response = s3.delete_objects(
                Bucket=BUCKET_NAME,
                Delete=objects_to_delete
            )
            
            # Check for successful or failed deletions
            if 'Deleted' in response:
                print(f"✅ Successfully deleted {len(response['Deleted'])} objects.")
            if 'Errors' in response:
                print(f"❌ WARNING: Encountered {len(response['Errors'])} errors during deletion.")
                for error in response['Errors']:
                    print(f"   - Key: {error['Key']}, Code: {error['Code']}")
        else:
            print("No objects found that are older than the cutoff date.")

    except Exception as e:
        print(f"An error occurred during S3 cleanup: {e}")

if __name__ == "__main__":
    # WARNING: Ensure you are targeting the correct bucket before running!
    cleanup_s3_bucket()