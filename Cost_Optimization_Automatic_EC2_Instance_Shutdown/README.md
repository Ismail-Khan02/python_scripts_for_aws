# Cost Optimization: Automatic EC2 Instance Shutdown 💰

A common task is to automatically stop unused development or staging EC2 instances outside of business hours to save costs. This script identifies instances with a specific tag (e.g., AutoStop: True) and stops them. This is typically run as an AWS Lambda function triggered by an Amazon EventBridge (CloudWatch Events) schedule.