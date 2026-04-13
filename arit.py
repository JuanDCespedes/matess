from abc import ABC, abstractmethod



class Expresion(ABC):
    @abstractmethod
    def evaluar(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Numero(Expresion):
    def __init__(self, valor):
        self.valor = float(valor)

    def evaluar(self):
        return self.valor

    def __str__(self):
        return str(self.valor)


class Operacion(Expresion):
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha


class Suma(Operacion):
    def evaluar(self):
        return self.izquierda.evaluar() + self.derecha.evaluar()

    def __str__(self):
        return f"({self.izquierda} + {self.derecha})"


class Resta(Operacion):
    def evaluar(self):
        return self.izquierda.evaluar() - self.derecha.evaluar()

    def __str__(self):
        return f"({self.izquierda} - {self.derecha})"


class Multiplicacion(Operacion):
    def evaluar(self):
        return self.izquierda.evaluar() * self.derecha.evaluar()

    def __str__(self):
        return f"({self.izquierda} * {self.derecha})"


class Division(Operacion):
    def evaluar(self):
        if self.derecha.evaluar() == 0:
            raise ValueError("División por cero")
        return self.izquierda.evaluar() / self.derecha.evaluar()

    def __str__(self):
        return f"({self.izquierda} / {self.derecha})"




def prioridad(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0



def infijo_a_postfijo(expresion):
    pila = []
    salida = []
    tokens = expresion.split()

    for token in tokens:
        if token.replace('.', '', 1).isdigit():
            salida.append(token)
        elif token == '(':
            pila.append(token)
        elif token == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()
        else:
            while (pila and prioridad(pila[-1]) >= prioridad(token)):
                salida.append(pila.pop())
            pila.append(token)

    while pila:
        salida.append(pila.pop())

    return salida



def construir_arbol(postfijo):
    pila = []

    for token in postfijo:
        if token.replace('.', '', 1).isdigit():
            pila.append(Numero(token))
        else:
            der = pila.pop()
            izq = pila.pop()

            if token == '+':
                nodo = Suma(izq, der)
            elif token == '-':
                nodo = Resta(izq, der)
            elif token == '*':
                nodo = Multiplicacion(izq, der)
            elif token == '/':
                nodo = Division(izq, der)

            pila.append(nodo)

    return pila[0]




if __name__ == "__main__":
    print("Escribe la expresion con espacios:")
    print("Ejemplo: ( 5 + 3 ) * ( 10 - 2 )")
    
    entrada = input(">> ")

    postfijo = infijo_a_postfijo(entrada)
    arbol = construir_arbol(postfijo)

    print("Expresion:", arbol)
    print("Resultado:", arbol.evaluar())