# Assignment 2 — NLU (Problem 1 & Problem 2)

This folder is the **hand-in bundle** for Natural Language Understanding Assignment 2: **Word2Vec on IIT Jodhpur text** (Problem 1) and **character-level name generation with RNN / BiLSTM / attention** (Problem 2).

- **How to run the code:** follow the sections below (order matters for Problem 1).
- **Full narrative, task checklists, and figure placeholders:** see **[`overall_report.md`](overall_report.md)** in this same folder (master document aligned with the assignment brief).

---

## Requirements

- **Python:** 3.10+ recommended (matches `from __future__ import annotations` in the preprocessing script).
- **OS:** Windows, macOS, or Linux — use a terminal in **this directory** (`Assignment 2/`) as the working directory unless noted.

### Install dependencies

```bash
cd "Assignment 2"   # or: cd path/to/Assignment 2
python -m venv venv
```

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**

```bash
source venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` includes: `torch`, `gensim`, `matplotlib`, `nltk`, `wordcloud`, `requests`, `pdfplumber`, `beautifulsoup4`, `langdetect`, and (for optional name regeneration) you can add `openai` manually if you use `P25CS0002_prob2_task1.py`.

---

## Repository layout (this folder)

| Item | Role |
| --- | --- |
| [`P25CS0002_prob1_task1.py`](P25CS0002_prob1_task1.py) | **Problem 1 — Task 1 pipeline:** read raw `.txt` from `IITJ_corpus/`, clean & tokenise, write `PA1_Task1_output/` |
| [`P25CS0002_prob1.ipynb`](P25CS0002_prob1.ipynb) | **Problem 1 — main notebook:** Word2Vec (Gensim + PyTorch), grids, neighbours, analogies, PCA/t-SNE |
| [`P25CS0002_prob2.ipynb`](P25CS0002_prob2.ipynb) | **Problem 2:** three char-level models, training, novelty/diversity, plots |
| [`P25CS0002_prob2_task1.py`](P25CS0002_prob2_task1.py) | **Optional:** regenerate `TrainingNamesGPT.txt` via OpenAI API (needs `OPENAI_API_KEY`) |
| [`TrainingNamesGPT.txt`](TrainingNamesGPT.txt) | **Problem 2 data:** 1000 names (one per line) — already included |
| [`P25CS0002-A2/clean_corpus.txt`](P25CS0002-A2/clean_corpus.txt) | **Bundled clean corpus** — use if you skip preprocessing |
| [`overall_report.md`](overall_report.md) | Full assignment write-up template + deliverables checklist |
| [`requirements.txt`](requirements.txt) | Python dependencies |

**Name map (if you read `overall_report.md` from the course template):** the report may mention `Problem1_IITJ.ipynb` / `PA1_Task1.py` / `problem2.ipynb`. In **this** repo those correspond to `P25CS0002_prob1.ipynb`, `P25CS0002_prob1_task1.py`, and `P25CS0002_prob2.ipynb` (see the table at the top of `overall_report.md`).

---

## Problem 1 — Word2Vec (IIT Jodhpur corpus)

### Step A — Build `PA1_Task1_output/clean_corpus.txt`

The notebook **expects**:

- `PA1_Task1_output/clean_corpus.txt`
- (Optional) `PA1_Task1_output/corpus_statistics.json` — produced by the same script

You can do **either** of the following.

#### Option 1 — Run the preprocessing script (full pipeline)

1. Create a folder **`IITJ_corpus/`** next to `P25CS0002_prob1_task1.py`.
2. Put your **raw** IIT Jodhpur-related `.txt` files there (one or more documents).
3. Run:

   ```bash
   python P25CS0002_prob1_task1.py
   ```

4. Outputs appear under **`PA1_Task1_output/`**: `clean_corpus.txt`, `corpus_statistics.json`, `wordcloud.png`.

#### Option 2 — Use the bundled clean corpus (quick start)

If you do **not** have raw `IITJ_corpus/` sources in the repo, copy the bundled file into the path the notebook checks:

**PowerShell (from `Assignment 2/`):**

```powershell
New-Item -ItemType Directory -Force -Path PA1_Task1_output | Out-Null
Copy-Item P25CS0002-A2\clean_corpus.txt PA1_Task1_output\clean_corpus.txt
```

**bash:**

```bash
mkdir -p PA1_Task1_output
cp P25CS0002-A2/clean_corpus.txt PA1_Task1_output/clean_corpus.txt
```

Then open the notebook; the first corpus cells should find `clean_corpus.txt`.

### Step B — Run the Problem 1 notebook

1. Start Jupyter, VS Code, or Cursor with the venv activated.
2. Open **`P25CS0002_prob1.ipynb`**.
3. **Run all cells** (order matters: corpus load → stats / word cloud → Word2Vec grids → analysis → plots).

Figures are written to **`PA1_Task1_output/`** (loss grids, PyTorch loss curves, PCA/t-SNE exports — exact filenames appear in notebook printouts).

**Note:** First run may download NLTK data if a cell uses NLTK tokenisers; follow any on-screen prompt or install punkt/stopwords as needed.

---

## Problem 2 — Character-level name generation

### Data

Keep **`TrainingNamesGPT.txt`** in the **same folder** as **`P25CS0002_prob2.ipynb`** (this is already the case). The notebook can optionally copy it to `TrainingNames.txt` for rubrics that require that exact name.

### Run the notebook

1. With venv activated, open **`P25CS0002_prob2.ipynb`**.
2. Run cells from the top. The `%pip` cell installs/updates `torch`, `pandas`, `matplotlib` if needed (restart kernel if the installer says so).
3. **Training** takes noticeable time on **CPU** (three models × many epochs); GPU is used automatically if PyTorch sees CUDA.

### Outputs (next to the notebook)

After a full run you should see files such as:

- `problem2_loss_placeholder.png` — training loss comparison  
- `problem2_novelty_diversity_bars.png` — novelty vs diversity bar chart  

### Optional — regenerate names with an LLM

Only if you want a **new** name list:

```powershell
$env:OPENAI_API_KEY = "sk-..."
# optional: $env:OPENAI_MODEL = "gpt-4o-mini"
pip install openai
python P25CS0002_prob2_task1.py
```

The script writes **`TrainingNamesGPT.txt`** in the current working directory — run it from **`Assignment 2/`** so the notebook picks it up. The script must be edited to use `OPENAI_MODEL` consistently if you override the model (the template may hard-code a model id in the API call).

---

## Reports and GitHub

- **`overall_report.md`** — assignment-wide document: objectives, tables, figure placeholders, declaration. Fill placeholders and embed or link figures exported from the notebooks.
- Optional extended markdown reports (e.g. `Problem1_IITJ_Report.md`, `Problem2_Report.md`) may live at the parent project root; this folder’s **`overall_report.md`** is the single file you need for a **self-contained** GitHub repo.

### Suggested `.gitignore` (if you initialise git here)

```
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
*.pt
*.model
```

Track notebooks, scripts, `requirements.txt`, `TrainingNamesGPT.txt`, small text corpora, and committed figures if you want them visible on GitHub. Large binary models are often excluded.

---

## Troubleshooting

| Issue | What to try |
| --- | --- |
| `FileNotFoundError: ... clean_corpus.txt` | Create `PA1_Task1_output/` and add `clean_corpus.txt` (Option 1 or 2 above). |
| `Can't find folder: IITJ_corpus` | Create `IITJ_corpus` and add `.txt` files, or skip the script and use Option 2. |
| PyTorch / CUDA | CPU works; install the appropriate wheel from [pytorch.org](https://pytorch.org) if you need GPU. |
| Notebook kernel not using venv | In VS Code / Jupyter, select the interpreter from `./venv`. |

---

## Licence / academic use

Course assignment materials — keep your institution’s plagiarism and collaboration rules in mind. The declaration section in **`overall_report.md`** is for your submission.
