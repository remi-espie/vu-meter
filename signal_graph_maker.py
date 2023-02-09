import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from matplotlib import animation
import sounddevice

RATE = 44100
# Initialize PyAudio
p = pyaudio.PyAudio()

# get default input device
default_input = sounddevice.default.device[0]

# Open input stream
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, input=True, input_device_index=default_input)

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 2048)
ax.set_ylim(-32768, 32767)
line, = ax.plot([], [])

# Start the stream
# Plot the data
def animate(i):
    data = stream.read(1024)
    data = np.frombuffer(data, dtype=np.int16)

    line.set_data(np.arange(len(data)), data)
    return line,


ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 44100, 1024), interval=5, blit=True)
plt.show()

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()
