from pandas.testing import assert_frame_equal


from app.utils.utils import process_students_data, read_students_data
from tests.fixtures.data import *


STUDENTS_DATA_TEST_PATH = "./tests/fixtures/student_data.csv"


def test_read_students_data(raw_students_df):
    actual_df = read_students_data(STUDENTS_DATA_TEST_PATH)
    assert_frame_equal(actual_df, raw_students_df, check_like=True)


def test_process_students_data(raw_students_df, processed_students_df):
    actual_df = process_students_data(raw_students_df)
    assert_frame_equal(actual_df, processed_students_df, check_like=True)
