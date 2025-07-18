from fpdf import FPDF
import tempfile

class RetentionPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "GC IntelliLab: Retention Time Report", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def retention_table(self, data):
        self.set_font("Arial", "B", 10)
        self.cell(50, 10, "Compound", 1)
        self.cell(30, 10, "RT (min)", 1)
        self.cell(40, 10, "Class", 1)
        self.cell(40, 10, "Formula", 1)
        self.ln()
        self.set_font("Arial", "", 10)
        for row in data:
            self.cell(50, 10, row["Compound"][:25], 1)
            self.cell(30, 10, str(row["RT"]), 1)
            self.cell(40, 10, row["Class"][:18], 1)
            self.cell(40, 10, row["Formula"], 1)
            self.ln()

def generate_retention_pdf(rt_df):
    pdf = RetentionPDF()
    pdf.add_page()
    data = rt_df.to_dict("records")
    pdf.retention_table(data)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name
