import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from Bio import SeqIO
import io
import base64
import pandas as pd
import json
from fpdf import FPDF
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)
server = app.server
app.title = "FermentoMap"

with open("fermentomap_proteins.json", "r") as f:
    fermento_db = json.load(f)

app.layout = html.Div([
    dcc.Store(id='gbk-raw'),
    dcc.Store(id='matched-genes'),
    dcc.Store(id='pdf-click-store', data=0),
    dcc.Tabs(id="tabs", value='analysis-tab', children=[
        dcc.Tab(label='🏠 Home', value='home-tab'),
        dcc.Tab(label='🧪 Analysis', value='analysis-tab'),
        dcc.Tab(label='📘 Documentation', value='documentation-tab')
    ]),
    html.Div(id='tab-content'),
    dcc.Download(id='download-pdf')
])

@app.callback(Output('tab-content', 'children'), Input('tabs', 'value'))
def render_tabs(tab):
    if tab == 'home-tab':
        return html.Div([
            html.Img(src='/assets/prof.png', style={'width': '150px', 'borderRadius': '50%'}),
            html.H2("LaPointes Research Group"),
html.P("Fermentation is a cornerstone of microbial metabolism, shaping ecosystems, industrial biotechnology, and food systems. Understanding the genomic basis of microbial fermentation is critical for predicting phenotypes, optimizing fermentation processes, and engineering strains with tailored metabolic outputs."),

html.P("FermentoMap was developed to address this gap. It is a Python-based, web-accessible application designed to extract, identify, and classify fermentation-related genes from annotated bacterial GenBank files. By integrating a curated database of fermentation-associated protein markers, FermentoMap performs rapid gene matching and categorizes genomes based on fermentation type (e.g., lactic acid, ethanol, acetate) and oxygen requirements (e.g., aerobic, anaerobic, facultative)."),

html.P("The significance of this tool lies in its versatility across research and industrial applications: In microbial ecology, it enables high-throughput screening of genomes for trait-based classification in environmental microbiomes. In food and dairy biotechnology, it supports selection of fermentative strains for probiotics, starter cultures, and functional foods. In synthetic biology, it aids in the rational design of microbial consortia with complementary fermentation pathways."),

html.P("Unlike existing genome browsers or annotation viewers, FermentoMap is tailored specifically to the metabolic domain of fermentation. It requires no installation or command-line usage, making it accessible to biologists and microbiologists with minimal computational experience. Its intuitive tab-based interface allows users to upload a .gbk file, run real-time classification, explore gene matches, and download structured PDF reports summarizing genomic potential."),

html.P("In summary, FermentoMap bridges the gap between genome annotation and phenotype prediction in the context of fermentation, offering a much-needed resource for comparative genomics, trait mining, and applied microbial research.")

        ])
    elif tab == 'analysis-tab':
        return html.Div([
            dcc.Upload(
                id='upload-gbk',
                children=html.Div(['📂 Drag and Drop or ', html.A('Select GenBank File (.gbk)')]),
                style={'width': '100%', 'height': '60px', 'lineHeight': '60px',
                       'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                       'textAlign': 'center', 'margin': '10px'}, multiple=False
            ),
            html.Div([
                html.A("📥 Download Example GenBank", href="/assets/example.gbk", download="example.gbk", style={"color": "lightblue"})
            ]),
            html.Div(id='uploaded-gbk-name', style={'color': 'lightgreen'}),
            html.Button("Run Gene Classification", id="run-btn", n_clicks=0),
            dcc.Loading(html.Div(id='analysis-output', style={'marginTop': '20px'})),
            html.Hr(),
            html.Button("📄 Download Results as PDF", id="btn-download-pdf")
        ])
    elif tab == 'documentation-tab':
        return html.Div([
            html.H4("📘 Usage Instructions"),
            html.P("1. Go to the 'Analysis' tab."),
            html.P("2. Upload a GenBank (.gbk) file containing annotated gene and product features."),
            html.P("3. Click 'Run Gene Classification' to match genes and generate a classification summary."),
            html.P("4. Use the button at the bottom to download results as PDF.")       
        ])

@app.callback(
    Output("uploaded-gbk-name", "children"),
    Output("gbk-raw", "data"),
    Input("upload-gbk", "contents"),
    State("upload-gbk", "filename")
)
def store_uploaded_gbk(contents, filename):
    if contents:
        return f"✅ Uploaded: {filename}", contents
    return "", None

@app.callback(
    Output("analysis-output", "children"),
    Output("matched-genes", "data"),
    Input("run-btn", "n_clicks"),
    State("gbk-raw", "data")
)
def analyze_gbk(n, content):
    if n == 0 or not content:
        raise PreventUpdate

    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    handle = io.StringIO(decoded.decode())

    matched = []
    fermentation_type_count = {}
    oxygen_type_count = {}

    for record in SeqIO.parse(handle, "genbank"):
        for feature in record.features:
            if feature.type == "CDS":
                gene = feature.qualifiers.get("gene", [""])[0].lower()
                product = feature.qualifiers.get("product", [""])[0].lower()
                for gene_id, ref in fermento_db.items():
                    ref_name = gene_id.lower()
                    if ref_name in gene or ref_name in product:
                        matched.append({
                            "Contig": record.name,
                            "Gene": gene_id,
                            "Start": int(feature.location.start),
                            "End": int(feature.location.end),
                            "Strand": "+" if feature.location.strand == 1 else "-",
                            "Product": product,
                            "Fermentation Type": ref["fermentation_type"],
                            "Oxygen Requirement": ref["oxygen_requirement"]
                        })
                        fermentation_type_count[ref["fermentation_type"]] = fermentation_type_count.get(ref["fermentation_type"], 0) + 1
                        oxygen_type_count[ref["oxygen_requirement"]] = oxygen_type_count.get(ref["oxygen_requirement"], 0) + 1
                        break

    df_matched = pd.DataFrame(matched)

    df_class = pd.DataFrame({
        "Fermentation Type": list(fermentation_type_count.keys()),
        "Detected Genes": list(fermentation_type_count.values())
    })

    df_oxy = pd.DataFrame({
        "Oxygen Class": list(oxygen_type_count.keys()),
        "Detected Genes": list(oxygen_type_count.values())
    })

    return html.Div([
        html.H5("✅ Gene Matching Complete - LaPointes Research Group"),
        html.P(f"Total Matches: {len(df_matched)}"),

        html.H6("Matched Genes (Top 20)"),
        dbc.Table.from_dataframe(df_matched.head(20), striped=True, bordered=True, hover=True, style={'color': 'white'}),

        html.H6("Detected Fermentation Types"),
        dbc.Table.from_dataframe(df_class, striped=True, bordered=True, hover=True, style={'color': 'lightblue'}),

        html.H6("Detected Oxygen Preferences"),
        dbc.Table.from_dataframe(df_oxy, striped=True, bordered=True, hover=True, style={'color': 'lightgreen'})
    ]), {
        "matched_genes": df_matched.to_dict(),
        "classification": {
            "fermentation": df_class.to_dict(),
            "oxygen": df_oxy.to_dict()
        }
    }

@app.callback(
    Output("download-pdf", "data"),
    Output("pdf-click-store", "data"),
    Input("btn-download-pdf", "n_clicks"),
    State("pdf-click-store", "data"),
    State("matched-genes", "data"),
    prevent_initial_call=True
)
def generate_pdf(n_clicks, prev_clicks, data):
    if not data or n_clicks is None or n_clicks == prev_clicks:
        raise PreventUpdate

    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(20, 20, 180)
    pdf.cell(200, 10, "FermentoMap Report", ln=True, align="C")
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 10, "LaPointes Research Group", ln=True, align="C")
    pdf.ln(10)

    # Matched Genes
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Top Detected Genes:", ln=True)
    pdf.set_font("Arial", "", 10)
    for gene in pd.DataFrame(data["matched_genes"]).to_dict(orient="records")[:15]:
        pdf.multi_cell(0, 8, f"{gene['Gene']} | {gene['Product']} | {gene['Fermentation Type']} | {gene['Oxygen Requirement']}")

    # Classification Summary Tables
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 10, "Fermentation Types (with Detected Genes):", ln=True)
    df_fer = pd.DataFrame(data["classification"]["fermentation"])
    pdf.set_font("Arial", "", 10)
    for idx, row in df_fer.iterrows():
        pdf.cell(0, 8, f"{row['Fermentation Type']} ({row['Detected Genes']})", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(100, 0, 0)
    pdf.cell(0, 10, "Oxygen Classes (with Detected Genes):", ln=True)
    df_oxy = pd.DataFrame(data["classification"]["oxygen"])
    pdf.set_font("Arial", "", 10)
    for idx, row in df_oxy.iterrows():
        pdf.cell(0, 8, f"{row['Oxygen Class']} ({row['Detected Genes']})", ln=True)

    output_path = "fermentomap_structured_report.pdf"
    pdf.output(output_path)
    return dcc.send_file(output_path), n_clicks

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
