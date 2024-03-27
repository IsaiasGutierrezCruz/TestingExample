from pathlib import Path
import pytest
import pandas as pd
from example.calculate_features import calculate_weekly_sales_last_n_days
from example.constants import LAST_DAY
from example.schemas import RawDataMerged

test_path = Path(__file__).resolve().parent

@pytest.fixture(scope="class")
def raw_data() -> pd.DataFrame:
    df =  pd.read_csv(test_path / 'test_data'/ "raw_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

@pytest.fixture(scope="class")
def output_features() -> pd.DataFrame:
    return pd.read_csv(test_path / 'test_data'/ "expected_data.csv", index_col=0)

class TestCalculateFeatures:
    @pytest.mark.parametrize(
        "number_of_days", [30, 60, 90]
    )
    def test_calculate_weekly_sales_last_n_days(self, number_of_days, raw_data: pd.DataFrame, output_features: pd.DataFrame) -> None:
        feat_name = f"SALES_LAST_{number_of_days}_DAYS"
        expected_output = output_features[f'expected_{feat_name}']

        sales = calculate_weekly_sales_last_n_days(raw_data, number_of_days, LAST_DAY)
        # assert sales.equals(output_features)
        pd.testing.assert_series_equal(sales, expected_output, check_names=False)
