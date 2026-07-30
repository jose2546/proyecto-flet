import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class ArbitrajeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SUREBET ANALYTICS PRO")
        self.geometry("850x880")
        self.configure(fg_color="#0B0E14")
        
        # Forzar maximizado automático al abrir para garantizar espacio completo
        self.after(0, lambda: self.state('zoomed'))

        # Encabezado Compacto
        ctk.CTkLabel(self, text="SUREBET ANALYTICS PRO", font=("Segoe UI", 22, "bold"), text_color="#00E676").pack(pady=(10,1))
        ctk.CTkLabel(self, text="Consola profesional de cobertura de riesgo y registro de operaciones", font=("Segoe UI", 11), text_color="#64748B").pack(pady=(0,8))

        # --- SECCIÓN: NOMBRE DEL ENFRENTAMIENTO / PARTIDO ---
        f_partido = ctk.CTkFrame(self, fg_color="#151922", corner_radius=8)
        f_partido.pack(pady=2, fill="x", padx=40)
        ctk.CTkLabel(f_partido, text="NOMBRE DEL ENFRENTAMIENTO / PARTIDO:", font=("Segoe UI", 11, "bold")).pack(side="left", padx=15, pady=6)
        self.txt_partido = ctk.CTkEntry(f_partido, font=("Segoe UI", 12), width=320, placeholder_text="Ej: Real Madrid vs Barcelona", fg_color="#0B0E14", text_color="#FFFFFF")
        self.txt_partido.pack(side="right", padx=15, pady=6)

        # 1. Entrada de Capital
        f_cap = ctk.CTkFrame(self, fg_color="#151922", corner_radius=8)
        f_cap.pack(pady=2, fill="x", padx=40)
        ctk.CTkLabel(f_cap, text="CAPITAL TOTAL INVERSIÓN ($ COP):", font=("Segoe UI", 11, "bold")).pack(side="left", padx=15, pady=6)
        self.txt_presupuesto = ctk.CTkEntry(f_cap, font=("Segoe UI", 12, "bold"), width=150, justify="right", fg_color="#0B0E14", text_color="#00E676")
        self.txt_presupuesto.insert(0, "100000")
        self.txt_presupuesto.pack(side="right", padx=15, pady=6)

        # 2. Switch de Estrategia
        self.sw_var = ctk.StringVar(value="on")
        self.sw = ctk.CTkSwitch(self, text="Incluir mercado de Empate (Estrategia 1X2)", command=self.conmutar, variable=self.sw_var, onvalue="on", offvalue="off", font=("Segoe UI", 11), progress_color="#00E676")
        self.sw.pack(pady=4, anchor="w", padx=45)

        # 3. Cuadrícula de Cuotas
        self.f_grid = ctk.CTkFrame(self, fg_color="#151922", corner_radius=8)
        self.f_grid.pack(pady=2, fill="x", padx=40)
        
        self.txt_l, self.txt_cl = self.crear_fila("🔹 Cuota Gana Local (1):", "BetPlay", 1)
        self.lbl_e, self.txt_e, self.txt_ce = self.crear_fila("🔸 Cuota Empate (X):", "BetPlay", 2, ret_todo=True)
        self.txt_v, self.txt_cv = self.crear_fila("🔹 Cuota Visitante (2):", "BetPlay", 3)

        # 4. Botón Evaluar Matriz (Más compacto en altura)
        ctk.CTkButton(self, text="⚡ EVALUAR MATRIZ DE APUESTAS", font=("Segoe UI", 12, "bold"), height=36, fg_color="#00E676", text_color="#0B0E14", hover_color="#00C853", command=self.calcular).pack(pady=6, fill="x", padx=40)

        # 5. Panel de Reportes (Compactado en sus márgenes internos)
        self.f_rep = ctk.CTkFrame(self, fg_color="#151922", corner_radius=8, border_width=1, border_color="#2A2F3D")
        self.f_rep.pack(pady=2, fill="x", padx=40)
        
        self.lbl_st = ctk.CTkLabel(self.f_rep, text="SISTEMA LISTO: INGRESE LOS VALORES", font=("Segoe UI", 12, "bold"), text_color="#64748B")
        self.lbl_st.pack(anchor="w", padx=20, pady=(8,2))
        
        self.lbl_op1 = ctk.CTkLabel(self.f_rep, text="", font=("Segoe UI", 12, "bold"), text_color="#E1E1E6")
        self.lbl_op1.pack(anchor="w", padx=20, pady=1)
        self.lbl_opX = ctk.CTkLabel(self.f_rep, text="", font=("Segoe UI", 12, "bold"), text_color="#E1E1E6")
        self.lbl_opX.pack(anchor="w", padx=20, pady=1)
        self.lbl_op2 = ctk.CTkLabel(self.f_rep, text="", font=("Segoe UI", 12, "bold"), text_color="#E1E1E6")
        self.lbl_op2.pack(anchor="w", padx=20, pady=1)

        self.btn_guardar = ctk.CTkButton(self.f_rep, text="📥 REGISTRAR OPERACIÓN EN BITÁCORA", font=("Segoe UI", 11, "bold"), height=26, fg_color="#2A2F3D", text_color="#FFFFFF", hover_color="#3E4457", state="disabled", command=self.registrar_log)
        self.btn_guardar.pack(pady=8, padx=20, anchor="e")

        # 6. Historial / Bitácora de Operaciones (Ahora tiene prioridad de expansión vertical)
        ctk.CTkLabel(self, text="📋 BITÁCORA HISTÓRICA DE OPERACIONES", font=("Segoe UI", 11, "bold"), text_color="#64748B").pack(pady=(6,2), anchor="w", padx=45)
        
        self.txt_log = ctk.CTkTextbox(self, font=("Consolas", 12), fg_color="#151922", border_color="#2A2F3D", border_width=1, text_color="#E1E1E6")
        self.txt_log.pack(pady=(0,15), fill="both", expand=True, padx=40)
        
        self.txt_log.insert("0.0", f"{'FECHA/HORA':<15} | {'ENFRENTAMIENTO':<32} | {'INVERSIÓN':<12} | {'RETORNO %':<10} | {'GANANCIA NETO'}\n")
        self.txt_log.insert("end", "-" * 95 + "\n")
        self.txt_log.configure(state="disabled")

        self.datos_operacion_actual = None

    def crear_fila(self, texto, casa, fila, ret_todo=False):
        lbl = ctk.CTkLabel(self.f_grid, text=texto, font=("Segoe UI", 11))
        lbl.grid(row=fila, column=0, sticky="w", padx=15, pady=4)
        txt = ctk.CTkEntry(self.f_grid, width=90, justify="center", fg_color="#0B0E14", font=("Segoe UI", 11, "bold"))
        txt.grid(row=fila, column=1, pady=4, padx=10)
        txt_c = ctk.CTkEntry(self.f_grid, width=120, justify="center", fg_color="#0B0E14", font=("Segoe UI", 11))
        txt_c.insert(0, casa)
        txt_c.grid(row=fila, column=2, pady=4, padx=10)
        return (lbl, txt, txt_c) if ret_todo else (txt, txt_c)

    def conmutar(self):
        if self.sw_var.get() == "on":
            self.lbl_e.grid()
            self.txt_e.grid()
            self.txt_ce.grid()
        else:
            self.lbl_e.grid_remove()
            self.txt_e.grid_remove()
            self.txt_ce.grid_remove()
            self.lbl_opX.configure(text="")

    def calcular(self):
        try:
            pres, c_l, c_v = float(self.txt_presupuesto.get()), float(self.txt_l.get()), float(self.txt_v.get())
            usa_e = (self.sw_var.get() == "on")
            c_e = float(self.txt_e.get()) if usa_e else None
            
            nombre_partido = self.txt_partido.get().strip()
            if not nombre_partido:
                nombre_partido = "Partido General"

            if pres <= 0 or c_l <= 1 or c_v <= 1 or (usa_e and c_e <= 1): raise ValueError
            
            ind = (1/c_l) + (1/c_e if usa_e else 0) + (1/c_v)
            rent, neto = (1 - ind) * 100, (pres / ind) - pres
            
            es_surebet = ind < 1.0
            col = "#00E676" if es_surebet else "#FF5252"
            
            txt_st = f"🔥 ARBITRAJE DETECTADO (+{round(rent,2)}%) | Retorno Neto: +${round(neto,2):,} COP" if es_surebet else f"❌ MERCADO CON PÉRDIDA ({round(rent,2)}%) | Retorno Neto: ${round(neto,2):,} COP"
            self.f_rep.configure(border_color=col)
            self.lbl_st.configure(text=txt_st, text_color=col)
            
            casa_l = self.txt_cl.get().strip()
            casa_v = self.txt_cv.get().strip()
            casa_e = self.txt_ce.get().strip() if usa_e else ""

            self.lbl_op1.configure(text=f"👉 Local (1)   : ${round(pres/(ind*c_l),2):,} COP en {casa_l}")
            if usa_e: 
                self.lbl_opX.configure(text=f"👉 Empate (X)  : ${round(pres/(ind*c_e),2):,} COP en {casa_e}")
            else:
                self.lbl_opX.configure(text="")
            self.lbl_op2.configure(text=f"👉 Visitante (2): ${round(pres/(ind*c_v),2):,} COP en {casa_v}")

            self.btn_guardar.configure(state="normal", fg_color="#00E676" if es_surebet else "#FF5252", text_color="#0B0E14" if es_surebet else "#FFFFFF")
            
            self.datos_operacion_actual = {
                "partido": nombre_partido[:30], 
                "inv": f"${pres:,}",
                "pct": f"+{round(rent,2)}%" if es_surebet else f"{round(rent,2)}%",
                "neto": f"+${round(neto,2):,}" if es_surebet else f"${round(neto,2):,}"
            }

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos mayores a 1.0.")

    def registrar_log(self):
        if self.datos_operacion_actual:
            ahora = datetime.now().strftime("%d/%m %H:%M")
            d = self.datos_operacion_actual
            
            linea_log = f"{ahora:<15} | {d['partido']:<32} | {d['inv']:<12} | {d['pct']:<10} | {d['neto']}\n"
            
            self.txt_log.configure(state="normal")
            self.txt_log.insert("end", linea_log)
            self.txt_log.configure(state="disabled")
            
            self.btn_guardar.configure(state="disabled", fg_color="#2A2F3D", text_color="#64748B")

if __name__ == "__main__":
    ArbitrajeApp().mainloop()
