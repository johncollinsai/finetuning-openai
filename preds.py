import traceback
import os
import openai
import json

def get_api_key():
    api_key = os.environ["OPENAI_API_KEY"]
    openai.api_key = api_key    
    return api_key

api_key = get_api_key()

def generate_response(
        prompt, 
        model, 
        project_type,
        max_batch_size=4, 
        max_tokens=2000, # max tokens for gpt-4 = 8192, for palm-2 supported range = [1, 1025)
        temperature=0.5, # 0 implies models will always pick most likely next word. Set zero but use high top_p and top_k values
        top_p=0.95, # top-P determines how selects tokens for output, where lower value = less random responses 
    ):
    try:        
        # Construct the specific prompt for this task
        rr_sequence = prompt.split("AAPL_rr:")[-1].split("AAPL_lr:")[0].strip()
        lr_sequence = prompt.split("AAPL_lr:")[-1].strip()
        
        user_prompt_rr = f"The sequence for AAPL_rr is: {rr_sequence} What are the next 50 values in this sequence?"
        user_prompt_lr = f"The sequence for AAPL_lr is: {lr_sequence} What are the next 50 values in this sequence?"
        
        # Use OpenAI API for prediction
        response_rr = openai.Completion.create(
            model="gpt-4-0613",
            prompt=user_prompt_rr,
            max_tokens=max_tokens,
            stop=None,
            temperature=temperature,
            top_p=top_p,
        )
        
        response_lr = openai.Completion.create(
            model="gpt-4-0613",
            prompt=user_prompt_lr,
            max_tokens=max_tokens,
            stop=None,
            temperature=temperature,
            top_p=top_p,
        )
        
        final_response_rr = response_rr['choices'][0]['text'].strip()
        final_response_lr = response_lr['choices'][0]['text'].strip()
        
        return f"AAPL_rr predictions: {final_response_rr}\n\nAAPL_lr predictions: {final_response_lr}"
        
    # except block to catche any other errors and print to terminal
    except Exception as e:
        print(f"An error of type {type(e).__name__} occurred during the generation: {str(e)}")
        traceback.print_exc()
        return str(e)