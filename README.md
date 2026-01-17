
# Assignment 1 – Text Normalization and Token Frequency Analysis

## Files
- `normalize_text.py` – Main script for normalization, counting, and analysis
- `environment.yml` – Conda environment specification
- `README.md` – Project documentation
- `output/` – Generated outputs (token count files and plots; created automatically)
---

## Requirements
- Python 3.14
- Conda 
- Required Python packages are listed in `environment.yml`

### Create or update the conda environment
From the repository root:

```bash
conda env create -f environment.yml
conda activate 4nl3
```

## How to Run

From the repository root:

```bash
# activate the provided conda environment
conda activate 4nl3

# show help
python normalize_text.py --help

# basic run (tokenize + counts)
python normalize_text.py data/pg2554.txt

# full pipeline with plot
python normalize_text.py data/pg2554.txt -lowercase -myopt -stopwords -stem -analyze

# lemmatization instead of stemming
python normalize_text.py data/Linux.txt -lowercase -lemmatize -analyze
```

Notes:
- Input and output use UTF-8.
- The custom option `-myopt` removes digit-only tokens (e.g., years, timestamps, PIDs) to reduce sparsity.
- `-stem` and `-lemmatize` are mutually exclusive by design.

## Rationale: UTF-8 with errors="replace"

The file reader uses UTF-8 with `errors="replace"` to ensure that any malformed bytes in large or mixed-encoding corpora do not crash the run. Invalid sequences are replaced with the Unicode replacement character, allowing processing to continue while keeping output deterministic.

## Generative AI Usage Disclosure (Required)

Generative AI tools were used **only for conceptual clarification, debugging guidance, and assistance with code structure and documentation wording**. All final code, decisions, and interpretations were written and verified by the student.

### AI Usage Details
- **Model:** ChatGPT 5.2
- **Provider:** OpenAI
- **Hardware type:** Cloud-based GPU/accelerator
- **Region of compute:** Unknown
- **Time used:** Approximately 2–3 hours total across multiple short interactions
- **How values were estimated:** Time was approximated based on active interaction duration during development and debugging
- **Estimated emissions:**  
  ~4.32 g CO₂ per query × ~25 queries ≈ **108 g CO₂**

