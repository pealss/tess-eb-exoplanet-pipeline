class ZooniverseInterface:
    """Automated candidate vetting with Zooniverse"""
    def __init__(self, project_id):
        self.client = zooniverse.ZooniverseClient()
        self.project = self.client.projects[project_id]
        
    def upload_candidate(self, lightcurve, metadata):
        subject = zooniverse.Subject(
            locations=[zooniverse.Location(lightcurve)],
            metadata=metadata
        )
        return self.project.subjects.add(subject)
    
    def get_votes(self, subject_id):
        classifications = self.project.subjects[subject_id].classifications
        return sum([c.annotations['planet'] for c in classifications])