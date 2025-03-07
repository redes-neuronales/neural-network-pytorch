import struct as st
import numpy as np

def read(fileName):
    """ Lee las imagenes desde first hasta last y las almacena en un arreglo 2D,
    donde cada renglon corresponde a una imagen.
    """
    file = open(fileName, "rb")
    # Leer numero magico
    magic = st.unpack('>4B', file.read(4))
    ## Los dos primeros bytes son cero
    byte = magic
    if byte[0] != 0 or byte[1] != 0:
        raise Exception("Encabezado corrupto: deben ser ceros" + str(byte))
        
    ## El tercero codifica el tipo de datos:
    ## 0x08: unsigned byte
    ## 0x09: signed byte
    ## 0x0B: short (2 bytes)
    ## 0x0C: int (4 bytes)
    ## 0x0D: float (4 bytes)
    ## 0x0E: double (8 bytes)
    switcher = {
        0x08 : np.uint8,
        0x09 : np.int8,
        0x0B : np.int16,
        0x0C : np.int32,
        0x0D : np.float32,
        0x0E : np.float64,
    }
    dataType = switcher.get(byte[2], None)
    ## Numero de dimensiones
    numDims = byte[3]
    ## Tamao de cada dimension (cada una es un int de 4 bytes MSB first)
    sizes = tuple(np.fromfile(file, dtype=np.int32, count=numDims).newbyteorder())
    print("Vector de ", numDims, " dimensiones: ", sizes, " tipo ", dataType)
    ## Resto
    a = np.fromfile(file, dtype=dataType)
    data = np.reshape(a, sizes)
    file.close()
    return data

def printFull(array):
    opt = np.get_printoptions()
    np.set_printoptions(threshold=np.inf)
    print(array)
    np.set_printoptions(**opt)