import sys
import wave
import pyaudio

CHUNK = 1024

# Get command-line args
if len(sys.argv) < 2:
    print(f"Plays a wave file. Usage: {sys.argv[0]} filename.wav")
    sys.exit(-1)

# Play audio file
with wave.open(sys.argv[1], "rb") as wave_file:
    # Instantiate PyAudio and initialize PortAudio system resources
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(
        format=p.get_format_from_width(wave_file.getsampwidth()),
        channels=wave_file.getnchannels(),
        rate=wave_file.getframerate(),
        output=True,
    )

    # Play samples from the wave file
    while len(data := wave_file.readframes(CHUNK)):
        stream.write(data)

    # Close stream
    stream.close()

    # Release PortAudio system resources
    p.terminate()
