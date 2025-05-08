<!-- Título centrado -->
<h1 align="center">📁 EPH Insight</h1>

<!-- Tabla de contenidos -->
## 📑 Tabla de Contenidos
- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Integrantes](#-integrantes)
- [Estructura del Proyecto](#-estructura-del-proyecto)

--------------------------------------------------------------------

## 🌟 Acerca del Proyecto
"Programa diseñado para, en base a los EPH de diferentes años y trimestres, generar nuevos datos (columnas), csv con estos nuevos datos y los viejos y consultar sobre estos. Por otro lado tambien esta el diseño de una pagina en Streamlit donde se pueden visualizar e interactuar con diferentes tareas"

--------------------------------------------------------------------

## 🌳 Requisitos

- **Python 3**
- **Editor de código**
- **Terminal/Consola**

--------------------------------------------------------------------

## 🛠️ Instalación

Sigue estos pasos para configurar el entorno de desarrollo:

1. **Clonar el repositorio**:
   ```bash
   Clone con SSH
    git clone git@gitlab.catedras.linti.unlp.edu.ar:python-2025/proyectos/grupo26/code.git
   Clone con HTTPS
    git clone https://gitlab.catedras.linti.unlp.edu.ar/python-2025/proyectos/grupo26/code.git

2. **Entrar a la carpeta del proyecto**:

    cd INDEC

3. **Crear y activar el entorno virtual**:
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

4. **Instala el requirements**:

    pip install -r requirements.txt

4. **Agregar archivos EPH**:

    1. Descarga archivos .zip de la Encuesta Permanente de Hogares (EPH) de la página oficial del INDEC
    2. Colocarlos en la carpeta /utils/data
        # Estructura final requerida 
            |──INDEC
            │   ├── utils                           
            │         ├── data                 
            │               ├── data_2_2019.zip
            |               ├── data_1_2020.zip

--------------------------------------------------------------------

## 👥 Integrantes

**Integrantes:**  
- Legajo 18143/6: [Lucentini Joaquin]
- Legajo 18137/7: [Loredo Lautaro]
- Legajo 18304/4: [Rodriguez Ulises]
- Legajo 18212/1: [Morano Axel Martin]
- Legajo 25550: [Carlos Martínez]

--------------------------------------------------------------------

## 🌳 Estructura del Proyecto

# Como es la estructura?
- La carpeta notebooks se encuentran la seccion A (individuos y hogares) y la seccion B (consultas) donde se encuentran separados cada uno de los puntos para ejecutar por separado
- La carpeta src tiene 1_ La funcion que me permite unir todos los DataSet de individuos y hogares (por separado), 2_ La funcion para poner ejecutar los Jupyter de la seccion A y B de forma automatizada, 3_ Una carpeta funciones con todas las funciones necesarias para la seccion A y 4_ Una carpeta consultas con todas las funciones necesarias para la seccion B
- La carpeta streamlit contiene el codigo y paginas necesarias para la resolucion de los puntos especificados para el mismo
- La carpeta Utils va a contener los csv cuando se generen con todos los DataSets y sus datos nuevos. Ademas va a contener una carpeta data donde contendra los archivos .zip del EPH suministrado por la pagina oficial del INDEC

# Tree

├── INDEC
│   ├── notebooks                           
│   │   ├── consultas.ipynb                 
│   │   ├── hogares.ipynb
│   │   └── individuos.ipynb
│   ├── src
│   │   ├── automatizar_jupyter.py
│   │   ├── consultas   #Carpeta con las funciones para la seccion B
│   │   ├── DataSet.py
│   │   ├── funciones   #Carpeta con las funciones para la seccion A
│   │   ├── __init__.py
│   ├── streamlit
│   │   ├── Inicio.py
│   │   └── pages               #Carpeta con paginas de Streamlit
│   ├── utils
│   │   ├── constantes.py
│   │   ├── data                #Carpeta con la data del EPH
│   │   └── __init__.py
│   ├── README.md
│   ├── requirements.txt
├── Python - Trabajo Integrador Parte 1.pdf