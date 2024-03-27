import pandas as pd
from pandera.typing import DataFrame
from example.schemas import RawDataWalmartData
import pandera as pa

class Repository:
    def __init__(self, path, url_walmart_data, url_store_info):
        self.path = path
        self.url_walmart_data = url_walmart_data
        self.url_store_info = url_store_info

    # @pa.check_types()
    # def get_walmart_data(self) -> DataFrame[RawDataWalmartData]:
    def get_walmart_data(self) -> DataFrame:
        url = self.url_walmart_data
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]
        data = pd.read_csv(url)
        return data

    def get_store_info_data(self) -> pd.DataFrame:
        url = self.url_store_info
        url='https://drive.google.com/uc?id=' + url.split('/')[-2]
        data = pd.read_csv(url)
        return data

    def get_merged_data(self) -> pd.DataFrame:
        df_walmart = self.get_walmart_data()
        df_store_info = self.get_store_info_data()
        return df_walmart.merge(
            df_store_info,
            how='left',
            on='Store'
        )

    def save_data(self, data: pd.DataFrame) -> None:
        data.to_csv(self.path, index=False)