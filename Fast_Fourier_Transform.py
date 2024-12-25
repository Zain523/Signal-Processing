
import numpy as np
import matplotlib.pyplot as plt

def fft_noise_reduction(audio, sr):
    # Perform FFT
    fft_values = np.fft.fft(audio)
    fft_freq = np.fft.fftfreq(len(fft_values), d=1/sr)

    # Filter: Example - Keep frequencies below 1000 Hz
    cutoff_freq = 1500  # Hz
    fft_filtered = fft_values.copy()
    fft_filtered[np.abs(fft_freq) > cutoff_freq] = 0  # Set high frequencies to 0

    # Inverse FFT to reconstruct the filtered audio
    filtered_audio = np.fft.ifft(fft_filtered).real

    # fft_magnitude = np.abs(fft_values)
    # Plot the time-domain and frequency-domain representation
    # plt.figure(figsize=(12, 6))

    # # Time-domain signal
    # plt.subplot(1, 2, 1)
    # time = np.linspace(0, len(audio) / sr, len(audio))
    # plt.plot(time, audio)
    # plt.title("Time-domain Signal")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Amplitude")

    # # Frequency-domain (FFT)
    # plt.subplot(1, 2, 2)
    # plt.plot(fft_freq[:len(fft_freq)//2], fft_magnitude[:len(fft_magnitude)//2])  # Only positive frequencies
    # plt.title("Frequency-domain Signal (FFT)")
    # plt.xlabel("Frequency (Hz)")
    # plt.ylabel("Magnitude")

    # plt.tight_layout()
    # plt.show()


    return filtered_audio