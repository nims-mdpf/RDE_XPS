import os
import glob

from pathlib import Path
import pandas as pd
import pytest

from rdetoolkit.models.rde2types import RdeOutputResourcePath
from modules_xps.ulvac_phi.pro.inputfile_handler import FileReader


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
        rawfiles=(Path('tests/ulvac_phi/files/XPS.pro'),),
        struct=Path('tests'),
        main_image=Path('tests'),
        other_image=Path('tests'),
        meta=Path('tests'),
        thumbnail=Path('tests'),
        logs=Path('tests'),
        invoice=temp_dir,
        invoice_schema_json=Path('tests'),
        invoice_org=temp_dir / 'invoice.json'
    )


@pytest.fixture
def read_meta():
    return {
        'Platform': 'PC',
        'Technique': 'XPS',
        'FileDesc': 'MIDATA001',
        'SoftwareVersion': 'SS 3.6.1.16',
        'InstrumentModel': 'PHI Quantera SXM',
        'AcqFilename': 'C:\\Datafiles\\Butsuzai\\XPS_PHI_QUANTERA_depth_1.pro',
        'FileDate': '2017 6 7',
        'AcqFileDate': '20170607',
        'ExperimentID': '20170606',
        'AnalyserWorkFcn': '4.250 eV',
        'PlatenID': 'MIDATA001',
        'PhotoFilename': 'MIDATA001.101.pho',
        'SourceAnalyserAngle': '45.0 d',
        'AnalyserSolidAngle': '0.38 sr',
        'SemFieldOfView': '0.0000000',
        'SputterRaster': '2.00 2.00 mm',
        'AnalyserMode': 'FAT',
        'NoDPDataCyc': '25',
        'NoPreSputterCyc': '1',
        'ProfSputterDelay': '5.0',
        'ProfXrayOffDuringSputter': 'no',
        'ProfSourceBlankDuringSputter': 'no',
        'ProfZalarHighAccuracyInterval': '20',
        'SampleRotation': 'off',
        'SputterMode': 'Alternating',
        'NoDepthReg': '3',
        'DepthCalDef': [
            ['1', 'Layer1', '1', '0.0000', '0.0000', 'Ar+', '6.00', '1.00', '6', "'1KV2x2'", '1.000', '150', '25.00', '0', '0', '719', '765', '39', '2.0', '2.0', '0.79', '-0.87', '0.00', '0.00', 'Ar'],
            ['2', 'Layer2', '7', '0.0000', '0.0000', 'Ar+', '6.00', '0.50', '12', "'1KV2x2'", '1.000', '150', '25.00', '0', '0', '719', '765', '39', '2.0', '2.0', '0.79', '-0.87', '0.00', '0.00', 'Ar'],
            ['3', 'Layer3', '19', '0.0000', '0.0000', 'Ar+', '6.00', '1.00', '6', "'1KV2x2'", '1.000', '150', '25.00', '0', '0', '719', '765', '39', '2.0', '2.0', '0.79', '-0.87', '0.00', '0.00', 'Ar']
        ],
        'NoSpectralReg': '2',
        'SpectralRegDef': [
            ['1', '1', 'O1s', '8', '201', '-0.1000', '543.0000', '523.0000', '542.0000', '524.0000', '0.240000', '112.00', 'AREA'],
            ['2', '1', 'Si2p', '14', '201', '-0.1000', '112.0000', '92.0000', '111.0000', '93.0000', '0.640000', '112.00', 'AREA']
        ],
        'SpectralRegDef2': [
            ['1', '20.0', '3', '0', '4', '1'],
            ['2', '20.0', '8', '0', '4', '1']
        ],
        'NoSpatialArea': '1',
        'SpatialAreaDef': '1 Point7 1 (-23673.4 8299.0 23281.0 45.0 0.0)',
        'SpatialAreaDesc': '1 #7 SiO2 25nm',
        'XraySource': 'Al 1486.6 mono',
        'XrayPower': '24.94 W',
        'XrayBeamDiameter': '100.0 um',
        'XRayHighPower': 'no',
        'EgunNeutMode': 'Neutralize',
        'NeutralizerCurrent': '20.0 uA',
        'NeutralizerEnergy': '1.40 V',
        'EgunNeutExtractor': '30.0 V',
        'StagePosition': '-23.9293 -6.9335 23.2812 45.0000 0.0044',
        'AutoIonNeut': 'yes',
        'Presputter': 'no',
        'ImageSizeXY': '100.0000 100.0000 Spot',
        'xlabelname': 'Binding Energy',
        'xlabelunit': 'eV',
        'xoption': 'reverse',
        'xlabel': 'Binding Energy (eV)',
        'ylabelname': 'Intensity',
        'ylabelunit': 'cps',
        'yoption': '',
        'ylabel': 'Intensity (cps)',
        'zlabelname': 'Sputter Time',
        'zlabelunit': 'min',
        'zoption': '',
        'zlabel': 'Sputter Time (min)'
    }


@pytest.fixture
def read_data():
    return pd.DataFrame({
        "Sputter Time (min)": ['0.0000', '1.0000', '2.0000', '3.0000', '4.0000', '5.0000', '6.0000', '6.5000', '7.0000', '7.5000', '8.0000', '8.5000', '9.0000', '9.5000', '10.0000', '10.5000', '11.0000', '11.5000', '12.0000', '13.0000', '14.0000', '15.0000', '16.0000', '17.0000', '18.0000'],
        "O1s_Intensity (arb.units)": ['88925.7344', '122217.8125', '125950.2109', '124797.8125', '126445.7344', '126408.9609', '125956.5625', '125266.2500', '125413.9609', '121401.1484', '116655.6250', '104749.8984', '78576.3516', '41802.5000', '14036.9795', '6139.1670', '1037.6041', '2302.2917', '0.0000', '359.3750', '1232.6041', '53.5417', '321.3542', '251.7708', '577.7083'],
        "Si2p_Intensity (arb.units)": ['27162.8125', '33092.1484', '33480.3516', '34007.4219', '33498.8672', '33854.0234', '33827.4219', '34128.2813', '33243.6719', '34090.7422', '33055.0781', '32977.3047', '33021.8750', '33490.2344', '33517.2266', '33545.5469', '32960.5859', '33315.2734', '33447.1875', '33582.9688', '33840.0781', '34365.4297', '34071.6797', '32135.1172', '32959.1797'],
    })


@pytest.fixture
def read_data_blocks():
    return [
        {'//Area Comment': '#7 SiO2 25nm', 'RegionNo': '1', 'AtomicName': 'O1s', 'Cycle': '25', 'XLabel': 'Binding Energy(eV),reverse', 'YLabel': 'Intensity(cps)', 'DataCount': '201', 'is_profile': False},
        {'//Area Comment': '#7 SiO2 25nm', 'RegionNo': '2', 'AtomicName': 'Si2p', 'Cycle': '25', 'XLabel': 'Binding Energy(eV),reverse', 'YLabel': 'Intensity(cps)', 'DataCount': '201', 'is_profile': False},
        {'//Area Comment': '#7 SiO2 25nm', 'AtomicName': 'O1s', 'XLabel': 'Sputter Time(min)', 'YLabel': 'Intensity', 'DataCount': '25', 'is_profile': True},
        {'//Area Comment': '#7 SiO2 25nm', 'AtomicName': 'Si2p', 'XLabel': 'Sputter Time(min)', 'YLabel': 'Intensity', 'DataCount': '25', 'is_profile': True}
    ]


@pytest.fixture
def read_data_atomics():
    # dataframeはすごく大きいので、ファイルを読み込んで展開する。
    return [
        {
            "file_cps": Path('tests/XPS_O1s.csv'),
            "file_counts": Path('tests/XPS_O1s_count.csv'),
        },
        {
            "file_cps": Path('tests/XPS_Si2p.csv'),
            "file_counts": Path('tests/XPS_Si2p_count.csv'),
        },
    ]


def test_read(resource_paths, read_meta, read_data, read_data_blocks, read_data_atomics):
    """ファイル読み込み"""

    # 正常(標準)
    reader = FileReader(RDE_CONFIG_YAML)
    reader.convert_raw2txt_with_wine(resource_paths)
    meta, data, data_blocks, data_atomics = reader.read(resource_paths)

    assert meta == read_meta
    pd.testing.assert_frame_equal(data, read_data, check_dtype=False)
    assert data_blocks == read_data_blocks
    assert data_atomics[0]['file_cps'] == read_data_atomics[0]['file_cps']
    assert data_atomics[0]['file_counts'] == read_data_atomics[0]['file_counts']
    assert data_atomics[1]['file_cps'] == read_data_atomics[1]['file_cps']
    assert data_atomics[1]['file_counts'] == read_data_atomics[1]['file_counts']
    # ハードコーディングがすごく大変なので、ファイルを読み込んで展開して比較する
    read_data_atomics_0_df_cps = pd.read_csv('tests/ulvac_phi/files/df_cps_0.csv', dtype=object)
    pd.testing.assert_frame_equal(data_atomics[0]['df_cps'], read_data_atomics_0_df_cps, check_dtype=False)
    read_data_atomics_0_df_counts = pd.read_csv('tests/ulvac_phi/files/df_counts_0.csv', dtype=object)
    pd.testing.assert_frame_equal(data_atomics[0]['df_counts'], read_data_atomics_0_df_counts, check_dtype=False)
    read_data_atomics_1_df_cps = pd.read_csv('tests/ulvac_phi/files/df_cps_1.csv', dtype=object)
    pd.testing.assert_frame_equal(data_atomics[1]['df_cps'], read_data_atomics_1_df_cps, check_dtype=False)
    read_data_atomics_1_df_counts = pd.read_csv('tests/ulvac_phi/files/df_counts_1.csv', dtype=object)
    pd.testing.assert_frame_equal(data_atomics[1]['df_counts'], read_data_atomics_1_df_counts, check_dtype=False)

    # 異常(データなし)
    # バイナリデータが編集できないので、スキップする

    # 後始末
    files_to_delete = glob.glob(os.path.join('tests', '*.log'))
    for file in files_to_delete:
        os.remove(file)
    os.remove('tests/XPS.txt')


def test_convert_raw2txt_with_wine(resource_paths):
    """フォーマット変換"""

    # 正常(標準)
    reader = FileReader(RDE_CONFIG_YAML)
    reader.convert_raw2txt_with_wine(resource_paths)
    assert os.path.exists('tests/XPS.txt')

    # 後始末
    files_to_delete = glob.glob(os.path.join('tests', '*.log'))
    for file in files_to_delete:
        os.remove(file)
    os.remove('tests/XPS.txt')
