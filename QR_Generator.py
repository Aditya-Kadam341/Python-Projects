import numpy as np
from PIL import Image

def encode_data(data):
    binary_string ="".join(format(ord(char),"08b")for char in data)
    return binary_string

def create_qr_matrix(data, size = 21):
    matrix = np.zeros((size,size), dtype=int)

    def add_finder_patterns(x,y) :
        pattern = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        for i in range (7) :
            for j in range(7) :
                matrix[x + i, y + j] = pattern[i][j]
    
    add_finder_patterns(0,0)
    add_finder_patterns(0,size -7)
    add_finder_patterns(size - 7 ,0)

    binary_data = encode_data(data)
    index = 0
    for row in range (8, size - 1):
        for col in range( 8,size - 1) :
            if index < len(binary_data):
                matrix[row, col] = int(binary_data[index])
                index +=1
    return matrix


def save(matrix, filename ="qr_code.png", scale = 10) :
    size = matrix.shape[0] * scale
    img = Image.new("L",(size,size), 255)
    pixels = img.load()

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color  = 0 if matrix [i,j] == 1 else 255
            for x in range(scale):
                for y in range(scale):
                    pixels[j * scale + x, i * scale + y] = color

    img.save(filename)
    img.show()

data = input("Enter a link : ")
qrmatrix = create_qr_matrix(data)
save(qrmatrix)