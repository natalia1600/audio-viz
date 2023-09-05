import wave, struct

wavefile = wave.open('time_goes.wav', 'r')

length = wavefile.getnframes()
print(wavefile.getparams().sampwidth * wavefile.getparams().nchannels)
for i in range(0, length):
    wavedata = wavefile.readframes(1)
    data = struct.unpack("<i", wavedata)
    print(int(data[0]))