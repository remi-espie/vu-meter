# import pyaudio
#
# p = pyaudio.PyAudio()
#
# for i in range(p.get_device_count()):
#     print(i, p.get_device_info_by_index(i))


import sounddevice

s = sounddevice.query_devices()
print(s)

s = sounddevice.default.device[0]
print(s)
