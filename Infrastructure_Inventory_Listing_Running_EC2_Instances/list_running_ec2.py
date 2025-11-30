import boto3
from tabulate import tabulate # You may need to pip install tabulate

# Initialize the EC2 resource
REGION = 'us-east-1'  # Change this to your desired region
ec2 = boto3.resource('ec2', region_name=REGION)

def list_running_instances():
    """
    Retrieves and prints details of all running EC2 instances in the specified region.
    """
    
    # Filter for instances in the 'running' state
    filters = [
        {'Name': 'instance-state-name', 'Values': ['running']}
    ]

    running_instances = ec2.instances.filter(Filters=filters)
    
    instance_data = []
    
    # Iterate through the filtered instances
    for instance in running_instances:
        # Get the 'Name' tag, or default to 'No Name Tag'
        instance_name = 'No Name Tag'
        if instance.tags:
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
                    break
        
        instance_data.append([
            instance_name,
            instance.id,
            instance.instance_type,
            instance.public_ip_address if instance.public_ip_address else '-',
            instance.launch_time.strftime("%Y-%m-%d %H:%M:%S")
        ])

    if instance_data:
        # Define table headers
        headers = ["Name", "Instance ID", "Type", "Public IP", "Launch Time (UTC)"]
        
        # Use the tabulate library for clean, console-friendly output
        print(f"## 🏃 Running EC2 Instances in {REGION} ##")
        print(tabulate(instance_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print(f"No running EC2 instances found in region {REGION}.")

if __name__ == "__main__":
    list_running_instances()