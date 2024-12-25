# import numpy as np
# import pywt

# def wavelet_denoising(audio, wavelet='db4', level=3):
#     coeffs = pywt.wavedec(audio, wavelet, level=level)
#     threshold = np.sqrt(2 * np.log(len(audio))) * np.median(np.abs(coeffs[-1]) / 0.6745)
    
#     # Apply soft thresholding
#     denoised_coeffs = [pywt.threshold(c, threshold, mode='soft') if i > 0 else c for i, c in enumerate(coeffs)]
    
#     # Reconstruct the signal
#     denoised_audio = pywt.waverec(denoised_coeffs, wavelet)
#     return denoised_audio
import numpy as np

def wavelet_transform(signal, wavelet_filter, level=3):
    coeffs = []
    for _ in range(level):
        approximation = np.convolve(signal, wavelet_filter, mode='full')[::2]
        detail = np.convolve(signal, wavelet_filter[::-1], mode='full')[::2]
        coeffs.append((approximation, detail))
        signal = approximation
    return coeffs

def wavelet_inverse(coeffs, wavelet_filter):
    signal = coeffs[-1][0]
    for approximation, detail in reversed(coeffs[:-1]):
        upsampled_approximation = np.zeros(2 * len(approximation))
        upsampled_approximation[::2] = approximation
        upsampled_detail = np.zeros(2 * len(detail))
        upsampled_detail[::2] = detail
        signal = np.convolve(upsampled_approximation, wavelet_filter[::-1], mode='full') + \
                 np.convolve(upsampled_detail, wavelet_filter, mode='full')
    return signal

def wavelet_denoising(audio, wavelet_filter=[0.5, 0.5], level=3):
    coeffs = wavelet_transform(audio, wavelet_filter, level)
    threshold = np.sqrt(2 * np.log(len(audio)))
    # threshold = 0.02 * np.max(coeffs[-1])
    denoised_coeffs = [(approximation, np.sign(detail) * np.maximum(np.abs(detail) - threshold, 0))
                       for approximation, detail in coeffs]
    denoised_audio = wavelet_inverse(denoised_coeffs, wavelet_filter)
    return denoised_audio

