Step 2: Executing in VS Code via Copilot Chat
Once the script generates the prompt_chunk_X.md files, you can leverage VS Code Copilot Chat to process them rapidly.

Open the Copilot Chat Panel in VS Code.

Open prompt_chunk_1.md in your editor.

In the Chat input box, type: @workspace read #file:prompt_chunk_1.md and execute the task exactly as described in the file.
(Note: Using #file: forces Copilot to read the entire contents of that specific file into its context window).

Copilot will output the newly generated CSV data with the logical names and descriptions.

Click the "Copy" button on the code block Copilot generates and paste it into a new results file (e.g., results_chunk_1.csv).

Repeat for the remaining chunks.

Step 3 (Optional): Combining the Results
After you have processed all chunks through Copilot, you can run a quick bash or python script to concatenate all the results_chunk_X.csv files back into a single master data dictionary.

Would you like a quick script to re-combine those output CSVs once Copilot finishes generating them?
