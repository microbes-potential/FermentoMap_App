# 🧬 FermentoMap: Genomic Fermentation Trait Classifier

FermentoMap is a web-based application built with Python and Dash that identifies and classifies fermentation-related genes from bacterial genome files in GenBank (.gbk) format. It provides a visual interface for uploading annotated genomes, detecting relevant genes, summarizing fermentation types and oxygen requirements, and exporting results as a structured PDF report.

---

## 🚀 Features

- Upload and parse annotated `.gbk` files
- Match genes to a curated database of fermentation-related proteins
- Classify detected genes by:
  - **Fermentation type** (e.g., lactic acid, ethanol, acetate)
  - **Oxygen requirement** (e.g., anaerobic, facultative, aerobic)
- View matched genes and summaries in interactive tables
- Export results as a branded PDF report
- Lightweight and deployable on Render or locally

---

## 📦 Requirements

- Python 3.7+
- Dash
- Dash Bootstrap Components
- Biopython
- Pandas
- FPDF

Install dependencies with:

```bash
pip install -r requirements.txt
```

## 🌐 Running Locally

1. Clone this repository and navigate to the project folder.
2. Ensure you have `fermentomap_proteins.json` and `example.gbk` in the same directory.
3. Run the app:

## 📄 File Structure

```
├── app.py              # Main app file
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment config
├── fermentomap_proteins.json       # Gene/protein reference database
├── assets/
│   └── example.gbk                 # Sample GenBank input file
```

