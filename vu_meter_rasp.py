import pyaudio
import numpy as np
import RPi.GPIO as GPIO
import sounddevice
from scipy.signal import butter, lfilter, filtfilt

# Initialize PyAudio
p = pyaudio.PyAudio()
RATE = 44100

# get default input device
default_input = sounddevice.default.device[0]

# Open input stream
stream = p.open(format=pyaudio.paInt16, channels=2, rate=RATE, input=True, frames_per_buffer=1024,
                input_device_index=default_input)

# Start the stream
stream.start_stream()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 1)

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (fs / 2), btype='low')
    filtered_signal = lfilter(b, a, data)
    return filtered_signal


def highpass_filter(signal, cutoff, fs, order=5):
    b, a = butter(order, cutoff / (fs / 2), btype='high')
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal


# Plot the data as VU
while True:
    # Read data from the input stream
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    # Calculate the volume level

    # for low pass
    lowpass_filtered_data = lowpass_filter(data, cutoff=300, fs=RATE)
    volume_norm_low = np.linalg.norm(lowpass_filtered_data) / (2 ** 15)

    # for high pass
    highpass_filtered_data = highpass_filter(data, 5000, fs=RATE)
    volume_norm_high = np.linalg.norm(highpass_filtered_data) / (2 ** 15)

    volume_norm = np.linalg.norm(data) / (2 ** 15)

    led_value = np.clip(volume_norm * 7.5, 0, 100)
    print(led_value)
    p.ChangeDutyCycle(led_value)


# Close the stream and terminate PyAudio
stream.stop_stream()
stream.close()
p.stop()
