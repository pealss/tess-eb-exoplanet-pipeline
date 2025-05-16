# Properly aligned code
import lightkurve as lk
import matplotlib.pyplot as plt

# Search for data
search = lk.search_lightcurve("TIC 231005575", sector=18)
print(f"Found {len(search)} observations")

# Download and plot
lc = search.download().normalize()
lc.plot()
plt.show()
