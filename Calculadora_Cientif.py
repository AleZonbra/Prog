import math
# Calculadora Científica en Python
def scientific_calculator():
    print("Calculadora Científica")
    print("Operaciones disponibles: +, -, *, /, %, sqrt, pow, sin, cos, tan")
# Bucle principal de la calculadora  
    while True:
        op = input("Ingrese operación (o 'salir' para terminar): ")
        if op == 'salir':
            break
# Verificar la operación y solicitar los números necesarios para realizar el cálculo       
        if op in ['+', '-', '*', '/', '%', 'pow']:
            a = float(input("Primer número: "))
            b = float(input("Segundo número: "))
            if op == '+':
                print("Resultado:", a + b)
            elif op == '-':
                print("Resultado:", a - b)
            elif op == '*':
                print("Resultado:", a * b)
            elif op == '/':
                print("Resultado:", a / b)
            elif op == '%':
                print("Resultado:", (a * b) / 100)
            elif op == 'pow':
                print("Resultado:", math.pow(a, b))
# Para operaciones de raíz cuadrada y funciones trigonométricas, solo se necesita un número
        elif op in ['sqrt', 'sin', 'cos', 'tan']:
            a = float(input("Número: "))
            if op == 'sqrt':
                print("Resultado:", math.sqrt(a))
            elif op == 'sin':
                print("Resultado:", math.sin(math.radians(a)))
            elif op == 'cos':
                print("Resultado:", math.cos(math.radians(a)))
            elif op == 'tan':
                print("Resultado:", math.tan(math.radians(a)))
        else:
            print("Operación no válida.")
# Ejecutar la calculadora científica
if __name__ == "__main__":
    scientific_calculator()