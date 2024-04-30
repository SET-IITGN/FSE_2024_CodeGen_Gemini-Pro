from time import sleep
import pandas as pd
from vertexai.preview.generative_models import GenerativeModel
from vertexai.preview.generative_models import FinishReason


def generate(prompt):
    model = GenerativeModel("gemini-pro")
    generated_responses = []

    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.0,
            "top_p": 1
        },
        stream=True,
    )

    for response in responses:
        if response.candidates[0].finish_reason != FinishReason.SAFETY and response.candidates[0].finish_reason != FinishReason.RECITATION:
            if response.candidates:
                generated_responses.append(response.candidates[0].content.parts[0].text)
            else:
                print("Warning: Empty response for prompt:", prompt)
        else:
            generated_responses.append("code not generated due to safety issues")

    return generated_responses


df = pd.read_csv('mutated_prompts.csv', encoding='latin1')

mutated_df = pd.DataFrame(
    columns=['ID', 'Mutation Option', 'Mutated Prompts', 'Generated Code'])

for index, row in df.iterrows():
    nl_prompt = row['Mutated Prompts']
    mutation_option = row['Mutation Option']
    print(index)
    generated_code = generate(nl_prompt)
    generated_code = '\n'.join(generated_code)

    mutated_df.at[index, 'ID'] = row['ID']
    mutated_df.at[index, 'Mutation Option'] = mutation_option
    mutated_df.at[index, 'Mutated Prompts'] = nl_prompt
    mutated_df.at[index, 'Generated Code'] = generated_code

    sleep(1)

mutated_df.to_csv('mutated_prompts_gen_code.csv', index=False)
