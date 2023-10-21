import os
import openai
import csv
import json

raw_data_path = "100000_lines_AAPL.txt"

def format_dataset_for_finetuning(raw_data_path):
    formatted_data = []

    with open(raw_data_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # skip headers

        # Store previous row's data for use in the next iteration
        prev_row = next(reader)
        
        for row in reader:
            user_content = ', '.join(prev_row)
            assistant_content = row[6]  # WeightedMidPrice column
            formatted_data.append(
                {
                    "messages": [
                        {"role": "system", "content": "Predict the WeightedMidPrice of AAPL for the next 50 steps based on historical data."},
                        {"role": "user", "content": user_content},
                        {"role": "assistant", "content": assistant_content}
                    ]
                }
            )
            prev_row = row
    
    print(f"Total formatted data points: {len(formatted_data)}")
    return formatted_data

formatted_dataset_path = "formatted_dataset.jsonl"
formatted_data = format_dataset_for_finetuning(raw_data_path)

# Write formatted_data to a new JSONL file
with open(formatted_dataset_path, 'w') as f:
    for entry in formatted_data:
        f.write(json.dumps(entry) + '\n')  #use json module's dumps method to convert dictionaries into valid JSON strings


def get_api_key():
    try:
        api_key = os.environ["OPENAI_API_KEY"]
        openai.api_key = api_key  
        print("API Key obtained.")
        return api_key
    except KeyError:
        print("Environment variable OPENAI_API_KEY is not set.")
        exit()

# Ensure API key is obtained
api_key = get_api_key()

# Upload the dataset file
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

# Create fine-tuning job
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

# Upload the dataset file and get the file ID
file_size = os.path.getsize(formatted_dataset_path)
print(f"Size of the formatted dataset file: {file_size} bytes")

file_id = upload_dataset(api_key, formatted_dataset_path)

# Create a fine-tuning job with the uploaded file ID
job_id = create_fine_tuning_job(api_key, file_id)

# Output the job ID
print("Fine-Tuning Job ID:", job_id)