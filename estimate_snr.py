import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from scipy.signal.windows import hamming
import argparse

class SNREstimator:
    def __init__(self, input_file, window_size, hop_size):
        self.sample_rate, self.audio_data = wavfile.read(input_file)
        self.frame_length = window_size
        self.hop_length = hop_size

    def frame_audio(self, signal):
        num_frames = 1 + (len(signal) - self.frame_length) // self.hop_length
        frames = [signal[i * self.hop_length: (i * self.hop_length) + self.frame_length] for i in range(num_frames)]
        return frames

    def calculate_log_energy(self, frame):
        energy = np.sum(frame ** 2)
        return np.log(energy)

    def calculate_snr(self, energy_high, energy_low):
        return 10 * np.log10(energy_high / energy_low)

    def estimate_snr(self):
        frames = self.frame_audio(self.audio_data)
        log_energies = [self.calculate_log_energy(frame * hamming(self.frame_length)) for frame in frames]
        
        energy_threshold_low = np.percentile(log_energies, 25)  #First quartile
        energy_threshold_high = np.percentile(log_energies, 75)  #Third quartile

        low_energy_frames = [log_energy for log_energy in log_energies if log_energy <= energy_threshold_low]
        high_energy_frames = [log_energy for log_energy in log_energies if log_energy >= energy_threshold_high]
        
        mean_low_energy = np.mean(low_energy_frames)
        mean_high_energy = np.mean(high_energy_frames)
        
        estimated_snr = self.calculate_snr(np.exp(mean_high_energy), np.exp(mean_low_energy))
        return estimated_snr, log_energies, energy_threshold_low, energy_threshold_high

    def plot_energy(self, log_energies, energy_threshold_low, energy_threshold_high):
        plt.figure(figsize=(10, 6))
        plt.plot(log_energies, label='Log Energy')
        plt.axhline(y=energy_threshold_low, color='r', linestyle='--', label='Low Energy Threshold (25th Percentile)')
        plt.axhline(y=energy_threshold_high, color='g', linestyle='--', label='High Energy Threshold (75th Percentile)')
        plt.xlabel('Frame')
        plt.ylabel('Log Energy')
        plt.title('Log Energy and Energy Thresholds')
        plt.legend()
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Estimate SNR from audio signal')
    parser.add_argument('--input', required=True, help='Input audio file in WAV format')
    parser.add_argument('--window_size', type=int, default=int(0.02 * 16000), help='Window size in samples (default: 320)')
    parser.add_argument('--hop_size', type=int, default=int(0.01 * 16000), help='Hop size in samples (default: 160)')
    parser.add_argument('--plot', action='store_true', help='Plot log energy and energy thresholds')
    args = parser.parse_args()

    snr_estimator = SNREstimator(args.input, args.window_size, args.hop_size)
    estimated_snr, log_energies, energy_threshold_low, energy_threshold_high = snr_estimator.estimate_snr()

    print("Estimated SNR:", estimated_snr)
    
    if args.plot:
        snr_estimator.plot_energy(log_energies, energy_threshold_low, energy_threshold_high)

if __name__ == '__main__':
    main()
