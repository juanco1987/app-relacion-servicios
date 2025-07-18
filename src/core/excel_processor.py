import pandas as pd
from src.utils.validation_utils import limpiar_valor_monetario

def extraer_servicios(excel_path, fecha_inicio, fecha_fin, log_callback=None):
    """
    Extrae los servicios del archivo Excel que cumplan con los criterios:
    1. FORMA DE PAGO = "EFECTIVO"
    2. ESTADO DEL SERVICIO = VACÍO
    3. En el rango de fechas especificado
    """
    if log_callback is None:
        log_callback = print

    log_callback("Procesando datos del archivo Excel...")

    try:
        xls = pd.ExcelFile(excel_path)
    except Exception as e:
        log_callback(f"Error al abrir el archivo Excel: {str(e)}", 'error')
        return pd.DataFrame()

    frames = []

    for hoja in xls.sheet_names:
        try:
            log_callback(f"\nAnalizando hoja: {hoja}")
            df = xls.parse(hoja)

            # Limpiar nombres de columnas (eliminar espacios al final)
            df.columns = df.columns.str.strip()

            # Mostrar todas las columnas que existen en la hoja
            log_callback(f"Columnas en la hoja {hoja}:")
            for col in df.columns:
                log_callback(f"  - '{col}'")

            if 'FECHA' not in df.columns:
                log_callback(f"Hoja {hoja} no tiene columna FECHA. Saltando...")
                continue

            # Filtrar filas con fecha no nula
            df = df[df['FECHA'].notnull()]
            df['FECHA'] = pd.to_datetime(df['FECHA'], errors='coerce', dayfirst=True)
            df = df[df['FECHA'].between(fecha_inicio, fecha_fin)]
            log_callback(f"Registros después de filtrar por fecha: {len(df)}")

            # Buscar exactamente la columna FORMA DE PAGO (ignorando espacios al final)
            columna_pago = None
            for col in df.columns:
                if col.strip() == 'FORMA DE PAGO':
                    columna_pago = col
                    break

            if not columna_pago:
                log_callback(f"No se encontró columna exacta 'FORMA DE PAGO' en hoja {hoja}. Saltando...")
                continue

            # Buscar exactamente la columna ESTADO DEL SERVICIO (ignorando espacios al final)
            columna_estado = None
            for col in df.columns:
                if col.strip() == 'ESTADO DEL SERVICIO':
                    columna_estado = col
                    break

            if not columna_estado:
                log_callback(f"No se encontró columna exacta 'ESTADO DEL SERVICIO' en hoja {hoja}. Saltando...")
                continue

            # Mostrar valores únicos en ambas columnas antes de filtrar
            log_callback(f"Valores únicos en {columna_pago}: {df[columna_pago].astype(str).str.upper().unique()}")
            log_callback(f"Valores únicos en {columna_estado}: {df[columna_estado].astype(str).str.upper().unique()}")

            # Filtrar por forma de pago = EFECTIVO
            df['FORMA_PAGO_CLEAN'] = df[columna_pago].astype(str).str.upper().str.strip()
            df = df[df['FORMA_PAGO_CLEAN'] == 'EFECTIVO']
            log_callback(f"Registros después de filtrar por forma de pago: {len(df)}")

            # Filtrar por estado del servicio vacío
            mascara_estado = df[columna_estado].isna() | (df[columna_estado].astype(str).str.strip() == '')
            df = df[mascara_estado]
            
            # Mostrar los registros que fueron excluidos (usando loc para evitar la advertencia)
            registros_excluidos = df.loc[~mascara_estado]
            if not registros_excluidos.empty:
                log_callback(f"Registros excluidos por tener estado: {len(registros_excluidos)}")
                for idx, row in registros_excluidos.iterrows():
                    log_callback(f"  - Registro {idx}: {row[columna_estado]}")
            
            log_callback(f"Registros después de filtrar por estado: {len(df)}")

            # Buscar columnas de dirección, servicio realizado, valor servicio y domicilio
            columna_direccion = None
            columna_servicio = None
            columna_valor = None
            columna_domicilio = None

            for col in df.columns:
                if 'DIRECCION' in col.upper():
                    columna_direccion = col
                if 'SERVICIO' in col.upper() and 'REALIZADO' in col.upper():
                    columna_servicio = col
                if 'VALOR' in col.upper() and 'SERVICIO' in col.upper():
                    columna_valor = col
                if 'DOMICILIO' in col.upper():
                    columna_domicilio = col

            # Si no hay columna de dirección, intentar alternativas
            if not columna_direccion:
                for posible_col in ['DIRECCION', 'DIRECCIÓN', 'UBICACION', 'UBICACIÓN']:
                    if posible_col in df.columns:
                        columna_direccion = posible_col
                        break

            # Si no hay columna de servicio realizado, intentar alternativas
            if not columna_servicio:
                for posible_col in ['SERVICIO', 'DESCRIPCION', 'DESCRIPCIÓN', 'TRABAJO']:
                    if posible_col in df.columns:
                        columna_servicio = posible_col
                        break

            # Si no hay valor de servicio ni columna de domicilio, no podemos calcular
            if not columna_valor and not columna_domicilio:
                log_callback(f"No se encontraron columnas de valor en hoja {hoja}. Saltando...")
                continue

            # Crear columnas para el informe
            df['DIRECCION_PARA_INFORME'] = ''
            if columna_direccion:
                df['DIRECCION_PARA_INFORME'] = df[columna_direccion].fillna('').astype(str)
            df['SERVICIO_PARA_INFORME'] = ''
            if columna_servicio:
                df['SERVICIO_PARA_INFORME'] = df[columna_servicio].fillna('').astype(str)

            # Crear columna combinada de valor
            df['VALOR_COMBINADO'] = 0
            df['VALOR_ORIGINAL'] = 0

            # Si existe columna de valor servicio, usarla cuando no es nula o cero
            if columna_valor:
                df[columna_valor] = df[columna_valor].apply(limpiar_valor_monetario)
                df.loc[df[columna_valor] > 0, 'VALOR_COMBINADO'] = df[columna_valor]
                df.loc[df[columna_valor] > 0, 'VALOR_ORIGINAL'] = df[columna_valor]

            # Si existe columna de domicilio, usarla cuando valor servicio es nulo o cero
            if columna_domicilio:
                df[columna_domicilio] = df[columna_domicilio].apply(limpiar_valor_monetario)
                mascara_usar_domicilio = df['VALOR_COMBINADO'] == 0
                df.loc[mascara_usar_domicilio & (df[columna_domicilio] > 0), 'VALOR_COMBINADO'] = df[columna_domicilio]
                df.loc[mascara_usar_domicilio & (df[columna_domicilio] > 0), 'VALOR_ORIGINAL'] = df[columna_domicilio]

            log_callback(f"Registros con valor combinado > 0: {len(df[df['VALOR_COMBINADO'] > 0])}")

            # Buscar columna de IVA
            columna_iva = None
            for col in df.columns:
                if 'IVA' in col.upper():
                    columna_iva = col
                    break

            # Columna de materiales
            columna_materiales = None
            for col in df.columns:
                if 'MATERIAL' in col.upper():
                    if not 'VALOR' in col.upper():  # Excluir columnas de valor de materiales
                        columna_materiales = col
                        break

            # Columna de valor de materiales
            columna_valor_materiales = None
            for col in df.columns:
                if 'VALOR' in col.upper() and 'MATERIAL' in col.upper():
                    columna_valor_materiales = col
                    break

            # Agregar columnas de materiales si existen
            if columna_materiales:
                df['MATERIALES'] = df[columna_materiales].fillna('').astype(str)
            else:
                df['MATERIALES'] = ''

            if columna_valor_materiales:
                try:
                    df['VALOR MATERIALES'] = df[columna_valor_materiales].fillna(0).astype(str).apply(limpiar_valor_monetario)
                except:
                    df['VALOR MATERIALES'] = 0
            else:
                df['VALOR MATERIALES'] = 0

            # Calcular valores financieros
            df['SUBTOTAL'] = df['VALOR_COMBINADO'] * 0.5
            if columna_iva:
                df['IVA'] = df[columna_iva].fillna(0).apply(limpiar_valor_monetario)
            else:
                df['IVA'] = pd.Series([0.0] * len(df), index=df.index)
            df['TOTAL EMPRESA'] = df['SUBTOTAL'] + df['IVA']

            # Filtrar registros con valor combinado mayor que cero (para evitar filas sin valor)
            df = df[df['VALOR_COMBINADO'] > 0]
            log_callback(f"Registros finales después de todos los filtros: {len(df)}")

            # Eliminar columnas que se hayan quedado completamente vacías (NaN) después del filtrado
            df.dropna(axis=1, how='all', inplace=True)
            df = df.reset_index(drop=True)

            # Registrar el número de servicios encontrados para esta hoja
            log_callback(f"Servicios encontrados en '{hoja}': {len(df)}", 'info')
            
            frames.append(df)
        except Exception as e:
            log_callback(f"Error al procesar hoja {hoja}: {str(e)}", 'error')
            continue

    result = pd.concat(frames) if frames else pd.DataFrame()
    log_callback(f"\nSe encontraron {len(result)} servicios en total.", 'success')
    return result 