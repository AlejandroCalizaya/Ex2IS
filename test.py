from datetime import datetime

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
        return f"Realizado en {fecha}"

BD.append(Cuenta("21345", "Arnaldo", 200, ["123", "456"]))
BD.append(Cuenta("123", "Luisa", 400, ["456"]))
BD.append(Cuenta("456", "Andrea", 300, ["21345"]))
BD.append(Cuenta("1983", "Alejandro", 50, []))

def test_pagar():
    assert BD[0].pagar("123", "01/01/2021", 50) == "Realizado en 01/01/2021"
    assert BD[0].saldo == 150
    assert BD[1].saldo == 450
    assert BD[0].operaciones[0].numerodestino == "123"
    assert BD[1].operaciones[0].numerodestino == "21345"
    assert BD[0].operaciones[0].valor == 50
    assert BD[1].operaciones[0].valor == 50
    print("Test_Pagar exitoso")

def test_pagar_no_contacto():
    assert BD[0].pagar("1983", "01/01/2021", 50) == "No se encontró el contacto"
    assert BD[0].saldo == 200
    assert BD[3].saldo == 50
    assert BD[0].operaciones == []
    assert BD[3].operaciones == []
    print("Test_Pagar_No_Contacto exitoso")

def test_pagar_sin_saldo():
    assert BD[0].pagar("123", "01/01/2021", 250) == "No tiene suficiente saldo"
    assert BD[0].saldo == 200
    assert BD[1].saldo == 400
    assert BD[0].operaciones == []
    assert BD[1].operaciones == []
    print("Test_Pagar_Sin_Saldo exitoso")

def test_sin_historial():
    BD[2].pagar("21345", "01/01/2021", 500)
    assert BD[2].historial() == []
    assert BD[0].historial() == []
    print("Test_Sin_Historial exitoso")

test_pagar()
# test_pagar_no_contacto()
# test_pagar_sin_saldo()
# test_sin_historial()