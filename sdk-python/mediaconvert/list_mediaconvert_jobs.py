import boto3

region = 'ap-northeast-2'  # Replace with your AWS region


def get_mediaconvert_job_statuses(region_name='us-east-1'):
    """
    Retrieves the status of all MediaConvert jobs in a region.

    Args:
        region_name (str, optional): The AWS region to list jobs from. Defaults to 'us-east-1'.

    Returns:
        dict: A dictionary where keys are job IDs and values are their statuses.
              Returns an empty dictionary if no jobs are found or an error occurs.
    """
    try:
        mediaconvert_client = boto3.client(
            'mediaconvert', region_name=region_name)

        job_statuses = {}

        # Initial call to list_jobs
        response = mediaconvert_client.list_jobs()

        # Process the current page of jobs
        for job in response.get('Jobs', []):
            job_id = job['Id']
            job_status = job['Status']
            job_statuses[job_id] = job_status

        # Handle pagination (if there are more jobs than the initial response)
        while 'NextToken' in response:
            response = mediaconvert_client.list_jobs(
                NextToken=response['NextToken'])
            for job in response.get('Jobs', []):
                job_id = job['Id']
                job_status = job['Status']
                job_statuses[job_id] = job_status

        return job_statuses

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


all_job_statuses = get_mediaconvert_job_statuses(region)

if all_job_statuses:
    print("MediaConvert Job Statuses:")
    print(all_job_statuses)
else:
    print("Could not retrieve job statuses.")
