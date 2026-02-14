import pandas as pd
import math
import os

# Configuration
CSV_FILE = 'data_dictionary.csv'
ABBREV_FILE = 'abbreviations.txt'
TABLES_PER_CHUNK = 50
OUTPUT_DIR = 'copilot_prompts'

def generate_prompts():
    # 1. Read the abbreviations into a string
    with open(ABBREV_FILE, 'r') as f:
        abbreviations = f.read()

    # 2. Read the data dictionary
    df = pd.read_csv(CSV_FILE)
    
    # 3. Get a list of unique tables
    # Assuming uniqueness is a combination of DB, Schema, and Table
    unique_tables = df[['DB_NAME', 'SCHEMA_NAME', 'TABLE_NAME']].drop_duplicates().to_dict('records')
    total_chunks = math.ceil(len(unique_tables) / TABLES_PER_CHUNK)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 4. Generate prompt files for each chunk
    for i in range(total_chunks):
        # Get the 50 tables for this chunk
        chunk_tables = unique_tables[i * TABLES_PER_CHUNK : (i + 1) * TABLES_PER_CHUNK]
        
        # Filter the main dataframe to only include rows for these 50 tables
        chunk_df = pd.DataFrame()
        for t in chunk_tables:
            temp_df = df[(df['DB_NAME'] == t['DB_NAME']) & 
                         (df['SCHEMA_NAME'] == t['SCHEMA_NAME']) & 
                         (df['TABLE_NAME'] == t['TABLE_NAME'])]
            chunk_df = pd.concat([chunk_df, temp_df])

        # Convert the chunked dataframe to a CSV string for the prompt
        data_string = chunk_df.to_csv(index=False)

        # 5. Construct the Copilot Prompt
        prompt_content = f"""
You are an expert data architect. Below is a list of common company abbreviations and a chunk of our data dictionary containing {len(chunk_tables)} tables.

### Task
Analyze the `COLUMN_NAME` for each row. Using the provided Abbreviations list, generate a `LOGICAL_NAME` (a human-readable business name) and a `DESCRIPTION` for what the column represents.

### Output Format
Respond ONLY with a CSV formatted block containing the following columns:
DB_NAME, SCHEMA_NAME, TABLE_NAME, COLUMN_NAME, DATA_TYPE, NULLABILITY, LOGICAL_NAME, DESCRIPTION

### Abbreviations
{abbreviations}

### Data Dictionary Chunk
{data_string}
"""
        # Write to file
        filename = os.path.join(OUTPUT_DIR, f'prompt_chunk_{i+1}.md')
        with open(filename, 'w') as f:
            f.write(prompt_content)
            
    print(f"Successfully generated {total_chunks} prompt files in the '{OUTPUT_DIR}' directory.")

if __name__ == "__main__":
    generate_prompts()
