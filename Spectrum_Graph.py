import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal as ss
import pandas as pd
from scipy.signal import find_peaks

# get_data opens the spectrum xml file and returning X Y values
def get_data(file):
    tree = et.parse(file)
    root = tree.getroot()
    root = root[1][0][5][6]

    y = []
    for point in root.iter("DataPoint"):
        datapoint = int(point.text)
        y.append(datapoint)
    x = np.linspace(0, 2600, 1024)
    df = pd.DataFrame({'energy': x, 'counts': y})
    return df


Ba133 = get_data("Ba133.xml")
Co60 = get_data("Co60.xml")
Cs137 = get_data("Cs137.xml")
peaks, properties = find_peaks(Cs137['counts'], height=10, distance=100)
print(Cs137.iloc[peaks])

Na22 = get_data("Na22.xml")


fig, ax = plt.subplots(2, 2)

ax[0, 0].plot(Ba133['energy'], Ba133['counts'], label="Ba133")
ax[0, 0].set_title('Ba-133 Spectrum')
ax[0, 0].set_xlabel('Energy (keV)')
ax[0, 0].set_ylabel('Counts')
ax[0, 0].set_yscale('log')
ax[0, 0].legend()

ax[0, 1].plot(Co60['energy'], Co60['counts'], label="Co60")
ax[0, 1].set_title('Co-60 Spectrum')
ax[0, 1].set_xlabel('Energy (keV)')
ax[0, 1].set_ylabel('Counts')
ax[0, 1].set_yscale('log')
ax[0, 1].legend()

ax[1, 0].plot(Cs137['energy'], Cs137['counts'], label="Cs137")
ax[1, 0].set_title('Cs-137 Spectrum')
ax[1, 0].set_xlabel('Energy (keV)')
ax[1, 0].set_ylabel('Counts')
ax[1, 0].set_yscale('log')
ax[1, 0].legend()

ax[1, 1].plot(Na22['energy'], Na22['counts'], label="Na22")
ax[1, 1].set_title('Na-22 Spectrum')
ax[1, 1].set_xlabel('Energy (keV)')
ax[1, 1].set_ylabel('Counts')
ax[1, 1].set_yscale('log')
ax[1, 1].legend()


# Adding an overall title for the figure
plt.suptitle('Gamma Spectra of Different Isotopes')
plt.tight_layout()
# Display the plot
plt.savefig("sample_spectra.svg", format="svg")

plt.show()
