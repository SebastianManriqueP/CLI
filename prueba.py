import requests
import json

urlBase = "http://localhost:8080"


def iniciar():
    uri = "/inicio"
    #solicitud GET
    response = requests.get(urlBase+uri)

    if response.status_code == 200:
        datos=response.text

        datos_json = json.loads(datos)
        argumentos={}

        for objeto in datos_json:
            #Si la uri esta vacia, imprime en pantalla
            if objeto["uriSiguiente"] is None:
                if "input" in objeto and objeto["input"] is False:
                    print(objeto["texto"])
                else:
                    argumentos[ objeto["nombreDato"]]=input(objeto["texto"])    
            else:
                #Dependiendo del metodo del siguiente uri usa funcion
                if (objeto["uriSiguiente"]["metodo"] == "POST"):
                    metodoPost(objeto["uriSiguiente"]["nombre"],argumentos )   
    else:
        print("Error en servidor")         

def metodoPost(uri,argumentos):
    #solicitud POST    
    response = requests.post(urlBase+uri,json=argumentos)
    datos=response.text
    datos_json = json.loads(datos)
    if not 'metodo' in datos_json:
        for objeto in datos_json:
            #Si El tipo de dato es JSON o texto segun eso imprime en pantalla
            if   objeto["tipoDato"] is not None:
                if objeto["tipoDato"] == "JSON":
                    json_con_formato = json.dumps(objeto["jsn"], indent=4)
                    print(json_con_formato)
            else:
                #Si no tiene Uri siguiente imprime en pantalla
                if objeto["uriSiguiente"] is None:
                    if "input" in objeto and objeto["input"] is False:
                        print(objeto["texto"])
                    else:
                        argumentos[objeto["nombreDato"]]=input(objeto["texto"])   
                else:
                    #Dependiendo del metodo del siguiente uri usa funcion
                    if (objeto["uriSiguiente"]["metodo"] == "POST"):
                        metodoPost(objeto["uriSiguiente"]["nombre"],argumentos )  
                    elif (objeto["uriSiguiente"]["metodo"] == "GET"):
                        if not argumentos:
                            metodoGet(objeto["uriSiguiente"]["nombre"])
                        else:    
                            metodoGet(objeto["uriSiguiente"]["nombre"]+list(argumentos.values())[0])
    elif datos_json['metodo'] == 'GET':
        metodoGet(datos_json['uriSiguiente'])
        

def metodoGet(uri):
    #solicitud GET
    response = requests.get(urlBase+uri)

    if response.status_code == 200:
        datos=response.text
        datos_json = json.loads(datos)
        argumentos={}

        for objeto in datos_json:
            #Si El tipo de dato es JSON o texto segun eso imprime en pantalla
            if   objeto["tipoDato"] is not None:
                if objeto["tipoDato"] == "JSON":
                    json_con_formato = json.dumps(objeto["jsn"], indent=4)
                    print(json_con_formato)
            else:
                #Si no tiene Uri siguiente imprime en pantalla
                if objeto["uriSiguiente"] is None:
                    if "input" in objeto and objeto["input"] is False:
                        print(objeto["texto"])
                    else:
                        argumentos[objeto["nombreDato"]]=input(objeto["texto"])   
                else:
                    #Dependiendo del metodo del siguiente uri usa funcion
                    if (objeto["uriSiguiente"]["metodo"] == "POST"):
                        metodoPost(objeto["uriSiguiente"]["nombre"],argumentos )  
                    elif (objeto["uriSiguiente"]["metodo"] == "GET"):
                        if not argumentos:
                            metodoGet(objeto["uriSiguiente"]["nombre"])
                        else:    
                            metodoGet(objeto["uriSiguiente"]["nombre"]+list(argumentos.values())[0])   
                        
    else:
        print("Error en servidor")

     
if __name__ == '__main__':

    iniciar()