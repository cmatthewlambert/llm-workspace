CONTEXT
You will receive physical metadata for ONE Snowflake table.

You ALSO have access to an enterprise acronym reference file:

ACRONYM_FILE: {{acronym_file_name_or_uri}}

The file contains mappings such as:
acronym → expansion → description → domain (optional)

Example:
"ARR" → "Annual Recurring Revenue"
"PII" → "Personally Identifiable Information"
"SKU" → "Stock Keeping Unit"

You MUST use this file when expanding or interpreting abbreviations.

---

TASK

Produce:

1) Logical display name + description for the table.
2) Logical display name + description for EVERY column.

Follow naming conventions and acronym rules below.

---

ACRONYM USAGE RULES

1. If a column/table contains an acronym present in the file:
   - Expand it in the logical name where appropriate.
   - Preserve the acronym in parentheses if widely recognized.
     Example: "Customer ID", "Annual Recurring Revenue (ARR)"

2. If acronym is universally standard (ID, URL, API, SSN):
   - Keep acronym form in logical name.

3. If acronym exists in file but expansion is domain-specific:
   - Use domain context from table/columns to choose best fit.

4. If acronym is NOT in file:
   - Do NOT guess.
   - Mark needs_human_review=true.
   - Ask a clarification question.

5. Never create new acronyms.

---

NAMING CONVENTIONS

- Logical names: Title Case, no underscores.
- IDs: “… ID”
- Booleans: Start with “Is” / “Has”
- Dates: “... Date”
- Timestamps: “... At”
- Amounts: Avoid currency assumptions unless explicit.
- Status/flags: Use business wording, not physical names.

---

OUTPUT JSON SCHEMA (STRICT)

{
  "table": {
    "database": "string",
    "schema": "string",
    "table_name_physical": "string",
    "table_name_logical": "string",
    "table_description": "string",
    "grain": "string",
    "primary_key_candidates": ["string"],
    "foreign_key_candidates": [
      {
        "column": "string",
        "references_hint": "string"
      }
    ],
    "classification": {
      "contains_pii": "boolean",
      "pii_columns": ["string"]
    },
    "needs_human_review": "boolean",
    "clarification_question": "string"
  },
  "columns": [
    {
      "column_name_physical": "string",
      "column_name_logical": "string",
      "data_type": "string",
      "nullable": "boolean",
      "description": "string",
      "semantic_type": "string",
      "pii": "boolean",
      "needs_human_review": "boolean",
      "clarification_question": "string"
    }
  ]
}

---

SEMANTIC TYPE ENUM

Choose one:

[
 "identifier",
 "timestamp",
 "date",
 "boolean",
 "currency_amount",
 "quantity",
 "status",
 "category",
 "free_text",
 "json",
 "geography",
 "other"
]

---

PHYSICAL METADATA

Database: {{database}}
Schema: {{schema}}
Table: {{table_name}}
Table Comment: {{table_comment_or_empty}}

Columns:

{{columns_block}}

Format per column:
name={{col_name}} | type={{data_type}} | nullable={{true/false}} | comment={{comment_or_empty}}

---

PII DETECTION RULES

Set contains_pii=true ONLY if strongly indicated by names such as:

email, ssn, phone, address, dob, first_name, last_name, ip_address.

---

GRAIN RULE

Describe “One row equals …” if inferable.
Else return: "Unknown".

---

FINAL INSTRUCTIONS

- Use the acronym file wherever applicable.
- Do not hallucinate meanings.
- Do not skip columns.
- Ensure JSON is valid and complete.
- Ask clarification questions only when necessary.

Now produce the JSON output.
