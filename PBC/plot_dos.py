# Source: https://pranabdas.github.io/espresso/hands-on/dos/
import matplotlib.pyplot as plt
import numpy as np


def plot_dos(fname):
    '''
    Loads DOS data from the output of dos.x and plots it using pyplot
    '''
    # load data
    energy, dos, idos = np.loadtxt(fname, unpack=True)
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
        f_e = float(lines[0].split()[-2])
        print(f_e)

    # make plot
    plt.figure(figsize=(12, 6))
    plt.plot(energy, dos, linewidth=0.75, color='red')
    plt.yticks([])
    plt.xlabel('Energy (eV)')
    plt.ylabel('DOS')
    plt.axvline(x=f_e, linewidth=0.5, color='k', linestyle=(0, (8, 10)))
    plt.xlim(4, 10)
    plt.ylim(0, )
    plt.fill_between(energy, 0, dos, where=(energy < f_e), facecolor='red', alpha=0.25)
    plt.text(f_e-0.1, 10, 'Fermi energy', rotation=90)
    # plt.text(6, 1.7, 'Fermi energy', fontsize= med, rotation=90)
    plt.show()

if __name__ == "__main__":
    # parameters/files
    fname = '3D_dimer.dos.dat'

    plot_dos(fname)
