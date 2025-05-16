import lightkurve as lk
import matplotlib.pyplot as plt

def analyze_tic(tic_id):
    try:
        print(f"Processing TIC {tic_id}...")

        # Search across all available sectors
        search = lk.search_lightcurve(f"TIC {tic_id}")

        if len(search) == 0:
            print("No data found!")
            return

        # Get list of available sectors from search results
        sectors = search.table['sector'].data.data if 'sector' in search.table.colnames else []
        
        # Iterate through all available light curves
        for idx, result in enumerate(search):
            # Get sector number from the search result table
            if len(sectors) > idx:
                sector = int(sectors[idx])
            else:
                print("No sector information available")
                continue

            print(f"Downloading Sector {sector}...")

            # Download and process light curve
            lc = result.download().PDCSAP_FLUX
            clean_lc = lc.remove_nans().remove_outliers()
            normalized_lc = clean_lc.normalize()

            # Period analysis
            period = normalized_lc.to_periodogram().period_at_max_power
            print(f"Sector {sector} period: {period.value:.3f} days")

            # Save phase-folded plot
            normalized_lc.fold(period).scatter()
            plt.title(f"TIC {tic_id} - Sector {sector}")
            plt.savefig(f"TIC{tic_id}_sector{sector}_plot.png")
            plt.close()

    except Exception as e:
        print(f"Error: {str(e)}")

# Run the analysis
analyze_tic(tic_id="38846515")