import pandas as pd
import code_bert_score


def calculate_similarity(base_code, mutated_code, language):
    reference_bert = [base_code]
    hypothesis_bert = [mutated_code]
    bert_score = code_bert_score.score(cands=hypothesis_bert, refs=reference_bert, lang=language)
    f1 = bert_score[2].item()
    return f1


base_code_df = pd.read_csv('gen_code.csv')
mutated_code_df = pd.read_csv('mutated_prompts_gen_code.csv')

results = []
base_prompt = ''
current_id = None

for _, mutated_row in mutated_code_df.iterrows():
    base_row = base_code_df[base_code_df['ID'] == mutated_row['ID']].iloc[0]

    if mutated_row['ID'] != current_id:
        base_prompt = base_row['NL Prompt']
        current_id = mutated_row['ID']
        print(int(mutated_row['ID']))
    language = base_row['Language']
    bert_score = calculate_similarity(base_row['Generated Code'], mutated_row['Generated Code'], language)

    results.append({
        'ID': mutated_row['ID'],
        'Base Prompt': base_prompt,
        'Base Code': base_row['Generated Code'],
        'Mutation Option': mutated_row['Mutation Option'],
        'Mutated Prompt': mutated_row['Mutated Prompts'],
        'Mutated Code': mutated_row['Generated Code'],
        'BERT Score': bert_score
    })

results_df = pd.DataFrame(results)
results_df.to_csv('similarity_results.csv', index=False)