import soundfile as sf
from sklearn.metrics import mean_squared_error
import numpy as np
import librosa
import librosa.display

# import techniques
from Fast_Fourier_Transform import fft_noise_reduction
from Spectral_Subtraction import denoise_audio
from Wavelet_Technique import wavelet_denoising
from Plot import plot_spectrogram

# Load noisy audio file
file_path = 'Sample_audio/conversation-in-class-room-66980.mp3'
#file_path = 'Sample_audio/Recording (2) (online-audio-converter.com) (1).mp3'
audio, sr = librosa.load(file_path, sr=None)

print(f"Sampling Rate: {sr}, Audio Duration: {len(audio)/sr:.2f} seconds")


# Apply FFT-based filtering
# audio_fft = fft_noise_reduction(audio, sr)

# plot_spectrogram(audio_fft, sr)

# Apply spectral subtraction
audio_spectral = denoise_audio(audio, sr)

# Apply wavelet-based denoising
audio_wavelet = wavelet_denoising(audio)

def calculate_mse(clean_signal, noised_signal):
    return mean_squared_error(clean_signal, noised_signal)

# Example usage
# mse_fft = calculate_mse(audio_fft, audio)
# print(f"MSE (FFT): {mse_fft}")


mse_fft = calculate_mse(audio_spectral, audio)
print(f"MSE (SS): {mse_fft}")

# mse_fft = calculate_mse(audio_wavelet, audio)
# print(f"MSE (AW): {mse_fft}")


# Example: Save the FFT denoised audio
# sf.write('denoised_fft.wav', audio_fft , samplerate=sr)

# # Example: Save the Spectral Subtraction denoised audio
sf.write('Denoise_audio/denoised_spectral.wav', audio_spectral, samplerate=sr)

# # # Example: Save the Wavelet Transform denoised audio
#sf.write('denoised_fft.wav', filtered_audio, samplerate=sr)
sf.write('Denoise_audio/denoised_wavelet.wav', audio_wavelet, samplerate=sr)


# sf.write('denoised_audio_noisereduce.wav', reduced_noise, sr)

print("Audio files saved successfully!")
def calculate_mse(clean_signal, noised_signal):
    # Truncate the longer signal to match the shorter one
    min_length = min(len(clean_signal), len(noised_signal))
    clean_signal = clean_signal[:min_length]
    noised_signal = noised_signal[:min_length]
    return mean_squared_error(clean_signal, noised_signal)

mse_wavelet = calculate_mse(audio_wavelet, audio)
print(f"MSE (Wavelet): {mse_wavelet}")
