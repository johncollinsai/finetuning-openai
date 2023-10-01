import os
import openai

def get_api_key():
    try:
        api_key = os.environ["OPENAI_API_KEY"]
        openai.api_key = api_key    # set api key for the openai library
        print("API Key obtained.")
        return api_key
    except KeyError:
        print("Environment variable OPENAI_API_KEY is not set.")
        exit()

api_key = get_api_key()
prompt = "Is Turbo a dog?"

def generate_response(api_key, prompt):
    try:
        print("Generating response for prompt:", prompt)
        response = openai.ChatCompletion.create(
            model="gpt-4",  # ensure that the model "gpt-4" is available
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.3,  
        )
        print("GPT-4 Response:", response)
        final_response = response.choices[0]["message"]["content"]
        return final_response.strip()

    except Exception as e:
        print("An error occurred:", e)

# Call the function to generate response
response = generate_response(api_key, prompt)
print("Final Response:", response)

