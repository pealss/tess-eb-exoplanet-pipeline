from reportlab.lib.units import inch
from reportlab.platypus.flowables import Flowable

class InteractivePlotFlowable(Flowable):
    """Embed Vega-Lite interactive plots in PDF"""
    def __init__(self, spec, width=6*inch, height=4*inch):
        self.spec = spec
        self.width = width
        self.height = height
        
    def draw(self):
        from altair import Chart
        c = Chart.from_dict(self.spec)
        img = c.save_as(format='svg').render()
        self.canv.saveState()
        self.canv.translate(0, self.height)
        self.canv.scale(1, -1)
        self.canv.drawImage(img, 0, 0, self.width, self.height)
        self.canv.restoreState()

class ARXIVSubmitter:
    """Automated paper submission system"""
    def __init__(self, report):
        self.tex = self._generate_latex(report)
        
    def _generate_latex(self, report):
        template = r"""
        \documentclass{aastex63}
        \begin{document}
        \title{%s}
        %s
        \end{document}
        """ % (report.title, report.content)
        return template
        
    def submit(self, api_key):
        import arxiv
        return arxiv.Submit(
            pdf=self.render_pdf(),
            metadata={'categories': ['astro-ph.SR']}
        )