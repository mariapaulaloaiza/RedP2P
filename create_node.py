import os
import range

class CreateNode:

    def __init__(self,id,myAddr,sucAddr):
        self.id = id
        self.predId = " "
        self.predAddr = " "
        self.sucId = " "
        self.myAddr = myAddr
        self.sucAddr = sucAddr
        self.rango = range.Range("","")

    def crear(self):
        try:
            os.mkdir(self.nombre)
        except OSError:
            print("La creación del directorio falló")
        else:
            print("Se ha creado el directorio:")

    def isFirst(self,id):
        self.rango = range.Range(id,0)
