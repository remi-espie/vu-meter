import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import RPi.GPIO as GPIO
from scipy.signal import butter, lfilter

# Initialize PyAudio
p = pyaudio.PyAudio()
RATE = 44100

# Open input stream
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, input=True, frames_per_buffer=1024,
                input_device_index=12)

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 10)
line, = ax.plot([], [])

# Start the stream
stream.start_stream()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 1)
# p.start(0)


def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (0.5 * fs), btype='low')
    y = lfilter(b, a, data)
    return y


# Plot the data as VU
def animate(i):
    # Read data from the input stream
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    # Calculate the volume level
    # Update the VU meter
    filtered_data = lowpass_filter(data, cutoff=300, fs=RATE)
    volume_norm = np.linalg.norm(filtered_data) / (2 ** 15)

    line.set_data(np.arange(len(filtered_data)), volume_norm)
    led_value = np.clip(volume_norm * 10, 0, 100)
    print(led_value)
    # p.ChangeDutyCycle(np.clip(led_value, 0, 100))
    return line,


# # Create an animation that updates the VU meter at a specified interval
ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 2 * np.pi, 128), interval=10)
#
plt.show()
# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.stop()
