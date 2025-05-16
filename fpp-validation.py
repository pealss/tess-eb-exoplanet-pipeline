validator = CandidateValidator(tic_id=123456, 
                             period=2.5, 
                             duration=0.1, 
                             depth=0.001, 
                             t0=2458325.6)
if validator.is_planet_candidate():
    print("Valid planet candidate!")