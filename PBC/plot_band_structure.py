# Adapted from source: http://levilentz.com/Codes/Bands.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline


def Symmetries(lines):
    '''
    This function extracts the high symmetry points from the output of bandx.out
    '''
    symlines = [line for line in lines if 'high-symmetry' in line]
    symlines = [line.replace("-", " -").split() for line in symlines]
    print(symlines)
    x = np.asarray([line[-1] for line in symlines], dtype=np.float64)
    r = np.asarray([line[3:6] for line in symlines], dtype=np.float64)
    return r, x


def read_datafile(fname):
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    splitlines = [idx for idx, line in enumerate(lines) if line == '']
    lines = [line.split() for line in lines]

    bands = []
    for start, end in zip([-1] + splitlines[:-1], splitlines + [len(lines)]):
        bands.append(lines[start+1:end])
    print([len(band) for band in bands])
    bands = np.asarray(bands, dtype=np.float64)
    return bands


def plotband(band, symm_x, ax):
    symm_x = np.unique(symm_x)
    for segment in zip(symm_x[: -1], symm_x[1:]):
        start = np.where(band[:, 0] == segment[0])[0][-1]
        end = np.where(band[:, 0] == segment[1])[0][0]
        line = band[start:end+1]
        xs = np.linspace(line[0,0], line[-1,0], 100)
        spl = make_interp_spline(line[:, 0], line[:, 1], k=3)
        power_smooth = spl(xs)
        ax.plot(xs, power_smooth, color="black")


def bndplot(datafile, fermi, symmetryfile, subplot, label):
    '''
    Creates the band structure plot from the following arguments:

    datafile: file containing plottable band data. Looks like "XXX.bands.dat"
    fermi: Fermi energy. Can be found in the first line of the "XXX.dos.dat" file, or toward the end of the "XXX.scf.out" file.
    symmetryfile: file containing high-symmetry points. Looks like "XXX.bandsx.out"
    subplot: pyplot Axes object to add the plot to.
    label: Label to be put at the top of the figure.
    '''
    bands = read_datafile(datafile)
    xcoords = np.unique(bands[:, :, 0])  # This is all the unique x-points
    print(xcoords)
    Fermi = float(fermi)
    bounds = [min(xcoords), max(xcoords), Fermi - 2, Fermi + 2]
    with open(symmetryfile, 'r') as f:
        symmlines = f.read().splitlines()
    _, symm_x = Symmetries(symmlines)
    for band in bands:  # Here we plots the bands
        plotband(band, symm_x, subplot)
    for x in symm_x:  # This is the high symmetry lines
        print(x)
        x1 = [x, x]
        x2 = [bounds[2], bounds[3]]
        subplot.plot(x1, x2, '--', lw=0.55, color='black', alpha=0.75)
    subplot.plot([min(xcoords), max(xcoords)], [Fermi, Fermi], color='red')
    subplot.set_xticklabels([])
    subplot.set_ylim([bounds[2],bounds[3]])
    subplot.set_xlim([bounds[0],bounds[1]])
    subplot.text((bounds[1]-bounds[0])/2.0, bounds[3]+0.2, label, va='center', ha='center', fontsize=20)


def main(datFile, fermi_energy, bandFile, label):
    fig, ax = plt.subplots()
    bndplot(datFile, fermi_energy, bandFile, ax, label)
    plt.show()


if __name__ == "__main__":

    # Parameters/files
    datFile = '3D_dimer.bands.dat'
    fermi_energy = 6.9723
    bandFile = '3D_dimer.bandsx.out'
    label = "3D dimer"

    main(datFile, fermi_energy, bandFile, label)  # Remove global variable risks
