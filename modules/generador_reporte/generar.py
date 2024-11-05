from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import pandas as pd
import os
import webbrowser
import datetime
import matplotlib.pyplot as plt
from ..analizador_datos.analisis.capa_transform import capa_a_dataframe

def generar_reporte_pdf(instance):
    capa_nombre = str(instance.inputCapaReporte.currentText())
    columnas_seleccionadas = []
    pdf_path = os.path.join(instance.plugin_dir, f"Reporte_{capa_nombre}.pdf")

    for i in range(instance.columnLayoutReporte.count()):
        checkbox = instance.columnLayoutReporte.itemAt(i).widget()
        if checkbox.isChecked():
            columnas_seleccionadas.append(checkbox.text())

    if capa_nombre and columnas_seleccionadas:
        df = capa_a_dataframe(capa_nombre, columnas_seleccionadas)
        columnas_numericas = []

        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                if df[col].dtype in ['float64', 'int64']:
                    columnas_numericas.append(col)
            except ValueError:
                continue

        if df.empty:
            print("No hay datos numéricos para graficar en esta capa.")
            return

        df = df[columnas_numericas]

        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        margin = 1 * inch
        styles = getSampleStyleSheet()
        c.setTitle("Reporte de Estadísticas Descriptivas")


        # Crear encabezado con logo y texto en una tabla
        logo_path = os.path.join(instance.plugin_dir, 'coperativalogo.jpg')
        logo_img = Image(logo_path, width=50, height=50)
        header_data = [[logo_img, "Cooperativa de Agua de OV"]]

        header_table = Table(header_data, colWidths=[1 * inch, 4 * inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),      # Alinea el logo a la izquierda
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),      # Alinea el texto a la izquierda
            ('LEFTPADDING', (1, 0), (1, 0), 8),     # Reduce el espacio del texto a la izquierda
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centra verticalmente el contenido
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, 0), 16),
        ]))


        header_table.wrapOn(c, margin, height - 50)
        header_table.drawOn(c, margin, height - 60)

        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        c.setFont("Helvetica-Bold", 16)

        # Ajustar la posición y del título
        titulo_y_position = height - 80  # Mueve el título un poco hacia abajo
        c.drawCentredString(width / 2, titulo_y_position, f"Reporte de Estadísticas Descriptivas para la capa: {capa_nombre}")

        c.setFont("Helvetica", 12)

        # Ajustar la posición y de la fecha
        fecha_y_position = titulo_y_position - 20  # Mueve la fecha un poco más abajo
        c.drawCentredString(width / 2, fecha_y_position, f"Fecha de generación: {fecha_actual}")

        y_position = fecha_y_position - 50  # Ajusta y_position para que el contenido empiece más abajo

        pieAgregado = False

        for col in columnas_numericas:
            if y_position < 150:
                c.showPage()  # Crear una nueva página si el espacio es insuficiente
                y_position = height - 100
                if pieAgregado:
                    pieAgregado = False

            stats = df[col].describe()

            data = [
                ["Métrica", "Valor"],
                ["Media", f"{stats['mean']:.2f}"],
                ["Mediana", f"{stats['50%']:.2f}"],
                ["Desviación Estándar", f"{stats['std']:.2f}"],
                ["Valor Mínimo", f"{stats['min']:.2f}"],
                ["Valor Máximo", f"{stats['max']:.2f}"],
            ]

            # Calcular el ancho disponible y el ancho de las columnas
            available_width = width - 2 * margin  # Ancho total menos márgenes izquierdo y derecho
            column_width = available_width / len(data[0])  # Ancho de cada columna

            table = Table(data, colWidths=[column_width] * len(data[0]))  # Ajustar ancho de columnas
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('BOX', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))

            # Calcular la posición horizontal centrada
            table_width, table_height = table.wrap(0, y_position - 80)  # Obtener el tamaño de la tabla
            centered_x_position = (width - table_width) / 2  # Posición centrada en el eje X

            table.drawOn(c, centered_x_position, y_position - 80)  # Dibujar la tabla centrada
            y_position -= 50

            # Generar y añadir gráfico
            fig, ax = plt.subplots()
            df[col].plot(kind="hist", ax=ax, color="skyblue", edgecolor="black")
            ax.set_title(f"Distribución de {col}")
            ax.set_xlabel(col)
            fig.savefig(f"{col}_hist.png")
            plt.close(fig)

            c.drawImage(f"{col}_hist.png", 100, y_position - 200, width=400, height=150)
            os.remove(f"{col}_hist.png")
            y_position -= 250

            if pieAgregado == False:
                pie_path = os.path.join(instance.plugin_dir, 'icon.png')
                logo_size = 20
                c.drawImage(pie_path, width - 80, 20, width=logo_size, height=logo_size)  # Logo pequeño en esquina derecha
                c.drawString(width - 140, 25, f"Página {c.getPageNumber()}")
                pieAgregado = True




        c.save()
        webbrowser.open_new(pdf_path)
