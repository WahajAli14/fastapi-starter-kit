import os

from fpdf import FPDF


def generate_pdf_file(payload):
    title = payload.get("title", "Untitled")
    content = payload.get("content", "")

    os.makedirs("generated_pdfs", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, title, ln=True, align="C")
    pdf.multi_cell(0, 10, content)

    file_name = f"{title.replace(' ', '_')}.pdf"
    output_path = os.path.join("generated_pdfs", file_name)
    pdf.output(output_path)

    print(f"✅ PDF generated at {output_path}")
