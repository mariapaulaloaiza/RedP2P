import os
import zmq 
import sys
import create_node
import range
from range import randomString


context = zmq.Context()



def conectar(nodo):

    while True:

        print("escuchando..."+str("mi direccion: " + nodo.myAddr)+" "+str(",direccion predecesor: "+nodo.predAddr)+" "+str(",direccion sucesor: " + nodo.sucAddr)+" "+ str(nodo.rango.toStr()))

        msg = myconex.recv_multipart()

        nodoId = int (msg[1].decode("utf-8"))

        nodoAddr =  msg[2].decode("utf-8")

        if responsable(nodo.rango, int(nodoId)):

            print(nodo.predAddr)

            msgpred =  [b'suc',nodo.id.encode(),nodo.myAddr.encode(),nodo.predAddr.encode()]

            myconex.send_multipart(msgpred)

            nodo.predId = nodoId

            nodo.predAddr = nodoAddr

            nodo.rango = range.Range(int(nodoId),int(nodo.id))

            if nodo.sucAddr=='0':

                nodo.sucAddr = nodoAddr
        else:

            msgpred =  [b'no suc',nodo.id.encode(),nodo.sucAddr.encode(),nodo.predAddr.encode()]

            myconex.send_multipart(msgpred)
       
                 
        
def responsable(rango,id):

    member = rango.member(int(id))

    return member

def conexServer(port):

    conexion = context.socket(zmq.REP)

    conexion.bind('tcp://*:'+str(port)) 

    return conexion

def conexClient(port):

    conexion = context.socket(zmq.REQ) 

    conexion.connect('tcp://localhost:'+str(port))

    return conexion


id = sys.argv[1]

myPORT = sys.argv[2]

SuccPORT = sys.argv[3]

Type = sys.argv[4]

nodo = create_node.CreateNode(id,myPORT,SuccPORT)


if (Type=="bootstrap"):

    nodo.isFirst()

    nodo.predAddr = myPORT

    myconex = conexServer(nodo.myAddr)

    conectar(nodo)

else:

    suc = conexClient(nodo.sucAddr)

    msg = [b'conect',nodo.id.encode(),nodo.myAddr.encode()] 

    suc.send_multipart(msg) # pregunta al nodo si es responsable de el 

    msgnodo = suc.recv_multipart()

    tipo = msgnodo[0].decode("utf-8")

    nodoId = msgnodo[1].decode("utf-8")

    nodoAddr = msgnodo[2].decode("utf-8")

    
    
   #Buscar responsable 

    nextAddr = msgnodo[2].decode("utf-8")

    while tipo!='suc':

        suc = conexClient(nextAddr)

        msg = [b'conect',nodo.id.encode(),nodo.myAddr.encode()] 

        suc.send_multipart(msg) # pregunta al nodo si es responsable de el 

        msgnodo = suc.recv_multipart()

        tipo =  msgnodo[0].decode("utf-8")

        nextAddr = msgnodo[2].decode("utf-8")

    #cuando si es responsable    

    myconex = conexServer(nodo.myAddr)

    predAddr = msgnodo[3].decode("utf-8")
        
    nodo.rango = range.Range(int(nodoId),int(nodo.id))

    nodo.predAddr = predAddr  

    nodo.sucAddr = nodoAddr

    conectar(nodo) # entra a la red
            

           
