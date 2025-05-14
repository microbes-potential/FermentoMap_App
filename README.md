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

---

## 🌐 Running Locally

1. Clone this repository and navigate to the project folder.
2. Ensure you have `fermentomap_proteins.json` and `example.gbk` in the same directory.
3. Run the app:

```bash
python app_render_ready.py
```

4. Open your browser at [http://127.0.0.1:8050](http://127.0.0.1:8050) to use the app.

---

## ☁️ Deployment on Render

1. Push the following files to a GitHub repository:
   - `app_render_ready.py`
   - `requirements.txt`
   - `render.yaml`
   - `fermentomap_proteins.json`
   - `assets/example.gbk`
2. Go to [https://dashboard.render.com](https://dashboard.render.com)
3. Click **New Web Service** and connect your GitHub repo
4. Render will detect `render.yaml` and set up your app
5. After build, your app will be live on your Render subdomain

---

## 📄 File Structure

```
├── app_render_ready.py              # Main app file
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render deployment config
├── fermentomap_proteins.json       # Gene/protein reference database
├── assets/
│   └── example.gbk                 # Sample GenBank input file
```

---

## 📚 About

**FermentoMap** was developed by **LaPointes Research Group** to help researchers and microbiologists identify genomic traits linked to fermentation, especially in the context of microbial ecology, dairy applications, and synthetic biology.

---

## 🧪 Citation

If you use FermentoMap in your research, please cite:

> Farooq, A., & Rafique, A. (2025). *FermentoMap: A Web Tool for Classification of Fermentation-Related Genes from Bacterial Genomes*. LaPointes Research Group.

---

## 📬 Contact

For issues or contributions, please contact the authors or open an issue on GitHub.

