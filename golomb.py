import math
import bitarray

def encode(residuals, parameter):
    m = 2 ** parameter
    encoded_data = bitarray.bitarray()

    for residual in residuals:
        # Convert residual to non-negative integer
        residual = abs(residual) * 2
        if residual < 0:
            residual -= 1

        # Compute quotient and remainder
        quotient = residual // m
        remainder = residual % m

        # Unary coding of quotient
        unary_code = bitarray.bitarray(quotient)
        unary_code.setall(1)
        unary_code.append(0)

        # Binary coding of remainder
        binary_code = bitarray.bitarray(format(remainder, f'0{parameter}b'))

        # Append the encoded residual to the output bitstream
        encoded_data.extend(unary_code)
        encoded_data.extend(binary_code)

    return encoded_data.tobytes()

def decode(compressed_data, parameter):
    m = 2 ** parameter
    decoded_residuals = []
    data = bitarray.bitarray(endian='big')
    data.frombytes(compressed_data)

    while len(data) > 0:
        # Unary decoding of quotient
        quotient = 0
        while data.pop(0):
            quotient += 1

        # Binary decoding of remainder
        remainder = data[:parameter].to01()
        remainder = int(remainder, 2)
        data = data[parameter:]

        # Reconstruct the residual
        residual = quotient * m + remainder

        # Convert residual back to signed integer
        if residual % 2 == 0:
            residual = residual // 2
        else:
            residual = -(residual + 1) // 2

        decoded_residuals.append(residual)

    return decoded_residuals
