import pandas as pd
import subprocess

mutation_options = ['bd', 'bf', 'bi', 'br', 'bp', 'bei', 'bed', 'ber', 'sr', 'sd', 'lds', 'lr2', 'li', 'ls', 'lp', 'lis', 'lrs', 'td', 'tr2', 'ts1', 'ts2', 'tr', 'uw', 'num', 'ft', 'fn', 'fo']


def generate_mutations(prompt, prompt_id):
    mutations = []
    for mutation_option in mutation_options:
        print(f"Prompt ID: {prompt_id} mutation option: {mutation_option}")
        mutation = subprocess.run(['./radamsa.exe', '-p', 'od', '-m', mutation_option], input=prompt, capture_output=True, text=True, encoding='latin-1')
        if mutation.returncode == 0 and mutation.stdout is not None:
            mutations.append((prompt_id, mutation_option, mutation.stdout.strip()))
        else:
            print(f"Error generating mutation for prompt ID: {prompt_id} with option: {mutation_option}")
    return mutations


base_prompts = pd.read_csv('LLMSecEval-prompts.csv')

mutated_prompts = []
for index, row in base_prompts.iterrows():
    prompt_id = row['ID']
    mutated_prompts.extend(generate_mutations(row['NL Prompt'].replace('<language>', row['Language']), prompt_id))

mutated_prompts_df = pd.DataFrame(mutated_prompts, columns=['ID', 'Mutation Option', 'Mutated Prompts'])
mutated_prompts_df.to_csv('mutated_prompts.csv', index=False)
