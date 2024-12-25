import numpy as np
import pywt

def wavelet_denoising(audio, wavelet='db4', level=3):
    coeffs = pywt.wavedec(audio, wavelet, level=level)
    threshold = np.sqrt(2 * np.log(len(audio))) * np.median(np.abs(coeffs[-1]) / 0.6745)
    
    # Apply soft thresholding
    denoised_coeffs = [pywt.threshold(c, threshold, mode='soft') if i > 0 else c for i, c in enumerate(coeffs)]
    
    # Reconstruct the signal
    denoised_audio = pywt.waverec(denoised_coeffs, wavelet)
    return denoised_audio