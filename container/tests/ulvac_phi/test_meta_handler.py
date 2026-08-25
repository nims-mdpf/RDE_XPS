import json
import pytest

from modules_xps.ulvac_phi.meta_handler import MetaParser
from rdetoolkit.rde2util import Meta


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
def metadata_def(tmp_path):
    """metadata-def.json"""
    metadata_def = {
        "measurement.specimen": {
            "name": {
                "ja": "試料",
                "en": "Specimen"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.reference": {
            "name": {
                "ja": "参考文献",
                "en": "Reference"
            },
            "schema": {
                "type": "string"
            }
        },
        "operator_identifier": {
            "name": {
                "ja": "測定者",
                "en": "Operator identifier"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "Operator"
        },
        "operator_affiliation_identifier": {
            "name": {
                "ja": "測定者所属機関",
                "en": "Operator affiliation identifier"
            },
            "schema": {
                "type": "string"
            }
        },
        "institution_idendfier": {
            "name": {
                "ja": "所属施設など",
                "en": "Institution idendfier"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "Institution"
        },
        "measurement_technique": {
            "name": {
                "ja": "測定手法",
                "en": "Measurement Technique"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "Technique"
        },
        "measurement_instrument": {
            "name": {
                "ja": "測定装置",
                "en": "Measurement Instrument"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "InstrumentModel"
        },
        "experiment_id": {
            "name": {
                "ja": "測定内容識別ID",
                "en": "Experiment ID"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "ExperimentID"
        },
        "file_property": {
            "name": {
                "ja": "測定ファイル_属性",
                "en": "File Property"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "FileType"
        },
        "xray_source": {
            "name": {
                "ja": "X線源",
                "en": "Xray Source"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "XraySource"
        },
        "xray_power": {
            "name": {
                "ja": "X線パワー",
                "en": "Xray Power"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "XrayPower",
            "unit": "W"
        },
        "analysis_source_label": {
            "name": {
                "ja": "分析線源ラベル",
                "en": "analysis source label"
            },
            "schema": {
                "type": "string"
            }
        },
        "analysis_source_characteristics_energy": {
            "name": {
                "ja": "分析線源特性エネルギー",
                "en": "analysis source characteristics energy"
            },
            "schema": {
                "type": "string"
            },
            "unit": "eV"
        },
        "analysis_source_beam_width_x": {
            "name": {
                "ja": "分析線源ビーム幅x",
                "en": "analysis source beam width x"
            },
            "schema": {
                "type": "string"
            },
            "unit": "um"
        },
        "analysis_source_beam_width_y": {
            "name": {
                "ja": "分析線源ビーム幅y",
                "en": "analysis source beam width y"
            },
            "schema": {
                "type": "string"
            },
            "unit": "um"
        },
        "xray_beam_diameter": {
            "name": {
                "ja": "X線ビーム径",
                "en": "Xray Beam Diameter"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "XrayBeamDiameter",
            "unit": "um"
        },
        "analysis_source_polar_angle_of_incidence": {
            "name": {
                "ja": "分析線源入射極角",
                "en": "analysis source polar angle of incidence"
            },
            "schema": {
                "type": "string"
            },
            "unit": "deg"
        },
        "analysis_source_azimuth": {
            "name": {
                "ja": "分析線源方位角",
                "en": "analysis source azimuth"
            },
            "schema": {
                "type": "string"
            },
            "unit": "deg"
        },
        "analyzer_mode": {
            "name": {
                "ja": "分析器分光動作モード",
                "en": "Analyzer Mode"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "AnalyserMode"
        },
        "analyzer_work_function": {
            "name": {
                "ja": "分析器仕事関数",
                "en": "Analyzer Work Function"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "AnalyserWorkFcn",
            "unit": "eV"
        },
        "xray_analyzer_angle": {
            "name": {
                "ja": "照射X線 分析器間角度",
                "en": "Xray Analyzer Angle"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SourceAnalyserAngle",
            "unit": "deg"
        },
        "analyzer_solid_angle": {
            "name": {
                "ja": "分析器取込立体角度",
                "en": "Analyzer Solid Angle"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "AnalyserSolidAngle",
            "unit": "sr"
        },
        "signal_mode": {
            "name": {
                "ja": "信号モード",
                "en": "signal mode"
            },
            "schema": {
                "type": "string"
            }
        },
        "analysis_region": {
            "name": {
                "ja": "測定領域設定",
                "en": "Analysis Region"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "ImageSizeXY"
        },
        "analysis_width_x": {
            "name": {
                "ja": "X成分",
                "en": "Analysis Width_x"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "ImageSizeXY",
            "unit": "um"
        },
        "analysis_width_y": {
            "name": {
                "ja": "Y成分",
                "en": "Analysis Width_y"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "ImageSizeXY",
            "unit": "um"
        },
        "sputtering_ion_energy": {
            "name": {
                "ja": "イオンスパッタリングビームエネルギー",
                "en": "Sputtering Ion Energy"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SputterEnergy",
            "unit": "kV"
        },
        "sputtering_raster_area": {
            "name": {
                "ja": "スパッタリングラスター範囲",
                "en": "Sputtering Raster Area"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SputterRaster",
            "unit": "mm"
        },
        "specimen_stage_rotation_setting_during_sputtering": {
            "name": {
                "ja": "スパッタ時試料台回転設定",
                "en": "Specimen Stage Rotation Setting During Sputtering"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SampleRotation"
        },
        "depth_profiling_preset_layer_number": {
            "name": {
                "ja": "デプスプロファイルスパッタ条件設定レイヤー数",
                "en": "Depth Profiling Preset Layer Number"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "NoDepthReg"
        },
        "time_from_sputtering_to_measurement": {
            "name": {
                "ja": "スパッタ後測定開始待機時間",
                "en": "Time from Sputtering to Measurement"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "ProfSputterDelay",
            "unit": "s"
        },
        "total_cycle_number": {
            "name": {
                "ja": "総サイクル数",
                "en": "Total Cycle Number"
            },
            "schema": {
                "type": "string"
            }
        },
        "cycle_control_preset": {
            "name": {
                "ja": "サイクル制御設定",
                "en": "Cycle Control Preset"
            },
            "schema": {
                "type": "string"
            }
        },
        "software_preset_sputtering_layer_name": {
            "name": {
                "ja": "ソフトウェア上設定レイヤー名",
                "en": "Software Preset Sputtering Layer Name"
            },
            "schema": {
                "type": "string"
            },
            "variable": 1
        },
        "sputtering_layer_preset_interval_time": {
            "name": {
                "ja": "スパッタレイヤー設定スパッタインターバル時間",
                "en": "Sputtering Layer Preset Interval Time"
            },
            "schema": {
                "type": "string"
            },
            "unit": "min",
            "variable": 1
        },
        "sputtering_layer_preset_cycle_number": {
            "name": {
                "ja": "スパッタレイヤー設定サイクル数",
                "en": "Sputtering Layer Preset Cycle Number"
            },
            "schema": {
                "type": "string"
            },
            "variable": 1
        },
        "sample_normal_polar_angle_of_tilt": {
            "name": {
                "ja": "試料法線極角",
                "en": "sample normal polar angle of tilt"
            },
            "schema": {
                "type": "string"
            },
            "unit": "deg"
        },
        "sample_normal_tilt_azimuth": {
            "name": {
                "ja": "試料法線方位角",
                "en": "sample normal tilt azimuth"
            },
            "schema": {
                "type": "string"
            },
            "unit": "deg"
        },
        "sample_rotation_angle": {
            "name": {
                "ja": "試料回転角",
                "en": "sample rotation angle"
            },
            "schema": {
                "type": "string"
            },
            "unit": "deg"
        },
        "peak_name": {
            "name": {
                "ja": "ピーク名",
                "en": "Peak Name"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef",
            "variable": 1
        },
        "transitions": {
            "name": {
                "ja": "スペクトルの元素種の遷移",
                "en": "Transitions"
            },
            "schema": {
                "type": "string"
            },
            "variable": 1
        },
        "pass_energy": {
            "name": {
                "ja": "パスエネルギー値",
                "en": "Pass Energy"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef",
            "unit": "eV",
            "variable": 1
        },
        "abscissa_start": {
            "name": {
                "ja": "横軸の起点",
                "en": "Abscissa start"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef",
            "unit": "eV",
            "variable": 1
        },
        "abscissa_end": {
            "name": {
                "ja": "横軸の終点",
                "en": "Abscissa end"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef",
            "unit": "eV",
            "variable": 1
        },
        "abscissa_increment": {
            "name": {
                "ja": "エネルギーステップ幅",
                "en": "Abscissa increment"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef",
            "unit": "eV",
            "variable": 1
        },
        "collection_time": {
            "name": {
                "ja": "シグナル収集時間（データ1点当たりの溜め込み時間）",
                "en": "Collection time"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef",
            "unit": "s",
            "variable": 1
        },
        "measurement_acquisition_number_per_peak_sweep": {
            "name": {
                "ja": "スイープ毎繰返し測定回数",
                "en": "Measurement Acquisition Number Per Peak Sweep"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SurvNumCycles"
        },
        "peak_sweep_number": {
            "name": {
                "ja": "ピークスイープ積算回数",
                "en": "Peak Sweep Number"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef2",
            "variable": 1
        },
        "total_acquisition_number": {
            "name": {
                "ja": "総積算回数",
                "en": "Total Acquisition Number"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpectralRegDef2",
            "variable": 1
        },
        "comment": {
            "name": {
                "ja": "コメント",
                "en": "Comment"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "SpatialAreaDesc"
        }
    }
    metadata_def_path = tmp_path / "metadata-def.json"
    with open(metadata_def_path, mode="w", encoding="utf-8") as f:
        json.dump(metadata_def, f)
    return metadata_def_path


@pytest.fixture
def default_value():
    return {
        'common.data_origin': 'experiments',
        'common.technical_category': 'measurement',
        'measurement.method_category': '分光法',
        'measurement.method_sub_category': 'X線光電子分光法',
        'measurement.analysis_field': '',
        'measurement.measurement_environment': '真空中',
    }


@pytest.fixture
def class_meta(metadata_def):
    return Meta(metadata_def)


@pytest.fixture
def set_meta():
    """入力メタデータ"""
    return {
        'Platform': 'PC',
        'Technique': 'XPS',
        'FileDesc': 'WWOHF3_D1_(WWOHF3_D1)_(5, 20221214onBa8AlxSi46-x, B-3)_(Profile(Ba3d5 112.00 0.200, F1s 112.00 0.200, O1s 112.00 0.200, C1s 112.00 0.200, Si2p 112.00 0.200, Al2p 112.00 0.200))',
        'SoftwareVersion': 'SS 4.2.0.28',
        'InstrumentModel': 'PHI Quantes',
        'FileDate': '123 12 14',
        'AcqFileDate': '20230720',
        'AcqFilename': 'C:\\Datafiles\\User\\Butsuzai_Taro\\20230719\\TempWWOHF3_D1.116_1.pro',
        'ExperimentID': '20230719',
        'StagePosition': '-19.8848 -21.6213 24.0329 45.0000 359.9979',
        'PhotoFilename': 'WWOHF3_D1.101.pho',
        'XraySource': 'Al 1486.6 mono',
        'XrayPower': '25.60 W',
        'XrayBeamDiameter': '100.0 um',
        'XRayHighPower': 'no',
        'SourceAnalyserAngle': '45.0 d',
        'AnalyserSolidAngle': '0.4 sr',
        'AnalyserMode': 'FAT',
        'AnalyserWorkFcn': '4.5 eV',
        'SputterRaster': '0.0 0.0 mm',
        'PreAcqSputterTime': '0',
        'PreAcqSputterRate': '0.0',
        'NoSpectralReg': '1',
        'SpectralRegDef': [['1', '6', 'Al2p', '13', '91', '-0.2000', '66.00000', '84.00000', '66.00000', '84.00000', '0.960000', '112.00', 'AREA']],
        'SpectralRegDef2': [['1', '18.000000', '12', '0', '4', '0']],
        'NoSpatialArea': '1',
        'SpatialAreaDef': '1 5 1 (-20060.0 22644.2 24033.0 45.0 360.0)',
        'SpatialAreaDesc': '1 B-3',
        'ImageSizeXY': '100.0000 100.0000 Spot',
        'xlabelname': 'Binding Energy',
        'xlabelunit': 'eV',
        'xoption': 'reverse',
        'xlabel': 'Binding Energy (eV)',
        'ylabelname': 'Intensity',
        'ylabelunit': 'cps',
        'yoption': '',
        'ylabel': 'Intensity (cps)',
    }


@pytest.fixture
def read_const_meta():
    return {
        'Platform': 'PC',
        'Technique': 'XPS',
        'FileDesc': 'WWOHF3_D1_(WWOHF3_D1)_(5, 20221214onBa8AlxSi46-x, B-3)_(Profile(Ba3d5 112.00 0.200, F1s 112.00 0.200, O1s 112.00 0.200, C1s 112.00 0.200, Si2p 112.00 0.200, Al2p 112.00 0.200))',
        'SoftwareVersion': 'SS 4.2.0.28',
        'InstrumentModel': 'PHI Quantes',
        'FileDate': '123 12 14',
        'AcqFileDate': '20230720',
        'AcqFilename': 'C:\\Datafiles\\User\\Butsuzai_Taro\\20230719\\TempWWOHF3_D1.116_1.pro',
        'ExperimentID': '20230719',
        'StagePosition': '-19.8848 -21.6213 24.0329 45.0000 359.9979',
        'PhotoFilename': 'WWOHF3_D1.101.pho',
        'XRayHighPower': 'no',
        'SputterRaster': '0.0 0.0 mm',
        'PreAcqSputterTime': '0',
        'PreAcqSputterRate': '0.0',
        'NoSpectralReg': '1',
        'NoSpatialArea': '1',
        'SpatialAreaDef': '1 5 1 (-20060.0 22644.2 24033.0 45.0 360.0)',
        'SpatialAreaDesc': '1 B-3',
        'xlabelname': 'Binding Energy',
        'xlabelunit': 'eV',
        'xoption': 'reverse',
        'xlabel': 'Binding Energy (eV)',
        'ylabelname': 'Intensity',
        'ylabelunit': 'cps',
        'yoption': '',
        'ylabel': 'Intensity (cps)',
        'measurement.measured_date': '2023-07-20T00:00:00+09:00',
    }


@pytest.fixture
def read_repeated_meta():
    return {
        'XraySource': ['Al 1486.6 mono'],
        'AnalyserMode': ['FAT'],
        'XrayPower': ['25.60'],
        'XrayBeamDiameter': ['100.0'],
        'SourceAnalyserAngle': ['45.0'],
        'AnalyserSolidAngle': ['0.4'],
        'AnalyserWorkFcn': ['4.5'],
        'analysis_width_x': ['100.0000'],
        'analysis_width_y': ['100.0000'],
        'analysis_region': ['Spot'],
        'peak_name': ['Al'],
        'transitions': ['2p'],
        'abscissa_increment': ['-0.2000'],
        'abscissa_start': ['66.00000'],
        'abscissa_end': ['84.00000'],
        'collection_time': ['0.960000'],
        'pass_energy': ['112.00'],
        'total_acquisition_number': [12],
        'peak_sweep_number': ['12']
    }


def test_parse(metadata_def, default_value, set_meta, read_const_meta, read_repeated_meta):
    """構文解析"""

    handler = MetaParser(metadata_def_json_path=metadata_def, config=RDE_CONFIG_YAML, default_value=default_value)
    handler.parse(set_meta, None)
    assert handler.const_meta_info == read_const_meta
    assert handler.repeated_meta_info == read_repeated_meta
