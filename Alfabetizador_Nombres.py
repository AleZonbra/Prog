def alfabetizador_nombres(nombres):
    return sorted(nombres, key=lambda nombre: nombre.lower())
# Ejemplo de uso
if __name__ == "__main__":
    import sys
# Solicitar al usuario que ingrese los nombres separados por comas
    entrada = input("Introduce los nombres separados por comas (ej: María, Juan, Ana): ").strip()
    if not entrada:
        print("No se ingresaron nombres. Ejecuta el programa e ingresa al menos un nombre.")
        sys.exit(1)
# Crear una lista de nombres a partir de la entrada del usuario, eliminando espacios adicionales
    lista = [n.strip() for n in entrada.split(",") if n.strip()]
# Ordenar los nombres alfabéticamente e imprimirlos
    nombres_ordenados = alfabetizador_nombres(lista)
    for nombre in nombres_ordenados:
        print(nombre)