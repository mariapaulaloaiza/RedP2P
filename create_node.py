import os
import range
import generate_id

class CreateNode:

    def __init__(self,myAddr,sucAddr):
        self.id = generate_id.randomName()
        self.predId = " "
        self.predAddr = " "
        self.sucId = " "
        self.myAddr = myAddr
        self.sucAddr = sucAddr
        self.rango = range.Range("","")

    def crear(self):
        try:
            os.mkdir('servidor'+self.id)
        except OSError:
            print("La creación del directorio falló")
        else:
            print("Se ha creado el directorio:")

    def isFirst(self,id):
        self.rango = range.Range(id,0)
