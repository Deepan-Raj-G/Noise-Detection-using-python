import pyaudio
import time
import wave
import sounddevice as sd
import numpy as np
count  = 1
def main():
    total_duration_minutes = 60
    total_duration_seconds = total_duration_minutes * 60

    start_time = time.time()

    while time.time() - start_time < total_duration_seconds:
        if(count==12):
            break
        def sound_detection_callback(indata, frames, time, status):
            if status:
                print(status)

            # Set a threshold for sound detection
            threshold = 0.1

            # Check if the amplitude of the incoming audio data exceeds the threshold
            if np.max(indata) > threshold:
                print("Sound detected!")
                your_function_to_call()  # Replace this with the function you want to call

        # Your function to be called when sound is detected
        def your_function_to_call():
            global count
        # Set audio recording parameters
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            RECORD_SECONDS = 5
            WAVE_OUTPUT_FILENAME = f"recordings/recorded_audio_{count}.wav"
            count += 1

        # Initialize PyAudio object
            audio = pyaudio.PyAudio()

            # Start audio recording
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                input=True, frames_per_buffer=CHUNK)
            print("Recording...")
            frames = []

            # Record audio for the specified duration
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            # Stop recording
            stream.stop_stream()
            stream.close()
            audio.terminate()

            # Save recorded audio to a file
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()

            print("Recording finished and saved to: " + WAVE_OUTPUT_FILENAME)

        # Set the duration and sampling frequency
        duration = 10  # in seconds
        fs = 44100  # 44.1 kHz sampling frequency

        # Start streaming audio and call the callback function for sound detection
        print("Listening for sound...")
        with sd.InputStream(callback=sound_detection_callback, channels=2, samplerate=fs):
            sd.sleep(int(duration * 1000))  # Sleep for the specified duration (in milliseconds)


if __name__ == "__main__":
    main()