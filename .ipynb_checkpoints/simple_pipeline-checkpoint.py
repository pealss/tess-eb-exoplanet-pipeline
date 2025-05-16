{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "357d4dd3",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'lightkurve'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 1\u001b[0m\n\u001b[1;32m----> 1\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mlightkurve\u001b[39;00m \u001b[38;5;28;01mas\u001b[39;00m \u001b[38;5;21;01mlk\u001b[39;00m\n\u001b[0;32m      2\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mlightkurve\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m LightCurve\n\u001b[0;32m      3\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mmatplotlib\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mpyplot\u001b[39;00m \u001b[38;5;28;01mas\u001b[39;00m \u001b[38;5;21;01mplt\u001b[39;00m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'lightkurve'"
     ]
    }
   ],
   "source": [
    "import lightkurve as lk\n",
    "from lightkurve import LightCurve\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "def analyze_tic(tic_id, sector):\n",
    "    # 1. Download Data\n",
    "    search = lk.search_lightcurve(f\"TIC {tic_id}\", sector=sector)\n",
    "    if len(search) == 0:\n",
    "        print(f\"No data found for TIC {tic_id} in Sector {sector}\")\n",
    "        return\n",
    "    \n",
    "    # 2. Get Light Curve\n",
    "    lc = search.download().PDCSAP_FLUX\n",
    "    \n",
    "    # 3. Simple Processing\n",
    "    clean_lc = lc.remove_nans().remove_outliers()\n",
    "    normalized_lc = clean_lc.normalize()\n",
    "    \n",
    "    # 4. Find Period\n",
    "    period = normalized_lc.to_periodogram().period_at_max_power\n",
    "    \n",
    "    # 5. Plot Results\n",
    "    normalized_lc.fold(period).scatter()\n",
    "    plt.title(f\"TIC {tic_id} - Sector {sector}\")\n",
    "    plt.savefig(f\"TIC{tic_id}_Sector{sector}_folded.png\")\n",
    "    plt.close()\n",
    "    \n",
    "    print(f\"Analysis complete! Saved plot for TIC {tic_id}\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    analyze_tic(tic_id=\"231005575\", sector=18)  # Known EB system"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "5315c4b7",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
