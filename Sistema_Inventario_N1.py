import datetime

class Producto:
    def __init__(self, id, nombre, marca, lote, fecha_vencimiento, precio_paquete, fecha_ingreso):
        self.id = id
        self.nombre = nombre
        self.marca = marca
        self.lote = lote
        self.fecha_vencimiento = fecha_vencimiento
        self.precio_paquete = precio_paquete
        self.fecha_ingreso = fecha_ingreso

class InventarioFIFO:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.productos.sort(key=lambda x: x.fecha_ingreso)  # Ordena por fecha de ingreso

    def retirar_producto(self, cantidad):
        retirados = []
        while cantidad > 0 and self.productos:
            retirados.append(self.productos.pop(0))
            cantidad -= 1
        return retirados

    def mostrar_inventario(self):
        for p in self.productos:
            print(f"ID: {p.id}, Producto: {p.nombre}, Marca: {p.marca}, Lote: {p.lote}, "
                  f"Vencimiento: {p.fecha_vencimiento}, Precio: {p.precio_paquete}, "
                  f"Ingreso: {p.fecha_ingreso}")
def pedir_producto():
    while True:
        try:
            id_val = int(input("ID (número entero): "))
            break
        except ValueError:
            print("ID inválido. Intente nuevamente.")

    nombre = input("Nombre: ").strip()
    marca = input("Marca: ").strip()
    lote = input("Lote: ").strip()

    while True:
        fecha_v = input("Fecha de vencimiento (AAAA-MM-DD): ").strip()
        try:
            datetime.datetime.strptime(fecha_v, "%Y-%m-%d")
            break
        except Exception:
            print("Formato de fecha inválido. Use AAAA-MM-DD.")

    while True:
        precio_s = input("Precio por paquete (ej: 12.50): ").strip()
        try:
            precio = float(precio_s)
            break
        except ValueError:
            print("Precio inválido. Ingrese un número.")

    fecha_ing = input("Fecha de ingreso (AAAA-MM-DD) [enter = hoy]: ").strip()
    if not fecha_ing:
        fecha_ing = datetime.date.today().isoformat()
    else:
        try:
            datetime.datetime.strptime(fecha_ing, "%Y-%m-%d")
        except Exception:
            print("Formato inválido para fecha de ingreso; se usará la fecha de hoy.")
            fecha_ing = datetime.date.today().isoformat()

    return Producto(id_val, nombre, marca, lote, fecha_v, precio, fecha_ing)


if __name__ == '__main__':
    inventario = InventarioFIFO()
    while True:
        print("\n--- Menú Inventario ---")
        print("1) Agregar producto")
        print("2) Mostrar inventario")
        print("3) Retirar N productos (FIFO)")
        print("4) Salir")
        opcion = input("Elija una opción: ").strip()

        if opcion == '1':
            p = pedir_producto()
            inventario.agregar_producto(p)
            print("Producto agregado correctamente.")
        elif opcion == '2':
            print("\nInventario actual:")
            inventario.mostrar_inventario()
        elif opcion == '3':
            try:
                n = int(input("Cantidad a retirar: "))
            except ValueError:
                print("Cantidad inválida.")
                continue
            retirados = inventario.retirar_producto(n)
            if retirados:
                for r in retirados:
                    print(f"Retirado: {r.nombre} (ID: {r.id})")
            else:
                print("No hay productos para retirar.")
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")