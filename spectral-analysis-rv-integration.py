class SyntheticSpectraGenerator:
    """NLTE spectral synthesis with SME"""
    def __init__(self, Teff, logg, metallicity):
        self.sme = SME.SME_Structure()
        self.sme.teff = Teff
        # ... other parameters ...
        
    def generate_rv_curve(self, time, mass_ratio):
        """Precision RV simulator"""
        rv1 = (149.6 * (1/(1+mass_ratio)) * 
              np.sin(2*np.pi*time/period) + 
              np.random.normal(0, 0.1))  # Instrument noise
        return rv1

class DopplerImaging:
    """Surface feature reconstruction"""
    def __init__(self, spectra_sequence):
        self.spectra = spectra_sequence
        
    def solve_tikhonov(self, regularization=1e-3):
        """Inverse problem solution"""
        A = self._build_rotation_matrix()
        return np.linalg.solve(A.T @ A + regularization*np.eye(A.shape[1]), 
                             A.T @ self.spectra)