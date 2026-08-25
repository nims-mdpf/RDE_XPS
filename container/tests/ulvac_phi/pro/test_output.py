import os
import shutil
from typing import List, Union


def setup_inputdata_folder(inputdata_name: Union[str, List[str]], manufacturer: str, case_name: str):
    """テスト実行のためのヘルパー関数
    テスト用でdataフォルダ群の作成とrawファイルの準備

    Args:
        inputdata_name (Union[str, List[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "inputdata"), exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "inputdata", manufacturer, case_name
    )
    if isinstance(inputdata_name, List):
        for item in inputdata_name:
            shutil.copy(
                os.path.join(inputdata_original_path, item),
                os.path.join(destination_path, "inputdata"),
            )
    else:
        shutil.copy(
            os.path.join(inputdata_original_path, inputdata_name),
            os.path.join(destination_path, "inputdata"),
        )
    shutil.copy(
        os.path.join(inputdata_original_path, "invoice.json"),
        os.path.join(destination_path, "invoice"),
    )

    # tasksupport
    os.makedirs(os.path.join(destination_path, "tasksupport"), exist_ok=True)
    tasksupport_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))),
        "template",
        manufacturer,
        "tasksupport",
    )
    print(tasksupport_original_path)
    shutil.copy(
        os.path.join(tasksupport_original_path, "invoice.schema.json"),
        os.path.join(destination_path, "tasksupport"),
    )
    shutil.copy(
        os.path.join(tasksupport_original_path, "metadata-def.json"),
        os.path.join(destination_path, "tasksupport"),
    )
    shutil.copy(
        os.path.join(tasksupport_original_path, "default_value.csv"),
        os.path.join(destination_path, "tasksupport"),
    )
    shutil.copy(
        os.path.join(tasksupport_original_path, "rdeconfig.yaml"),
        os.path.join(destination_path, "tasksupport"),
    )


class TestOutputCase1:
    """case1
    単一ファイルのテスト: XPS.pro
    """

    inputdata: Union[str, List[str]] = "XPS.pro"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata, "ulvac_phi", "pro")

    def test_raw_data(self, setup_main, data_path):
        assert os.path.exists(os.path.join(data_path, "nonshared_raw", "XPS.pro"))

    def test_main_image(self, data_path):
        assert os.path.exists(os.path.join(data_path, "main_image", "XPS.png"))

    def test_structured(self, data_path):
        assert os.path.exists(os.path.join(data_path, "structured", "XPS.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS.txt"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_O1s_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_O1s.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Si2p_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Si2p.csv"))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "XPS.png"))

    def test_meta(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))


class TestOutputCase2:
    """case2
    単一ファイルのテスト: XPS.ang
    3Dグラフあり
    """

    inputdata: Union[str, List[str]] = "XPS.ang"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata, "ulvac_phi", "ang")

    def test_raw_data(self, setup_main, data_path):
        assert os.path.exists(os.path.join(data_path, "nonshared_raw", "XPS.ang"))

    def test_main_image(self, data_path):
        assert os.path.exists(os.path.join(data_path, "main_image", "XPS.png"))

    def test_structured(self, data_path):
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Al1s_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Al1s.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Hf3d3_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Hf3d3.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Hf3d5_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Hf3d5.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_O1s_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_O1s.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Si1s_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Si1s.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Survey_count.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS_Survey.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS.csv"))
        assert os.path.exists(os.path.join(data_path, "structured", "XPS.txt"))

    def test_other_image(self, data_path):
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Al1s_3d.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Al1s.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Hf3d3_3d.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Hf3d3.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Hf3d5_3d.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Hf3d5.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_O1s_3d.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_O1s.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Si1s_3d.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Si1s.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_speall_3d.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_speall_count.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_speall.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Survey_3d.png"))
        assert os.path.exists(os.path.join(data_path, "other_image", "XPS_Survey.png"))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "XPS.png"))

    def test_meta(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))
