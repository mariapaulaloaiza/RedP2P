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

    global suc
    if (Type=="bootstrap"):
        nodo.isFirst()
        pred.bind('tcp://*:'+nodo.myAddr) 
        print("boot if")
        #suc.connect('tcp://localhost:'+nodo.myAddr)
        
        
    else:
        #pred.bind('tcp://*:'+nodo.myAddr) 
        suc.connect('tcp://localhost:'+nodo.sucAddr)
        msgsucc = [b'newNode',b'pred',nodo.id.encode(),nodo.myAddr.encode()]
        suc.send_multipart(msgsucc)

    while True:

        print("escuchando...")
        msgpred = pred.recv_multipart()
        print(msgpred[0]) 
        nodoid = msgpred[2].decode("utf-8")

        if msgpred[0].decode("utf-8")=='newNode'and responsable(nodo.rango,int(nodoid)):
            msgRes = [b'responsable',b'si',nodo.id.encode(),nodo.myAddr.encode()]
            print('hola primer if {}'.format(nodo.sucAddr))
            '''if nodo.sucAddr=='0':
                print('hola sub if')
                sucPort = msgpred[3].decode("utf-8")
                nodo.sucAddr = sucPort 
                print(nodo.sucAddr)
                print('hola sub if 2')
                suc.close()
                suc = context.socket(zmq.REQ)
                suc.connect('tcp://localhost:'+ nodo.sucAddr)
                suc.send_multipart(msgRes)
                print('hola sub if 3')
            else:
                print("sub else")'''
            pred.send_multipart(msgRes)
            print('final 1')

        else: 
            print('else final')
            msgRes = [b'aqui',b'nada',nodo.id.encode(),nodo.myAddr.encode()] 
            #suc.close()
            #suc = context.socket(zmq.REQ)
            #suc.connect('tcp://localhost:'+ nodo.sucAddr)
            suc.send_multipart(msgRes)
            print('else final 2')
            
       
        '''elif msgpred[0].decode("utf-8")=='responsable' and msgpred[1].decode("utf-8")=='si':
            print('hola segundo if')
            id_predecesor = msgpred[2].decode("utf-8")
            nodo.rango = range.Range(id_predecesor,nodo.id)
            #suc.connect('tcp://localhost:'+nodo.sucAddr)
            suc.close()
            suc = context.socket(zmq.REQ)
            suc.connect('tcp://localhost:'+ nodo.sucAddr)
            msgRes = [b'pred',b'cambiar',nodo.id.encode(),nodo.myAddr.encode()] #nodo actual address 
            suc.send_multipart(msgRes)'''
        
       
     
        
def responsable(rango,id):

    member = rango.member(id)

    return member


id = sys.argv[1]

PredPORT = sys.argv[2]

SuccPORT = sys.argv[3]

Type = sys.argv[4]

nodo = create_node.CreateNode(id,PredPORT,SuccPORT)

conectar(nodo)
