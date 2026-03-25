# Assignment 2 — NLU (Problem 1 & Problem 2)

**Written report:** [`P25CS0002-A2/report.pdf`](P25CS0002-A2/report.pdf) — full write-up, results, and figures for both problems.

This README only explains **how to set up the environment and run the code** (notebooks and scripts).

---

## Requirements

- **Python:** 3.10+ recommended.
- **Working directory:** open a terminal in **`Assignment 2/`** (the folder that contains this file).

### Install dependencies

```bash
cd "Assignment 2"
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

For optional name regeneration (`P25CS0002_prob2_task1.py`), also run: `pip install openai`.

---

## What’s in this folder

| File / folder | Purpose |
| --- | --- |
| `P25CS0002_prob1_task1.py` | Problem 1 — preprocess raw `.txt` from `IITJ_corpus/` → `PA1_Task1_output/` |
| `P25CS0002_prob1.ipynb` | Problem 1 — Word2Vec (Gensim + PyTorch), plots, analysis |
| `P25CS0002_prob2.ipynb` | Problem 2 — char-level RNN / BiLSTM / attention, training, metrics, figures |
| `P25CS0002_prob2_task1.py` | Optional — regenerate names via API (`OPENAI_API_KEY`) |
| `TrainingNamesGPT.txt` | Problem 2 — name list (one per line) |
| `P25CS0002-A2/clean_corpus.txt` | Bundled clean corpus if you skip preprocessing |
| `P25CS0002-A2/report.pdf` | **Submission report** |

**Report vs code names:** the PDF may refer to notebooks as `Problem1_IITJ.ipynb` / `problem2.ipynb`. In this repo they are **`P25CS0002_prob1.ipynb`** and **`P25CS0002_prob2.ipynb`**; preprocessing is **`P25CS0002_prob1_task1.py`** (not `PA1_Task1.py`).

---

## Problem 1 — run order

### 1) Get `PA1_Task1_output/clean_corpus.txt`

**Option A — Preprocess your own raw text**

1. Create **`IITJ_corpus/`** next to `P25CS0002_prob1_task1.py`.
2. Add IIT Jodhpur-related **`.txt`** files.
3. Run:

   ```bash
   python P25CS0002_prob1_task1.py
   ```

4. Check **`PA1_Task1_output/`** for `clean_corpus.txt`, `corpus_statistics.json`, `wordcloud.png`.

**Option B — Use the bundled corpus**

From **`Assignment 2/`**:

**PowerShell:**

```powershell
New-Item -ItemType Directory -Force -Path PA1_Task1_output | Out-Null
Copy-Item P25CS0002-A2\clean_corpus.txt PA1_Task1_output\clean_corpus.txt
```

**bash:**

```bash
mkdir -p PA1_Task1_output
cp P25CS0002-A2/clean_corpus.txt PA1_Task1_output/clean_corpus.txt
```

### 2) Run the notebook

1. Activate the venv; open **`P25CS0002_prob1.ipynb`** in Jupyter / VS Code / Cursor.
2. **Run all** cells in order.

Figures and exports go under **`PA1_Task1_output/`** (paths are printed in the notebook).

If a cell needs **NLTK** data, install what it asks for (e.g. punkt).

---

## Problem 2 — run order

1. Keep **`TrainingNamesGPT.txt`** in the **same folder** as **`P25CS0002_prob2.ipynb`**.
2. Activate the venv; open **`P25CS0002_prob2.ipynb`**.
3. Run from the top. Use **Restart kernel** if `%pip` tells you to after installing packages.
4. Training is slow on **CPU**; **GPU** is used if PyTorch detects CUDA.

**Outputs** (same folder as the notebook after a full run), e.g.:

- `problem2_loss_placeholder.png`
- `problem2_novelty_diversity_bars.png`

### Optional — new name list via API

```powershell
$env:OPENAI_API_KEY = "sk-..."
pip install openai
python P25CS0002_prob2_task1.py
```

Run that from **`Assignment 2/`** so it writes `TrainingNamesGPT.txt` next to the notebook.

---

## GitHub (optional)

**`.gitignore` ideas:** `venv/`, `__pycache__/`, `.ipynb_checkpoints/`, `*.pt`, large `.model` files.

Commit `report.pdf`, notebooks, scripts, `requirements.txt`, and small data files as needed.

---

## Troubleshooting

| Issue | Try |
| --- | --- |
| Missing `clean_corpus.txt` | Option A or B under Problem 1. |
| Missing `IITJ_corpus` | Create the folder and add `.txt` files, or use Option B. |
| Wrong Python / packages | Select the **`venv`** interpreter for the notebook kernel. |
| CUDA | Optional; CPU works. See [pytorch.org](https://pytorch.org) for GPU wheels. |
