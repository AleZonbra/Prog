def alfabetizador_nombres(nombres):
    return sorted(nombres, key=lambda nombre: nombre.lower())

if __name__ == "__main__":
    import sys

    entrada = input("Introduce los nombres separados por comas (ej: María, Juan, Ana): ").strip()
    if not entrada:
        print("No se ingresaron nombres. Ejecuta el programa e ingresa al menos un nombre.")
        sys.exit(1)

    lista = [n.strip() for n in entrada.split(",") if n.strip()]

    nombres_ordenados = alfabetizador_nombres(lista)
    for nombre in nombres_ordenados:
        print(nombre)