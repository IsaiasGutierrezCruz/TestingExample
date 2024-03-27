import pandera as pa
from pandera.typing import Series
from pandera.engines import pandas_engine

class RawDataWalmartData(pa.SchemaModel):
    Store : Series[pa.Int64]
    # Date : Series[pandas_engine.DateTime] = pa.Field(
    #     dtype_kwargs={"to_datetime_kwargs": {"format": "%d-%m-%Y"}}
    # )
    Date: Series[pa.DateTime]
    Weekly_Sales: Series[pa.Float]
    Holiday_Flag: Series[pa.Int]
    Temperature: Series[pa.Float]
    Fuel_Price: Series[pa.Float]
    CPI: Series[pa.Float]
    Unemployment: Series[pa.Float]

    class Config:
        coerce = True
        strict = False


class RawDataWalmartInfo(pa.SchemaModel): 
    Store : Series[pa.Int64]
    Code : Series[pa.String] = pa.Field(nullable=True)
    City : Series[pa.String]= pa.Field(nullable=True)

    class Config:
        coerce = True
        strict = False


class RawDataMerged(RawDataWalmartData, RawDataWalmartInfo):
    class Config:
        coerce = True
        strict = False