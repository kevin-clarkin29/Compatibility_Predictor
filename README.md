# Compatibility Predictor – Datahouse Take‑Home

Python 3 script that reads team / applicant data from an input JSON, scores each applicant on a **0 – 1** scale, and writes a new JSON file with **one‑decimal** scores (matching the sample in the PDF). The score can become more precise by tweaking the score variable on line 95 from 1 to the desired decimal point.

---

## 📂 Project layout

```text
.
├── compatibility.py       
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
---

## 🧮 How scoring works

1. **Team mean** – average attribute vector  
   `v̄ = (1 / |T|) × Σ t∈T t_attributes`

2. **Similarity** – Euclidean distance `d` between an applicant vector `a` and `v̄`.

3. **Normalise & invert**  
   `score = 1 – (d / d_max)`  
   where `d_max` is the distance if every attribute differed by 10  
   (i.e. between `[0, 0, …]` and `[10, 10, …]`).  
   Result is rounded to **one decimal place**.

 
 ---

