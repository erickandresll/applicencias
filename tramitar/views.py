import csv
from django.shortcuts import render
from .models import nomina_licencia
from datetime import datetime
from .forms import UploadFilesForm
import pandas as pd 
import re




##### CARGA DE ARCHIVO EN DB NOMINA_LICENCIAS ##### 
##### CARGA DE ARCHIVO EN DB NOMINA_LICENCIAS ##### 
##### CARGA DE ARCHIVO EN DB NOMINA_LICENCIAS ##### 
##### CARGA DE ARCHIVO EN DB NOMINA_LICENCIAS ##### 
##### CARGA DE ARCHIVO EN DB NOMINA_LICENCIAS ##### 
##### CARGA DE ARCHIVO EN DB NOMINA_LICENCIAS ##### 

def indexpag(request): 
    return render(request, 'tramitar/index.html')

def load_licencias(request):
    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo_csv = request.FILES['archivo_csv']

        if archivo_csv.name.endswith('.csv'):
            # Procesar el archivo CSV
            datos_csv = archivo_csv.read().decode('latin-1').splitlines()
            reader = csv.DictReader(datos_csv, delimiter=';')

            # Guardar los datos en la base de licencia
            for row in reader:
                fecha_otorgamiento = datetime.strptime(row['Fecha otorgamiento'], '%d/%m/%Y').strftime('%Y-%m-%d')
                fecha_inicio = datetime.strptime(row['Fecha inicio'], '%d/%m/%Y').strftime('%Y-%m-%d')

                nueva_licencia = nomina_licencia.objects.create(
                        folio=row['Folio'],
                        run=row['Run'],
                        fecha_emision = fecha_otorgamiento,
                        fecha_inicio = fecha_inicio,
                        dias = row['Dias'],
                        tipo_licencia = row['Tipo licencia'],
                        tipo_repo = row['Tipo reposo'],
                        run_profesional = row['Nombre profesional'],
                        apellido_profesional = row['Apellido profesional'],
                        tipo_profesional = row['Tipo profesional'],
                        especialidad = row['Especialidad'],
                        cotizante = row['Cotizante'],

                )

            nueva_licencia.fecha_otorgamiento_original = row['Fecha otorgamiento']
            nueva_licencia.fecha_inicio_original = row['Fecha inicio']
            nueva_licencia.save()

            # Obtener los datos guardados para mostrar en el template
            datos_guardados = nomina_licencia.objects.all()

            return render(request, 'tramitar/loadlicencias.html', {'datos_guardados': datos_guardados})

    return render(request, 'tramitar/loadlicencias.html')





##### PRORRATEO ##### 
##### PRORRATEO ##### 
##### PRORRATEO ##### 
##### PRORRATEO ##### 
##### PRORRATEO ##### 
##### PRORRATEO ##### 

def normalize_rut(rut):
    rut = re.sub(r'[^\w]', '', rut)  # Eliminar caracteres no alfanuméricos
    rut = rut.upper()  # Convertir a mayúsculas
    
    # Agregar un guion medio antes del último carácter
    rut = rut[:-1] + '-' + rut[-1]
    
    if len(rut) == 9:  # Agregar un 0 al principio si el RUT tiene solo 9 caracteres
        rut = '0' + rut
    return rut

def procesar_archivo_planilla(planilla):
    try:
        planilla_df = pd.read_excel(planilla)
        planilla_df['FEC INICIO'] = pd.to_datetime(planilla_df['FEC INICIO'], format='%d/%m/%Y')
        return planilla_df
    except Exception as e:
        # Manejar excepciones al leer el archivo de planilla
        print(f"Error al procesar el archivo de planilla: {e}")
        return None

def filtrar_programas(programas_df, rut, fec_inicio):
    filtro_programas = ((programas_df['RUT'].apply(normalize_rut) == rut) &
                        (programas_df['MES'] == fec_inicio.month) &
                        (programas_df['AÑO'] == fec_inicio.year))
    return programas_df[filtro_programas]

def calcular_horas_prorrateadas(row, programas_filtrados, monto):
    resultados = []
    montos_prorrateados = []

    for _, programa_row in programas_filtrados.iterrows():
        horas_programa = programa_row['HORAS PROGRAMA']
        programa = programa_row['PROGRAMA']
        cc = programa_row['CC']

        horas_prorrateadas = round((horas_programa / programa_row['TOTAL HORAS']) * monto)
        montos_prorrateados.append(horas_prorrateadas)

        resultados.append({
            'FOLIO': row['FOLIO'],
            'RUT': normalize_rut(row['RUT']),
            'NOMBRE': row['NOMBRE'],
            'FEC INICIO': row['FEC INICIO'],
            'FEC TERMINO': row['FEC TERMINO'],
            'MONTO': horas_prorrateadas,
            'FORMA_DE_PAGO': 'Transferencia',
            'BANCO': '', 
            'CTA.CTE': '',
            'CC': cc,
            'HORAS': horas_programa,
            'PROGRAMA': programa,
        })

    fec_inicio = row['FEC INICIO']
    fec_termino = row['FEC TERMINO']
    return resultados, montos_prorrateados

def carga_archivos(request):
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            planilla = request.FILES['planilla']
            programas_df = pd.read_excel('data/Programas.xlsx')  # Ruta específica donde esté el archivo de programas

            planilla_df = procesar_archivo_planilla(planilla)
            if planilla_df is None:
                # Manejar error al procesar el archivo de planilla
                return render(request, 'tramitar/error.html')

            resultados = []
            diferencias = []

            for index, row in planilla_df.iterrows():
                rut = normalize_rut(row['RUT'])
                fec_inicio = row['FEC INICIO']
                fec_termino = row['FEC TERMINO']
                monto = row['MONTO']

                programas_filtrados = filtrar_programas(programas_df, rut, fec_inicio)

                if len(programas_filtrados) > 0:
                    res, montos = calcular_horas_prorrateadas(row, programas_filtrados, monto)
                    resultados.extend(res)
                    suma_prorrateados = sum(montos)
                    if suma_prorrateados != monto:
                        diferencia = monto - suma_prorrateados
                        diferencias.append(f"DIFERENCIA: RUT {rut} tiene una diferencia de {diferencia}.")

            resultados_df = pd.DataFrame(resultados)
            resultados_df['FEC INICIO'] = resultados_df['FEC INICIO'].dt.strftime('%d/%m/%Y')
            resultados_df['FEC TERMINO'] = resultados_df['FEC TERMINO'].dt.strftime('%d/%m/%Y')
            resultados_df.to_excel('FINAL.xlsx', index=False)

            return render(request, 'tramitar/resultado.html', {'resultados': resultados, 'diferencias': diferencias})
    else:
        form = UploadFilesForm()
    return render(request, 'tramitar/carga_archivos.html', {'form': form})