# get_mediaconvert_job_status
import boto3


def get_mediaconvert_job_status(job_id):

    # Create a MediaConvert client
    mediaconvert = boto3.client('mediaconvert')

    # Get the job status
    response = mediaconvert.get_job(Id=job_id)

    # Extract the job status from the response
    job_status = response['Job']['Status']

    return job_status


if __name__ == "__main__":
    # Replace with your MediaConvert job ID
    job_id = 'your_job_id_here'
    status = get_mediaconvert_job_status(job_id)
    print(status)
    # COMPLETE, ERROR, PROGRESSING, CANCELED
