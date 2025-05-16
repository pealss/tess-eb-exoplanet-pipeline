from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

class ScienceReport:
    def __init__(self, filename):
        self.doc = SimpleDocTemplate(filename, pagesize=A4)
        self.styles = getSampleStyleSheet()
        self.story = []
        
    def add_title(self, text):
        self.story.append(Paragraph(text, self.styles['Title']))
        
    def add_figure(self, path, caption):
        img = Image(path, width=500, height=300)
        self.story.append(img)
        self.story.append(Paragraph(caption, self.styles['Caption']))
        
    def add_parameters_table(self, params):
        """Create professional parameter table"""
        from reportlab.lib import colors
        from reportlab.platypus import Table
        
        data = [["Parameter", "Value", "Uncertainty"]]
        for key, val in params.items():
            data.append([key, f"{val[0]:.4f}", f"±{val[1]:.4f}"])
            
        table = Table(data)
        table.setStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER')
        ])
        self.story.append(table)
        
    def build(self):
        self.doc.build(self.story)