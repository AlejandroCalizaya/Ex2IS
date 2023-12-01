import flask
from datetime import datetime

app = flask.Flask(__name__)

BD = list()

class Operacion:
    def __init__(self, numerodestino: str, fecha: str, valor: int):
        self.numerodestino = numerodestino
        self.fecha = fecha
        self.valor = valor

class Cuenta:
    def __init__(self, numero: str, nombre:str, saldo: int, contactos: str):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = list()
    
    def historial(self):
        return self.operaciones
    
    def pagar(self, numerodestino: str, fecha: str, valor: int):
        if numerodestino not in self.contactos:
            return "No se encontró el contacto"
        
        if valor > self.saldo:
            return "No tiene suficiente saldo"

        self.operaciones.append(Operacion(numerodestino, fecha, valor))
        self.saldo -= valor
        for cuenta in BD:
            if cuenta.numero == numerodestino:
                cuenta.saldo += valor
                cuenta.operaciones.append(Operacion(self.numero, fecha, valor))
        date = datetime.now()
        fecha = date.strftime("%d/%m/%Y")
        return f"Realizado en {fecha}"

BD.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
BD.append(Cuenta("123", "Luisa", 400, ["456"]))
BD.append(Cuenta("456", "Andrea", 300, ["21345"]))

@app.route('/')
def index():
    return "Bienvenido a la aplicación de transferencias"

@app.route('/billetera/contactos')
def contactos():
    minumero = flask.request.args.get('minumero')
    nombres = dict()
    for cuenta in BD:
        nombres[cuenta.numero] = cuenta.nombre

    for cuenta in BD:
        if cuenta.numero == minumero:
            stringReturn = ""
            contactos = cuenta.contactos

            if contactos == []:
                return "No tiene contactos"

            for c in contactos:
                stringReturn += f"{c}: {nombres[c]}\n"
            
            return stringReturn
    return "No se encontró la cuenta"

@app.route('/billetera/pagar')
def pagar():
    minumero = flask.request.args.get('minumero')
    numerodestino = flask.request.args.get('numerodestino')
    valor = flask.request.args.get('valor')
    valor = int(valor)
    for cuenta in BD:
        if cuenta.numero == minumero:
            date = datetime.now()
            fecha = date.strftime("%d/%m/%Y")
            return cuenta.pagar(numerodestino, fecha, valor)
    return "No se encontró la cuenta"

@app.route('/billetera/historial')
def historial():
    minumero = flask.request.args.get('minumero')
    nombres = dict()
    for cuenta in BD:
        nombres[cuenta.numero] = cuenta.nombre

    for cuenta in BD:
        if cuenta.numero == minumero:
            stringReturn = f"Saldo de {cuenta.nombre}: {cuenta.saldo}\nOperaciones de {cuenta.nombre}\n"
            for operacion in cuenta.historial():
                if operacion.numerodestino == cuenta.numero:
                    nombredestino = nombres[operacion.numerodestino]
                    stringReturn += f"Pago recibido de {operacion.valor} de {nombredestino}\n"
                else:
                    nombredestino = nombres[operacion.numerodestino]
                    stringReturn += f"Pago enviado de {operacion.valor} a {nombredestino}\n"
            return stringReturn
    return "No se encontró la cuenta"

app.run()