import streamlit as st
from utils.config import STUDENTS_DATA_PATH

from ui.ui import (
    add_absences_plot,
    add_complexity_score_plot,
    build_sidebar_body_fiters,
    add_kpis,
    add_two_bar_plot_columns,
)
from utils.utils import process_students_data, read_students_data
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

SUCCESS_COLOR_MAP = {"Yes": "lightslategrey", "No": "crimson"}

st.set_page_config(
    page_title="Student achievement ",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "About": "Data source :  Paulo Cortez, University of Minho, Guimares, Portugal, http://www3.dsi.uminho.pt/pcortez"
    },
)


df = read_students_data(STUDENTS_DATA_PATH)
df = process_students_data(df)

df = build_sidebar_body_fiters(df)

# Body

st.markdown("## :pencil: Personal informations ")

st.markdown("---")

add_kpis(df)

st.markdown("---")

add_two_bar_plot_columns(
    df=df,
    column_1=school_column,
    column_2=sex_column,
    color_column="success",
    color_discrete_map=SUCCESS_COLOR_MAP,
)

add_two_bar_plot_columns(
    df=df,
    column_1=medu_column,
    column_2=fedu_column,
    color_column="success",
    color_discrete_map=SUCCESS_COLOR_MAP,
    barnorm="percent",
)

add_two_bar_plot_columns(
    df=df,
    column_1=address_column,
    column_2=failuers_column,
    color_column="success",
    color_discrete_map=SUCCESS_COLOR_MAP,
    barnorm="percent",
)

st.markdown("---")

st.markdown("## :dart: Accompaniment  informations ")

add_two_bar_plot_columns(
    df=df,
    column_1=studytime_column,
    column_2=walc_column,
    color_column="success",
    color_discrete_map=SUCCESS_COLOR_MAP,
    barnorm="percent",
)

add_absences_plot(df)

st.markdown("---")

st.markdown("#### Complexity of accompaniment according to final grades obtained")
add_complexity_score_plot(df)

st.markdown(
    """
## Engagement and Study Habits Index
### Complexity of accompaniment score
- ***Definition***: A metric gauging the complexity of student involvement and study routines.
- ***Range***: 0 (low risk) to 100 (high risk).
- ***Interpretation***:
    * **Higher scores** might signal a notable alcohol consumption rate and/or an increased count of absences, both of which could detrimentally affect students' overall well-being and academic achievements.
    * **Lower scores** imply that students are spending more time on studying and are actively engaged in their educational pursuits.

The students to prioritize for assistance would be those who have high scores in the upper left
corner of the graph at the top. This indicates that these students display both
high alcohol consumption and/or a high number of absences.

"""
)

st.markdown("### Detailed Data View")
st.dataframe(df)
st.markdown("---")
