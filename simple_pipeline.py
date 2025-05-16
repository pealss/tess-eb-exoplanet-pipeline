import lightkurve as lk
import matplotlib.pyplot as plt

def analyze_tic(tic_id, sector):
    try:
        # Download data
        print(f"Processing TIC {tic_id} (Sector {sector})...")
        search = lk.search_lightcurve(f"TIC {tic_id}", sector=sector)
        
        if len(search) == 0:
            print("No data found!")
            return

        # Get light curve
        lc = search.download().PDCSAP_FLUX
        
        # Clean and normalize
        clean_lc = lc.remove_nans().remove_outliers()
        normalized_lc = clean_lc.normalize()
        
        # Find period
        period = normalized_lc.to_periodogram().period_at_max_power
        print(f"Detected period: {period.value:.3f} days")
        
        # Plot and save
        normalized_lc.fold(period).scatter()
        plt.title(f"TIC {tic_id}")
        plt.savefig(f"TIC{tic_id}_plot.png")
        plt.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")

# Run the analysis
analyze_tic(tic_id="38846515")  # Example EB system

