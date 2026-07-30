import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "SUREBET ANALYTICS PRO"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.scroll = ft.ScrollMode.AUTO

    # Campos de Entrada de Parámetros
    txt_partido = ft.TextField(label="Enfrentamiento / Partido", hint_text="Ej: Real Madrid vs Barcelona", border_color="#2A2F3D")
    txt_presupuesto = ft.TextField(label="Capital Total Inversión ($ COP)", value="100000", text_align=ft.TextAlign.RIGHT, border_color="#2A2F3D", text_style=ft.TextStyle(color="#00E676", weight=ft.FontWeight.BOLD))

    # Entradas de Cuotas y Operadores
    txt_l = ft.TextField(label="Cuota Local (1)", width=110, text_align=ft.TextAlign.CENTER)
    txt_cl = ft.TextField(label="Casa", value="BetPlay", width=120, text_align=ft.TextAlign.CENTER)
    
    txt_e = ft.TextField(label="Cuota Empate (X)", width=110, text_align=ft.TextAlign.CENTER)
    txt_ce = ft.TextField(label="Casa", value="BetPlay", width=120, text_align=ft.TextAlign.CENTER)
    
    txt_v = ft.TextField(label="Cuota Visita (2)", width=110, text_align=ft.TextAlign.CENTER)
    txt_cv = ft.TextField(label="Casa", value="Wplay", width=120, text_align=ft.TextAlign.CENTER)

    # Componentes de Reportes
    lbl_st = ft.Text("SISTEMA LISTO: PARAMETRIZAR MATRIZ", font_family="Segoe UI", size=13, weight=ft.FontWeight.BOLD, color="#64748B")
    lbl_op1 = ft.Text("", size=12)
    lbl_opX = ft.Text("", size=12)
    lbl_op2 = ft.Text("", size=12)
    
    # Registro Histórico Táctil
    txt_log = ft.ListView(expand=True, spacing=5, height=185)
    txt_log.controls.append(ft.Text(f"{'FECHA':<8} | {'PARTIDO':<16} | {'RET %':<6} | {'GANANCIA'}", font_family="Consolas", size=11, color="#64748B"))
    
    datos_operacion = {}

    def conmutar_empate(e):
        fila_empate.visible = sw_empate.value
        lbl_opX.visible = sw_empate.value
        page.update()

    sw_empate = ft.Switch(label="Incluir mercado de Empate (1X2)", value=True, on_change=conmutar_empate, active_color="#00E676")

    fila_empate = ft.Row([ft.Text("🔸 Empate (X):", width=110), txt_e, txt_ce], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def calcular_operacion(e):
        try:
            pres = float(txt_presupuesto.value)
            c_l = float(txt_l.value)
            c_v = float(txt_v.value)
            usa_e = sw_empate.value
            c_e = float(txt_e.value) if usa_e else None

            if pres <= 0 or c_l <= 1 or c_v <= 1 or (usa_e and c_e <= 1): raise ValueError

            ind = (1/c_l) + (1/c_e if usa_e else 0) + (1/c_v)
            rent = (1 - ind) * 100
            neto = (pres / ind) - pres
            
            es_surebet = ind < 1.0
            col = "#00E676" if es_surebet else "#FF5252"
            
            lbl_st.value = f"🔥 ARBITRAJE (+{round(rent,2)}%) | Neto: +${round(neto,2):,} COP" if es_surebet else f"❌ PÉRDIDA ({round(rent,2)}%) | Neto: ${round(neto,2):,} COP"
            lbl_st.color = col
            
            lbl_op1.value = f"👉 Local (1): ${round(pres/(ind*c_l),2):,} en {txt_cl.value}"
            if usa_e: lbl_opX.value = f"👉 Empate (X): ${round(pres/(ind*c_e),2):,} en {txt_ce.value}"
            lbl_op2.value = f"👉 Visita (2): ${round(pres/(ind*c_v),2):,} en {txt_cv.value}"
            
            btn_guardar.disabled = False
            btn_guardar.bgcolor = col
            btn_guardar.color = "#0B0E14" if es_surebet else "#FFFFFF"
            
            datos_operacion["partido"] = txt_partido.value.strip()[:14] if txt_partido.value else "Partido"
            datos_operacion["pct"] = f"+{round(rent,1)}%" if es_surebet else f"{round(rent,1)}%"
            datos_operacion["neto"] = f"+${round(neto,0):,}" if es_surebet else f"${round(neto,0):,}"
            page.update()
        except ValueError:
            lbl_st.value = "ERROR: VALORES INVÁLIDOS"
            lbl_st.color = "#FF5252"
            page.update()

    def registrar_bitacora(e):
        ahora = datetime.now().strftime("%d/%m")
        linea = f"{ahora:<8} | {datos_operacion['partido']:<16} | {datos_operacion['pct']:<6} | {datos_operacion['neto']}"
        txt_log.controls.append(ft.Text(linea, font_family="Consolas", size=12))
        btn_guardar.disabled = True
        btn_guardar.bgcolor = "#2A2F3D"
        btn_guardar.color = "#64748B"
        page.update()

    btn_guardar = ft.ElevatedButton("📥 REGISTRAR OPERACIÓN", disabled=True, on_click=registrar_bitacora, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)))

    # CORREGIDO: Reemplazado 'corner_radius' por 'border_radius' en los contenedores táctiles
    page.add(
        ft.Container(
            content=ft.Column([
                txt_partido, txt_presupuesto, sw_empate,
                ft.Container(
                    content=ft.Column([
                        ft.Row([ft.Text("🔹 Local (1):", width=110), txt_l, txt_cl], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        fila_empate,
                        ft.Row([ft.Text("🔹 Visita (2):", width=110), txt_v, txt_cv], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ]), bgcolor="#151922", padding=15, border_radius=10
                ),
                ft.ElevatedButton("⚡ EVALUAR APUESTAS", on_click=calcular_operacion, bgcolor="#00E676", color="#0B0E14", width=400, height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6))),
                ft.Container(
                    content=ft.Column([
                        lbl_st, lbl_op1, lbl_opX, lbl_op2,
                        ft.Row([btn_guardar], alignment=ft.MainAxisAlignment.END)
                    ]), bgcolor="#151922", padding=15, border_radius=10
                ),
                ft.Text("📋 HISTORIAL DE ARBITRAJES", font_family="Segoe UI", size=11, weight=ft.FontWeight.BOLD, color="#64748B"),
                ft.Container(content=txt_log, bgcolor="#151922", padding=10, border_radius=10)
            ]), margin=15
        )
    )

if __name__ == "__main__":
    # MODIFICADO: Usamos ft.app en su formato nativo moderno compatible con Python 3.14
    ft.app(target=main)
