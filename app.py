import streamlit as st
import pandas as pd
import plotly.express as px


diccionario = {"entidad1":
                   {"ua1":{"Serie1":{"sub2":[11,54,67,39],                  #Cada sub tiene una lista de datos
                                         "sub3":[1,32,6],
                                         "sub100":[611,171,118],
                                         "sub200":[1212],
                                         "sub4":[87,34]},
                              "Serie2":{"sub5":[77,44,33,22],
                                        "sub6":[64]},
                              "Serie3":{"sub7":[88,54,65,50]}},
                      "ua2":{"Serie4":{"sub8":[90,80,70]},
                              "Serie5":{"sub9":[91,92],
                                         "sub10":[81]},
                              "Serie6":{"sub11":[13,14,15]}}},
                "entidad2":
                   {"ua3": {"Serie7":{"sub12":[45,12,99]},
                             "Serie8":{"sub13":[4],
                                        "sub14":[900,600,800]}},
                   "ua4": {"Serie9":{"sub5":[123,456],
                                        "sub6":[76,790],
                                        "sub7":[155,156,157]}}}}











niveles_nombres = {1:"Entidad", 2:"Unidad Administrativa", 3:"Serie", 4:"Subserie"}
# print(diccionario["entidad1"]["ua1"]["Serie1"])



# Multi selects
if 's_entidad' not in st.session_state:
    st.session_state["s_entidad"] = None
if 's_ua' not in st.session_state:
    st.session_state["s_ua"] = None
if 's_serie' not in st.session_state:
    st.session_state["s_serie"] = None
if 's_sub' not in st.session_state:
    st.session_state["s_sub"] = None

# niveles de diccionario
def counto(d):
    return max(counto(v) if isinstance(v,dict) else 0 for v in d.values()) + 1
niveles = counto(diccionario) - 1

# Encabezado
# st.title("Dozzier Gestión Documental")
st.subheader("Visualizador de Datos - Gestión Documental")

# Botone y contador
    # Columnas
col1, col2 = st.columns(2)
if "contador" not in st.session_state:
    st.session_state["contador"] = 0

if st.session_state['contador'] < niveles:
    if col1.button(label="Agregar Nivel"):

        st.session_state["contador"] += 1


if st.session_state["contador"] >= 1: # Si hay 0 niveles apagar el menos
    if col2.button(label="Reducir Nivel"):

        st.session_state["contador"] -= 1

# Agregar multiselects



if st.session_state["contador"] == 0:
    st.session_state["s_entidad"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[1]}", options=diccionario.keys())




    st.info(f"{st.session_state['s_entidad']}")

    # Division de series por UA

    df = pd.DataFrame(diccionario)
    df = df[st.session_state["s_entidad"]].dropna().apply(len).transpose().reset_index()

    #


    # Division de subseries por UA

    df1 = pd.DataFrame(diccionario[st.session_state["s_entidad"]]).reset_index().drop(columns=["index"])

    df2 = {}
    for col in df1:
        df2[col] = 0
        for cell in df1[col]:
            if type(cell) == dict:
                df2[col] += len(cell.keys())
    df2 = pd.DataFrame(df2.items())

    # Numero de datos por UA

    df3 = {}
    for col in df1:
        df3[col] = 0
        for cell in df1[col]:
            if type(cell) == dict:
                for x in cell.values():
                    for y in x:
                        df3[col] += y

    df3 = pd.DataFrame(df3.items())



    col3, col4 = st.columns(2)
    col3.metric("Unidades Administrativas", len(diccionario[st.session_state['s_entidad']]))
    col4.metric("Series", sum(df[st.session_state['s_entidad']]))
    col3.metric("Sub-Series", sum(df2[1]))
    col4.metric("Datos", sum(df3[1]))

    fig = px.pie(df, values=st.session_state["s_entidad"], names="index", title="Series por Unidad Administrativa", width=350, height=350)
    fig2 = px.pie(df2, names=0, values=1, title="Sub-Series por Unidad Administrativa", width=350, height=350)
    fig3 = px.pie(df3, names=0, values=1, title="Datos por Unidad Administrativa", width=350, height=350)

    col3.write(fig)
    col4.write(fig2)
    col3.write(fig3)



if st.session_state["contador"] == 1:
    st.session_state["s_entidad"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[1]}", options=diccionario.keys())
    st.session_state["s_ua"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[2]}",options=diccionario[st.session_state["s_entidad"]])


    st.info(f"{st.session_state['s_entidad']} - {st.session_state['s_ua']}")

    # Subseries por serie

    df = pd.DataFrame(diccionario[st.session_state['s_entidad']])
    #st.write(df)
    df = df[st.session_state["s_ua"]].dropna().apply(len).transpose().reset_index()
    #st.write(df)
    #

    # Datos por serie

    df1 = pd.DataFrame(diccionario[st.session_state["s_entidad"]][st.session_state["s_ua"]]).reset_index().drop(columns=["index"])
    #st.write(df1)

    df2 = {}
    for col in df1:
        df2[col] = 0
        for cell in df1[col]:
            if type(cell) == list:
                df2[col] += sum(cell)
    df2 = pd.DataFrame(df2.items())
    #st.write(df2)



    col3, col4, col5 = st.columns(3)
    col3.metric("Series", len(df["index"]))
    col4.metric("Sub-Series", sum(df[st.session_state['s_ua']]))
    col5.metric("Datos", sum(df2[1]))

    fig = px.pie(df, values=st.session_state["s_ua"], names="index", title="Sub-Series por Serie",
                 width=350, height=350)
    fig2 = px.pie(df2, names=0, values=1, title="Datos por serie", width=350, height=350)


    col3.write(fig)
    col5.write(fig2)

if st.session_state["contador"] == 2:
    st.session_state["s_entidad"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[1]}", options=diccionario.keys())
    st.session_state["s_ua"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[2]}",options=diccionario[st.session_state["s_entidad"]])
    st.session_state["s_serie"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[3]}",options=diccionario[st.session_state["s_entidad"]][st.session_state["s_ua"]])


    st.info(f"{st.session_state['s_entidad']} - {st.session_state['s_ua']} - {st.session_state['s_serie']}")

    # Subseries por serie

    df = pd.DataFrame(diccionario[st.session_state['s_entidad']][st.session_state["s_ua"]])
    #st.write(df)
    df = df[st.session_state["s_serie"]].dropna().apply(sum).transpose().reset_index()
    #st.write(df)
    #

    # Datos por serie

    #df1 = pd.DataFrame(diccionario[st.session_state["s_entidad"]][st.session_state["s_ua"]][st.session_state["s_serie"]]).reset_index().drop(columns=["index"])
    #st.write(df1)

    df2 = {}
    for col in df:
        df2[col] = 0
        for cell in df[col]:
            if type(cell) == list:
                df2[col] += sum(cell)
    df2 = pd.DataFrame(df2.items())
    #st.write(df2)

    col3, col4, col5 = st.columns(3)
    col3.metric("Sub-Series", len(df["index"]))
    col4.metric("Datos", sum(df[st.session_state['s_serie']]))

    fig = px.pie(df, values=st.session_state["s_serie"], names="index", title="Sub-Series por Serie",
                 width=350, height=350)
    #fig2 = px.pie(df2, names=0, values=1, title="Datos por serie", width=350, height=350)

    col3.write(fig)
    #col4.write(fig2)


if st.session_state["contador"] == 3:
    st.session_state["s_entidad"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[1]}", options=diccionario.keys())
    st.session_state["s_ua"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[2]}",options=diccionario[st.session_state["s_entidad"]])
    st.session_state["s_serie"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[3]}",
                                            options=diccionario[st.session_state["s_entidad"]][st.session_state["s_ua"]])
    st.session_state["s_sub"] = st.sidebar.selectbox(label=f"Seleccionar {niveles_nombres[4]}",
                                               options=diccionario[st.session_state["s_entidad"]][
                                                   st.session_state["s_ua"]][st.session_state["s_serie"]])


    datos = diccionario[st.session_state['s_entidad']][st.session_state['s_ua']][st.session_state['s_serie']][st.session_state['s_sub']]
    #st.write(datos)

    st.info(f"{st.session_state['s_entidad']} - {st.session_state['s_ua']} - {st.session_state['s_serie']} - {st.session_state['s_sub']}")
    st.metric("Datos en la Sub-Serie", value=sum(datos))


# st.write(st.session_state["contador"])
#
# st.write(niveles)
