import os
import zmq 
import sys
import create_node
import range
from range import randomString


context = zmq.Context()

pred = context.socket(zmq.REP)

suc = context.socket(zmq.REQ)

def conectar(nodo):

    if (Type=="bootstrap"):
        nodo.isFirst()
        pred.bind('tcp://*:'+nodo.myAddr) 
      #  suc.connect('tcp://localhost:'+nodo.sucAddr)
        
        
    else:
        pred.bind('tcp://*:'+nodo.myAddr) 
        suc.connect('tcp://localhost:'+nodo.sucAddr)
        msgsucc = [b'newNode',b'pred',nodo.id.encode(),nodo.myAddr.encode()]
        suc.send_multipart(msgsucc)

    while True:

        print("escuchando...")
        msgpred = pred.recv_multipart()
        print(msgpred[2]) 
        print(nodo.sucAddr)
        nodoid = msgpred[2].decode("utf-8")

        if msgpred[0].decode("utf-8")=='newNode'and responsable(nodo.rango,int(nodoid)):
            msgRes = [b'responsable',b'si',nodo.id.encode(),nodo.myAddr.encode()]
            print('hola primer if')
            if nodo.sucAddr==0:
                print('hola sub if')
                sucPort = msgpred[3].decode("utf-8")
                nodo.sucAddr = sucPort 
                suc.close()
                suc.connect('tcp://localhost:'+sucPort)
                print('hola sub if')
                suc.send_multipart(msgRes)
            else:
                suc.send_multipart(msgRes)

        elif msgpred[0].decode("utf-8")=='responsable' and msgpred[1]=='si':
            print('hola segundo if')
            id_predecesor = msgRes[2].decode("utf-8")
            nodo.rango = range.Range(id_predecesor,nodo.id)
            suc.connect('tcp://localhost:'+nodo.sucAddr)
            msgRes = [b'pred',b'cambiar',nodo.id.encode(),SuccPORT.encode()] #nodo actual address 
            suc.send_multipart(msgRes)

        elif msgpred[0].decode("utf-8")=='pred' and msgpred[1]=='si':
            print('hola segundo if')
            id_predecesor = msgRes[2].decode("utf-8")
            nodo.rango = range.Range(id_predecesor,nodo.id)
            msgRes = [b'pred',b'cambiar',nodo.id.encode(),SuccPORT.encode()]
            suc.send_multipart(msgRes)
        

        else:
            msgRes = [b'aqui',b'si',nodo.id.encode(),SuccPORT.encode()]
            print("entre aca")
            suc.send_multipart(msgRes)
 
        
def responsable(rango,id):

    member = rango.member(id)

    return member


id = sys.argv[1]

PredPORT = sys.argv[2]

SuccPORT = sys.argv[3]

Type = sys.argv[4]

nodo = create_node.CreateNode(id,PredPORT,SuccPORT)

conectar(nodo)
