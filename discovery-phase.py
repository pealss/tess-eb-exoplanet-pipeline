# Automated candidate reporting to astronomical databases  
from astroquery.vizier import Vizier  

def report_candidate(tic_id, params):  
    Vizier.ROW_LIMIT = -1  
    catalog_data = {  
        'TIC': tic_id,  
        'Period': params['period'],  
        'Depth': params['depth']  
    }  
    Vizier(publish=True).upload([catalog_data], 'TESS_EB_CANDIDATES')  