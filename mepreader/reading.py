import numpy as np
import neo as neo
import os

HAS_MPL = True
try:
    import matplotlib
    from matplotlib import pyplot as plt
except ImportError:
    HAS_MPL = False

from . import __version__, __version_info__

#---------------------------------------------------------------------------
NO_VERBOSE = 0
VERBOSE = 1
EXTRA_VERBOSE = 2
INSANE_VERBOSE = 3

#---------------------------------------------------------------------------
def plotSignals(emg_signal=None, derivative=None, timesteps=None,
                    trigger_indices=None,trigger_index_minmax_dict=None,
                    markWindow=False, windows=None,
                    plotDerivative=False):
    num_plots = 1
    if plotDerivative:
        num_plots +=1

    fig = plt.figure()
    ax = fig.add_subplot(num_plots,1,1)
    ax.set_title("Channel Data")
    ax.plot(timesteps, emg_signal)
    plt.xlabel('time')
    plt.ylabel('voltage')
    for index in trigger_indices:
        # Annotate trigger points
        ax.annotate('trigger', xy=(timesteps[index], emg_signal[index]),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )
        # Annotate min
        min_after_trigger_index = trigger_index_minmax_dict[index][0]
        ax.annotate('min', xy=(timesteps[min_after_trigger_index], emg_signal[min_after_trigger_index]),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )
        # Annotate max
        max_after_trigger_index = trigger_index_minmax_dict[index][1]
        ax.annotate('max', xy=(timesteps[max_after_trigger_index], emg_signal[max_after_trigger_index]),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )

    if markWindow:
        for window in windows:
            ax.axvspan(timesteps[window[0]], timesteps[window[1]], facecolor='g', alpha=0.5)

    if plotDerivative:
        bx = fig.add_subplot(num_plots,1,2)
        bx.set_title("Channel Derivative")
        bx.plot(timesteps, derivative)

    plt.tight_layout()
    fig.canvas.draw()
    plt.show()

#---------------------------------------------------------------------------
def ReadAnalogData(inputFile=None,verbose=VERBOSE, plotSignal=False,
    outputPath=None,
    plotDerivative=False,
    pairedPulse=False):
    reader = neo.io.Spike2IO(filename=inputFile.name)
    seg = reader.read_segment(lazy=False, cascade=True)
    if verbose >= VERBOSE:
        print("Segment 0: {}\nSize 0: {}".format(seg.analogsignals[0],seg.analogsignals[0].size))

    acquisition_time = seg.analogsignals[0].size / seg.analogsignals[0].sampling_rate
    if verbose >= VERBOSE:
        print("acquisition_time: {}".format(acquisition_time))

    timesteps = np.zeros((seg.analogsignals[0].size))
    dt = float(seg.analogsignals[0].sampling_period)
    for i in range(0,len(timesteps)):
        timesteps[i] = float(dt*i)

    analog_deriv = np.diff(seg.analogsignals[0])
    # Just append zero until the derivative array's size matches
    # the timesteps size
    while analog_deriv.size < timesteps.size:
        analog_deriv = np.append(analog_deriv, [[0]])

    # For now just look for where the derivative is > 1.0.  
    # In the future this might be interactive, or make this
    # value configurable.
    trigger_indices = []
    # Trigger waiting period: for paired pulse data there are two triggers within 30ms of eachother.
    # Skip ahead the corresponding number of samples to avoid tagging both triggers. Non-pp data
    # doesn't have close-together triggers so we can do this safely for both.
    trigger_waiting_period = int(0.030*seg.analogsignals[0].sampling_rate)
    #for i in range(0, len(analog_deriv)):
    i=0
    while i < len(analog_deriv):
        if analog_deriv[i] > 1.0:
            trigger_indices.append(i)
            i += trigger_waiting_period
        else:
            i += 1

    # Gather post-trigger windows, print peak-to-peak, mean
    trigger_window_timepoints = np.array([0.02, 0.10]) # seconds
    if pairedPulse:
        trigger_window_timepoints[1] = 0.065
    #index offset from trigger
    trigger_window_indices = trigger_window_timepoints*seg.analogsignals[0].sampling_rate 
    trigger_index_minmax_dict = dict()
    window_indices = []
    for trigger_index in trigger_indices:
        window = seg.analogsignals[0][trigger_index+int(trigger_window_indices[0]):trigger_index+int(trigger_window_indices[1])]
        window_start_index = trigger_index + int(trigger_window_indices[0])
        window_stop_index = trigger_index + int(trigger_window_indices[1])
        max_index = np.argmax(window)
        min_index = np.argmin(window)
        window_indices.append([window_start_index,window_stop_index])
        window_max = window[max_index]
        window_min = window[min_index]
        trigger_index_minmax_dict[trigger_index] = [window_start_index+min_index,window_start_index+max_index]
        print("Trigger at {}s min/max/mean/peak-to-peak: {}, {}, {}, {}".format(timesteps[trigger_index],window_max, window_min, np.mean(np.array([window_min, window_max])), abs(window_max)+abs(window_min)))

    if plotSignal and HAS_MPL:
        plotSignals(emg_signal=seg.analogsignals[0], derivative=analog_deriv, timesteps=timesteps,
                    trigger_indices=trigger_indices,trigger_index_minmax_dict=trigger_index_minmax_dict,
                    markWindow=True, windows=window_indices, plotDerivative=plotDerivative)

    ecg_signal = seg.analogsignals[0]
    trigger_timepoints = np.array([timesteps[trigger] for trigger in trigger_indices])
    trigger_mins = np.array([ecg_signal[trigger_index_minmax_dict[trigger][0]] for trigger in trigger_indices])
    trigger_maxs = np.array([ecg_signal[trigger_index_minmax_dict[trigger][1]] for trigger in trigger_indices])
    trigger_means = (trigger_mins + trigger_maxs) / 2
    trigger_p2p = abs(trigger_mins) + abs(trigger_maxs)
    print("Final Peak-To-Peak Average: {}".format(np.mean(trigger_p2p)))
    if outputPath:
        np.savetxt(outputPath, \
            np.hstack(arr.reshape(-1,1) for arr in \
                [trigger_timepoints,trigger_mins,trigger_maxs,trigger_means, trigger_p2p]), \
            header="trigger,min,max,mean,peak2peak", delimiter=",", fmt="%.5e")
