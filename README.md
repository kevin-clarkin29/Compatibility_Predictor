# Compatibility Predictor – Datahouse Take‑Home

Tiny Python 3 script that reads team / applicant data (JSON), scores each applicant on a **0 – 1** scale, and writes a new JSON file with **one‑decimal** scores (matching the sample in the PDF).

---

## 📂 Project layout

```text
.
├── compatibility.py       # < 70 LOC, no external deps
├── sample_input.json      # given data
├── output.json            # produced by the script
├── .gitignore             # excludes venv/, __pycache__, etc.
└── README.md              # you are here
```

---

## Quick start
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
python compatibility.py sample_input.json > output.json
```

Example result:

```json
{
  "scoredApplicants": [
    { "name": "John", "score": 0.8 },
    { "name": "Jane", "score": 0.8 },
    { "name": "Joe",  "score": 0.6 }
  ]
}
```

*(Values may vary slightly if you tweak parameters; see below.)*

---

## 🧮 How scoring works

1. **Team mean** – compute the average attribute vector  
   $
    \overline{v} \;=\; \frac{1}{|T|}\sum_{t \in T} t_{\text{attributes}}
   $

2. **Similarity** – calculate **Euclidean distance** $d$ between an applicant vector $a$ and $\overline{v}$.

3. **Normalise & invert**

   $
   \text{score} = 1 - \frac{d}{d_{\text{max}}}
   $  
   where $d_{\text{max}}$ is the worst-case distance (all 0 vs all 10).
 
   Result is rounded to **one decimal place**.

---

