import numpy as np
from PIL import Image

def encode_data(data):
    mode_indicator = "0100"  # Byte mode
    length_indicator = format(len(data), "08b")  # Length of data
    binary_string = mode_indicator + length_indicator + "".join(format(ord(char), "08b") for char in data)
    return binary_string + "0000"  # Terminator bits

def create_qr_matrix(data, size=21):
    matrix = np.zeros((size, size), dtype=int)

    def add_finder_patterns():
        pattern = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        positions = [(0, 0), (0, size - 7), (size - 7, 0)]
        for x, y in positions:
            for i in range(7):
                for j in range(7):
                    matrix[x + i, y + j] = pattern[i][j]

    def add_timing_patterns():
        for i in range(8, size - 8, 2):
            matrix[6, i] = matrix[i, 6] = 1

    add_finder_patterns()
    add_timing_patterns()

    binary_data = encode_data(data)
    index = 0
    for col in range(size - 1, 0, -2):
        if col == 6:
            continue  # Skip the timing pattern column
        for row in range(size - 1, -1, -1) if (size - col) % 4 else range(size):
            for offset in [0, -1]:
                if col + offset < 0 or index >= len(binary_data):
                    continue
                if matrix[row, col + offset] == 0:
                    matrix[row, col + offset] = int(binary_data[index])
                    index += 1
    return matrix

def save(matrix, filename="qr_code.png", scale=10):
    size = matrix.shape[0] * scale
    img = Image.new("L", (size, size), 255)
    pixels = img.load()

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color = 0 if matrix[i, j] == 1 else 255
            for x in range(scale):
                for y in range(scale):
                    pixels[j * scale + x, i * scale + y] = color

    img.save(filename)
    img.show()

data = input("Enter a link: ")
qrmatrix = create_qr_matrix(data)
save(qrmatrix)
