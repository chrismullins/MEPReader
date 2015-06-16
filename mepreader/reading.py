
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

#---------------------------------------------------------------------------
def ReadAnalogData(inputFile=None,verbose=VERBOSE):
    #print "In the main function"
    reader = neo.io.Spike2IO(filename=inputFile.name)
    seg = reader.read_segment(lazy=False, cascade=True)
    print("Segment 0: {}\nSize 0: {}".format(seg.analogsignals[0],seg.analogsignals[0].size))

    acquisition_time = seg.analogsignals[0].size / seg.analogsignals[0].sampling_rate
    print("acquisition_time: {}".format(acquisition_time))

    timesteps = np.zeros((seg.analogsignals[0].size))
    dt = float(seg.analogsignals[0].sampling_period)
    for i in range(0,len(timesteps)):
        timesteps[i] = float(dt*i)

    analog_deriv = np.diff(seg.analogsignals[0])
    analog_deriv = np.append(analog_deriv, [[0]])

    trigger_indices = []
    for i in range(0, len(analog_deriv)):
        if analog_deriv[i] > 1.0:
            trigger_indices.append(i)




    fig = plt.figure()
    ax = fig.add_subplot(2,1,1)
    ax.set_title("Channel Data")
    ax.plot(timesteps, seg.analogsignals[0])
    plt.xlabel('time')
    plt.ylabel('voltage')
    for index in trigger_indices:
        ax.annotate('trigger', xy=(timesteps[index], seg.analogsignals[0][index]),  xycoords='data',
                xytext=(-50, 30), textcoords='offset points',
                bbox=dict(boxstyle="round", fc="0.8"),
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                )


    bx = fig.add_subplot(2,1,2)
    bx.set_title("Channel Derivative")
    bx.plot(timesteps, analog_deriv)

    plt.tight_layout()
    fig.canvas.draw()
    plt.show()

