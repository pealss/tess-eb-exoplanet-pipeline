import os
import yaml
import lightkurve as lk
import matplotlib.pyplot as plt

# Configuration Loader ======================
def load_config():
    """Load settings from YAML file"""
    config_path = os.path.join("config", "settings.yaml")
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Config file {config_path} not found! Using defaults.")
        return {
            'data': {'download_dir': './data/raw', 'sectors': []},
            'processing': {'sigma_clip': 5.0},
            'output': {'plot_format': 'png'}
        }

# Main Analysis Function =====================
def analyze_tic(tic_id):
    config = load_config()  # ← Load configuration here
    
    try:
        print(f"Processing TIC {tic_id}...")

        # Use config for sector selection
        sectors = config['data']['sectors'] or None  # Auto-detect if empty
        
        search = lk.search_lightcurve(f"TIC {tic_id}", sector=sectors)
        
        if len(search) == 0:
            print("No data found!")
            return

        for result in search:
            sector = result.sector if hasattr(result, 'sector') else "unknown"
            print(f"Downloading Sector {sector}...")

            # Use config for download location
            lc = result.download(download_dir=config['data']['download_dir']).PDCSAP_FLUX
            
            # Use config for processing
            clean_lc = lc.remove_outliers(sigma=config['processing']['sigma_clip'])
            normalized_lc = clean_lc.normalize()

            period = normalized_lc.to_periodogram().period_at_max_power
            print(f"Period: {period.value:.3f} days")

            # Use config for output format
            plot_path = f"TIC{tic_id}_sector{sector}.{config['output']['plot_format']}"
            normalized_lc.fold(period).scatter()
            plt.savefig(plot_path)
            plt.close()

    except Exception as e:
        print(f"Error: {str(e)}")

# Run ========================================
if __name__ == "__main__":
    analyze_tic("38846515")  # Example TIC ID