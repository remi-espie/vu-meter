import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import sounddevice
from matplotlib import animation
import RPi.GPIO as GPIO
from scipy.signal import butter, lfilter, filtfilt

# Initialize PyAudio
p = pyaudio.PyAudio()
RATE = 44100
BUFFER = 882

# get default input device
default_input = sounddevice.default.device[0]

# Open input stream
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=BUFFER,
                input_device_index=default_input)

# Create plots
fig, ax = plt.subplots(2, 1)

# Set up VU Meter plot
ax[0].set_xlim(0, 5)
ax[0].set_ylim(0, 15)
ax[0].set_title("VU Meter")
line_lowpass, = ax[0].plot([], [])
line_highpass, = ax[0].plot([], [])
line_global, = ax[0].plot([], [])

# Set up Spectrometer plot
ax[1].set_xlim(0, RATE / 2 + 1)
ax[1].set_ylim(-60, 60)
ax[1].set_title("Spectrometer")
line_spectrometer, = ax[1].plot([], [])

r = range(0, int(RATE / 2 + 1), int(RATE / BUFFER))

# Start the stream
stream.start_stream()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 60)

p.start(0)

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (fs / 2), btype='low')
    filtered_signal = lfilter(b, a, data)
    return filtered_signal


def highpass_filter(signal, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (fs / 2), btype='high')
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal


# Plot the data as VU
def animate(i):
    # Read data from the input stream
    data = np.frombuffer(stream.read(BUFFER), dtype=np.int16)
    # Calculate the volume level
    # Update the VU meter
    lowpass_filtered_data = lowpass_filter(data, cutoff=300, fs=RATE)
    volume_norm_low = np.linalg.norm(lowpass_filtered_data) / (2 ** 15)

    highpass_filtered_data = highpass_filter(data, 5000, fs=RATE)
    volume_norm_high = np.linalg.norm(highpass_filtered_data) / (2 ** 15)

    volume_norm = np.linalg.norm(data) / (2 ** 15)

    line_lowpass.set_data([0, 2], volume_norm_low)
    line_highpass.set_data([3, 5], volume_norm_high)
    line_global.set_data([2, 3], volume_norm)

    # Update the spectrometer
    fft = np.fft.rfft(data)
    fft = np.log10(np.sqrt(np.real(fft) ** 2 + np.imag(fft) ** 2) / BUFFER) * 10
    line_spectrometer.set_data(r, fft)

    # simulated LED
    led_value = np.clip(volume_norm * 7.5, 0, 100)
    p.ChangeDutyCycle(led_value)
    # print(led_value)

    return line_lowpass, line_highpass, line_global, line_spectrometer


# Create an animation that updates the VU meter at a specified interval
ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 2 * np.pi, 128), interval=0, blit=True)
# show the plot
plt.grid()
plt.show()
# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.stop()