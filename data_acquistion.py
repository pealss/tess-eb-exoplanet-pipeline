import numpy as np
from astroquery.mast import Observations
from lightkurve import search_tesscut
import lightkurve as lk

class TessDataHandler:
    def __init__(self, tic_id=None, name=None):
        """Initialize with either TIC ID or target name"""
        self.tic_id = tic_id
        self.name = name
        self.observations = None
        
    def query_mast(self, radius=0.1):
        """Query MAST for TESS observations"""
        if self.tic_id:
            obs = Observations.query_criteria(target_name=f"TIC {self.tic_id}", 
                                            obs_collection="TESS",
                                            radius=radius)
        elif self.name:
            obs = Observations.query_criteria(objectname=self.name,
                                            obs_collection="TESS",
                                            radius=radius)
        self.observations = obs
        return obs
        
    def download_lcs(self, download_dir="data", sector=None):
        """Download light curves using lightkurve"""
        if self.tic_id:
            search_result = lk.search_lightcurve(f"TIC {self.tic_id}", sector=sector)
        elif self.name:
            search_result = lk.search_lightcurve(self.name, sector=sector)
            
        if len(search_result) == 0:
            raise ValueError("No light curves found")
            
        lcs = search_result.download_all(download_dir=download_dir)
        return lcs

    def get_tessebs_data(self):
        """Alternative method for TESS EBs catalog data (requires web scraping)"""
        # Implementation note: You'll need to handle authentication 
        # and parse HTML/API responses from tessebs.villanova.edu
        pass