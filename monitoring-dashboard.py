from grafana_dashboard import Dashboard, Row, TimeSeries

class PipelineMonitor:
    def __init__(self):
        self.dashboard = Dashboard("EB Pipeline Metrics")
        
    def add_metric(self, name, query):
        row = Row(title=name)
        panel = TimeSeries(title=name)
        panel.add_target(query)
        row.add_panel(panel)
        self.dashboard.add_row(row)
        
    def deploy(self):
        self.dashboard.push_to_grafana()