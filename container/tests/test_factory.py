import csv
import os
import pytest
from pathlib import Path
import yaml

from rdetoolkit.exceptions import StructuredError

from modules_xps.factory import XpsFactory, get_classes

from modules_xps.scienta_omicron.vms.graph_handler import GraphPlotter as VmsGraphPlotter
from modules_xps.scienta_omicron.vms.inputfile_handler import FileReader as VmsFileReader
from modules_xps.scienta_omicron.vms.meta_handler import MetaParser as VmsMetaParser
from modules_xps.ulvac_phi.meta_handler import MetaParser as UlvacPhiMetaParser
from modules_xps.ulvac_phi.pro.graph_handler import GraphPlotter as ProGraphPlotter
from modules_xps.ulvac_phi.pro.inputfile_handler import FileReader as ProFileReader
from modules_xps.ulvac_phi.spe.graph_handler import GraphPlotter as SpeGraphPlotter
from modules_xps.ulvac_phi.spe.inputfile_handler import FileReader as SpeFileReader


INVOICE_FILE = Path('tests/scienta_omicron/files/invoice.json')
INPUT_FILE = Path('tests/scienta_omicron/files/XPS.vms')
RDE_CONFIG_YAML: dict = {
    'system': {
        'magic_variable': True,
        'save_thumbnail_image': True,
    },
    'xps': {
        'manufacturer': 'scienta_omicron',
        'no3dimage': False,
    }
}

DEFAULT_VALUE = [
    ["key", "value"],
    ["common.data_origin", "experiments"],
    ["common.technical_category", "measurement"],
    ["measurement.method_category", "分光法"],
    ["measurement.method_sub_category", "X線光電子分光法"],
    ["measurement.analysis_field", "化学状態"],
    ["measurement.measurement_environment", "真空中"]
]


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


def test_get_config(temp_dir):
    """コンフィグ取得"""

    # 正常
    with open(temp_dir / 'rdeconfig.yaml', 'w') as fw:
        yaml.dump(RDE_CONFIG_YAML, fw, default_flow_style=False)
    assert XpsFactory.get_config(INVOICE_FILE, temp_dir) == RDE_CONFIG_YAML

    # 設定ファイルなし
    if os.path.exists(temp_dir / 'rdeconfig.yaml'):
        os.remove(temp_dir / 'rdeconfig.yaml')
    with pytest.raises(StructuredError) as e:
        XpsFactory.get_config(INVOICE_FILE, temp_dir)
    assert str(e.value).startswith("File not found")

    # 設定ファイル読み込みエラー
    with open(temp_dir / 'rdeconfig.yaml', 'w') as fe:
        fe.write("!!python/name:module.function")
    with pytest.raises(StructuredError) as e:
        XpsFactory.get_config(INVOICE_FILE, temp_dir)
    assert str(e.value).startswith("Invalid configuration file")


def test_get_objects(temp_dir):
    """使用クラス取得"""

    # 正常
    with open(temp_dir / 'rdeconfig.yaml', 'w') as fw:
        yaml.dump(RDE_CONFIG_YAML, fw, default_flow_style=False)
    with open(temp_dir / 'default_value.csv', 'w') as cfw:
        csv.writer(cfw).writerows(DEFAULT_VALUE)
    metadata_def, module, suffix = XpsFactory.get_objects(INPUT_FILE, temp_dir, RDE_CONFIG_YAML)
    assert metadata_def.name == "metadata-def.json"
    assert str(module.invoice_writer).startswith('<modules_xps.invoice_handler.InvoiceWriter')
    assert str(module.file_reader).startswith('<modules_xps.scienta_omicron.vms.inputfile_handler.FileReader')
    assert str(module.meta_parser).startswith('<modules_xps.scienta_omicron.vms.meta_handler.MetaParser')
    assert str(module.graph_plotter).startswith('<modules_xps.scienta_omicron.vms.graph_handler.GraphPlotter')
    assert str(module.structured_processor).startswith('<modules_xps.structured_handler.StructuredDataProcessor')
    assert suffix == ".vms"

    # 拡張子対象外
    with pytest.raises(StructuredError) as e:
        XpsFactory.get_objects(Path('tests/scienta_omicron/files/XPS.raw'), temp_dir, RDE_CONFIG_YAML)
    assert str(e.value) == "Format Error: Input data extension is incorrect: .raw"


@pytest.mark.parametrize(
    ["manufacturer", "suffix", "expected"],
    [
        ("scienta_omicron", ".vms", (VmsFileReader, VmsMetaParser, VmsGraphPlotter)),
        ("ulvac_phi", ".spe", (SpeFileReader, UlvacPhiMetaParser, SpeGraphPlotter)),
        ("ulvac_phi", ".pro", (ProFileReader, UlvacPhiMetaParser, ProGraphPlotter)),
        ("ulvac_phi", ".ang", (ProFileReader, UlvacPhiMetaParser, ProGraphPlotter)),
    ]
)
def test_get_classes(manufacturer, suffix, expected):
    """使用クラス取得"""

    # 正常
    assert get_classes(manufacturer, suffix) == expected

    # エラー
    with pytest.raises(StructuredError) as e:
        get_classes("unknown_manufacturer", ".raw")
    assert str(e.value) == "Unsupported combination of manufacturer 'unknown_manufacturer' and file extension '.raw'"
