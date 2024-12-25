import numpy as np
import librosa

def stft(audio):
    """Performs Short-Time Fourier Transform (STFT) on the audio signal."""
    return librosa.stft(audio)


def spectral_subtraction(noise_profile, input_signal):
    """Performs spectral subtraction to reduce noise from the input signal."""
    # Compute STFT
    N = stft(noise_profile)
    mN = np.abs(N)  # magnitude spectrum

    Y = stft(input_signal)
    mY = np.abs(Y)
    pY = np.angle(Y)  # phase spectrum
    poY = np.exp(1.0j * pY)  # phase information

    # Spectral subtraction
    noise_mean = np.mean(mN, axis=1, dtype="float64")  # Find noise mean
    noise_mean = noise_mean[:, np.newaxis]  # Perform subtraction
    output_X = mY - noise_mean
    X = np.clip(output_X, a_min=0.0, a_max=None)

    # Add phase info
    X = X * poY

    # Inverse STFT
    output_x = librosa.istft(X)
    return output_x


def detect_noise_segment(audio, sr, energy_threshold=0.1, min_duration=0.5):

    frame_length = 2048
    hop_length = 512
    energy = np.array([
        np.sum(np.abs(audio[i:i+frame_length])**2)
        for i in range(0, len(audio), hop_length)
    ])

    # Normalize energy values
    energy = energy / np.max(energy)

    # Detect noise (low energy)
    noise_frames = np.where(energy < energy_threshold)[0]

    if len(noise_frames) == 0:
        return None, None

    # Calculate noise start and end samples
    noise_start_frame = noise_frames[0]
    noise_end_frame = noise_frames[-1]

    noise_start_sample = noise_start_frame * hop_length
    noise_end_sample = noise_end_frame * hop_length

    if (noise_end_sample - noise_start_sample) / sr < min_duration:
        return None, None

    return noise_start_sample, noise_end_sample


def denoise_audio(audio, sample_rate):

    y = audio
    fs_y = sample_rate

    # If audio is multi-channel (e.g., stereo), convert to mono
    if y.ndim > 1:
        y = librosa.to_mono(y)

    # Detect noise segment
    noise_start, noise_end = detect_noise_segment(y, fs_y, energy_threshold=0.1, min_duration=0.5)
    if noise_start is None or noise_end is None:
        raise ValueError("Failed to detect a valid noise segment in the input audio.")


    # Extract noise profile
    noise_profile = y[noise_start:noise_end]

    # Perform spectral subtraction
    output_x = spectral_subtraction(noise_profile, y)

    return output_x

