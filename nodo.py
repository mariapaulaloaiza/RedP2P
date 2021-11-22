import zmq 
import sys
import create_node
import random
import range

id = sys.argv[1]

PredPORT = sys.argv[2]

SuccPORT = sys.argv[3]

Type = sys.argv[4]

node = create_node.CreateNode(id,PredPORT,Type)

context = zmq.Context()


def ConexPred(PredPORT):

    pred = context.socket(zmq.REP)

    pred.bind('tcp://*:'+PredPORT)

    return pred


def ConexSuc(SuccPORT):

    suc = context.socket(zmq.REQ)

    suc.connect('tcp://localhost:'+SuccPORT)

    return suc 


def responsable(node,id):

    member = node.rango.member(id)

    return member



type = "node"

op = "pred"

nodeid = node.id

suc = ConexSuc(SuccPORT)

pred = ConexPred(PredPORT)


suc.send_multipart([type.encode(),op.encode(),nodeid.encode()])






while True:

    print("escuchando...")

    mensaje_predecesor = pred.recv_multipart()

    id_predecesor = mensaje_predecesor[2].decode("utf-8")

    print("mi ID es: " + id_predecesor)

    node.rango = range.Range(id_predecesor,node.id)

    print(node.id +"->" + node.rango.toStr())

    

    
    
