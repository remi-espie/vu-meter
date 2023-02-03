import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from matplotlib import animation
from scipy.signal import butter, lfilter

RATE = 44100
# Initialize PyAudio
p = pyaudio.PyAudio()

# Open input stream
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, input=True, input_device_index=13)

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 2048)
ax.set_ylim(-32768, 32767)
line, = ax.plot([], [])



def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (0.5 * fs), btype='low')
    y = lfilter(b, a, data)
    return y

# Start the stream
# Plot the data
def animate(i):
    data = stream.read(1024)
    data = np.frombuffer(data, dtype=np.int16)
    filtered_data = lowpass_filter(data, cutoff=300, fs=RATE)

    line.set_data(np.arange(len(filtered_data)), filtered_data)
    return line,


ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 44100, 1024), interval=5, blit=True)
plt.show()

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()
