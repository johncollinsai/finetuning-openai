import traceback
import os
import openai
import json

def get_api_key():
    api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = api_key    
    return api_key

api_key = get_api_key()

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_response(
        model="gpt-4-0613",
        max_tokens=2000,
        temperature=0.5,
        top_p=0.95,
    ):
    try:
        # Read the file's content and set it as the prompt
        prompt = read_file("100_lines_AAPL.txt")
        
        # Print the provided prompt
        print("Provided Prompt:", prompt)
        
        # Construct the specific prompt for this task
        rr_sequence = prompt.split("AAPL_rr:")[-1].split("AAPL_lr:")[0].strip()
        lr_sequence = prompt.split("AAPL_lr:")[-1].strip()
        
        # Print the extracted sequences for AAPL_rr and AAPL_lr
        print("\nExtracted Sequence for AAPL_rr:", rr_sequence)
        print("Extracted Sequence for AAPL_lr:", lr_sequence)

        user_prompt_rr = f"For a hypothetical scenario, based on the sequence for AAPL_rr: {rr_sequence}, what might be the next 10 values?"
        user_prompt_lr = f"For a hypothetical scenario, based on the sequence for AAPL_lr: {lr_sequence}, what might be the next 10 values?"

        # Print the constructed prompts for AAPL_rr and AAPL_lr
        print("\nConstructed Prompt for AAPL_rr:", user_prompt_rr)
        print("Constructed Prompt for AAPL_lr:", user_prompt_lr)
        
        # Print the chosen model
        print("\nUsing Model:", model)
        
        # Use OpenAI API for prediction
        print("\nSending prompt to OpenAI for AAPL_rr...")
        response_rr = openai.ChatCompletion.create(
            model=model,        
            messages=[
                {"role": "system", "content": "You are a mathematician. Analyze the sequence and provide a hypothetical continuation based on mathematical patterns."},
                {"role": "user", "content": user_prompt_rr}
            ],
            max_tokens=max_tokens,
            stop=None,
            temperature=temperature,
            top_p=top_p,
        )

        print("Response from OpenAI for AAPL_rr:", response_rr)

        response_lr = openai.ChatCompletion.create(
            model=model,        
            messages=[
                {"role": "system", "content": "You are a mathematician. Analyze the sequence and provide a hypothetical continuation based on mathematical patterns."},
                {"role": "user", "content": user_prompt_rr}
            ],
            max_tokens=max_tokens,
            stop=None,
            temperature=temperature,
            top_p=top_p,
        )

        print("Response from OpenAI for AAPL_lr:", response_lr)
        
        final_response_rr = response_rr['choices'][0]['message']['content'].strip()
        final_response_lr = response_lr['choices'][0]['message']['content'].strip()
        
        # Print the obtained predictions
        print("\nPredicted Values for AAPL_rr:", final_response_rr)
        print("Predicted Values for AAPL_lr:", final_response_lr)
        
        return f"AAPL_rr predictions: {final_response_rr}\n\nAAPL_lr predictions: {final_response_lr}"
        
    # except block to catch any other errors and print to terminal
    except Exception as e:
        print(f"\nAn error of type {type(e).__name__} occurred during the generation: {str(e)}")
        traceback.print_exc()
        return str(e)

if __name__ == "__main__":
    response = generate_response()
    print(response)
