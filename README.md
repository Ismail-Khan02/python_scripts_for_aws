## 🐍 DevOps Python Scripts for AWS Automation

This repository contains essential Python scripts leveraging the Boto3 library for automating various tasks across the AWS cloud environment, focusing on cost management, inventory, storage, deployment, and security.

| Script File | Category | Description |
| :--- | :--- | :--- |
| `auto_stop_ec2.py` | Cost Optimization | Automatically stops idle EC2 instances based on a specific tag to save compute costs. |
| `list_running_ec2.py` | Inventory & Monitoring | Retrieves and displays a list of all running EC2 instances with key metadata in a clean, tabular format. |
| `s3_cleanup.py` | Storage Management | Cleans up specified S3 buckets by deleting objects older than a defined retention period. |
| `deploy_api_gateway.py` | CI/CD & Automation | Automates the creation of a new Deployment and updates the specified API Gateway Stage to promote the latest API version. |
| `secrets_manager_util.py` | Security | Demonstrates the secure retrieval of credentials from Secrets Manager and outlines the structure for custom secret rotation. |

---

### 1. Cost Optimization: Automatic EC2 Instance Shutdown 💰

### `auto_stop_ec2.py`

This Python script is designed for **AWS cost management** by automatically stopping idle or unnecessary EC2 instances. It is typically deployed as an **AWS Lambda function** triggered by an EventBridge (CloudWatch Events) schedule (e.g., every weekday at 7 PM).

The script identifies all currently **running EC2 instances** that possess the specific tag `AutoStop: True` and issues the command to stop them, preventing unnecessary compute costs during non-business hours.

### 2. Infrastructure Inventory: Listing Running EC2 Instances 🔍

### `list_running_ec2.py`

This is a fundamental **infrastructure visibility** script that uses the AWS SDK (**Boto3**) to query the specified AWS region. It retrieves a comprehensive list of all **currently running EC2 instances**.

The script extracts key information for each running instance, including its **Instance ID**, **Instance Type**, the **Name** tag, **Public IP Address**, and **Launch Time**. It then presents this data in a clean, easily readable table format in the console, making it useful for auditing, reporting, and quick inventory checks.

### 3. Storage Management: S3 Cleanup Tool 🗑️

### `s3_cleanup.py`

This script is crucial for **storage cost control and hygiene** in AWS S3. It connects to a specified S3 bucket and automatically identifies and deletes objects (files) that are older than a configurable threshold (default is **30 days**).

By using the `delete_objects` API call, the script efficiently removes stale artifacts, old logs, and temporary build files. This practice helps ensure the bucket only retains necessary data, minimizing accumulated storage costs.

### 4. Automation: API Gateway Deployment Tool 🚀

### `deploy_api_gateway.py`

Designed to be integrated into a **CI/CD pipeline**, this script automates the final steps of deploying an API. It uses the `apigateway` client to create a new **Deployment** for the specified Rest API ID.

After creating the deployment (which captures the current configuration), the script updates a designated **Stage** (e.g., `Prod`) to point to the new deployment ID. This process ensures that the live API endpoint reflects the latest code changes, allowing for controlled and automated promotion of API versions.

### 5. Security: Secrets Manager Rotation and Retrieval 🔑

### `secrets_manager_util.py`

This utility script demonstrates two essential functions related to **AWS Secrets Manager**:

1.  **Retrieval:** It shows the secure method for applications (e.g., running on EC2 or Lambda) to fetch sensitive credentials (like database passwords) at runtime, ensuring they are never hardcoded.
2.  **Rotation Outline:** It provides the conceptual structure required for writing a custom **Lambda rotation function**. Rotation scripts are key for security compliance, automatically creating, setting, and finalizing new passwords to prevent credentials from becoming static.

---

Would you like me to generate a simple example of how to run one of these Python scripts using the command line?