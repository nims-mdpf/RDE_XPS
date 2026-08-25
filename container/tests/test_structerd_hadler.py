import pandas as pd
import pytest
from pathlib import Path
import shutil

from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules_xps.structured_handler import StructuredDataProcessor


RDE_CONFIG_SO_YAML: dict = {
    'system': {
        'magic_variable': True,
        'save_thumbnail_image': True,
    },
    'xps': {
        'manufacturer': 'scienta_omicron',
        'no3dimage': False,
    }
}

RDE_CONFIG_UP_YAML: dict = {
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
        rawfiles=(temp_dir,),
        struct=temp_dir,
        main_image=Path('tests'),
        other_image=Path('tests'),
        meta=Path('tests'),
        thumbnail=Path('tests'),
        logs=Path('tests'),
        invoice=Path('tests'),
        invoice_schema_json=Path('tests'),
        invoice_org=Path('tests')
    )


@pytest.fixture
def meta():
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
def data_vms():
    return pd.DataFrame({
        0: [192.0, 192.1, 192.2, 192.3, 192.4, 192.5, 192.6, 192.7, 192.8, 192.9],
        1: [60107.0, 60592.0, 60340.0, 60581.0, 60892.0, 60560.0, 59975.0, 60153.0, 60551.0, 60424.0]
    })


@pytest.fixture
def data_pro():
    return pd.DataFrame({
        "Sputter Time (min)": ['0.0000', '1.0000', '2.0000', '3.0000', '4.0000', '5.0000', '6.0000', '6.5000', '7.0000', '7.5000', '8.0000', '8.5000', '9.0000', '9.5000', '10.0000', '10.5000', '11.0000', '11.5000', '12.0000', '13.0000', '14.0000', '15.0000', '16.0000', '17.0000', '18.0000'],
        "O1s_Intensity (arb.units)": ['88925.7344', '122217.8125', '125950.2109', '124797.8125', '126445.7344', '126408.9609', '125956.5625', '125266.2500', '125413.9609', '121401.1484', '116655.6250', '104749.8984', '78576.3516', '41802.5000', '14036.9795', '6139.1670', '1037.6041', '2302.2917', '0.0000', '359.3750', '1232.6041', '53.5417', '321.3542', '251.7708', '577.7083'],
        "Si2p_Intensity (arb.units)": ['27162.8125', '33092.1484', '33480.3516', '34007.4219', '33498.8672', '33854.0234', '33827.4219', '34128.2813', '33243.6719', '34090.7422', '33055.0781', '32977.3047', '33021.8750', '33490.2344', '33517.2266', '33545.5469', '32960.5859', '33315.2734', '33447.1875', '33582.9688', '33840.0781', '34365.4297', '34071.6797', '32135.1172', '32959.1797'],
    })


@pytest.fixture
def data_blocks_vms():
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
def data_atomics_spe(temp_dir):
    return [{
        "kind": "cps",
        "file": (temp_dir / "XPS_Al2p.csv"),
        "df": pd.DataFrame({
            "Binding Energy (eV)": ['84.0000', '83.8000', '83.6000', '83.4000', '83.2000', '83.0000', '82.8000', '82.6000', '82.4000', '82.2000', '82.0000', '81.8000', '81.6000', '81.4000', '81.2000', '81.0000', '80.8000', '80.6000', '80.4000', '80.2000', '80.0000', '79.8000', '79.6000', '79.4000', '79.2000', '79.0000', '78.8000', '78.6000', '78.4000', '78.2000', '78.0000', '77.8000', '77.6000', '77.4000', '77.2000', '77.0000', '76.8000', '76.6000', '76.4000', '76.2000', '76.0000', '75.8000', '75.6000', '75.4000', '75.2000', '75.0000', '74.8000', '74.6000', '74.4000', '74.2000', '74.0000', '73.8000', '73.6000', '73.4000', '73.2000', '73.0000', '72.8000', '72.6000', '72.4000', '72.2000', '72.0000', '71.8000', '71.6000', '71.4000', '71.2000', '71.0000', '70.8000', '70.6000', '70.4000', '70.2000', '70.0000', '69.8000', '69.6000', '69.4000', '69.2000', '69.0000', '68.8000', '68.6000', '68.4000', '68.2000', '68.0000', '67.8000', '67.6000', '67.4000', '67.2000', '67.0000', '66.8000', '66.6000', '66.4000', '66.2000', '66.0000'],
            "Intensity (cps)": ['856.2500', '-0.0937', '-1.8693', '841.6678', '828.1250', '864.5834', '-0.0937', '2.0042', '564123419017216.0000', '-1.8693', '776.0428', '7.5167616426713623E0030', '0.0523', '-1.8693', '797.9178', '-1.17449400666740036E0029', '766.9648', '837.5000', '748.9584', '-0.0937', '-3.96965573877554872E0028', '770.9648', '-0.0937', '-3.96965573877554872E0028', '758.9648', '-1.17449400666740036E0029', '722.9648', '-0.0937', '-3.96966754469175589E0028', '786.9648', '768.7500', '740.6250', '-0.0937', '1.0406234146896403E0034', '-3.96966518350851445E0028', '774.9648', '737.5000', '740.6250', '-1.17449400666740036E0029', '746.9648', '781.2500', '0.0000', '-6.07473607334803301E0028', '-1.8730', '-6.07566685178180662E0028', '-1.8730', '53967056797696.0000', '53978263977984.0000', '54012657270784.0000', '-1.17449400666740036E0029', '0.0000', '-0.0937', '-1.8698', '-0.0937', '-0.0937', '-1.17449400666740036E0029', '-6.08884508768890265E0028', '-1.8730', '0.0000', '0.0000', '-1.8672', '-6.10177964948548261E0028', '0.0000', '-1.8672', '-6.10468107145255772E0028', '-1.8730', '-6.1040766085427504E0028', '-1.8730', '0.0000', '-6.102088020016814E0028', '-1.8730', '0.0000', '0.0000', '-7.79905483182662753E0028', '0.0000', '-1.17449400666740036E0029', '0.0000', '-0.0937', '-5.94214430066190883E0028', '0.0000', '-0.0937', '-0.0937', '-1.17449400666740036E0029', '-6.08884508768890265E0028', '-5.16039005822486744E0028', '-6.08884508768890265E0028', '-1.8730', '-0.0937', '-1.8672', '0.0000', '53975189553152.0000'],
            "Intensity (counts)": ['822.0000', '-0.0900', '-1.7945', '808.0011', '795.0000', '830.0001', '-0.0900', '1.9240', '541558482256527.3125', '-1.7945', '745.0011', '7216091176964507497393943478272.0000', '0.0502', '-1.7945', '766.0011', '-112751424640070429646780366848.0000', '736.2862', '804.0000', '719.0001', '-0.0900', '-38108695092245268016255729664.0000', '740.1262', '-0.0900', '-38108695092245268016255729664.0000', '728.6062', '-112751424640070429646780366848.0000', '694.0462', '-0.0900', '-38108808429040856887740858368.0000', '755.4862', '738.0000', '711.0000', '-0.0900', '9989984781020546224424601499205632.0000', '-38108785761681735595006623744.0000', '743.9662', '708.0000', '711.0000', '-112751424640070429646780366848.0000', '717.0862', '750.0000', '0.0000', '-58317466304141116188724822016.0000', '-1.7981', '-58326401777105343520299810816.0000', '-1.7981', '51808374525788.1562', '51819133418864.6406', '51852150979952.6406', '-112751424640070429646780366848.0000', '0.0000', '-0.0900', '-1.7950', '-0.0900', '-0.0900', '-112751424640070429646780366848.0000', '-58452912841813464371328712704.0000', '-1.7981', '0.0000', '0.0000', '-1.7925', '-58577084635060633729654325248.0000', '0.0000', '-1.7925', '-58604938285944555841370718208.0000', '-1.7981', '-58599135442010402102894919680.0000', '-1.7981', '0.0000', '-58580044992161410127033794560.0000', '-1.7981', '0.0000', '0.0000', '-74870926385535621496448221184.0000', '0.0000', '-112751424640070429646780366848.0000', '0.0000', '-0.0900', '-57044585286354319520135380992.0000', '0.0000', '-0.0900', '-0.0900', '-112751424640070429646780366848.0000', '-58452912841813464371328712704.0000', '-49539744558958722873617809408.0000', '-58452912841813464371328712704.0000', '-1.7981', '-0.0900', '-1.7925', '0.0000', '51816181971025.9219'],
        })
    }]


@pytest.fixture
def data_atomics_pro(temp_dir):
    # dataframeはすごく大きいので、ファイルを読み込んで展開する。
    return [
        {
            "file_cps": (temp_dir / 'XPS_O1s.csv'),
            "file_counts": (temp_dir / 'XPS_O1s_count.csv'),
        },
        {
            "file_cps": (temp_dir / 'XPS_Si2p.csv'),
            "file_counts": (temp_dir / 'XPS_Si2p_count.csv'),
        },
    ]


@pytest.fixture
def read_data_vms():
    return pd.DataFrame({
        "kinetic energy(eV)": [192.0, 192.1, 192.2, 192.3, 192.4, 192.5, 192.6, 192.7, 192.8, 192.9],
        "count rate(c/s)": [60107.0, 60592.0, 60340.0, 60581.0, 60892.0, 60560.0, 59975.0, 60153.0, 60551.0, 60424.0]
    })


def test_save_csv_vms(temp_dir, resource_paths, meta, data_vms, data_blocks_vms, read_data_vms):
    """.vmsファイル"""
    shutil.copy(Path("tests/scienta_omicron/files/XPS.vms"), (temp_dir / "XPS.vms"))
    resource_paths.rawfiles = ((temp_dir / "XPS.vms"),)
    processor = StructuredDataProcessor(config=RDE_CONFIG_SO_YAML)
    processor.save_file(resource_paths, meta, data_vms, data_blocks_vms, None)

    df = pd.read_csv(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.csv"), header=0)
    pd.testing.assert_frame_equal(df, read_data_vms, check_dtype=False)


def test_save_csv_spe(temp_dir, resource_paths, data_atomics_spe):
    """.speファイル"""
    shutil.copy(Path("tests/ulvac_phi/files/XPS.spe"), (temp_dir / "XPS.spe"))
    resource_paths.rawfiles = ((temp_dir / "XPS.spe"),)
    processor = StructuredDataProcessor(config=RDE_CONFIG_UP_YAML)
    processor.save_file(resource_paths, None, None, None, data_atomics_spe)

    df = pd.read_csv(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_Al2p.csv"), header=0)
    assert df.columns.to_list() == ['Binding Energy (eV)', 'Intensity (cps)', 'Intensity (counts)']
    assert df.iloc[0, :].to_list() == [84.0000, 856.2500, 822.0000]


def test_save_csv_pro(temp_dir, resource_paths, data_pro, data_atomics_pro):
    """.proファイル"""
    data_atomics_pro[0]['df_cps'] = pd.read_csv('tests/ulvac_phi/files/df_cps_0.csv', dtype=object)
    data_atomics_pro[0]['df_counts'] = pd.read_csv('tests/ulvac_phi/files/df_counts_0.csv', dtype=object)
    data_atomics_pro[1]['df_cps'] = pd.read_csv('tests/ulvac_phi/files/df_cps_1.csv', dtype=object)
    data_atomics_pro[1]['df_counts'] = pd.read_csv('tests/ulvac_phi/files/df_counts_1.csv', dtype=object)

    shutil.copy(Path("tests/ulvac_phi/files/XPS.pro"), (temp_dir / "XPS.pro"))
    resource_paths.rawfiles = ((temp_dir / "XPS.pro"),)
    processor = StructuredDataProcessor(config=RDE_CONFIG_UP_YAML)
    processor.save_file(resource_paths, None, data_pro, None, data_atomics_pro)

    df = pd.read_csv(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.csv"), header=0)
    assert df.columns.to_list() == ['Sputter Time (min)', 'O1s_Intensity (arb.units)', 'Si2p_Intensity (arb.units)']
    assert df.iloc[0, :].to_list() == [0.0000, 88925.7344, 27162.8125]

    df_o1s = pd.read_csv(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_O1s.csv"), header=0)
    assert df_o1s.columns.to_list() == ['Binding Energy (eV)', '0min_Intensity (cps)', '1min_Intensity (cps)', '2min_Intensity (cps)', '3min_Intensity (cps)', '4min_Intensity (cps)', '5min_Intensity (cps)', '6min_Intensity (cps)', '6.5min_Intensity (cps)', '7min_Intensity (cps)', '7.5min_Intensity (cps)', '8min_Intensity (cps)', '8.5min_Intensity (cps)', '9min_Intensity (cps)', '9.5min_Intensity (cps)', '10min_Intensity (cps)', '10.5min_Intensity (cps)', '11min_Intensity (cps)', '11.5min_Intensity (cps)', '12min_Intensity (cps)', '13min_Intensity (cps)', '14min_Intensity (cps)', '15min_Intensity (cps)', '16min_Intensity (cps)', '17min_Intensity (cps)', '18min_Intensity (cps)']
    assert df_o1s.iloc[0, :].to_list() == [543.0000, 3412.5000, 4162.5000, 4462.5000, 4387.5000, 4558.3335, 5029.1665, 5037.5000, 4937.5000, 5200.0000, 5070.8335, 5175.0000, 5020.8335, 5033.3335, 4420.8335, 3800.0000, 3629.1667, 3362.5000, 3179.1667, 3304.1667, 3395.8333, 3354.1667, 3454.1667, 3312.5000, 3408.3333, 3362.5000]

    df_o1s_count = pd.read_csv(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_O1s_count.csv"), header=0)
    assert df_o1s_count.columns.to_list() == ['Binding Energy (eV)', '0min_Intensity (counts)', '1min_Intensity (counts)', '2min_Intensity (counts)', '3min_Intensity (counts)', '4min_Intensity (counts)', '5min_Intensity (counts)', '6min_Intensity (counts)', '6.5min_Intensity (counts)', '7min_Intensity (counts)', '7.5min_Intensity (counts)', '8min_Intensity (counts)', '8.5min_Intensity (counts)', '9min_Intensity (counts)', '9.5min_Intensity (counts)', '10min_Intensity (counts)', '10.5min_Intensity (counts)', '11min_Intensity (counts)', '11.5min_Intensity (counts)', '12min_Intensity (counts)', '13min_Intensity (counts)', '14min_Intensity (counts)', '15min_Intensity (counts)', '16min_Intensity (counts)', '17min_Intensity (counts)', '18min_Intensity (counts)']
    assert df_o1s_count.iloc[0, :].to_list() == [543.0000, 819.0000, 999.0000, 1071.0000, 1053.0000, 1094.0000, 1207.0000, 1209.0000, 1185.0000, 1248.0000, 1217.0000, 1242.0000, 1205.0000, 1208.0000, 1061.0000, 912.0000, 871.0000, 807.0000, 763.0000, 793.0000, 815.0000, 805.0000, 829.0000, 795.0000, 818.0000, 807.0000]

    df_si2p = pd.read_csv(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_Si2p.csv"), header=0)
    assert df_si2p.columns.to_list() == ['Binding Energy (eV)', '0min_Intensity (cps)', '1min_Intensity (cps)', '2min_Intensity (cps)', '3min_Intensity (cps)', '4min_Intensity (cps)', '5min_Intensity (cps)', '6min_Intensity (cps)', '6.5min_Intensity (cps)', '7min_Intensity (cps)', '7.5min_Intensity (cps)', '8min_Intensity (cps)', '8.5min_Intensity (cps)', '9min_Intensity (cps)', '9.5min_Intensity (cps)', '10min_Intensity (cps)', '10.5min_Intensity (cps)', '11min_Intensity (cps)', '11.5min_Intensity (cps)', '12min_Intensity (cps)', '13min_Intensity (cps)', '14min_Intensity (cps)', '15min_Intensity (cps)', '16min_Intensity (cps)', '17min_Intensity (cps)', '18min_Intensity (cps)']
    assert df_si2p.iloc[0, :].to_list() == [112.0000, 631.2500, 770.3125, 714.0625, 751.5625, 707.8125, 742.1875, 734.3750, 845.3125, 790.6250, 884.3750, 942.1875, 1287.5000, 1657.8125, 2131.2500, 2765.6250, 2846.8750, 2925.0000, 2948.4375, 2979.6875, 2954.6875, 3043.7500, 2935.9375, 2926.5625, 3025.0000, 2940.6250]

    df_si2p_count = pd.read_csv(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_Si2p_count.csv"), header=0)
    assert df_si2p_count.columns.to_list() == ['Binding Energy (eV)', '0min_Intensity (counts)', '1min_Intensity (counts)', '2min_Intensity (counts)', '3min_Intensity (counts)', '4min_Intensity (counts)', '5min_Intensity (counts)', '6min_Intensity (counts)', '6.5min_Intensity (counts)', '7min_Intensity (counts)', '7.5min_Intensity (counts)', '8min_Intensity (counts)', '8.5min_Intensity (counts)', '9min_Intensity (counts)', '9.5min_Intensity (counts)', '10min_Intensity (counts)', '10.5min_Intensity (counts)', '11min_Intensity (counts)', '11.5min_Intensity (counts)', '12min_Intensity (counts)', '13min_Intensity (counts)', '14min_Intensity (counts)', '15min_Intensity (counts)', '16min_Intensity (counts)', '17min_Intensity (counts)', '18min_Intensity (counts)']
    assert df_si2p_count.iloc[0, :].to_list() == [112.0000, 404.0000, 493.0000, 457.0000, 481.0000, 453.0000, 475.0000, 470.0000, 541.0000, 506.0000, 566.0000, 603.0000, 824.0000, 1061.0000, 1364.0000, 1770.0000, 1822.0000, 1872.0000, 1887.0000, 1907.0000, 1891.0000, 1948.0000, 1879.0000, 1873.0000, 1936.0000, 1882.0000]
