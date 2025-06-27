import pandas as pd

def fecha_larga(fecha):
    """
    Convierte una fecha al formato largo en español: 1 de junio de 2024

    Args:
        fecha: Fecha a convertir (puede ser string o datetime)
        
    Returns:
        str: Fecha en formato largo o cadena vacía si es inválida
"""
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    if pd.isnull(fecha):
        return ""
    if isinstance(fecha, str):
        try:
            fecha = pd.to_datetime(fecha, dayfirst=True)
        except Exception:
            return fecha
    return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}" 

def mes_espaniol(fecha):
    """
    Devuelve el mes y año en españos al log
    """
    meses=[
        "Enero", "Febrero", "Marzo", "Abril", "Mayo",
        "junio", "julio", "Agosto", "septiembre", "octubre",
        "Noviembre", "Diciembre"
    ]
    if hasattr(fecha, "month",) and hasattr(fecha, "year"):
        return f"{meses[fecha.month - 1].capitalize()} {fecha.year}"
        
    return ""
