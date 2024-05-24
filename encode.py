import argparse
import wave
import struct
import lpc
import golomb

def main():
    parser = argparse.ArgumentParser(description='Encode WAV file to compressed format')
    parser.add_argument('input_file', help='Input WAV file')
    parser.add_argument('output_file', help='Output compressed file')
    args = parser.parse_args()

    with wave.open(args.input_file, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        sample_width = wav_file.getsampwidth()
        num_channels = wav_file.getnchannels()
        num_frames = wav_file.getnframes()

        samples = []
        for _ in range(num_frames):
            frame = wav_file.readframes(1)
            sample = struct.unpack('<h', frame)[0]
            samples.append(sample)

    lpc_order = 10
    residuals = lpc.encode(samples, lpc_order)

    golomb_parameter = 8
    compressed_data = golomb.encode(residuals, golomb_parameter)

    with open(args.output_file, 'wb') as output_file:
        output_file.write(struct.pack('<I', sample_rate))
        output_file.write(struct.pack('<I', sample_width))
        output_file.write(struct.pack('<I', num_channels))
        output_file.write(struct.pack('<I', lpc_order))
        output_file.write(struct.pack('<I', golomb_parameter))
        output_file.write(compressed_data)

    print(f'Compression complete. Compressed file: {args.output_file}')

if __name__ == '__main__':
    main()
