import boto3

# --- Configuration ---
API_ID = 'abcdef1234'  # << Your RestApiId
STAGE_NAME = 'Prod'    # << The stage to update (e.g., Dev, Staging, Prod)
# ---------------------

apigw_client = boto3.client('apigateway')

def deploy_api_stage(api_id, stage_name):
    """
    Creates a new deployment for the API Gateway and links the stage to it.
    """
    print(f"Starting deployment process for API ID: {api_id}...")
    
    try:
        # 1. Create the Deployment
        # A deployment effectively 'freezes' the current state of the API
        response = apigw_client.create_deployment(
            restApiId=api_id,
            description=f'CI/CD Deployment triggered on {datetime.now().isoformat()}'
        )
        
        deployment_id = response['id']
        print(f"✅ Created new Deployment ID: {deployment_id}")

        # 2. Update the Stage to use the new Deployment
        # This is what makes the new changes live
        apigw_client.update_stage(
            restApiId=api_id,
            stageName=stage_name,
            patchOperations=[
                {
                    'op': 'replace',
                    'path': '/deploymentId',
                    'value': deployment_id
                }
            ]
        )
        
        print(f"✅ Successfully updated stage '{stage_name}' to use the new deployment.")
        print(f"API URL should now reflect the latest changes.")
        
    except Exception as e:
        print(f"❌ An error occurred during API Gateway deployment: {e}")
        # In a real pipeline, you would likely fail the build here
        raise e

if __name__ == "__main4":
    from datetime import datetime
    # Note: Replace API_ID with a valid one before running
    # deploy_api_stage(API_ID, STAGE_NAME)
    print("Script ran successfully (requires valid API_ID to execute deployment).")