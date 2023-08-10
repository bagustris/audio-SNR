# Mixing and Estimate audio file with a noise file at any Signal-to-Noise Ratio
The script `create_mixed_audio_file.py` and `create_mixed_audio_file_with_soundfile.py` can mix an audio file with a noise file at any Signal-to-Noise Ratio (SNR). 

You can listen to the results of [mixtures](/data/16_bit/output_mixed) of the [clean voice](data/16_bit/source_clean) and the [noise](data/16_bit/source_noise).

## Installation
No need to install, just install the necessary libraries in each python file if you don't have them.

### File format
To use this code, the format of source waveforms is as follows.

- WAV file
- 1 channel

Additionally, the sampling rate of a clean file and that of a noise file are supposed to be the same.

## Usage
There are two files for creating a mixture.

- `create_mixed_audio_file.py`:
  - Uses wave module
  - Can read wav file with 16-bit PCM only

- `create_mixed_audio_file_with_soundfile.py`:
  - Uses soundfile library
  - Can read wav file with various encoding types such as 16-bit PCM, 32-bit PCM, 32-bit float, and 64-bit float. 

After activating a virtualenv, you can run the files to mix an audio file with a noise file at any signal-to-noise ratio.

Example of `create_mixed_audio_file.py`: 

```bash
$ python3 create_mixed_audio_file.py --clean_file ./data/16_bit/source_clean/arctic_a0001.wav --noise_file ./data/16_bit/source_noise/ch01.wav --snr 20 --output_mixed_file ./data/16_bit/output_mixed/20dB.wav
```

Example of `create_mixed_audio_file_with_soundfile.py`:

```bash
$ python3 create_mixed_audio_file_with_soundfile.py --clean_file ./data/64_bit/source_clean/arctic_a0001_64bit.wav --noise_file ./data/64_bit/source_noise/ch01_64bit.wav --snr 0 --output_mixed_file ./data/64_bit/output_mixed/0dB.wav
```

Example of `estimate_snr.py`:

```bash
$ python estimate_snr.py --input data/16_bit/output_mixed/20dB.wav 
Estimated SNR: 22.589152898412486
```

## Dataset

- [Voices](http://festvox.org/cmu_arctic/) - CMU_ARCTIC speech synthesis databases
- [Noises](https://zenodo.org/record/1227121#.W2wUVNj7TUI) - DEMAND: a collection of multi-channel recordings of acoustic noise in diverse environments
