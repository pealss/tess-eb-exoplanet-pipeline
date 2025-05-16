from lightkurve import search_lightcurve
from lightkurve.correctors import PLDCorrector

class PlanetSearch:
    def __init__(self, tic_id):
        self.tic_id = tic_id
        self.lcs = search_lightcurve(f"TIC {tic_id}", author="SPOC").download_all()
        self.corrected_lc = self._pld_correct()
        
    def _pld_correct(self):
        return PLDCorrector(self.lcs).correct()
    
    def search_all(self):
        # Implement full pipeline chain
        pass