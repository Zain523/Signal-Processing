import librosa
import librosa.display
import matplotlib.pyplot as plt

def plot_spectrogram(audio, sr):
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(audio, sr=sr)
    plt.title('Waveform of Filtered Audio')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()