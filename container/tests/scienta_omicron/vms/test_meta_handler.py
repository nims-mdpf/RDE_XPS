import json
import pytest

from modules_xps.scienta_omicron.vms.meta_handler import MetaParser
from rdetoolkit.rde2util import Meta


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


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


@pytest.fixture
def metadata_def(tmp_path):
    """metadata-def.json"""
    metadata_def = {
        "common.data_origin": {
            "name": {
                "ja": "データの起源",
                "en": "Data Origin"
            },
            "schema": {
                "type": "string"
            }
        },
        "common.technical_category": {
            "name": {
                "ja": "技術カテゴリー",
                "en": "Technical Category"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.method_category": {
            "name": {
                "ja": "計測法カテゴリー",
                "en": "Method category"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.method_sub_category": {
            "name": {
                "ja": "計測法サブカテゴリー",
                "en": "Method sub-category"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.analysis_field": {
            "name": {
                "ja": "分析分野",
                "en": "Analysis field"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.specimen": {
            "name": {
                "ja": "試料",
                "en": "Specimen"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.measurement_environment": {
            "name": {
                "ja": "測定環境",
                "en": "Measurement environment"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.energy_level_transition_structure_etc_of_interest": {
            "name": {
                "ja": "対象準位_遷移_構造",
                "en": "Energy Level_Transition_Structure etc. of interest"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.measured_date": {
            "name": {
                "ja": "分析年月日",
                "en": "Measured date"
            },
            "schema": {
                "type": "string",
                "format": "date"
            }
        },
        "measurement.standardized_procedure_specified_number": {
            "name": {
                "ja": "標準手順",
                "en": "Standardized procedure"
            },
            "schema": {
                "type": "string"
            }
        },
        "measurement.instrumentation_site": {
            "name": {
                "ja": "装置設置場所",
                "en": "Instrumentation site"
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
            "originalName": "operator_identifier"
        },
        "institution_identifier": {
            "name": {
                "ja": "所属施設など",
                "en": "Institution Identifier"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "institution_identifier"
        },
        "measurement_technique": {
            "name": {
                "ja": "測定手法",
                "en": "Measurement Technique"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "technique",
            "variable": 1
        },
        "measurement_instrument": {
            "name": {
                "ja": "測定装置",
                "en": "Measurement Instrument"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "instrument_model_identifier"
        },
        "experiment_id": {
            "name": {
                "ja": "測定内容識別ID",
                "en": "Experiment ID"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "experiment_identifier"
        },
        "operation_date_time_year": {
            "name": {
                "ja": "測定日時[年]",
                "en": "Operation Date-time[Year]"
            },
            "schema": {
                "type": "integer"
            },
            "originalName": "year_in_full",
            "variable": 1
        },
        "operation_date_time_month": {
            "name": {
                "ja": "測定日時[月]",
                "en": "Operation Date-time[Month]"
            },
            "schema": {
                "type": "integer"
            },
            "originalName": "month",
            "variable": 1
        },
        "operation_date_time_day": {
            "name": {
                "ja": "測定日時[日]",
                "en": "Operation Date-time[Day]"
            },
            "schema": {
                "type": "integer"
            },
            "originalName": "day_of_month",
            "variable": 1
        },
        "operation_date_time_hour": {
            "name": {
                "ja": "測定日時[時]",
                "en": "Operation Date-time[Hour]"
            },
            "schema": {
                "type": "integer"
            },
            "originalName": "hours",
            "variable": 1
        },
        "operation_date_time_minute": {
            "name": {
                "ja": "測定日時[分]",
                "en": "Operation Date-time[Minute]"
            },
            "schema": {
                "type": "integer"
            },
            "originalName": "minutes",
            "variable": 1
        },
        "operation_date_time_second": {
            "name": {
                "ja": "測定日時[秒]",
                "en": "Operation Date-time[Second]"
            },
            "schema": {
                "type": "integer"
            },
            "originalName": "seconds",
            "variable": 1
        },
        "experiment_mode": {
            "name": {
                "ja": "実験モード",
                "en": "experiment mode"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "experiment_mode"
        },
        "xray_power": {
            "name": {
                "ja": "X線パワー",
                "en": "Xray Power"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_characteristic_energy",
            "unit": "W",
            "variable": 1
        },
        "analyzer_mode": {
            "name": {
                "ja": "分析器分光動作モード",
                "en": "Analyzer Mode"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analyser_mode",
            "variable": 1
        },
        "analyzer_work_function": {
            "name": {
                "ja": "分析器仕事関数",
                "en": "Analyzer Work Function"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analyser_work_function_or_acceptance_energy_of_atom_or_ion",
            "unit": "eV",
            "variable": 1
        },
        "xray_analyzer_angle": {
            "name": {
                "ja": "照射X線 分析器間角度",
                "en": "Xray Analyzer Angle"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analyser_axis_take_off_polar_angle",
            "unit": "deg",
            "variable": 1
        },
        "analyzer_solid_angle": {
            "name": {
                "ja": "分析器取込立体角度",
                "en": "Analyzer Solid Angle"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analyser_axis_take_off_azimuth",
            "unit": "sr",
            "variable": 1
        },
        "analysis_width_x": {
            "name": {
                "ja": "X成分",
                "en": "Analysis Width_x"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_width_x",
            "unit": "um",
            "variable": 1
        },
        "analysis_width_y": {
            "name": {
                "ja": "Y成分",
                "en": "Analysis Width_y"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_width_y",
            "unit": "um",
            "variable": 1
        },
        "peak_name": {
            "name": {
                "ja": "ピーク名",
                "en": "Peak Name"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "species_label",
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
            "originalName": "transition_or_charge_state_label",
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
            "originalName": "analyser_pass_energy_or_retard_ratio_or_mass_resolution",
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
            "originalName": "abscissa_start",
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
            "originalName": "abscissa_increment",
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
            "originalName": "signal_collection_time",
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
            "originalName": "number_of_scans_to_compile_this_block",
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
            "originalName": "comment"
        },
        "scan_mode": {
            "name": {
                "ja": "スキャンモード",
                "en": "Scan Mode"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "scan_mode"
        },
        "sample_identifier": {
            "name": {
                "ja": "測定試料識別子",
                "en": "sample identifier"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "sample_identifier",
            "variable": 1
        },
        "number_of_lines_in_block_comment": {
            "name": {
                "ja": "ブロックコメント行数",
                "en": "number of lines in block comment"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "number_of_lines_in_block_comment",
            "variable": 1
        },
        "block_comment": {
            "name": {
                "ja": "ブロックコメント",
                "en": "block comment"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "block_comment",
            "variable": 1
        },
        "values_of_experimental_variables": {
            "name": {
                "ja": "実験変数値",
                "en": "Values of experimental variables"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "values_of_experimental_variables",
            "variable": 1
        },
        "analysis_source_label": {
            "name": {
                "ja": "分析線源ラベル",
                "en": "analysis source label"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_label",
            "variable": 1
        },
        "analysis_source_characteristics_energy": {
            "name": {
                "ja": "分析線源特性エネルギー",
                "en": "analysis source characteristics energy"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_characteristic_energy",
            "unit": "eV",
            "variable": 1
        },
        "analysis_source_strength": {
            "name": {
                "ja": "入射プローブの強度",
                "en": "Analysis source strength"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_strength",
            "unit": "W",
            "variable": 1
        },
        "analysis_source_beam_width_x": {
            "name": {
                "ja": "分析線源ビーム幅x",
                "en": "analysis source beam width x"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_beam_width_x",
            "unit": "um",
            "variable": 1
        },
        "analysis_source_beam_width_y": {
            "name": {
                "ja": "分析線源ビーム幅y",
                "en": "analysis source beam width y"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_beam_width_y",
            "unit": "um",
            "variable": 1
        },
        "analysis_source_polar_angle_of_incidence": {
            "name": {
                "ja": "分析線源入射極角",
                "en": "analysis source polar angle of incidence"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_polar_angle_of_incidence",
            "unit": "deg",
            "variable": 1
        },
        "analysis_source_azimuth": {
            "name": {
                "ja": "分析線源方位角",
                "en": "analysis source azimuth"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "analysis_source_azimuth",
            "unit": "deg",
            "variable": 1
        },
        "target_bias": {
            "name": {
                "ja": "測定試料バイアス電圧",
                "en": "target bias"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "target_bias",
            "unit": "V",
            "variable": 1
        },
        "abscissa_label": {
            "name": {
                "ja": "横軸ラベル",
                "en": "abscissa label"
            },
            "schema": {
                "type": "string"
            },
            "description": "「abscissa label」と「abscissa units」の値を合成",
            "variable": 1
        },
        "corresponding_variables_label": {
            "name": {
                "ja": "対応変数ラベル",
                "en": "corresponding variables label"
            },
            "schema": {
                "type": "string"
            },
            "description": "「corresponding variable label」と「corresponding variable units」の値を合成",
            "variable": 1
        },
        "signal_mode": {
            "name": {
                "ja": "信号モード",
                "en": "signal mode"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "signal_mode",
            "variable": 1
        },
        "signal_time_correction": {
            "name": {
                "ja": "1掃引あたりの積算時間補正",
                "en": "signal time correction"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "signal_time_correction",
            "unit": "s",
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
            "originalName": "sample_normal_polar_angle_of_tilt",
            "unit": "deg",
            "variable": 1
        },
        "sample_normal_tilt_azimuth": {
            "name": {
                "ja": "試料法線方位角",
                "en": "sample normal tilt azimuth"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "sample_normal_tilt_azimuth",
            "unit": "deg",
            "variable": 1
        },
        "sample_rotation_angle": {
            "name": {
                "ja": "試料回転角",
                "en": "sample rotation angle"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "sample_rotation_angle",
            "unit": "deg",
            "variable": 1
        },
        "number_of_ordinate_values": {
            "name": {
                "ja": "データ点数",
                "en": "number of ordinate values"
            },
            "schema": {
                "type": "string"
            },
            "originalName": "number_of_ordinate_values",
            "variable": 1
        }
    }
    metadata_def_path = tmp_path / "metadata-def.json"
    with open(metadata_def_path, mode="w", encoding="utf-8") as f:
        json.dump(metadata_def, f)
    return metadata_def_path


@pytest.fixture
def class_meta(metadata_def):
    return Meta(metadata_def)


@pytest.fixture
def default_value():
    return {
        'common.data_origin': 'experiments',
        'common.technical_category': 'measurement',
        'measurement.method_category': '分光法',
        'measurement.method_sub_category': 'X線光電子分光法',
        'measurement.analysis_field': '化学状態',
        'measurement.measurement_environment': '真空中'
    }


@pytest.fixture
def set_meta():
    return {
        'format_identifier': 'VAMAS Surface Chemical Analysis Standard Data Transfer Format 2008 May 4',
        'institution_identifier': '',
        'instrument_model_identifier': '',
        'operator_identifier': '',
        'experiment_identifier': '',
        'number_of_lines_in_comment': 1,
        'comment': 'Experiment Type: XPS',
        'experiment_mode': 'NORM',
        'scan_mode': 'REGULAR',
        'number_of_spectral_regions': 1,
        'number_of_experimental_variables': 0,
        'experimental_variable_labels': [],
        'experimental_variable_units': [],
        'number_of_entries_in_parameter_inclusion_or_exclusion_list': 0,
        'parameter_inclusion_or_exclusion_prefix_numbers': [],
        'number_of_manually_entered_items_in_block': 0,
        'prefix_numbers_of_manually_entered_items': [],
        'number_of_future_upgrade_experiment_entries': 0,
        'number_of_future_upgrade_block_entries': 0,
        'future_upgrade_experiment_entries': [],
        'number_of_blocks': 1
    }


@pytest.fixture
def set_data_blocks():
    return [{
        'block_identifier': '',
        'sample_identifier': '',
        'year_in_full': '2008',
        'month': '4',
        'day_of_month': '11',
        'hours': '16',
        'minutes': '12',
        'seconds': '29',
        'number_of_hours_in_advance_of_greenwich_mean_time': 0,
        'number_of_lines_in_block_comment': 0,
        'technique': 'XPS',
        'values_of_experimental_variables': [],
        'analysis_source_label': '',
        'analysis_source_characteristic_energy': '1253.6',
        'analysis_source_strength': '300.0',
        'analysis_source_beam_width_x': '',
        'analysis_source_beam_width_y': '',
        'analysis_source_polar_angle_of_incidence': '',
        'analysis_source_azimuth': '',
        'analyser_mode': 'FAT',
        'analyser_pass_energy_or_retard_ratio_or_mass_resolution': '5.00',
        'magnification_of_analyser_transfer_lens': '5.0',
        'analyser_work_function_or_acceptance_energy_of_atom_or_ion': '4.500',
        'target_bias': '',
        'analysis_width_x': '2400',
        'analysis_width_y': '1200',
        'analyser_axis_take_off_polar_angle': '',
        'analyser_axis_take_off_azimuth': '',
        'species_label': '',
        'transition_or_charge_state_label': '',
        'charge_of_detected_particle': '-1',
        'abscissa_label': 'kinetic energy',
        'abscissa_units': 'eV',
        'abscissa_start': '192.0',
        'abscissa_increment': '0.100',
        'number_of_corresponding_variables': 1,
        'corresponding_variable_labels': ['count rate'],
        'corresponding_variable_units': ['c/s'],
        'signal_mode': 'pulse counting',
        'signal_collection_time': '0.100',
        'number_of_scans_to_compile_this_block': '1',
        'signal_time_correction': '70E-9',
        'sample_normal_polar_angle_of_tilt': '',
        'sample_normal_tilt_azimuth': '',
        'sample_rotation_angle': '',
        'number_of_additional_numerical_parameters': 0,
        'number_of_ordinate_values': 10,
        'minimum_ordinate_values': ['59471'],
        'maximum_ordinate_values': ['84709'],
        'ordinate_values': [['60107', '60592', '60340', '60581', '60892', '60560', '59975', '60153', '60551', '60424']]
    }]


@pytest.fixture
def read_const_meta():
    return {
        'format_identifier': 'VAMAS Surface Chemical Analysis Standard Data Transfer Format 2008 May 4',
        'institution_identifier': '',
        'instrument_model_identifier': '',
        'operator_identifier': '',
        'experiment_identifier': '',
        'number_of_lines_in_comment': 1,
        'comment': 'Experiment Type: XPS',
        'experiment_mode': 'NORM',
        'scan_mode': 'REGULAR',
        'number_of_spectral_regions': 1,
        'number_of_experimental_variables': 0,
        'number_of_entries_in_parameter_inclusion_or_exclusion_list': 0,
        'number_of_manually_entered_items_in_block': 0,
        'number_of_future_upgrade_experiment_entries': 0,
        'number_of_future_upgrade_block_entries': 0,
        'number_of_blocks': 1,
        'measurement.measured_date': '2008-04-11T00:00:00+09:00',
        'abscissa_end': [192.9],
        'abscissa_label': ['kinetic energy (eV)'],
        'corresponding_variables_label': ['count rate (c/s)']
    }


@pytest.fixture
def read_repeated_meta():
    return {
        'hours': ['16'],
        'target_bias': [''],
        'number_of_lines_in_block_comment': [0],
        'analyser_mode': ['FAT'],
        'analyser_axis_take_off_polar_angle': [''],
        'analysis_source_strength': ['300.0'],
        'signal_time_correction': ['70E-9'],
        'minimum_ordinate_values': ['59471'],
        'analyser_work_function_or_acceptance_energy_of_atom_or_ion': ['4.500'],
        'values_of_experimental_variables': [''],
        'maximum_ordinate_values': ['84709'],
        'corresponding_variable_units': ['c/s'],
        'signal_collection_time': ['0.100'],
        'analysis_source_label': [''],
        'signal_mode': ['pulse counting'],
        'sample_normal_tilt_azimuth': [''],
        'block_identifier': [''],
        'abscissa_increment': ['0.100'],
        'abscissa_start': ['192.0'],
        'day_of_month': ['11'],
        'analyser_pass_energy_or_retard_ratio_or_mass_resolution': ['5.00'],
        'charge_of_detected_particle': ['-1'],
        'analysis_width_x': ['2400'],
        'analyser_axis_take_off_azimuth': [''],
        'number_of_hours_in_advance_of_greenwich_mean_time': [0],
        'seconds': ['29'],
        'number_of_corresponding_variables': [1],
        'sample_identifier': [''],
        'month': ['4'],
        'abscissa_units': ['eV'],
        'analysis_source_characteristic_energy': ['1253.6'],
        'number_of_scans_to_compile_this_block': ['1'],
        'analysis_source_azimuth': [''],
        'number_of_additional_numerical_parameters': [0],
        'species_label': [''],
        'corresponding_variable_labels': ['count rate'],
        'year_in_full': ['2008'],
        'number_of_ordinate_values': [10],
        'analysis_source_beam_width_y': [''],
        'technique': ['XPS'],
        'magnification_of_analyser_transfer_lens': ['5.0'],
        'analysis_source_beam_width_x': [''],
        'transition_or_charge_state_label': [''],
        'sample_normal_polar_angle_of_tilt': [''],
        'minutes': ['12'],
        'sample_rotation_angle': [''],
        'analysis_width_y': ['1200'],
        'analysis_source_polar_angle_of_incidence': ['']
    }


def test_parse(metadata_def, default_value, set_meta, set_data_blocks, read_const_meta, read_repeated_meta):
    """構文解析"""

    handler = MetaParser(metadata_def_json_path=metadata_def, config=RDE_CONFIG_YAML, default_value=default_value)
    handler.parse(set_meta, set_data_blocks)
    assert handler.const_meta_info == read_const_meta
    assert handler.repeated_meta_info == read_repeated_meta
