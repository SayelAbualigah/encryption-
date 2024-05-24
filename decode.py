import argparse
import wave
import struct
import lpc
import golomb

def main():
    parser = argparse.ArgumentParser(description='Decode compressed file to WAV format')
    parser.add_argument('input_file', help='Input compressed file')
    parser.add_argument('output_file', help='Output WAV file')
    args = parser.parse_args()

    with open(args.input_file, 'rb') as input_file:
        sample_rate = struct.unpack('<I', input_file.read(4))[0]
        sample_width = struct.unpack('<I', input_file.read(4))[0]
        num_channels = struct.unpack('<I', input_file.read(4))[0]
        lpc_order = struct.unpack('<I', input_file.read(4))[0]
        golomb_parameter = struct.unpack('<I', input_file.read(4))[0]

        compressed_data = input_file.read()

    residuals = golomb.decode(compressed_data, golomb_parameter)
    samples = lpc.decode(residuals, lpc_order)

    with wave.open(args.output_file, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(struct.pack('<' + 'h' * len(samples), *samples))

    print(f'Decompression complete. Reconstructed WAV file: {args.output_file}')

if __name__ == '__main__':
    main()
