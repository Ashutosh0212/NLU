# Assignment-2 — Natural Language Understanding

**Student:** Anand Mishra  
**Date:** February 25, 2026  

**This folder (`Assignment 2/`) — filename map for code and reports**

| Report / brief mentions | File in this repository |
| --- | --- |
| `Problem1_IITJ.ipynb` | `P25CS0002_prob1.ipynb` |
| `PA1_Task1.py` | `P25CS0002_prob1_task1.py` |
| `problem2.ipynb` | `P25CS0002_prob2.ipynb` |
| `PA1_Task1_output/clean_corpus.txt` | Produced by the Task-1 script (see **README.md**), or copy from `P25CS0002-A2/clean_corpus.txt` |
| `Problem1_IITJ_Report.md`, `Problem2_Report.md` | Optional extended reports at repo root; otherwise use the sections below |

---

## Important notes (from the assignment brief)


| Note          | Detail                                                                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Instructions  | Read the problem statements carefully. Failure to follow instructions may result in **zero marks**.                                                           |
| Plagiarism    | **Strictly prohibited.** Copying from LLMs or other students may result in **zero marks**. Submissions may be compared against LLM output and peer work.      |
| Code comments | Write **detailed, meaningful comments** to show understanding and originality. Submissions **without proper comments** may receive **only 50%** of the marks. |
| Submission    | Guidelines will be shared close to the deadline.                                                                                                              |
| **Deadline**  | **March 20, 2026** (firm — no extension)                                                                                                                      |


---

# Problem 1 — Learning word embeddings from IIT Jodhpur data

## Objective

Train **Word2Vec** models on text collected from **IIT Jodhpur** sources and analyse the **semantic structure** captured by the learned embeddings.

**Primary artefacts in this submission**


| Artefact                      | Location / role                           |
| ----------------------------- | ----------------------------------------- |
| Source notebook               | `Problem1_IITJ.ipynb`                     |
| Detailed technical write-up   | `Problem1_IITJ_Report.md`                 |
| Cleaned corpus                | `PA1_Task1_output/clean_corpus.txt`       |
| Corpus statistics (JSON)      | `PA1_Task1_output/corpus_statistics.json` |
| Preprocessing pipeline script | `PA1_Task1.py`                            |


---

## TASK-1: Dataset preparation

### Assignment requirements (summary)

- Collect English text from **at least three** suggested source types (e.g. official site, **academic regulations (required)**, newsletters, faculty, syllabus).
- **Remove non-English** text where it appears.
- **Preprocess:** (i) boilerplate / formatting noise, (ii) tokenisation, (iii) lowercasing, (iv) punctuation / non-text cleanup.
- **Report:** document count, token count, vocabulary size, and a **word cloud** of frequent words.

### Our pipeline (Step-1 … Step-5)


| Step       | What we did                                                                                                                                                                                                              |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Step-1** | Gathered IIT Jodhpur–related material (e.g. regulations, faculty-related text, news) into raw inputs.                                                                                                                    |
| **Step-2** | Extracted text **page-by-page** (e.g. from PDFs); used **ChatGPT** with prompts for **plain English**, **Word2Vec-friendly** lines.                                                                                      |
| **Step-3** | Saved merged extracts as `.txt` under `IITJ_corpus/`.                                                                                                                                                                    |
| **Step-4** | Ran `**PA1_Task1.py`**: boilerplate removal (URLs, cookies, etc.), lowercasing, punctuation normalisation, paragraph split, short-chunk filtering, tokenisation → `**clean_corpus.txt**` + `**corpus_statistics.json**`. |
| **Step-5** | `**Problem1_IITJ.ipynb`** loads the clean corpus for stats, word cloud (content words), and all Word2Vec experiments.                                                                                                    |


### Dataset statistics (fill from notebook / JSON or paste your latest numbers)


| Metric                                  | Value                                    |
| --------------------------------------- | ---------------------------------------- |
| Total documents (source files)          | *e.g. 3 — from `corpus_statistics.json`* |
| Total lines / chunks in clean corpus    | *e.g. 1 340*                             |
| Total tokens (whitespace split)         | *e.g. 27 299*                            |
| Vocabulary size (all tokens)            | *e.g. 3 778*                             |
| Content tokens (for word cloud filters) | *optional: from notebook*                |
| Content vocabulary                      | *optional*                               |


### Figure / chart placeholders — TASK-1

**Figure P1-1 — Word cloud (most frequent *content* words)**  

*Paste or embed your image below. Default path from this project:*

Word cloud — IIT Jodhpur clean corpus (content words)

---

## TASK-2: Model training

### Assignment requirements (summary)

- Train **CBOW** and **Skip-gram with negative sampling**.
- Vary formally: **embedding dimension**, **context window**, **number of negative samples**.
- Present results **formally** in the report (tables + discussion).

### Hyperparameter grid (Gensim) — summary table

*Copy your best/lowest-loss settings or full grid summary from the notebook.*


| Model     | Embedding dim           | Window         | Negative samples | Notes                   |
| --------- | ----------------------- | -------------- | ---------------- | ----------------------- |
| CBOW      | *e.g. 2, 100, 200, 300* | *e.g. 5, 7, 9* | *e.g. 5, 10, 15* | Grid search in notebook |
| Skip-gram | *same*                  | *same*         | *same*           | Grid search in notebook |


### Reference models (fixed hyperparameters for TASK-3/4)


| Model             | Embedding dim | Window   | Negative | Epochs           |
| ----------------- | ------------- | -------- | -------- | ---------------- |
| Gensim CBOW       | *e.g. 100*    | *e.g. 5* | *e.g. 5* | *as in notebook* |
| Gensim Skip-gram  | *e.g. 100*    | *e.g. 5* | *e.g. 5* | *as in notebook* |
| PyTorch Skip-gram | *e.g. 100*    | *e.g. 5* | *e.g. 5* | *as in notebook* |


### Figure / chart placeholders — TASK-2 (line charts)

**Figure P1-2 — Gensim CBOW: training loss vs embedding dimension (by window & negative samples)**  

CBOW loss grid

**Figure P1-3 — Gensim Skip-gram: training loss vs embedding dimension (by window & negative samples)**  

Skip-gram loss grid

**Figure P1-4 — PyTorch skip-gram: average training loss per epoch** *(optional but recommended)*  

PyTorch training loss curve

*Add a short paragraph under each figure interpreting trends (e.g. which hyperparameters lowered loss, caveats about Gensim’s loss scale).*

---

## TASK-3: Semantic analysis

### 1. Top-5 nearest neighbours (cosine similarity)

Words: **research**, **student**, **phd**, **exam** (listed once in the table).


| Target word | Model            | Neighbour 1 | Neighbour 2 | Neighbour 3 | Neighbour 4 | Neighbour 5 |
| ----------- | ---------------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| research    | Gensim CBOW      | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |
| research    | Gensim Skip-gram | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |
| student     | Gensim CBOW      | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |
| student     | Gensim Skip-gram | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |
| phd         | Gensim CBOW      | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |
| phd         | Gensim Skip-gram | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |
| exam        | Gensim CBOW      | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |
| exam        | Gensim Skip-gram | *fill*      | *fill*      | *fill*      | *fill*      | *fill*      |


*Source: outputs from `Problem1_IITJ.ipynb` (TASK-3 cells).*

### 2. Analogy experiments (at least three)


| #   | Pattern (example)    | Positive words             | Negative words       | Top predictions       | Meaningful? (Y / partial / N) |
| --- | -------------------- | -------------------------- | -------------------- | --------------------- | ----------------------------- |
| 1   | UG : BTech :: PG : ? | *e.g. btech, postgraduate* | *e.g. undergraduate* | *paste from notebook* | *your comment*                |
| 2   | *your design*        |                            |                      |                       |                               |
| 3   | *your design*        |                            |                      |                       |                               |


**Discussion space (3–6 sentences):**  
*Explain whether analogies align with human semantics on this small, domain-specific corpus; mention noise and OOV issues.*

---

## TASK-4: Visualisation (PCA or t-SNE)

### Figure placeholders — TASK-4

**Figure P1-5 — 2D projection (e.g. PCA): Gensim CBOW**  

*Export from notebook or paste screenshot here.*

PCA / t-SNE — CBOW

**Figure P1-6 — 2D projection (e.g. PCA): Gensim Skip-gram**  

*If your notebook saves under different names, update the path.*

PCA / t-SNE — Skip-gram

> **If the files above do not exist yet:** keep these blocks as placeholders, export plots from `Problem1_IITJ.ipynb`, save into `PA1_Task1_output/`, then refresh the paths.

**Interpretation (write here):**  

- *How do clusters differ between CBOW and Skip-gram?*  
- *Do related words (e.g. course, semester, exam) sit together?*

---

## Problem 1 — Deliverables checklist


| Deliverable              | Included? | Path / notes                                             |
| ------------------------ | --------- | -------------------------------------------------------- |
| Source code (documented) | ☐         | `Problem1_IITJ.ipynb`, `PA1_Task1.py`                    |
| Cleaned corpus           | ☐         | `PA1_Task1_output/clean_corpus.txt`                      |
| Visualisations           | ☐         | Word cloud, loss grids, PCA/t-SNE, optional PyTorch loss |
| Report                   | ☐         | This file + `Problem1_IITJ_Report.md`                    |


---

# Problem 2 — Character-level name generation using RNN variants

## Objective

Design and **compare** sequence models for **character-level** name generation using **recurrent** architectures.

**Primary artefacts**


| Artefact                       | Location                                                         |
| ------------------------------ | ---------------------------------------------------------------- |
| Source notebook                | `problem2.ipynb`                                                 |
| Extended write-up with numbers | `Problem2_Report.md`                                             |
| Name list (LLM-generated)      | `TrainingNamesGPT.txt` *(and/or `TrainingNames.txt` per rubric)* |


---

## TASK-0: Dataset

- Generate **1000 Indian names** (LLM); store as `**TrainingNames.txt*`* per brief.  
- *This project uses `**TrainingNamesGPT.txt*`* as the main file; copy/rename to `TrainingNames.txt` if required for submission.*


| Item                   | Value                                      |
| ---------------------- | ------------------------------------------ |
| Number of names loaded | *e.g. 1000*                                |
| File used              | *TrainingNamesGPT.txt / TrainingNames.txt* |


---

## TASK-1: Model implementation

### Architectures (brief)


| #   | Model               | Core idea                                                                  |
| --- | ------------------- | -------------------------------------------------------------------------- |
| 1   | **Vanilla RNN**     | Char embedding → `nn.RNN` → last hidden → logits for next character.       |
| 2   | **BiLSTM (BLSTM)**  | Char embedding → bidirectional `nn.LSTM` → concat directions → logits.     |
| 3   | **RNN + attention** | `nn.RNN` over prefix; attention over time steps (padding masked) → logits. |


### Hyperparameters (shared — fill from notebook)


| Setting       | Value   |
| ------------- | ------- |
| Embedding dim | *64*    |
| Hidden size   | *128*   |
| Layers        | *1*     |
| Optimiser     | *Adam*  |
| Learning rate | *0.001* |
| Batch size    | *64*    |
| Epochs        | *35*    |


### Trainable parameters & vanilla RNN size


| Model           | Trainable parameters | Approx. size (MB) |
| --------------- | -------------------- | ----------------- |
| Vanilla RNN     | *e.g. 30 429*        | *e.g. 0.116*      |
| BiLSTM          | *e.g. 207 965*       | *(optional)*      |
| RNN + Attention | *e.g. 50 525*        | *(optional)*      |


*Paste exact numbers from `problem2.ipynb` after “Run all”.*

---

## TASK-2: Quantitative evaluation


| Model           | Novelty rate | Diversity    |
| --------------- | ------------ | ------------ |
| Vanilla RNN     | *e.g. 0.998* | *e.g. 0.558* |
| BiLSTM          | *e.g. 1.000* | *e.g. 0.889* |
| RNN + Attention | *e.g. 0.990* | *e.g. 0.782* |


**Comparison (4–6 sentences — align with `problem2.ipynb` Discussion cell):**  
After training, **BiLSTM** usually has the **lowest loss**, **highest novelty**, and **highest diversity**; **RNN + Attention** is typically second; the **vanilla RNN** is smallest but often **underfits** (higher loss, more repeated samples). **BiLSTMs** use gating to carry information over the prefix better than a plain RNN, and the **backward** direction sees the whole prefix from the other side—helpful for short but structured strings like names.

### Figure — TASK-2 (training loss)

*`problem2.ipynb` saves this automatically after the training cell.*

![Problem 2 — training loss comparison](problem2_loss_placeholder.png)

---

## TASK-3: Qualitative analysis

### Realism and failure modes

*Write here: spacing, Indian name patterns, too-short outputs, gibberish, near-duplicates of training names.*

### Representative samples (paste from notebook)

**Vanilla RNN**  

```
(paste ~10–20 lines)
```

**BiLSTM**  

```
(paste ~10–20 lines)
```

**RNN + Attention**  

```
(paste ~10–20 lines)
```

---

## Problem 2 — Deliverables checklist


| Deliverable              | Included? | Path / notes                                                                   |
| ------------------------ | --------- | ------------------------------------------------------------------------------ |
| Source code (all models) | ☐         | `problem2.ipynb`                                                               |
| Generated name samples   | ☐         | Notebook output + optional `.txt` export                                       |
| Evaluation scripts       | ☐         | Metrics cells in notebook *(add `problem2_evaluate.py` if you split code out)* |
| Report                   | ☐         | `Problem2_Report.md` + this `overall_report.md`                                |


---

# Master deliverables — Assignment-2 (both problems)


| Category    | Items                                                                                |
| ----------- | ------------------------------------------------------------------------------------ |
| **Code**    | `Problem1_IITJ.ipynb`, `PA1_Task1.py`, `problem2.ipynb`                              |
| **Data**    | `PA1_Task1_output/clean_corpus.txt`, `TrainingNamesGPT.txt` / `TrainingNames.txt`    |
| **Figures** | Word cloud, Word2Vec loss grids, PCA/t-SNE, PyTorch loss (P1); optional P2 plots     |
| **Reports** | `overall_report.md` (this document), `Problem1_IITJ_Report.md`, `Problem2_Report.md` |


---

## Declaration

I confirm that I have read the plagiarism and commenting requirements. The implementation comments in the submitted notebooks and scripts reflect my own understanding.

**Signature / date:** _________________________  

---

*End of overall report template. Replace italic placeholders and check image paths before PDF export or submission.*