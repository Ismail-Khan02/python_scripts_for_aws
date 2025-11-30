import boto3
import os

# Initialize the EC2 client
# The region can be set via an environment variable or hardcoded
REGION = os.environ.get('AWS_REGION', 'us-east-1')
ec2 = boto3.client('ec2', region_name=REGION)

def lambda_handler(event, context):
    """
    Stops EC2 instances that have the tag 'AutoStop' with value 'True'.
    """
    
    # Define the filter to target specific instances
    # Key: Tag name, Value: Tag value
    filters = [
        {'Name': 'tag:AutoStop', 'Values': ['True']},
        {'Name': 'instance-state-name', 'Values': ['running']}
    ]

    try:
        # Get a list of all running instances matching the filter
        response = ec2.describe_instances(Filters=filters)
        
        # Extract the Instance IDs
        instance_ids_to_stop = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_ids_to_stop.append(instance['InstanceId'])

        if instance_ids_to_stop:
            print(f"Found {len(instance_ids_to_stop)} instances to stop: {instance_ids_to_stop}")
            
            # Stop the instances
            ec2.stop_instances(InstanceIds=instance_ids_to_stop)
            print("Successfully stopped instances.")
        else:
            print("No running instances found with tag 'AutoStop: True'.")

        return {
            'statusCode': 200,
            'body': f"Stopped {len(instance_ids_to_stop)} instances."
        }

    except Exception as e:
        print(f"Error stopping instances: {e}")
        raise e

# To test locally, you would need to set up AWS credentials and environment variable:
# if __name__ == "__main__":
#     # Set a dummy region for local testing if needed
#     # os.environ['AWS_REGION'] = 'us-east-1' 
#     lambda_handler(None, None)