try:
    from triceratops.fpp import FPPCalculator
    TRICERATOPS_AVAILABLE = True
except ImportError:
    TRICERATOPS_AVAILABLE = False

class CandidateValidator:
    def __init__(self, tic_id, period, duration, depth, t0):
        self.tic_id = tic_id
        self.period = period
        self.duration = duration
        self.depth = depth
        self.t0 = t0
        
    def calculate_fpp(self):
        if not TRICERATOPS_AVAILABLE:
            raise ImportError("TRICERATOPS not installed")
            
        fpp = FPPCalculator(
            ID=self.tic_id,
            sectors=self.get_sectors(),
            period=self.period,
            duration=self.duration,
            depth=self.depth,
            t0=self.t0
        )
        return fpp.compute()
    
    def get_sectors(self):
        # Query MAST for sector information
        obs = Observations.query_criteria(target_name=f"TIC {self.tic_id}")
        return list(set(obs['sequence_number']))

    def is_planet_candidate(self, fpp_threshold=0.01):
        fpp, _ = self.calculate_fpp()
        return fpp < fpp_threshold