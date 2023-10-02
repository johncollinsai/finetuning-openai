import os
import openai

def get_api_key():
    try:
        api_key = os.environ["OPENAI_API_KEY"]
        openai.api_key = api_key  # set api key for the openai library
        print("API Key obtained.")
        return api_key
    except KeyError:
        print("Environment variable OPENAI_API_KEY is not set.")
        exit()

# Ensure API key is obtained
api_key = get_api_key()

# Function to upload the dataset file
def upload_dataset(api_key, file_path):
    try:
        print(f"Uploading dataset from: {file_path}")
        response = openai.File.create(
            file=open(file_path, "rb"),
            purpose="fine-tune"
        )
        print("Upload Response:", response)
        file_id = response["id"]
        return file_id
    except Exception as e:
        print("An error occurred during file upload:", e)
        exit()

# Function to create a fine-tuning job
def create_fine_tuning_job(api_key, file_id, model="gpt-3.5-turbo"):
    try:
        print(f"Creating fine-tuning job for file id: {file_id}")
        response = openai.FineTuningJob.create(
            training_file=file_id,
            model=model
        )
        print("Fine-Tuning Job Response:", response)
        job_id = response["id"]
        return job_id
    except Exception as e:
        print("An error occurred during fine-tuning job creation:", e)
        exit()

# Path to your dataset file
dataset_file_path = "path/to/your/dataset.jsonl"

# Upload the dataset file and get the file ID
file_id = upload_dataset(api_key, dataset_file_path)

# Create a fine-tuning job with the uploaded file ID
job_id = create_fine_tuning_job(api_key, file_id)

# Output the job ID
print("Fine-Tuning Job ID:", job_id)


