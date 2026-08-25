import os
import pandas as pd
from pathlib import Path
import pytest

from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules_xps.scienta_omicron.vms.graph_handler import GraphPlotter


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
def resource_paths(temp_dir):
    return RdeOutputResourcePath(
        raw=Path('tests'),
        nonshared_raw=Path('tests'),
        rawfiles=(Path('tests/scienta_omicron/files/XPS.vms'),),
        struct=Path('tests'),
        main_image=temp_dir,
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
def read_data():
    return pd.DataFrame({
        "kinetic energy(eV)": [192.0, 192.1, 192.2, 192.3, 192.4, 192.5, 192.6, 192.7, 192.8, 192.9],
        "count rate(c/s)": [60107.0, 60592.0, 60340.0, 60581.0, 60892.0, 60560.0, 59975.0, 60153.0, 60551.0, 60424.0]
    })


@pytest.fixture
def read_data_blocks():
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
def resource_paths_multiple(temp_dir):
    return RdeOutputResourcePath(
        raw=Path('tests'),
        nonshared_raw=Path('tests'),
        rawfiles=(Path('tests/scienta_omicron/files/Si_SR.vms'),),
        struct=Path('tests'),
        main_image=temp_dir,
        other_image=temp_dir,
        meta=Path('tests'),
        thumbnail=Path('tests'),
        logs=Path('tests'),
        invoice=temp_dir,
        invoice_schema_json=Path('tests'),
        invoice_org=temp_dir / 'invoice.json'
    )


@pytest.fixture
def read_data_multiple():
    return pd.DataFrame({
        0: [86.7, 87.7, 88.7, 89.7, 90.7, 91.7, 92.7, 93.7, 94.7, 95.7],
        1: [515, 484, 484, 520, 487, 5, 7, 4, 4, 1],
        2: [1378.7, 1378.8, 1378.9, 1379, 1379.1, 1379.2, 1379.3, 1379.4, 1379.5, 1379.6],
        3: [980, 996, 968, 999, 995, 248, 283, 266, 261, 244],
        4: [946.7, 946.8, 946.9, 947, 947.1, 947.2, 947.3, 947.4, 947.5, 947.6],
        5: [4268, 4409, 4440, 4321, 4415, 4067, 4241, 4052, 4068, 4160],
        6: [1192.7, 1192.8, 1192.9, 1193, 1193.1, 1193.2, 1193.3, 1193.4, 1193.5, 1193.6],
        7: [4009, 3904, 3979, 4007, 3968, 3974, 3940, 3936, 3905, 3870],
        8: [1452.7, 1452.8, 1452.9, 1453, 1453.1, 1453.2, 1453.3, 1453.4, 1453.5, 1453.6],
        9: [537, 581, 565, 645, 614, 8, 9, 8, 5, 12],
    })


@pytest.fixture
def read_data_blocks_multiple():
    return [
      {
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
      },
      {
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
      },
      {
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
      },
      {
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
      },
      {
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
      }
    ]


def test_plot_main(temp_dir, resource_paths, read_meta, read_data, read_data_blocks):

    plotter = GraphPlotter()
    plotter.plot_main(resource_paths, read_meta, read_data, read_data_blocks, None, RDE_CONFIG_YAML)
    main_image = temp_dir / "XPS.png"
    assert main_image.exists(), "The plot was not saved correctly."
    if os.path.exists(main_image):
        os.remove(main_image)


def test_plot_main_multiple(temp_dir, resource_paths_multiple, read_meta, read_data_multiple, read_data_blocks_multiple):

    plotter = GraphPlotter()
    plotter.plot_main(resource_paths_multiple, read_meta, read_data_multiple, read_data_blocks_multiple, None, RDE_CONFIG_YAML)
    main_image = temp_dir / "Si_SR.png"
    assert main_image.exists(), "The plot was not saved correctly."
    other_image_1 = temp_dir / "Si_SR_data1.png"
    other_image_2 = temp_dir / "Si_SR_data2.png"
    other_image_3 = temp_dir / "Si_SR_data3.png"
    other_image_4 = temp_dir / "Si_SR_data4.png"
    other_image_5 = temp_dir / "Si_SR_data5.png"
    assert other_image_1.exists(), "The plot was not saved correctly."
    assert other_image_2.exists(), "The plot was not saved correctly."
    assert other_image_3.exists(), "The plot was not saved correctly."
    assert other_image_4.exists(), "The plot was not saved correctly."
    assert other_image_5.exists(), "The plot was not saved correctly."
    if os.path.exists(main_image):
        os.remove(main_image)
    if os.path.exists(other_image_1):
        os.remove(other_image_1)
    if os.path.exists(other_image_2):
        os.remove(other_image_2)
    if os.path.exists(other_image_3):
        os.remove(other_image_3)
    if os.path.exists(other_image_4):
        os.remove(other_image_4)
    if os.path.exists(other_image_5):
        os.remove(other_image_5)
