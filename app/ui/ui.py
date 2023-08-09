import streamlit as st
import plotly.express as px
import pandas as pd

from utils.utils import CategoryColumn
from utils.utils import school_column, sex_column, studytime_column, walc_column


def _plot_bar_chart(
    df: pd.DataFrame,
    x_column: str,
    x_column_label: str,
    title: str,
    category_orders: list,
    color_column: str = None,
    color_discrete_map: dict = {},
    barnorm: str = None,
) -> None:
    st.markdown(f"#### {title}")

    fig = px.histogram(
        df,
        x=x_column,
        color=color_column,
        barnorm=barnorm,
        color_discrete_map=color_discrete_map,
        barmode="relative",
    )
    fig.update_xaxes(categoryorder="array", categoryarray=category_orders)
    fig.update_layout(yaxis_title="Count", xaxis_title=x_column_label)
    st.plotly_chart(fig, use_container_width=True)


def add_kpis(df: pd.DataFrame) -> None:
    kpi1, kpi2, kpi3 = st.columns(3)

    students_count = len(df["studentid"].unique())
    avg_age = df["age"].mean()

    success_percent = df[df["success"] == "Yes"].shape[0] / df.shape[0] * 100

    kpi1.metric(
        label="Total students counts",
        value=int(students_count),
    )
    kpi2.metric(
        label="Average age",
        value=round(avg_age),
    )

    kpi3.metric(
        label="Success percent",
        value=f"{round(success_percent)} %",
    )


def add_two_bar_plot_columns(
    df: pd.DataFrame,
    column_1: CategoryColumn,
    column_2: CategoryColumn,
    color_column: str,
    color_discrete_map: str,
    barnorm: str = None,
) -> None:
    fig_column_1, fig_column_2 = st.columns(2)
    with fig_column_1:
        _plot_bar_chart(
            df=df,
            x_column=f"{column_1.name}_category",
            x_column_label=column_1.full_name,
            title=f"Number of successes by {column_1.full_name}",
            category_orders=list(column_1.categories_mapping.values()),
            color_column=color_column,
            color_discrete_map=color_discrete_map,
            barnorm=barnorm,
        )

    with fig_column_2:
        _plot_bar_chart(
            df=df,
            x_column=f"{column_2.name}_category",
            x_column_label=column_2.full_name,
            title=f"Number of successes by {column_2.full_name}",
            category_orders=list(column_2.categories_mapping.values()),
            color_column=color_column,
            color_discrete_map=color_discrete_map,
            barnorm=barnorm,
        )


def add_complexity_score_plot(df: pd.DataFrame) -> None:
    fig = px.strip(
        df,
        x="finalgrade",
        y="accompanying_complexity",
        color="success",
        color_discrete_map={"Yes": "lightslategrey", "No": "crimson"},
    )
    # fig = px.scatter(df, x="finalgrade", y="accompanying_complexity", trendline="ols")
    fig.update_layout(
        yaxis_title="Accompanying complexity score", xaxis_title="Final grade"
    )
    st.plotly_chart(fig, use_container_width=True)


def add_absences_plot(df: pd.DataFrame) -> None:
    fig_column_1, _ = st.columns(2)
    with fig_column_1:
        fig = px.histogram(
            df,
            x="absences",
            color="success",
            facet_col="success",
            color_discrete_map={"Yes": "lightslategrey", "No": "crimson"},
        )
        fig.update_layout(yaxis_title="Count", xaxis_title="Absences")
        st.plotly_chart(fig, use_container_width=True)


def build_sidebar_body_fiters(df):
    st.sidebar.markdown("# Filters")
    st.sidebar.markdown("## Personal informations")
    school_filters = _get_user_multiselect_filter_value(df, school_column)
    sex_filters = _get_user_multiselect_filter_value(df, sex_column)

    st.sidebar.markdown("## Accompaniment informations")
    absences_range = _get_user_slider_filter_value(df, "absences")
    studytime_filters = _get_user_multiselect_filter_value(df, studytime_column)
    walc_filters = _get_user_multiselect_filter_value(df, walc_column)

    st.sidebar.markdown("## Accompanying complexity score")
    accompanying_complexity_range = _get_user_slider_filter_value(
        df, "accompanying_complexity"
    )

    st.sidebar.markdown("## Final grade informations")
    final_grade_range = _get_user_slider_filter_value(df, "finalgrade")

    df = _filtre_data(
        df,
        school_filters,
        sex_filters,
        studytime_filters,
        walc_filters,
        absences_range,
        final_grade_range,
        accompanying_complexity_range,
    )

    return df


def _get_user_multiselect_filter_value(
    df: pd.DataFrame, column: CategoryColumn
) -> list:
    list_of_categories = sorted(df[f"{column.name}_category"].unique())
    filter_categories = []
    filter_categories = st.sidebar.multiselect(
        f"Select a {column.full_name} levels", list_of_categories
    )
    return filter_categories


def _get_user_slider_filter_value(
    df: pd.DataFrame, numerical_column_name: str
) -> tuple:
    filter_range = ()
    filter_range = st.sidebar.slider(
        f"Select a range of values of {numerical_column_name}",
        min_value=df[numerical_column_name].min(),
        max_value=df[numerical_column_name].max(),
        value=(df[numerical_column_name].min(), df[numerical_column_name].max()),
    )
    return filter_range


@st.cache_data
def _filtre_data(
    df: pd.DataFrame,
    school_filters: list,
    sex_filters: list,
    studytime_filters: list,
    walc_filters: list,
    absences_range: tuple,
    final_grade_range: tuple,
    accompanying_complexity_range: tuple,
):

    if len(school_filters) != 0:
        df = df[(df["school_category"].isin(school_filters))]

    if len(sex_filters) != 0:
        df = df[(df["sex_category"].isin(sex_filters))]

    if len(studytime_filters) != 0:
        df = df[(df["studytime_category"].isin(studytime_filters))]

    if len(walc_filters) != 0:
        df = df[(df["walc_category"].isin(walc_filters))]

    if len(absences_range) != 0:
        df = df[
            (df["absences"] >= absences_range[0])
            & (df["absences"] <= absences_range[1])
        ]

    if len(final_grade_range) != 0:
        df = df[
            (df["finalgrade"] >= final_grade_range[0])
            & (df["finalgrade"] <= final_grade_range[1])
        ]

    if len(accompanying_complexity_range) != 0:
        df = df[
            (df["accompanying_complexity"] >= accompanying_complexity_range[0])
            & (df["accompanying_complexity"] <= accompanying_complexity_range[1])
        ]

    return df
