import streamlit as st
import plotly.express as px
import pandas as pd
from ui.ui import (
    add_absences_plot,
    add_complexity_score_plot,
    build_sidebar_body_fiters,
    add_kpis,
    add_two_bar_plot_columns,
)
from utils.utils import procces_students_data, read_students_data
from utils.utils import (
    school_column,
    sex_column,
    medu_column,
    fedu_column,
    studytime_column,
    walc_column,
    address_column,
    failuers_column,
)

st.set_page_config(
    page_title="Student achievement ",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "# This is a header. This is an *extremely* cool app!"},
)


df = read_students_data(
    "/home/mtribak/students-improvability/app/data/student_data.csv"
)
df = procces_students_data(df)


df = build_sidebar_body_fiters(df)

st.markdown("## :pencil: Personal informations ")

st.markdown("---")

add_kpis(df)

st.markdown("---")

add_two_bar_plot_columns(
    df=df,
    column_1=school_column,
    column_2=sex_column,
    color_column="success",
    color_discrete_map={"Yes": "lightslategrey", "No": "crimson"},
)

add_two_bar_plot_columns(
    df=df,
    column_1=medu_column,
    column_2=fedu_column,
    color_column="success",
    color_discrete_map={"Yes": "lightslategrey", "No": "crimson"},
    barnorm="percent",
)

add_two_bar_plot_columns(
    df=df,
    column_1=address_column,
    column_2=failuers_column,
    color_column="success",
    color_discrete_map={"Yes": "lightslategrey", "No": "crimson"},
    barnorm="percent",
)

st.markdown("---")

st.markdown("## :dart: Accompaniment  informations ")

add_two_bar_plot_columns(
    df=df,
    column_1=studytime_column,
    column_2=walc_column,
    color_column="success",
    color_discrete_map={"Yes": "lightslategrey", "No": "crimson"},
    barnorm="percent",
)

add_absences_plot(df)

st.markdown("---")

st.markdown("#### Complexity of accompaniment according to final grades obtained")
add_complexity_score_plot(df)


st.markdown("### Detailed Data View")
st.dataframe(df)
st.markdown("---")
