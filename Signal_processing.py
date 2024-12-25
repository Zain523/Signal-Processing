import soundfile as sf
# from sklearn.metrics import mean_squared_error
import librosa
import os

# import techniques
from Fast_Fourier_Transform import fft_noise_reduction
from Spectral_Subtraction import denoise_audio
from Wavelet_Technique import wavelet_denoising
# from Plot import plot_spectrogram

def reduce_noise(file_path, technique):
    audio, sr = librosa.load(file_path, sr=None)
    print(f"Sampling Rate: {sr}, Audio Duration: {len(audio)/sr:.2f} seconds")

    if(technique == 'fft'):
        filter_audio = fft_noise_reduction(audio, sr)

    elif(technique == 'spectral'):
        filter_audio = denoise_audio(audio, sr)

    else:
      filter_audio = wavelet_denoising(audio)

    print("Audio files denoised successfully!")

    # We save file directly to client assets folder until we use cloud storage because from there we easily access that file 
    
    sf.write('D:/Python/Signal Processing/client/public/assets/filter_audio.wav', filter_audio , samplerate=sr)

    print("Audio files save successfully!")
    
    # filter_audio_path = os.path.abspath('filter_audio.wav')
    return 'filter_audio.wav'


# def calculate_mse(clean_signal, noised_signal):
#     return mean_squared_error(clean_signal, noised_signal)

# Example usage
# mse_fft = calculate_mse(audio_fft, audio)
# print(f"MSE (FFT): {mse_fft}")

# Example: Save the FFT denoised audio
# sf.write('denoised_fft.wav', audio_fft , samplerate=sr)
