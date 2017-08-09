import numpy as np
import os
import seaborn as sns
sns.set(style="white", font_scale=0.9)
import matplotlib as mpl
mpl.rcParams['axes.linewidth'] = 0.5

import matplotlib.pyplot as plt
from scipy import signal

# Load libraries
exec(open('C:/Users/Raphael/Desktop/These/GitHub/Example/elan2array.py').read(), globals())
exec(open('C:/Users/Raphael/Desktop/These/GitHub/visbrain/visbrain/utils/sleep/event.py').read(), globals())
exec(open('C:/Users/Raphael/Desktop/These/GitHub/visbrain/visbrain/utils/filtering.py').read(), globals())
exec(open('C:/Users/Raphael/Desktop/These/GitHub/visbrain/visbrain/utils/sigproc.py').read(), globals())

# DEFINE FUNCTIONS
def plot_stage(chan, epochs, data, time, amplitude, pal, outdir, savefig):

    fig, axs = plt.subplots(nrows=len(chan), ncols=len(epochs), figsize=(16, 7),
                            facecolor='w', edgecolor='k')
    fig.subplots_adjust(top=0.9, bottom=0.1, right=0.9, left=0.1, hspace=0, wspace=0.05)
    sns.despine(bottom=True, left=False, right=False)

    for j, ep in enumerate(epochs):

        r = range(epochs[ep] * sf, (epochs[ep] + time) * sf)
        axs[0, j].set_title(ep, y=1.06, fontweight='bold', fontsize=16,
           color=pal[ep])

        for i, key in enumerate(chan):

            # Filter signal
            if key != 'EMG':
                data_filt = filt(sf, np.array([0.1, 25]), data[i, r])
            else:
                data_filt = data[i, r]

            # axs[i, j].axhline(y=0, xmin=0,xmax=time*sf,c="lightgrey",lw=0.5, ls=':')
            axs[i, j].plot(r, data_filt, linewidth=0.7, color=pal[ep], label=key)

            axs[i, j].set_xlim([min(r), max(r)])
            axs[i, j].set_ylim([-amplitude, amplitude])
            axs[i, j].get_yaxis().set_ticks([])

            if j == 0:
                axs[i, j].set_ylabel(key, rotation=0, fontsize=13, labelpad=30, ha='center', va='center')

            if i < len(chan):
                axs[i, j].set_xlabel('')
                axs[i, j].get_xaxis().set_visible(False)

            if j == len(epochs) - 1 and i == len(chan) - 1 :
                axs[i, 0].spines['bottom'].set_visible(True)
                axs[i, 0].get_xaxis().set_visible(True)
                r_0 = range(epochs['Wake'] * sf, (epochs['Wake'] + time) * sf)
                axs[i, 0].set_xticks(np.arange(min(r_0), max(r_0)+sf, 2*sf))
                axs[i, 0].set_xticklabels(np.arange(0, time+1, 2))
                axs[i, 0].set_xlabel('Time [sec]')
                axs[i, 0].xaxis.set_tick_params(size=3, direction='in')

                axs[i, j].spines['right'].set_visible(True)
                axs[i, j].get_yaxis().set_visible(True)
                axs[i, j].yaxis.tick_right()
                axs[i, j].yaxis.set_ticks_position('right')
                axs[i, j].yaxis.set_label_position("right")
                axs[i, j].set_yticks([-amplitude, 0, amplitude])
                axs[i, j].set_yticklabels([-amplitude, 0, amplitude])
                axs[i, j].set_ylabel('Amplitude [µV]')
                axs[i, j].yaxis.set_tick_params(size=3, direction='in')

            if i == 0:
                axs[i, j].spines['top'].set_visible(True)
            if i == len(chan) - 1:
                axs[i, j].spines['bottom'].set_visible(True)

    if savefig:
        plt.savefig(os.path.join(outdir, 'stage_mt.png'), bbox_inches='tight', format='png', dpi=1000)

def plot_psd(chan, epochs, data, time, outdir, savefig):
    # Plot power spectral density
    fig, axs = plt.subplots(ncols=len(epochs), figsize=(16, 3.7),
                            facecolor='w', edgecolor='k')
    fig.subplots_adjust(top=0.9, bottom=0.4, right=0.9, left=0.1, hspace=0, wspace=0.1)
    sns.despine(bottom=True, left=True)

    for j, ep in enumerate(epochs):

        r = range(epochs[ep] * sf, (epochs[ep] + time) * sf)

        f, t, Sxx = signal.spectrogram(data[elec[chan['Cz']], r], sf, nperseg=1000, noverlap=990)
        mesh = axs[j].pcolormesh(t, f, Sxx, cmap='viridis', vmin=0, vmax=100)

        # axs[j].set_title(ep, y=1.06, fontweight='bold', fontsize=14, color=pal[ep])

        axs[j].set_ylim(0, 20)

        axs[j].set_xticks(np.arange(0.5, time+1, 1.8))
        axs[j].set_xticklabels(np.arange(0, time+1, 2))

#        if j == 4:
#            cbar = fig.colorbar(mesh)
#            cbar.ax.set_ylabel('Power spectral density [V² / Hz]', rotation=270, labelpad=15)

        if j == 0:
            axs[j].set_ylabel('Frequency [Hz]')
            axs[j].set_xlabel('Time [sec]')
        else:
            axs[j].get_yaxis().set_ticks([])
            axs[j].get_xaxis().set_ticks([])

    # plt.tight_layout()
    if savefig:
        plt.savefig(os.path.join(outdir, 'psd.png'), format='png', dpi=1000)

# DEFINE PARAMETERS AND INPUT

# Load data with no downsampling
path = 'C:/Users/Raphael/Desktop/These/GitHub/Example/Elan/s112_sleep.eeg'
sfori, sf, data, chan, _, _  = elan2array(path, 200)

# chan = { 'Fz': 1, 'Cz': 0, 'EOG1':21, 'EOG2':22, 'EMG':23 }
chan = { 'Fz': 1, 'Cz': 0, 'EOG1':21, 'EMG':23 }
elec = np.fromiter(iter(chan.values()), dtype=int)
data = data[elec, :]

# Plot parameters
# Epochs expressed in starting seconds
epochs = { 'Wake': 990, 'N1':180, 'N2': 567, 'N3': 6780, 'REM': 21335 } # S101
epochs = { 'Wake': 80, 'N1':10407, 'N2': 11059, 'N3': 18970, 'REM': 20940 } # S112

time = 10
amplitude = 200
# Color palette
pal = {'Wake': '#61bd7f', 'N1':"#4b7e93", 'N2':"#4b8093", 'N3':"#1e333a",
       'REM': "#ab4642"}
#sns.palplot(sns.color_palette(pal.values()))

outdir = 'C:/Users/Raphael/Desktop/These/Thesis/Fig/Intro_Sleep_Stages_PSD'

# Run plot
savefig = False
plot_stage(chan, epochs, data, time, amplitude, pal, outdir, savefig)
plot_psd(chan, epochs, data, time, outdir, savefig)
