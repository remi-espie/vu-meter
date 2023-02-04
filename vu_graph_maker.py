import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import RPi.GPIO as GPIO
from scipy.signal import butter, lfilter, filtfilt

# Initialize PyAudio
p = pyaudio.PyAudio()
RATE = 44100

# Open input stream
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, input=True, frames_per_buffer=1024,
                input_device_index=2)

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(0, 5)
ax.set_ylim(0, 10)
line1, = ax.plot([], [])
line2, = ax.plot([], [])
line3, = ax.plot([], [])

# Start the stream
stream.start_stream()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 1)


# p.start(0)


def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (fs / 2), btype='low')
    filtered_signal = lfilter(b, a, data)
    return filtered_signal


def highpass_filter(signal, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (fs/2), btype='high')
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal


# Plot the data as VU
def animate(i):
    # Read data from the input stream
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    # Calculate the volume level
    # Update the VU meter
    lowpass_filtered_data = lowpass_filter(data, cutoff=300, fs=RATE)
    volume_norm_low = np.linalg.norm(lowpass_filtered_data) / (2 ** 15)

    highpass_filtered_data = highpass_filter(data, 5000, fs=RATE)
    volume_norm_high = np.linalg.norm(highpass_filtered_data) / (2 ** 15)

    volume_norm = np.linalg.norm(data) / (2 ** 15)

    line1.set_data(np.arange(len(lowpass_filtered_data)), volume_norm_low)
    line2.set_data(np.arange(len(highpass_filtered_data)), volume_norm_high)
    line3.set_data(np.arange(len(data)), volume_norm)

    led_value = np.clip(volume_norm * 10, 0, 100)
    print(volume_norm_high)
    # p.ChangeDutyCycle(np.clip(led_value, 0, 100))
    return line1, line2, line3,


# # Create an animation that updates the VU meter at a specified interval
ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 2 * np.pi, 128), interval=10)
#
plt.show()
# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.stop()
