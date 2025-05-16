from fpdf import FPDF
from datetime import datetime

class ReportGenerator(FPDF):
    def __init__(self, target_info):
        super().__init__()
        self.target_info = target_info
        self.add_page()
        
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'TESS EB Analysis Report - {datetime.today().strftime("%Y-%m-%d")}', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_section(self, title, content, image_path=None):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, content)
        if image_path:
            self.image(image_path, x=10, w=190)
            self.ln(5)

def generate_full_report(eb_params, candidates, output_path):
    pdf = ReportGenerator(eb_params)
    pdf.add_section("Target Information", 
                   f"TIC ID: {eb_params['tic_id']}\nPeriod: {eb_params['period']:.3f} days")
    pdf.add_section("Best-fit Parameters",
                   str(eb_params), 
                   image_path="model_fit.png")
    pdf.add_section("Planet Candidates",
                   "\n".join([f"Candidate {i}: Period {c['period']:.2f} days" 
                            for i, c in enumerate(candidates)]),
                   image_path="tls_periodogram.png")
    pdf.output(output_path)