# AI Claim Denial Analyzer
# Live Demo

Streamlit Application:  
https://healthcare-rcm-dashboard.streamlit.app/


## Overview

AI Claim Denial Analyzer is an AI-powered healthcare revenue cycle management (RCM) system designed to automate insurance claim denial analysis using EDI 835 and EDI 837 healthcare claim data.

The system analyzes denied claims, identifies root causes, predicts recoverability, performs historical similarity matching, and groups claims into actionable denial clusters.

This project was developed as part of the Gabeo AI ML Engineer Take-Home Assignment.

---

# Problem Statement

Healthcare providers lose billions of dollars annually due to insurance claim denials. Billing teams manually review denials, identify the causes, compare historical claims, and decide whether a claim should be appealed.

This project automates that workflow using AI/ML techniques and rule-based healthcare claim reasoning.

The system processes:

- EDI 835 Remittance Advice data
- EDI 837 Claim Submission data
- CARC denial codes
- Historical claim patterns

and generates structured denial intelligence.

---

# Features

## 1. Claim Denial Root Cause Analysis

The system analyzes denied claims and determines:

- Root cause of denial
- CARC denial interpretation
- Recoverability prediction
- Confidence score
- Supporting evidence from claim data

Example denial categories:

- Timely Filing
- Missing Information
- Duplicate Claim
- Medical Necessity
- Missing Prior Authorization

---

## 2. Recoverability Prediction

Each claim is classified into:

- Recoverable
- Not Recoverable
- Needs Review
- Not Applicable

The prediction uses:

- filing deadlines
- authorization availability
- modifiers
- claim status
- denial reason patterns

---

## 3. Historical Similarity Matching

The system identifies historically similar claims using TF-IDF based similarity analysis.

Similarity features include:

- payer
- CPT/HCPCS procedure code
- diagnosis code
- provider patterns

This helps determine whether a denied claim has historically been recoverable.

---

## 4. Denial Clustering & Batch Intelligence

Denied claims are grouped into clusters using KMeans clustering.

This enables:

- grouping similar denial patterns
- identifying high-value denial groups
- batch-level denial intelligence
- operational prioritization

Cluster summaries include:

- total denied amount
- number of claims
- cluster grouping

---

# System Architecture

```text
EDI 835 Data + EDI 837 Data
                │
                ▼
        Data Loading Layer
                │
                ▼
          Claim Merge Engine
                │
                ▼
      Denial Analysis Engine
                │
                ├────────► Recoverability Prediction
                │
                ├────────► Historical Similarity Engine
                │
                └────────► Denial Clustering Engine
                                │
                                ▼
                    Streamlit Dashboard UI
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Dashboard | Streamlit |
| Data Processing | Pandas |
| Machine Learning | Scikit-learn |
| Similarity Search | TF-IDF + Cosine Similarity |
| Clustering | KMeans |
| Synthetic Data Generation | Faker |

---

# Project Structure

```text
gabeo-ai-assignment/
│
├── app.py
├── generate_synthetic.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── 835_claims.csv
│   ├── 837_claims.csv
│
├── prompts/
│   └── denial_analysis.txt
│
├── src/
│   ├── data_loader.py
│   ├── preprocess.py
│   ├── denial_engine.py
│   ├── similarity_engine.py
│   ├── clustering.py
│   └── utils.py
│
└── output/
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository_url>
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Generate Synthetic Dataset

```bash
python generate_synthetic.py
```

This creates:

- data/835_claims.csv
- data/837_claims.csv

with synthetic denied and paid claims.

---

## 4. Run Streamlit Application

```bash
streamlit run app.py
```

---

# Dashboard Features

The Streamlit dashboard includes:

- Merged claims data viewer
- Structured JSON outputs
- Denial analysis table
- Historical similarity matrix
- Claim clustering visualization
- Cluster summaries
- CSV export functionality
- KPI metrics dashboard

---

# Example JSON Output

```json
{
    "claim_id": "CLM-1000",
    "carc_reason": "Timely Filing",
    "root_cause": "Claim submitted after filing deadline",
    "recoverability": "Not Recoverable",
    "confidence": 0.95,
    "evidence": [
        "Service Date: 2025-06-15",
        "Received Date: 2026-03-20",
        "Days Difference: 278",
        "Insurance Type: Commercial"
    ]
}
```

---

# Design Decisions

## Rule-Based Denial Analysis

A rule-based engine was selected for denial analysis because:

- healthcare denials require explainability
- CARC code logic is deterministic
- billing teams need interpretable outputs
- confidence scoring becomes easier to justify

This approach improves transparency and reduces hallucination risk.

---

## TF-IDF Similarity Search

TF-IDF vectorization combined with cosine similarity was used because:

- claim attributes are sparse and high-dimensional
- lightweight implementation
- interpretable similarity scoring
- fast computation for historical matching

---

## KMeans Clustering

KMeans clustering was used to group denial patterns because:

- easy to implement and scale
- effective for claim amount grouping
- useful for operational prioritization
- lightweight for demo-scale systems

---

## Streamlit Dashboard

Streamlit was selected because:

- rapid prototyping
- easy deployment
- clean visualization support
- suitable for ML demos

---

# Evaluation Methodology

The system was evaluated using:

| Metric | Purpose |
|---|---|
| Root Cause Accuracy | Correct denial classification |
| Recoverability Logic | Appeal potential correctness |
| Similarity Confidence | Historical matching quality |
| Clustering Consistency | Grouping quality |
| End-to-End Pipeline Validation | Functional correctness |

---

# Synthetic Dataset

A synthetic dataset containing:

- paid claims
- denied claims
- multiple CARC codes
- multiple payers
- multiple diagnosis codes
- multiple procedure codes

was generated using Faker and Python.

This was necessary because no real patient healthcare data was provided.

---

# Known Limitations

## Current Limitations

- Uses synthetic data instead of real EDI transactions
- Limited CARC code coverage
- No real payer policy integration
- No production database
- Clustering based mainly on claim amount
- No deep learning models
- No real appeal outcome history

---

# Future Improvements

Potential future enhancements:

- LLM-powered denial reasoning
- Vector database integration
- Real payer policy engine
- Advanced recoverability prediction models
- Transformer-based claim embeddings
- Real-time API deployment
- Appeal recommendation generation
- Retrieval-Augmented Generation (RAG)
- Denial trend analytics

---

# Trade-Offs Considered

| Trade-Off | Decision |
|---|---|
| Explainability vs Complexity | Chose explainable rule-based logic |
| Speed vs Deep Modeling | Used lightweight ML models |
| Scalability vs Simplicity | Focused on modular architecture |
| Cost vs Accuracy | Avoided expensive LLM-heavy pipelines |

---

# Production Readiness Considerations

The current implementation is designed as a prototype/demo system.

For production deployment, the following would be added:

- database layer
- API services
- authentication
- payer rule management
- logging and monitoring
- claim audit trails
- scalable infrastructure

---

# Conclusion

This project demonstrates:

- healthcare denial reasoning
- explainable AI workflows
- machine learning integration
- modular software engineering
- practical healthcare analytics

The system successfully automates core denial analysis workflows while maintaining interpretability and operational usability.

---

# Author

Kunjbihari
M.Sc. Statistics  
Indian Institute of Technology Bombay
=======
# Healthcare-RCM-Denial-Intelligence-Dashboard
