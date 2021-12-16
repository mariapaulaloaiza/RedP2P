import zmq
import sys
import base64
import json
import shasum

context = zmq.Context()

diccionario = {}


def enviar(opcion,nombreArchivo,puerto):

    ConexionServidor = context.socket(zmq.REQ)

    archivo = open(nombreArchivo, 'rb')

    while True:

        contenido = archivo.read(1024*1024)

        if not contenido:

            archivo_encode = base64.encodebytes(b'0')

            break

        archivo_encode = base64.encodebytes(contenido)

        llaveArchivo = shasum.shasum(archivo_encode)

        ConexionServidor.connect('tcp://localhost:'+puerto)

        ConexionServidor.send_multipart([b'cliente',str(llaveArchivo).encode(),opcion.encode(),nombreArchivo.encode(),archivo_encode])
        
        msgServidor = ConexionServidor.recv_multipart()

        respuesta = msgServidor[0].decode("utf-8")

        nextAddr = msgServidor[1].decode("utf-8")

        while respuesta!='responsable':

            ConexionServidor.connect('tcp://localhost:'+nextAddr)

            ConexionServidor.send_multipart([b'cliente',str(llaveArchivo).encode(),opcion.encode(),nombreArchivo.encode(),archivo_encode]) 

            msgServidor = ConexionServidor.recv_multipart()

            respuesta = msgServidor[0].decode("utf-8")

            nextAddr = msgServidor[1].decode("utf-8") #direccion del siguiente nodo

        diccionario[llaveArchivo]=nextAddr




#Empieza
opcion = sys.argv[1]

nombreArchivo = sys.argv[2]

puerto = sys.argv[3]

if opcion =='upload':

    enviar(opcion,nombreArchivo,puerto)

    with open(nombreArchivo+'.json','w') as file:

        json.dump(diccionario,file)

    file.close()

    print(diccionario)

    
