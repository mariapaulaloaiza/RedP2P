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
        suc.connect('tcp://localhost:'+nodo.myAddr)
        #msgsucc = [b'newNode',b'pred',nodo.id.encode(),nodo.myAddr.encode()]
        #suc.send_multipart(msgsucc)

    if (Type=="second"):
        pred.bind('tcp://*:'+nodo.myAddr) 
        suc.connect('tcp://localhost:'+nodo.sucAddr)
        msgsucc = [b'newNode',b'pred',nodo.id.encode(),nodo.myAddr.encode()]
        suc.send_multipart(msgsucc)

    while True:

        print("escuchando...")
        msgpred = pred.recv_multipart()
        print(msgpred[2]) 
        succadr = str(msgpred[3].decode("utf-8"))
        suc.connect('tcp://localhost:'+succadr)
        msgsucc = [b'newNode',b'pred',nodo.id.encode(),nodo.myAddr.encode()]
        suc.send_multipart(msgsucc)

      

def responsable(rango,id):

    member = rango.member(id)

    return member


id = sys.argv[1]

PredPORT = sys.argv[2]

SuccPORT = sys.argv[3]

Type = sys.argv[4]

nodo = create_node.CreateNode(id,PredPORT,SuccPORT)

conectar(nodo)
