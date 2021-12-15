import os
import zmq 
import sys
import create_node
import range
from range import randomString


context = zmq.Context()



def conectar(nodo): #red de nodos servidores

    while True:

        print("escuchando..."+str("mi direccion: " + nodo.myAddr)+" "+str(",direccion predecesor: "+nodo.predAddr)+" "+str(",direccion sucesor: " + nodo.sucAddr)+" "+ str(nodo.rango.toStr()))

        msg = myconex.recv_multipart()

        tipo = msg[0].decode("utf-8")

        print(tipo)

        nodoId = int (msg[1].decode("utf-8"))

        nodoAddr =  msg[2].decode("utf-8")

        if tipo == 'conect' and responsable(nodo.rango, int(nodoId)):

            lb = str(nodo.rango.lb)

            msgpred =  [b'suc',lb.encode(),nodo.myAddr.encode(),nodo.predAddr.encode()]

            print(nodo.rango.lb)

            myconex.send_multipart(msgpred)

            nodo.predId = nodoId

            nodo.predAddr = nodoAddr

            nodo.rango = range.Range(int(nodoId),int(nodo.id))
 
            if nodo.sucAddr=='0':

                nodo.sucAddr = nodoAddr
        
        elif tipo == 'new suc':

            print("entro al nuevo suc")

            nodo.sucAddr = nodoAddr

            nodo.sucId = nodoId

            msgpred =  [b'sucesor cambiado',nodo.id.encode(),nodo.myAddr.encode(),nodo.predAddr.encode()]

            myconex.send_multipart(msgpred)

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

def comunicatePred(port,nodoAddr,nodoId): #le dice a su nuevo predecesor que el es su nuevo sucesor
    
    conexion = context.socket(zmq.REQ) 

    conexion.connect('tcp://localhost:'+str(port))

    msg = [b'new suc',nodoId.encode(),nodoAddr.encode()] 

    conexion.send_multipart(msg)

    print('mensaje enviado')

    conexion.close()

    


id = sys.argv[1]

myPORT = sys.argv[2]

SuccPORT = sys.argv[3]

Type = sys.argv[4]

nodo = create_node.CreateNode(id,myPORT,SuccPORT)


if (Type=="bootstrap"): # si es el primer nodo

    nodo.isFirst(int(nodo.id)) #su rango los incluye a todos

    nodo.predAddr = myPORT 

    myconex = conexServer(nodo.myAddr)

    conectar(nodo) #entra a la red

else:

    suc = conexClient(nodo.sucAddr)

    msg = [b'conect',nodo.id.encode(),nodo.myAddr.encode()] 

    suc.send_multipart(msg) # pregunta al nodo si es responsable de el 

    msgnodo = suc.recv_multipart()

    tipo = msgnodo[0].decode("utf-8")

   
   #Buscar responsable 

    nextAddr = msgnodo[2].decode("utf-8")

    while tipo!='suc':

        suc = conexClient(nextAddr)

        msg = [b'conect',nodo.id.encode(),nodo.myAddr.encode()] 

        suc.send_multipart(msg) # pregunta al nodo si es responsable de el 

        msgnodo = suc.recv_multipart()

        tipo =  msgnodo[0].decode("utf-8")

        nextAddr = msgnodo[2].decode("utf-8") #le manda la direccion del siguiente nodo

    #cuando encuentra el  responsable   

    suc.close()

    nodoId = msgnodo[1].decode("utf-8")

    nodoAddr = msgnodo[2].decode("utf-8")

    predAddr = msgnodo[3].decode("utf-8")

    comunicatePred(predAddr,nodo.myAddr,nodo.id) 

    myconex = conexServer(nodo.myAddr)
        
    nodo.rango = range.Range(int(nodoId),int(nodo.id))

    nodo.predAddr = predAddr  

    nodo.sucAddr = nodoAddr

    conectar(nodo) # entra a la red
            

           
