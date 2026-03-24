import datetime
import flet as ft

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
        self.productos.sort(key=lambda x: x.fecha_ingreso)

    def retirar_producto(self, id):
        for i, p in enumerate(self.productos):
            if p.id == id:
                return self.productos.pop(i)
        return None

    def mostrar_inventario(self):
        if not self.productos:
            return "Inventario vacío."
        result = ""
        for p in self.productos:
            result += f"ID: {p.id}, Producto: {p.nombre}, Marca: {p.marca}, Lote: {p.lote}, "
            result += f"Vencimiento: {p.fecha_vencimiento}, Precio: {p.precio_paquete}, "
            result += f"Ingreso: {p.fecha_ingreso}\n"
        return result


def main(page: ft.Page):
    page.title = "Sistema de Inventario FIFO (Flet)"
    page.window_width = 1400
    page.window_height = 1000
    page.window_resizable = True
    page.window_top = 30
    page.window_left = 30
    page.scroll = ft.ScrollMode.AUTO

    inventario = InventarioFIFO()
    is_logged_in = False

    # Campos de login
    txt_usuario = ft.TextField(label="Usuario", width=300, on_submit=lambda e: login(e))
    txt_contrasena = ft.TextField(label="Contraseña", password=True, width=300, on_submit=lambda e: login(e))
    lbl_error = ft.Text("", color=ft.Colors.RED)

    def build_login():
        return ft.Container(
            content=ft.Column([
                ft.Text("Inicio de Sesión", size=40, weight="bold"),
                txt_usuario,
                txt_contrasena,
                ft.ElevatedButton("Iniciar Sesión", on_click=login),
                lbl_error,
            ], alignment="center", horizontal_alignment="center", spacing=20),
            alignment=ft.Alignment.CENTER,
            padding=50,
        )

    def login(e):
        nonlocal is_logged_in, dark_mode
        if txt_usuario.value == "admin" and txt_contrasena.value == "1234":
            is_logged_in = True
            dark_mode = False
            set_theme()
            lbl_error.value = ""
            page.controls.clear()
            page.add(build_main())
            page.update()
        else:
            lbl_error.value = "Usuario o contraseña incorrectos."
            page.update()

    # Aquí va el resto del código de la interfaz principal, pero movido a build_main

    dark_mode = False

    def set_theme():
        if dark_mode:
            page.theme_mode = ft.ThemeMode.DARK
            page.theme = ft.Theme(
                color_scheme_seed="#1e1e1e",
                use_material3=True,
                text_theme=ft.TextTheme(body_large=ft.TextStyle(color="#ffffff")),
                icon_theme=ft.IconTheme(color="#ffffff"),
            )
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.theme = ft.Theme(
                color_scheme_seed="#1976d2",
                use_material3=True,
                text_theme=ft.TextTheme(body_large=ft.TextStyle(color="#000000")),
                icon_theme=ft.IconTheme(color="#000000"),
            )
        page.bgcolor = None  # Let theme handle it

    def get_inventario_color():
        return "#2a2a2a" if dark_mode else "#f1f5f9"

    def get_log_color():
        return "#1f1f1f" if dark_mode else "#ffffff"


    def togglear_modo(e):
        nonlocal dark_mode
        dark_mode = not dark_mode
        if dark_mode:
            btn_modo_dark.text = "Modo Claro"
        else:
            btn_modo_dark.text = "Modo Oscuro"
        set_theme()
        page.update()

    def recargar_inventario():
        color_text = "#ffffff" if dark_mode else "#000000"
        dt_inventario.rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(p.id), color=color_text)),
                ft.DataCell(ft.Text(p.nombre, color=color_text)),
                ft.DataCell(ft.Text(p.marca, color=color_text)),
                ft.DataCell(ft.Text(p.lote, color=color_text)),
                ft.DataCell(ft.Text(p.fecha_vencimiento, color=color_text)),
                ft.DataCell(ft.Text(str(p.precio_paquete), color=color_text)),
                ft.DataCell(ft.Text(p.fecha_ingreso, color=color_text)),
            ])
            for p in inventario.productos
        ]
        page.update()

    def agregar_producto(e):
        try:
            id_val = int(txt_id.value)
        except Exception:
            grabar_log("ERROR: ID inválido (entero requerido).")
            return
        nombre = txt_nombre.value.strip()
        marca = txt_marca.value.strip()
        lote = txt_lote.value.strip()

        try:
            fecha_v = f"{int(txt_vto_a.value):04d}-{int(txt_vto_m.value):02d}-{int(txt_vto_d.value):02d}"
            datetime.datetime.strptime(fecha_v, "%Y-%m-%d")
        except Exception:
            grabar_log("ERROR: Fecha de vencimiento inválida (DD/MM/AAAA).")
            return

        try:
            precio = float(txt_precio.value.strip())
        except Exception:
            grabar_log("ERROR: Precio inválido.")
            return

        try:
            fecha_ing = f"{int(txt_ing_a.value):04d}-{int(txt_ing_m.value):02d}-{int(txt_ing_d.value):02d}"
            datetime.datetime.strptime(fecha_ing, "%Y-%m-%d")
        except Exception:
            grabar_log("ADVERTENCIA: Fecha de ingreso inválida, se usa hoy.")
            fecha_ing = datetime.date.today().isoformat()

        producto = Producto(id_val, nombre, marca, lote, fecha_v, precio, fecha_ing)
        inventario.agregar_producto(producto)
        grabar_log(f"Producto agregado: {nombre} (ID {id_val})")
        recargar_inventario()

        txt_id.value = ""
        txt_nombre.value = ""
        txt_marca.value = ""
        txt_lote.value = ""
        txt_vto_d.value = ""
        txt_vto_m.value = ""
        txt_vto_a.value = ""
        txt_precio.value = ""
        txt_ing_d.value = ""
        txt_ing_m.value = ""
        txt_ing_a.value = ""
        page.update()

    def retirar_por_id(e):
        try:
            id_val = int(txt_retirar_id.value)
        except Exception:
            grabar_log("ERROR: ID inválido.")
            return
        removed = inventario.retirar_producto(id_val)
        if removed:
            grabar_log(f"Retirado: {removed.nombre} (ID {removed.id})")
            recargar_inventario()
        else:
            grabar_log("Producto con esa ID no encontrado.")
        txt_retirar_id.value = ""
        page.update()

    def buscar_producto(e):
        term = txt_buscar.value.strip()
        if not term:
            grabar_log("Ingrese un término de búsqueda.")
            return
        found = []
        for p in inventario.productos:
            if str(p.id) == term or term.lower() in p.nombre.lower():
                found.append(p)
        if found:
            for p in found:
                grabar_log(f"Encontrado: ID {p.id}, {p.nombre}, Marca {p.marca}, Lote {p.lote}, Venc: {p.fecha_vencimiento}")
        else:
            grabar_log("Producto no encontrado.")
        txt_buscar.value = ""
        page.update()

    # Campos de la interfaz principal
    txt_id = ft.TextField(label="ID", width=200)
    txt_nombre = ft.TextField(label="Nombre", width=200)
    txt_marca = ft.TextField(label="Marca", width=200)
    txt_lote = ft.TextField(label="Lote", width=200)
    txt_vto_d = ft.TextField(label="Venc. Día", width=80)
    txt_vto_m = ft.TextField(label="Venc. Mes", width=80)
    txt_vto_a = ft.TextField(label="Venc. Año", width=100)

    txt_precio = ft.TextField(label="Costo de lote", width=200)

    txt_ing_d = ft.TextField(label="Ingreso Día", width=80)
    txt_ing_m = ft.TextField(label="Ingreso Mes", width=80)
    txt_ing_a = ft.TextField(label="Ingreso Año", width=100)

    txt_retirar_id = ft.TextField(label="ID a retirar", width=200)

    txt_buscar = ft.TextField(label="Buscar por ID o Nombre", width=200)

    # Log removido de la UI (no se muestra)
    log = None

    dt_inventario = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color="#ffffff" if dark_mode else "#000000")),
            ft.DataColumn(ft.Text("Nombre", color="#ffffff" if dark_mode else "#000000")),
            ft.DataColumn(ft.Text("Marca", color="#ffffff" if dark_mode else "#000000")),
            ft.DataColumn(ft.Text("Lote", color="#ffffff" if dark_mode else "#000000")),
            ft.DataColumn(ft.Text("Vencimiento", color="#ffffff" if dark_mode else "#000000")),
            ft.DataColumn(ft.Text("Costo lote", color="#ffffff" if dark_mode else "#000000")),
            ft.DataColumn(ft.Text("Ingreso", color="#ffffff" if dark_mode else "#000000")),
        ],
        rows=[],
        width=1100,
        border=ft.border.all(1, "#999" if not dark_mode else "#444"),
        heading_row_color="#2b2b2b" if dark_mode else "#e0e7ff",
        data_row_color="#333333" if dark_mode else "#ffffff",
    )

    table_section = ft.Container(
        content=dt_inventario,
        padding=12,
        width=1100,
        height=300,
        border=ft.border.all(1, "#999" if not dark_mode else "#444"),
        bgcolor=get_inventario_color(),
        visible=False,
    )

    def grabar_log(mensaje):
        # Log en UI deshabilitado.
        return

    btn_modo_dark = ft.ElevatedButton("Modo Oscuro", on_click=togglear_modo)

    txt_id.on_submit = lambda e: agregar_producto(e)
    txt_nombre.on_submit = lambda e: agregar_producto(e)
    txt_marca.on_submit = lambda e: agregar_producto(e)
    txt_lote.on_submit = lambda e: agregar_producto(e)
    txt_vto_a.on_submit = lambda e: agregar_producto(e)
    txt_vto_m.on_submit = lambda e: agregar_producto(e)
    txt_vto_d.on_submit = lambda e: agregar_producto(e)
    txt_precio.on_submit = lambda e: agregar_producto(e)
    txt_ing_a.on_submit = lambda e: agregar_producto(e)
    txt_ing_m.on_submit = lambda e: agregar_producto(e)
    txt_ing_d.on_submit = lambda e: agregar_producto(e)

    panel_agregar = ft.Column([
        txt_id,
        txt_nombre,
        txt_marca,
        txt_lote,
        ft.Row([txt_vto_d, txt_vto_m, txt_vto_a], spacing=8),
        txt_precio,
        ft.Row([txt_ing_d, txt_ing_m, txt_ing_a], spacing=8),
        ft.ElevatedButton("Agregar Producto", on_click=agregar_producto),
    ], spacing=12, alignment="start", horizontal_alignment="start")

    txt_buscar.on_submit = lambda e: buscar_producto(e)

    panel_buscar = ft.Column([
        txt_buscar,
        ft.ElevatedButton("Buscar Producto", on_click=buscar_producto),
    ], spacing=12, alignment="start", horizontal_alignment="start")

    txt_retirar_id.on_submit = lambda e: retirar_por_id(e)

    panel_eliminar = ft.Column([
        txt_retirar_id,
        ft.ElevatedButton("Retirar Producto", on_click=retirar_por_id),
    ], spacing=12, alignment="start", horizontal_alignment="start")

    panel_mostrar = ft.Column([
        ft.ElevatedButton("Mostrar Inventario", on_click=lambda e: recargar_inventario()),
    ], spacing=12, alignment="start", horizontal_alignment="start")

    panel_tabs = ft.Column([panel_agregar])
    tab_actual = "Agregar"

    def seleccionar_tab(nombre):
        nonlocal tab_actual
        tab_actual = nombre
        if nombre == "Agregar":
            panel_tabs.controls = [panel_agregar]
            table_section.visible = False
        elif nombre == "Buscar":
            panel_tabs.controls = [panel_buscar]
            table_section.visible = True
        elif nombre == "Eliminar":
            panel_tabs.controls = [panel_eliminar]
            table_section.visible = False
        elif nombre == "Mostrar":
            panel_tabs.controls = [panel_mostrar]
            table_section.visible = True
            recargar_inventario()
        page.update()

    def build_main():
        set_theme()
        page.padding = 20

        return ft.Container(
            width=1300,
            height=900,
            bgcolor="transparent",
            content=ft.Card(
                elevation=2,
                content=ft.Container(
                    width=1200,
                    height=850,
                    border_radius=ft.border_radius.all(12),
                    padding=ft.padding.all(24),
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Sistema de Inventario FIFO", size=40, weight="bold"),
                            ft.Row([
                                ft.ElevatedButton("Actualizar tabla", on_click=lambda e: recargar_inventario(), style=ft.ButtonStyle(bgcolor=ft.Colors.CYAN_400, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=ft.padding.symmetric(12, 8))),
                                btn_modo_dark,
                            ], spacing=10),
                        ], alignment="spaceBetween", vertical_alignment="center"),
                        ft.Row([
                            ft.Text("Navegación", size=18, weight="bold"),
                        ], alignment="start", spacing=12, vertical_alignment="center"),
                        ft.Row([
                            ft.ElevatedButton("Agregar", on_click=lambda e: seleccionar_tab("Agregar"), style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_300, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=ft.padding.symmetric(16, 10))),
                            ft.ElevatedButton("Buscar", on_click=lambda e: seleccionar_tab("Buscar"), style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_300, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=ft.padding.symmetric(16, 10))),
                            ft.ElevatedButton("Eliminar", on_click=lambda e: seleccionar_tab("Eliminar"), style=ft.ButtonStyle(bgcolor=ft.Colors.RED_300, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=ft.padding.symmetric(16, 10))),
                            ft.ElevatedButton("Mostrar", on_click=lambda e: seleccionar_tab("Mostrar"), style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_300, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=12), padding=ft.padding.symmetric(16, 10))),
                        ], alignment="center", spacing=12),
                        ft.Container(
                            ref=lambda c: None,
                            content=panel_tabs,
                            padding=ft.padding.all(0),
                            width=1100,
                        ),

                        table_section,
                    ], alignment="center", horizontal_alignment="center", tight=False, scroll=ft.ScrollMode.AUTO),
                ),
            ),
            alignment=ft.Alignment(0, 0),
        )

    # Inicialmente aplicar modo claro y mostrar login
    set_theme()
    page.add(build_login())


if __name__ == "__main__":
    ft.app(target=main)
