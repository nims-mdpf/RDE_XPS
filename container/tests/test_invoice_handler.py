import json
import os
from pathlib import Path
import pytest

from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules_xps.invoice_handler import InvoiceWriter


RDE_CONFIG_YAML: dict = {
    'system': {
        'magic_variable': True,
        'save_thumbnail_image': True,
    },
    'xps': {
        'manufacturer': 'ulvac_phi',
        'no3dimage': False,
    }
}


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def resource_paths(temp_dir):
    return RdeOutputResourcePath(
        raw=Path('tests'),
        nonshared_raw=Path('tests'),
        rawfiles=(Path('tests'),),
        struct=Path('tests'),
        main_image=Path('tests'),
        other_image=Path('tests'),
        meta=Path('tests'),
        thumbnail=Path('tests'),
        logs=Path('tests'),
        invoice=temp_dir,
        invoice_schema_json=Path('tests/ulvac_phi/files/invoice.schema.json'),
        invoice_org=temp_dir / 'invoice.json'
    )


@pytest.fixture
def read_meta():
    """サンプルの出力メタデータ"""
    return {
        'AcqFileDate': '11/21/2017 08:32:31'
    }


def test_overwrite_invoice_measured_date(resource_paths, read_meta):
    """計測日上書き"""
    writer = InvoiceWriter(RDE_CONFIG_YAML)
    resource_paths.rawfiles = (Path('tests/ulvac_phi/files/XPS.spe'),)
    data_invoice = {
        'custom': {'measurement_measured_date': None},
        'sample': {'sampleId': '254cec7b-39ae-47f1-8afc-1cde0dfaadbb', 'names': ['']}
    }

    # 正常(標準)
    with open(resource_paths.invoice_org, 'w') as fw:
        json.dump(data_invoice, fw)
    writer.overwrite_invoice_measured_date(resource_paths.rawfiles[0].suffix, resource_paths, read_meta)
    with open(resource_paths.invoice.joinpath("invoice.json")) as fr:
        assert json.load(fr) == {
            'custom': {'measurement_measured_date': '2017-11-21'},
            'sample': {'sampleId': '254cec7b-39ae-47f1-8afc-1cde0dfaadbb', 'names': ['']}
        }

    # データ変更なし
    with open(resource_paths.invoice_org, 'w') as fw:
        json.dump(data_invoice, fw)
    writer.overwrite_invoice_measured_date(resource_paths.rawfiles[0].suffix, resource_paths, {})
    with open(resource_paths.invoice.joinpath("invoice.json")) as fr:
        assert json.load(fr) == {
            'custom': {'measurement_measured_date': None},
            'sample': {'sampleId': '254cec7b-39ae-47f1-8afc-1cde0dfaadbb', 'names': ['']}
        }

    if os.path.exists(resource_paths.invoice_org):
        os.remove(resource_paths.invoice_org)
