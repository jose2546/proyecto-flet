import flet as ft
from datetime import datetime

def main(page: ft.Page):
    # --- CONFIGURACIÓN DE LA PÁGINA ---
    page.title = "SUREBET ANALYTICS PRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0E14"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 30

    # Variables globales de control dentro de la app
    datos_operacion_actual = {"valido": False, "partido": "", "inv": "", "pct": "", "neto": ""}

    # --- ELEMENTOS VISUALES / ENTRADAS ---
    txt_partido = ft.TextField(
        label="NOMBRE DEL ENFRENTAMIENTO / PARTIDO",
        placeholder_text="Ej: Real Madrid vs Barcelona",
        width=400,
        border_color="#2A2F3D",
        focused_border_color="#00E676"
    )

    txt_presupuesto = ft.TextField(
        label="CAPITAL TOTAL INVERSIÓN ($ COP)",
        value="100000",
        width=200,
        text_align=ft.TextAlign.RIGHT,
        border_color="#2A2F3D",
        focused_border_color="#00E676",
        text_style=ft.TextStyle(color="#00E676", weight=ft.FontWeight.BOLD)
    )

    # Inputs para la cuadrícula de cuotas
    txt_l = ft.TextField(value="2.10", width=100, text_align=ft.TextAlign.CENTER, border_color="#2A2F3D")
    txt_cl = ft.TextField(value="BetPlay", width=150, border_color="#2A2F3D")

    txt_e = ft.TextField(value="3.40", width=100, text_align=ft.TextAlign.CENTER, border_color="#2A2F3D")
    txt_ce = ft.TextField(value="BetPlay", width=150, border_color="#2A2F3D")
    lbl_e_text = ft.Text("🔸 Cuota Empate (X):", width=180)

    txt_v = ft.TextField(value="2.50", width=100, text_align=ft.TextAlign.CENTER, border_color="#2A2F3D")
    txt_cv = ft.TextField(value="BetPlay", width=150, border_color="#2A2F3D")

    # Fila dinámica del empate
    row_empate = ft.Row([lbl_e_text, txt_e, txt_ce], alignment=ft.MainAxisAlignment.START)

    # --- COMPONENTES DEL PANEL DE REPORTES ---
    lbl_st = ft.Text("SISTEMA LISTO: INGRESE LOS VALORES", font_family="Segoe UI", size=13, weight=ft.FontWeight.BOLD, color="#64748B")
    lbl_op1 = ft.Text("", font_family="Segoe UI", size=13, color="#E1E1E6", weight=ft.FontWeight.BOLD)
    lbl_opX = ft.Text("", font_family="Segoe UI", size=13, color="#E1E1E6", weight=ft.FontWeight.BOLD)
    lbl_op2 = ft.Text("", font_family="Segoe UI", size=13, color="#E1E1E6", weight=ft.FontWeight.BOLD)

    # Contenedor del Reporte (Equivalente al CTkFrame de reportes)
    panel_reporte = ft.Container(
        content=ft.Column([
            lbl_st,
            lbl_op1,
            lbl_opX,
            lbl_op2,
        ], spacing=5),
        bgcolor="#151922",
        padding=20,
        border_radius=8,
        border=ft.border.all(1, "#2A2F3D")
    )

    # Cuadro de Bitácora Histórica (Equivalente al CTkTextbox)
    txt_log = ft.TextField(
        multiline=True,
        read_only=True,
        min_lines=8,
        max_lines=12,
        text_style=ft.TextStyle(font_family="Consolas", size=12, color="#E1E1E6"),
        bgcolor="#151922",
        border_color="#2A2F3D"
    )
    
    # Inicializar cabecera de la bitácora
    txt_log.value = f"{'FECHA/HORA':<15} | {'ENFRENTAMIENTO':<25} | {'INVERSIÓN':<12} | {'RETORNO %':<10} | {'GANANCIA NETO'}\n" + "-" * 85 + "\n"

    # --- FUNCIONES DE LÓGICA ---
    def conmutar(e):
        row_empate.visible = sw.value
        if not sw.value:
            lbl_opX.value = ""
        page.update()

    def calcular(e):
        try:
            pres = float(txt_presupuesto.value)
            c_l = float(txt_l.value)
            c_v = float(txt_v.value)
            usa_e = sw.value
            c_e = float(txt_e.value) if usa_e else None

            nombre_partido = txt_partido.value.strip() if txt_partido.value.strip() else "Partido General"

            if pres <= 0 or c_l <= 1 or c_v <= 1 or (usa_e and c_e <= 1):
                raise ValueError

            ind = (1 / c_l) + (1 / c_e if usa_e else 0) + (1 / c_v)
            rent = (1 - ind) * 100
            neto = (pres / ind) - pres

            es_surebet = ind < 1.0
            col = "#00E676" if es_surebet else "#FF5252"

            txt_st = f"🔥 ARBITRAJE DETECTADO (+{round(rent,2)}%) | Retorno Neto: +${round(neto,2):,} COP" if es_surebet else f"❌ MERCADO CON PÉRDIDA ({round(rent,2)}%) | Retorno Neto: ${round(neto,2):,} COP"
            
            panel_reporte.border = ft.border.all(1, col)
            lbl_st.value = txt_st
            lbl_st.color = col

            casa_l = txt_cl.value.strip()
            casa_v = txt_cv.value.strip()
            casa_e = txt_ce.value.strip() if usa_e else ""

            lbl_op1.value = f"👉 Local (1)   : ${round(pres/(ind*c_l),2):,} COP en {casa_l}"
            if usa_e:
                lbl_opX.value = f"👉 Empate (X)  : ${round(pres/(ind*c_e),2):,} COP en {casa_e}"
            else:
                lbl_opX.value = ""
            lbl_op2.value = f"👉 Visitante (2): ${round(pres/(ind*c_v),2):,} COP en {casa_v}"

            btn_guardar.disabled = False
            btn_guardar.bgcolor = col
            btn_guardar.color = "#0B0E14" if es_surebet else "#FFFFFF"

            # Guardar en memoria temporal
            datos_operacion_actual["valido"] = True
            datos_operacion_actual["partido"] = nombre_partido[:23]
            datos_operacion_actual["inv"] = f"${int(pres):,}"
            datos_operacion_actual["pct"] = f"+{round(rent,2)}%" if es_surebet else f"{round(rent,2)}%"
            datos_operacion_actual["neto"] = f"+${round(neto,2):,}" if es_surebet else f"${round(neto,2):,}"

        except ValueError:
            lbl_st.value = "⚠️ ERROR: VERIFIQUE QUE LAS CUOTAS SEAN MAYORES A 1 Y EL CAPITAL VÁLIDO"
            lbl_st.color = "#FF5252"
            panel_reporte.border = ft.border.all(1, "#FF5252")
            btn_guardar.disabled = True
            btn_guardar.bgcolor = "#2A2F3D"
            btn_guardar.color = "#64748B"
        
        page.update()

    def registrar_log(e):
        if datos_operacion_actual["valido"]:
            ahora = datetime.now().strftime("%d/%m %H:%M")
            nueva_linea = f"{ahora:<15} | {datos_operacion_actual['partido']:<25} | {datos_operacion_actual['inv']:<12} | {datos_operacion_actual['pct']:<10} | {datos_operacion_actual['neto']}\n"
            txt_log.value += nueva_linea
            btn_guardar.disabled = True
            btn_guardar.bgcolor = "#2A2F3D"
            btn_guardar.color = "#64748B"
            page.update()

    # Botones de Acción
    btn_evaluar = ft.ElevatedButton(
        text="⚡ EVALUAR MATRIZ DE APUESTAS",
        style=ft.ButtonStyle(
            bgcolor="#00E676", color="#0B0E14",
            shape=ft.RoundedRectangleBorder(radius=8),
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=13)
        ),
        height=45,
        on_click=calcular
    )

    btn_guardar = ft.ElevatedButton(
        text="📥 REGISTRAR OPERACIÓN EN BITÁCORA",
        disabled=True,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
        height=35,
        on_click=registrar_log
    )

    sw = ft.Switch(
        label="Incluir mercado de Empate (Estrategia 1X2)",
        value=True,
        active_color="#00E676",
        on_change=conmutar
    )

    # --- DISEÑO Y ESTRUCTURA DE LA INTERFAZ ---
    page.add(
        ft.Column([
            ft.Text("SUREBET ANALYTICS PRO", size=24, weight=ft.FontWeight.BOLD, color="#00E676"),
            ft.Text("Consola profesional de cobertura de riesgo y registro de operaciones web", size=12, color="#64748B"),
            ft.Divider(height=10, color="transparent"),
            
            # Form de partido
            ft.Container(
                content=ft.Row([ft.Text("🔹 Partido:", width=100), txt_partido], alignment=ft.MainAxisAlignment.START),
                bgcolor="#151922", padding=12, border_radius=8
            ),
            # Form de Inversión
            ft.Container(
                content=ft.Row([ft.Text("💰 Inversión:", width=100), txt_presupuesto], alignment=ft.MainAxisAlignment.START),
                bgcolor="#151922", padding=12, border_radius=8
            ),
            
            sw,
            
            # Form Matriz de Cuotas
            ft.Container(
                content=ft.Column([
                    ft.Row([ft.Text("🔹 Cuota Gana Local (1):", width=180), txt_l, txt_cl]),
                    row_empate,
                    ft.Row([ft.Text("🔹 Cuota Visitante (2):", width=180), txt_v, txt_cv]),
                ], spacing=10),
                bgcolor="#151922", padding=15, border_radius=8
            ),
            
            ft.Row([btn_evaluar], alignment=ft.MainAxisAlignment.CENTER),
            
            panel_reporte,
            ft.Row([btn_guardar], alignment=ft.MainAxisAlignment.END),
            
            ft.Text("📋 BITÁCORA HISTÓRICA DE OPERACIONES", size=12, color="#64748B", weight=ft.FontWeight.BOLD),
            txt_log
        ], spacing=15)
    )

# Configuración final para Render (Ejecución puramente web)
if __name__ == "__main__":
    ft.app(target=main, view=None, port=8080)
