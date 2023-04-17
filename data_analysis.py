import os
import librosa
import pyworld as pw
import numpy as np
import pandas as pd
# define the directory containing the audio files
audio_dir = "/data/speech_synth/TTS_Dataset_Creater/output/wavs/SPEAKER_01"

# define the analysis window size in seconds
window_size = 0.1
results_df = pd.DataFrame(columns=["filename", "duration", "pitch", "energy", "speaking_rate", "snr"])

# iterate over all audio files in the directory
for filename in os.listdir(audio_dir):
    if filename.endswith(".wav"):
        # load the audio file
        audio_path = os.path.join(audio_dir, filename)
        y, sr = librosa.load(audio_path, sr=None)
        y=y.astype(np.float64)
        # extract the fundamental frequency (pitch) using the WORLD vocoder
        f0, t = pw.dio(y, sr)
        f0 = pw.stonemask(y, f0, t, sr)
        f0_mean = np.mean(f0)
        
        # calculate the audio duration
        duration = librosa.get_duration(y, sr)

        # extract the energy using the root-mean-square (RMS) amplitude
        rms = librosa.feature.rms(y, frame_length=int(window_size*sr), hop_length=int(window_size*sr))
        energy_mean = rms.mean()

        # calculate the speaking rate as the number of voiced segments per second
        voiced_segments = pw.harvest(y, sr)
        speaking_rate = len(voiced_segments) / y.shape[0] * sr
        
        # calculate the signal-to-noise ratio (SNR)
        noise = np.random.randn(y.shape[0])
        noise *= np.sqrt(np.var(y)) / np.sqrt(np.var(noise))
        snr = 20 * np.log10(np.linalg.norm(y) / np.linalg.norm(noise))

        # # Compute formant frequencies
        # fft_size = pw.get_cheaptrick_fft_size(sr)
        # sp = pw.cheaptrick(y, f0, t, sr, fft_size=fft_size)
        # sp = pw.code_spectral_envelope(sp, sr, pw.get_cheaptrick_fft_size(sr))
        # formants = sp

        # append the results to the DataFrame
        results_df = results_df.append({
            "filename": filename,
            "duration": duration,
            "pitch": f0_mean,
            "energy": energy_mean,
            "speaking_rate": speaking_rate,
            "snr": snr
        }, ignore_index=True)

results_df.to_csv("analysis_results.csv", index=False)