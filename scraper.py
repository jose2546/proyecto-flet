class MotorArbitraje:
    @staticmethod
    def calcular_surebet(c_local, c_visita, presupuesto, c_empate=None, usa_empate=True):
        if usa_empate and c_empate:
            # FÓRMULA DE 3 VÍAS (Con Empate)
            indice = (1 / c_local) + (1 / c_empate) + (1 / c_visita)
            apuesta_X = presupuesto / (indice * c_empate)
        else:
            # FÓRMULA DE 2 VÍAS (Sin Empate - Ejemplo: Basketball, Tenis o mercado DNB)
            indice = (1 / c_local) + (1 / c_visita)
            apuesta_X = 0.0

        rentabilidad = (1 - indice) * 100
        ganancia_neta = (presupuesto / indice) - presupuesto
        
        apuesta_1 = presupuesto / (indice * c_local)
        apuesta_2 = presupuesto / (indice * c_visita)
        
        return {
            "es_surebet": indice < 1.0,
            "rentabilidad": round(rentabilidad, 2),
            "ganancia_neta": round(ganancia_neta, 2),
            "apuesta_local": round(apuesta_1, 2),
            "apuesta_empate": round(apuesta_X, 2),
            "apuesta_visitante": round(apuesta_2, 2)
        }
