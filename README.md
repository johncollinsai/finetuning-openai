```markdown
# finetuning-openai
![Prompt Engineering vs Fine-Tuning for Stock Price Predictions](finetuning-openai-3.png)

## Prompt Engineering vs Fine-Tuning for Stock Price Predictions
This repo contains code and examples from my blog post on using prompt engineering and fine-tuning with GPT models for stock price predictions.

## Overview
In this post, I dive deep into the fine-tuning of language models and prompt engineering, using the problem setting of stock price prediction based on high-frequency OHLC stock price data for AAPL.

I demonstrate that fine-tuning, especially with models like GPT-3.5 Turbo, is the stronger approach. The ability to train a model on specific data, such as price sequences, enhances its understanding and predictive power for those unique use cases.

## Key topics covered:
- Formatting stock price data for fine-tuning
- Training loops and hyperparameters
- Monitoring training progress
- Generating predictions from a fine-tuned model


- Engineering effective prompts with context
- Token limits and other challenges of prompting
- Using ChatGPT's advanced data analysis plugin

## Code:

Various Python scripts support the work reported in the post:

### createfile.py
This script reads the first 100,000 lines from an input file `df_data_AAPL.txt` and writes them to a new output file `100000_lines_AAPL.txt`.

```python
# File paths
input_file_path = "/home/john/finetuning-openai/df_data_AAPL.txt"
output_file_path = "/home/john/finetuning-openai/100000_lines_AAPL.txt"
linecount = 100000

# Read the first linecount lines and write to the new file
with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    for _ in range(linecount):
        line = infile.readline()
        if not line:
            break  # Break if there are fewer than 100,000 lines
        outfile.write(line)
```

### finetuning.py
This script formats a raw CSV stock price dataset into JSONL, uploads it to OpenAI, and creates a fine-tuning job to train a GPT-3.5 model on predicting stock prices.

```python
import os
import openai
import csv
import json

raw_data_path = "100000_lines_AAPL.txt"

# Function to format dataset for fine-tuning
def format_dataset_for_finetuning(raw_data_path):
    formatted_data = []
    with open(raw_data_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # skip headers
        prev_row = next(reader)  # Store previous row's data for use in the next iteration
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
        f.write(json.dumps(entry) + '\n')  # Use json module's dumps method to convert dictionaries into valid JSON strings

# ... rest of the code for API key retrieval, dataset upload, and fine-tuning job creation ...
```

### preds.py
This code extracts stock price sequences from a CSV, constructs prompts to get hypothetical continuations from GPT-4, and prints the predicted next values.

```python
import traceback
import os
import openai
import json
import pandas as pd
from io import StringIO

# ... rest of the code for API key retrieval and file reading ...

def generate_response(
        model="gpt-4-0613",
        max_tokens=2000,
        temperature=0.5,
        top_p=0.95,
    ):
    try:
        content = read_file("100_lines_AAPL.txt")
        rr_sequence, lr_sequence = extract_sequences_from_csv(content)
        user_prompt_rr = f"For a hypothetical scenario, based on the sequence for AAPL_rr: {rr_sequence}, what might be the next 10 values?"
        user_prompt_lr = f"For a hypothetical scenario, based on the sequence for AAPL_lr: {lr_sequence}, what might be the next 10 values?"

        # ... rest of the code for sending prompts to OpenAI and obtaining responses ...

        return f"AAPL_rr predictions: {final_response_rr}\n\nAAPL_lr predictions: {final_response_lr}"

    except Exception as e:
        print(f"\nAn error of type {type(e).__name__} occurred during the generation: {str(e)}")
        traceback.print_exc()
        return str(e)

if __name__ == "__main__":
    response = generate_response()
    print(response)
```

## References

- **OpenAI Documentation.** "Fine-tuning." [\<https://platform.openai.com/docs/guides/fine-tuning\>](https://platform.openai.com/docs/guides/fine-tuning)
- **OpenAI Documentation.** "API reference." [\<https://platform.openai.com/docs/api-reference/fine-tuning\>](https://platform.openai.com/docs/api-reference/fine-tuning)
- **OpenAI Updates.** "GPT-3.5 Turbo fine-tuning and API." [\<https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates\>](https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates)
- **OpenAI Documentation.** "DALL·E 3." [\<https://openai.com/dall-e-3\>](https://openai.com/dall-e-3)
- Refer to the original post <a href="https://johncollins.ai/finetuning-openai" target="_blank">Prompt Engineering vs. Fine-Tuning: Navigating GPT Models for Stock Price and Volatility Predictions</a> for additional details and examples.
```