
import numpy as np
import neo as neo

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

def plotSignals(emg_signal=None, derivative=None, timesteps=None,
                    trigger_indices=None,trigger_index_minmax_dict=None,
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
    if plotDerivative:
        bx = fig.add_subplot(num_plots,1,2)
        bx.set_title("Channel Derivative")
        bx.plot(timesteps, derivative)

    plt.tight_layout()
    fig.canvas.draw()
    plt.show()

#---------------------------------------------------------------------------
def ReadAnalogData(inputFile=None,verbose=VERBOSE, plotSignal=False,
    plotDerivative=False):
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
    for i in range(0, len(analog_deriv)):
        if analog_deriv[i] > 1.0:
            trigger_indices.append(i)

    # Gather post-trigger windows, print peak-to-peak, mean
    trigger_window_timepoints = np.array([0.02, 0.05]) # seconds
    #index offset from trigger
    trigger_window_indices = trigger_window_timepoints*seg.analogsignals[0].sampling_rate 
    trigger_index_minmax_dict = dict()
    for trigger_index in trigger_indices:
        window = seg.analogsignals[0][trigger_index+int(trigger_window_indices[0]):trigger_index+int(trigger_window_indices[1])]
        window_start_index = trigger_index + int(trigger_window_indices[0])
        window_stop_index = trigger_index + int(trigger_window_indices[1])
        max_index = np.argmax(window)
        min_index = np.argmin(window)
        window_max = window[max_index]
        window_min = window[min_index]
        trigger_index_minmax_dict[trigger_index] = [window_start_index+min_index,window_start_index+max_index]
        print("Trigger at {}s min/max/mean: {}, {}, {}".format(timesteps[trigger_index],window_max, window_min, np.mean(np.array([window_min, window_max]))))

    if plotSignal and HAS_MPL:
        plotSignals(emg_signal=seg.analogsignals[0], derivative=analog_deriv, timesteps=timesteps,
                    trigger_indices=trigger_indices,trigger_index_minmax_dict=trigger_index_minmax_dict,
                    plotDerivative=plotDerivative)

    

    

