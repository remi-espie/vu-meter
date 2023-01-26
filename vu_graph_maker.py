import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open input stream
stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 5)
line, = ax.plot([], [])

# Start the stream
stream.start_stream()


# Plot tge data as VU
def animate():
    # Read data from the input stream
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    # Calculate the volume level
    volume_norm = np.linalg.norm(data) / (2 ** 15)
    # Update the VU meter
    line.set_data(np.arange(len(data)), volume_norm)
    return line,


# Create an animation that updates the VU meter at a specified interval
ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 2 * np.pi, 128), interval=10)

plt.show()
# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.terminate()
