import pandas as pd
import numpy as np
import streamlit as st


from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_selector as selector
from sklearn.preprocessing import OrdinalEncoder
from sklearn.decomposition import PCA
from dataclasses import dataclass


@dataclass
class CategoryColumn:
    name: str
    full_name: str
    categories_mapping: dict


school_column = CategoryColumn(
    name="school",
    full_name="School",
    categories_mapping={"GP": "Gabriel Pereira", "MS": "Mousinho da Silveira"},
)

sex_column = CategoryColumn(
    name="sex", full_name="Gender", categories_mapping={"F": "Female", "M": "Male"}
)

address_column = CategoryColumn(
    name="address",
    full_name="Address type",
    categories_mapping={"U": "Urban", "R": "Rural"},
)

medu_column = CategoryColumn(
    name="medu",
    full_name="Mother's education",
    categories_mapping={
        0: "No education",
        1: "Primary education (4th grade)",
        2: "5th to 9th grade",
        3: "Secondary education",
        4: "Higher education",
    },
)

fedu_column = CategoryColumn(
    name="fedu",
    full_name="Father's education",
    categories_mapping={
        0: "No education",
        1: "Primary education (4th grade)",
        2: "5th to 9th grade",
        3: "Secondary education",
        4: "Higher education",
    },
)

studytime_column = CategoryColumn(
    name="studytime",
    full_name="Weekly study time ",
    categories_mapping={
        1: "<2 hours",
        2: "2 to 5 hours",
        3: "5 to 10 hours",
        4: "4 - >10 hours",
    },
)

walc_column = CategoryColumn(
    name="walc",
    full_name="Weekend alcohol consumption",
    categories_mapping={
        1: "Very low",
        2: "Low",
        3: "Medium",
        4: "High",
        5: "Very high",
    },
)

failuers_column = CategoryColumn(
    name="failures",
    full_name="Past class failure",
    categories_mapping={
        0: "No",
        1: "Yes",
        2: "Yes",
        3: "Yes",
    },
)


def read_students_data(url: str) -> pd.DataFrame:
    students_df = pd.read_csv(url)
    return students_df


@st.cache_data
def process_students_data(raw_students_df: pd.DataFrame) -> pd.DataFrame:
    students_df = raw_students_df.copy()
    students_df.columns = students_df.columns.str.lower()
    pca_features_names = ["studytime", "walc", "absences"]
    students_df.loc[:, "success"] = (students_df.loc[:, "finalgrade"] >= 10).replace(
        {True: "Yes", False: "No"}
    )
    students_df.loc[
        :, "accompanying_complexity"
    ] = _score_accompanying_complexity_with_pca(students_df[pca_features_names])
    for categorical_column in [
        school_column,
        sex_column,
        address_column,
        medu_column,
        fedu_column,
        studytime_column,
        walc_column,
        failuers_column,
    ]:
        students_df.loc[:, f"{categorical_column.name}_category"] = students_df.loc[
            :, categorical_column.name
        ].replace(categorical_column.categories_mapping)
    return students_df


def _get_categorical_features(df: pd.DataFrame) -> list:
    categorical_columns_selector = selector(dtype_include=object)
    categorical_features = categorical_columns_selector(df)
    return categorical_features


def _normalize_score(scores: np.array) -> np.array:
    return np.floor((scores - np.min(scores)) / (np.max(scores) - np.min(scores)) * 100)


def _buil_pca_pipeline(df: pd.DataFrame) -> Pipeline:
    categorical_features = _get_categorical_features(df)

    categorical_transformer = Pipeline(
        steps=[
            (
                "encoder",
                OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_transformer, categorical_features),
        ],
        remainder="passthrough",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("scaling", StandardScaler()),
            ("pca", PCA(n_components=2, svd_solver="full")),
        ]
    )
    return pipeline


@st.cache_resource
def _score_accompanying_complexity_with_pca(df: pd.DataFrame) -> np.array:
    pipeline = _buil_pca_pipeline(df)
    pca_coordinates = pipeline.fit_transform(df)
    scores = _normalize_score(pca_coordinates[:, 0])
    return scores
