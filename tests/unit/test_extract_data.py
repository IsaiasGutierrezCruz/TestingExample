from example.extract_data import Repository
from example.constants import URL_FILE_WALMART_DATA, URL_FILE_STORE_INFO
import pytest
import pandas as pd
from pytest_mock import MockerFixture


@pytest.fixture(scope="class")
def repository() -> Repository:
    return Repository(
        path="",
        url_walmart_data=URL_FILE_WALMART_DATA,
        url_store_info=URL_FILE_STORE_INFO,
    )


@pytest.mark.raw_data_tests
class TestRepository:
    def test_create_repository_obj(self) -> None:
        repo = Repository(
            path="",
            url_walmart_data=URL_FILE_WALMART_DATA,
            url_store_info=URL_FILE_STORE_INFO,
        )
        assert repo is not None
        assert repo.path == ""
        assert repo.url_walmart_data == URL_FILE_WALMART_DATA
        assert repo.url_store_info == URL_FILE_STORE_INFO

    def test_get_walmart_data_download(self) -> None:
        repo = Repository(
            path="",
            url_walmart_data=URL_FILE_WALMART_DATA,
            url_store_info=URL_FILE_STORE_INFO,
        )
        data = repo.get_walmart_data()
        assert data.empty is False

    def test_get_walmart_data(
        self, repository: Repository, mocker: MockerFixture
    ) -> None:
        url_to_validate = URL_FILE_WALMART_DATA
        url_to_validate = (
            "https://drive.google.com/uc?id=" + url_to_validate.split("/")[-2]
        )
        mock_read_csv = mocker.patch(
            "example.extract_data.pd.read_csv", return_value=pd.DataFrame()
        )

        data = repository.get_walmart_data()
        mock_read_csv.assert_called_once_with(url_to_validate)
        assert data.empty is True

    def test_get_store_info_data(
        self, repository: Repository, mocker: MockerFixture
    ) -> None:
        url_to_validate = URL_FILE_STORE_INFO
        url_to_validate = (
            "https://drive.google.com/uc?id=" + url_to_validate.split("/")[-2]
        )
        mock_read_csv = mocker.patch(
            "example.extract_data.pd.read_csv", return_value=pd.DataFrame()
        )

        data = repository.get_store_info_data()
        mock_read_csv.assert_called_once_with(url_to_validate)
        assert data.empty is True

    def test_get_merged_data(
        self, repository: Repository, mocker: MockerFixture
    ) -> None:
        mock_get_walmart_data = mocker.patch.object(
            repository,
            "get_walmart_data",
            return_value=pd.DataFrame(
                columns=[
                    "Store",
                    "Date",
                    "Weekly_Sales",
                    "Holiday_Flag",
                    "Temperature",
                    "Fuel_Price",
                    "CPI",
                    "Unemployment",
                ]
            ),
        )
        mock_get_store_info_data = mocker.patch.object(
            repository,
            "get_store_info_data",
            return_value=pd.DataFrame(columns=["Store", "Code", "City"]),
        )
        data = repository.get_merged_data()
        mock_get_walmart_data.assert_called_once()
        mock_get_store_info_data.assert_called_once()
        assert data.empty is True

    def test_store_data(self, repository: Repository, mocker: MockerFixture) -> None:
        mock_data = mocker.MagicMock()
        mock_data.to_csv = mocker.MagicMock()
        repository.save_data(mock_data)
        mock_data.to_csv.assert_called_once_with(repository.path, index=False)

    def test_store_data_2(
        self, tmp_path, repository: Repository
    ) -> None:
        d = tmp_path 
        repository.path = d / "data.csv"
        repository.save_data(pd.DataFrame(columns=["a", "b"]))
        df = pd.read_csv(repository.path)
        assert df.empty is True
