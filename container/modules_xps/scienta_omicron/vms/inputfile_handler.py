from __future__ import annotations

import re
from io import TextIOWrapper

import numpy as np
import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath
from rdetoolkit.rde2util import CharDecEncoding

from modules_xps.inputfile_handler import FileReader as XpsFileReader


class FileReader(XpsFileReader):
    """Reads and processes structured ras files into data and metadata blocks.

    This class is responsible for reading structured files which have specific patterns for data and metadata.
    It then separates the contents into data blocks and metadata blocks.

    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.meta: MetaType = {}
        self.rawfile_name: str = ""

    def read(self, resource_paths: RdeOutputResourcePath) -> tuple[MetaType, pd.DataFrame, list[dict], None]:
        """Read the structured file and returns separated data and metadata.

        Args:
            resource_paths (RdeOutputResourcePath): The path of the structured file to read.

        Returns:
            dict[str, ExtendMetaType]: Meta data.
            pd.DataFrame: All measurement data.
            list[dict]: Block-by-Block additional data.
            None: (Not used in vms files.)

        Raises:
            StructuredError: If the file is formatted incorrectly.

        """
        self.rawfile_name = resource_paths.rawfiles[0].stem
        enc = CharDecEncoding.detect_text_file_encoding(resource_paths.rawfiles[0])
        data = pd.DataFrame()
        with open(resource_paths.rawfiles[0], encoding=enc) as f:

            self._get_experiment_info(f)
            data_blocks = self._get_block_info(f)

            # Get nemiric columns
            x_label = ""
            y_label = ""
            if len(data_blocks) > 0:
                # Read from the first block (RDE1.0 compliant)
                x_label = data_blocks[0].get("abscissa_label", [""]).strip() + \
                    "(" + data_blocks[0].get("abscissa_units", [""]).strip() + ")"
                y_label = ",".join(data_blocks[0].get("corresponding_variable_labels", [""])).strip() + \
                    "(" + ",".join(data_blocks[0].get("corresponding_variable_units", [""])).strip() + ")"

            # Read numeric values
            for _, data_block in enumerate(data_blocks):
                abscissa_start = float(data_block["abscissa_start"])
                abscissa_increment = float(data_block["abscissa_increment"])
                decimal_point = self._count_decimal_places(abscissa_increment)
                data_y = []
                for data_ar in data_block.get("ordinate_values", []):
                    data_y += data_ar
                data_x = [round(float(abscissa_start + n * abscissa_increment), decimal_point) for n in range(len(data_y))]
                df = pd.DataFrame(np.vstack((data_x, data_y)).T, columns=[x_label, y_label]).astype('float')
                data = pd.concat([data, df], ignore_index=True, axis=1)

        return self.meta, data, data_blocks, None

    def _get_experiment_info(self, f: TextIOWrapper) -> None:
        """Obtain metadata.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.

        """
        self._get_experiment_info_1(f)
        self._get_experiment_info_2(f)
        self._get_experiment_info_3(f)

    def _get_experiment_info_1(self, f: TextIOWrapper) -> None:
        """Obtain metadata part 1.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.

        """
        # Experiment
        # 1 format_identifier
        self.meta["format_identifier"] = self._read_line(f)

        # 2 institution_identifier
        self.meta["institution_identifier"] = self._read_line(f)

        # 3 instrument_model_identifier
        self.meta["instrument_model_identifier"] = self._read_line(f)

        # 4 operator_identifier
        self.meta["operator_identifier"] = self._read_line(f)

        # 5 experiment_identifier
        self.meta["experiment_identifier"] = self._read_line(f)

        # 6 number_of_lines_in_comment
        self.meta["number_of_lines_in_comment"] = int(self._read_line(f))

        # 7 comment
        comments: list = []
        if isinstance(self.meta["number_of_lines_in_comment"], int):
            comments = [
                self._read_line(f)
                for _
                in range(self.meta["number_of_lines_in_comment"])
                if self.meta["number_of_lines_in_comment"] > 0
            ]
            self.meta["comment"] = "\n".join(comments)

        # 8 experiment_mode
        self.meta["experiment_mode"] = self._read_line(f)

        # 9 scan_mode
        self.meta["scan_mode"] = self._read_line(f)

        # 10 number_of_spectral_regions
        if isinstance(self.meta["experiment_mode"], str) and \
                self.meta["experiment_mode"].upper() in ["MAP", "MAPDP", "NORM", "SDP"]:
            self.meta["number_of_spectral_regions"] = int(self._read_line(f))

        if isinstance(self.meta["experiment_mode"], str) and \
                self.meta["experiment_mode"].upper() in ["MAP", "MAPDP"]:
            # 11 number_of_analysis_positions
            self.meta["number_of_analysis_positions"] = int(self._read_line(f))
            # 12 number_of_discrete_x_coordinates_in_full_map
            self.meta["number_of_discrete_x_coordinates_in_full_map"] = self._read_line(f)
            # 13 number_of_discrete_y_coordinates_in_full_map
            self.meta["number_of_discrete_y_coordinates_in_full_map"] = self._read_line(f)
        # 14 number_of_experimental_variables
        self.meta["number_of_experimental_variables"] = int(self._read_line(f))

    def _get_experiment_info_2(self, f: TextIOWrapper) -> None:
        """Obtain metadata part 2.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.

        """
        # 15 experimental_variable_labels
        # 16 experimental_variable_units
        self.meta["experimental_variable_labels"] = []
        self.meta["experimental_variable_units"] = []
        if isinstance(self.meta["number_of_experimental_variables"], int):
            self.meta["experimental_variable_labels"] = [
                self._read_line(f)
                for _
                in range(self.meta["number_of_experimental_variables"])
                if self.meta["number_of_experimental_variables"] > 0
            ]
            self.meta["experimental_variable_units"] = [
                self._read_line(f)
                for _
                in range(self.meta["number_of_experimental_variables"])
                if self.meta["number_of_experimental_variables"] > 0
            ]

        # 17 number_of_entries_in_parameter_inclusion_or_exclusion_list
        self.meta["number_of_entries_in_parameter_inclusion_or_exclusion_list"] = int(self._read_line(f))

        # 18 parameter_inclusion_or_exclusion_prefix_numbers
        if isinstance(self.meta["number_of_entries_in_parameter_inclusion_or_exclusion_list"], int):
            self.meta["parameter_inclusion_or_exclusion_prefix_numbers"] = [
                int(self._read_line(f))
                for _
                in range(abs(self.meta["number_of_entries_in_parameter_inclusion_or_exclusion_list"]))
                if self.meta["number_of_entries_in_parameter_inclusion_or_exclusion_list"] > 0
            ]

        # 19 number_of_manually_entered_items_in_block
        self.meta["number_of_manually_entered_items_in_block"] = int(self._read_line(f))

    def _get_experiment_info_3(self, f: TextIOWrapper) -> None:
        """Obtain metadata part 3.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.

        """
        # 20 prefix_numbers_of_manually_entered_items
        if isinstance(self.meta["number_of_manually_entered_items_in_block"], int):
            # Note that the process of reading lines from the file is different only for these four locations (RDE1.0 compliant).
            self.meta["prefix_numbers_of_manually_entered_items"] = [
                int(f.readline().strip())
                for _
                in range(self.meta["number_of_manually_entered_items_in_block"])
                if self.meta["number_of_manually_entered_items_in_block"] > 0
            ]

        # 21 number_of_future_upgrade_experiment_entries
        self.meta["number_of_future_upgrade_experiment_entries"] = int(f.readline().strip())

        # 22 number_of_future_upgrade_block_entries
        self.meta["number_of_future_upgrade_block_entries"] = int(f.readline().strip())

        # 23 future_upgrade_experiment_entries
        if isinstance(self.meta["number_of_future_upgrade_block_entries"], int):
            self.meta["future_upgrade_experiment_entries"] = [
                f.readline().strip()
                for _
                in range(self.meta["number_of_future_upgrade_block_entries"])
                if self.meta["number_of_future_upgrade_block_entries"] > 0
            ]

        # 24 number_of_blocks
        self.meta["number_of_blocks"] = int(self._read_line(f))

    def _get_block_info(self, f: TextIOWrapper) -> list[dict]:
        """Obtain data for each block from the measurement file.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.

        Returns:
            list[dict]: Block-by-Block additional data.

        """
        data_blocks = []
        for _ in range(self.meta["number_of_blocks"] if isinstance(self.meta["number_of_blocks"], int) else 0):
            data_block: dict = {}
            data_block = self._get_block_info_01_16(f, data_block)
            data_block = self._get_block_info_17_46(f, data_block)
            data_block = self._get_block_info_47_57(f, data_block)
            data_block = self._get_block_info_58_71(f, data_block)
            data_block = self._get_block_info_72_76(f, data_block)
            data_blocks.append(data_block)

        return data_blocks

    def _get_block_info_01_16(self, f: TextIOWrapper, block: dict) -> dict:
        """Obtain additional information in the block.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.
            block (dict): Block data before item addition.

        Returns:
            dict: Block data after item addition.

        """
        # 1 block_identifier
        block["block_identifier"] = self._read_line(f)
        # 2 sample_identifier
        block["sample_identifier"] = self._read_line(f)
        # 3 year_in_full
        block["year_in_full"] = self._read_line(f)
        # 4 month
        block["month"] = self._read_line(f)
        # 5 day_of_month
        block["day_of_month"] = self._read_line(f)
        # 6 hours
        block["hours"] = self._read_line(f)
        # 7 minutes
        block["minutes"] = self._read_line(f)
        # 8 seconds
        block["seconds"] = self._read_line(f)
        # 9 number_of_hours_in_advance_of_greenwich_mean_time
        block["number_of_hours_in_advance_of_greenwich_mean_time"] = int(self._read_line(f))
        # 10 number_of_lines_in_block_comment
        block["number_of_lines_in_block_comment"] = int(self._read_line(f))
        # 11 block_comment
        block_comments = []
        for _ in range(block["number_of_lines_in_block_comment"]):
            block_comments.append(self._read_line(f))
        if len(block_comments) > 0:
            block["block_comment"] = "\n".join(block_comments)

        # 12 technique
        block["technique"] = self._read_line(f)

        if (isinstance(self.meta["experiment_mode"], str)) and (self.meta["experiment_mode"].upper() in ["MAP", "MAPDP"]):
            # 13 x_coordinate
            block["x_coordinate"] = self._read_line(f)
            # 14 y_coordinate
            block["y_coordinate"] = self._read_line(f)

        # 15 values_of_experimental_variables
        block["values_of_experimental_variables"] = []
        for _ in range(self.meta["number_of_experimental_variables"] if isinstance(self.meta["number_of_experimental_variables"], int) else 0):
            block["values_of_experimental_variables"].append(self._read_line(f))

        # 16 analysis_source_label
        block["analysis_source_label"] = self._read_line(f)

        return block

    def _get_block_info_17_46(self, f: TextIOWrapper, block: dict) -> dict:
        """Obtain additional information in the block.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.
            block (dict): Block data before item addition.

        Returns:
            dict: Block data after item addition.

        """
        # 17,18,19
        experiment_mode_list = ["MAPDP", "MAPSVDP", "SDP", "SDPSV"]
        technique_list = ["FABMS",
                          "FABMS energy spec",
                          "ISS",
                          "SIMS",
                          "SIMS energy spec",
                          "SNMS",
                          "SNMS energy spec"]
        technique_list = [s.upper() for s in technique_list]
        if ((isinstance(self.meta["experiment_mode"], str)) and (self.meta["experiment_mode"].upper() in experiment_mode_list)
                or (block["technique"].upper() in technique_list)):
            # 17 sputtering_ion_or_atomic_number
            block["sputtering_ion_or_atomic_number"] = self._read_line(f)
            # 18 number_of_atoms_in_sputtering_ion_or_atom_particle
            block["number_of_atoms_in_sputtering_ion_or_atom_particle"] = self._read_line(f)
            # 19 sputtering_ion_of_atom_charge_sign_and_number
            block["sputtering_ion_of_atom_charge_sign_and_number"] = self._read_line(f)

        # 20 analysis_source_characteristic_energy
        block["analysis_source_characteristic_energy"] = self._read_line(f)
        # 21 analysis_source_strength
        block["analysis_source_strength"] = self._read_line(f)
        # 22 analysis_source_beam_width_x
        block["analysis_source_beam_width_x"] = self._read_line(f)
        # 23 analysis_source_beam_width_y
        block["analysis_source_beam_width_y"] = self._read_line(f)

        modes = ["MAP", "MAPDP", "MAPSV", "MAPSVDP", "SEM"]
        if (isinstance(self.meta["experiment_mode"], str)) and (self.meta["experiment_mode"].upper() in modes):
            # 24 field_of_view_x
            block["field_of_view_x"] = self._read_line(f)
            # 25 field_of_view_y
            block["field_of_view_y"] = self._read_line(f)

        modes = ["MAPSV", "MAPSVDP", "SEM"]
        if (isinstance(self.meta["experiment_mode"], str)) and (self.meta["experiment_mode"].upper() in modes):
            # 26 first_linescan_start_x_coordinate
            block["first_linescan_start_x_coordinate"] = self._read_line(f)
            # 27 first_linescan_start_y_coordinate
            block["first_linescan_start_y_coordinate"] = self._read_line(f)
            # 28 first_linescan_finish_x_coordinate
            block["first_linescan_finish_x_coordinate"] = self._read_line(f)
            # 29 first_linescan_finish_y_coordinate
            block["first_linescan_finish_y_coordinate"] = self._read_line(f)
            # 30 last_linescan_finish_x_coordinate
            block["last_linescan_finish_x_coordinate"] = self._read_line(f)
            # 31 last_linescan_finish_y_coordinate
            block["last_linescan_finish_y_coordinate"] = self._read_line(f)

        # 32 analysis_source_polar_angle_of_incidence
        block["analysis_source_polar_angle_of_incidence"] = self._read_line(f)
        # 33 analysis_source_azimuth
        block["analysis_source_azimuth"] = self._read_line(f)
        # 34 analyser_mode
        block["analyser_mode"] = self._read_line(f)
        # 35 analyser_pass_energy_or_retard_ratio_or_mass_resolution
        block["analyser_pass_energy_or_retard_ratio_or_mass_resolution"] = self._read_line(f)
        # 36 differential_width
        if (block["technique"].upper() == "AES DIFF"):
            block["differential_width"] = self._read_line(f)
        # 37 magnification_of_analyser_transfer_lens
        block["magnification_of_analyser_transfer_lens"] = self._read_line(f)
        # 38 analyser_work_function_or_acceptance_energy_of_atom_or_ion
        block["analyser_work_function_or_acceptance_energy_of_atom_or_ion"] = self._read_line(f)
        # 39 target_bias
        block["target_bias"] = self._read_line(f)
        # 40 analysis_width_x
        block["analysis_width_x"] = self._read_line(f)
        # 41 analysis_width_y
        block["analysis_width_y"] = self._read_line(f)
        # 42 analyser_axis_take_off_polar_angle
        block["analyser_axis_take_off_polar_angle"] = self._read_line(f)
        # 43 analyser_axis_take_off_azimuth
        block["analyser_axis_take_off_azimuth"] = self._read_line(f)
        # 44 species_label
        block["species_label"] = self._read_line(f)
        # 45 transition_or_charge_state_label
        block["transition_or_charge_state_label"] = self._read_line(f)
        # 46 charge_of_detected_particle
        block["charge_of_detected_particle"] = self._read_line(f)

        return block

    def _get_block_info_47_57(self, f: TextIOWrapper, block: dict) -> dict:
        """Obtain additional information in the block.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.
            block (dict): Block data before item addition.

        Returns:
            dict: Block data after item addition.

        """
        if (isinstance(self.meta["scan_mode"], str)) and (self.meta["scan_mode"].upper() == "REGULAR"):
            # 47 abscissa_label
            block["abscissa_label"] = self._read_line(f)
            # 48 abscissa_units
            block["abscissa_units"] = self._read_line(f)
            # 49 abscissa_start
            block["abscissa_start"] = self._read_line(f)
            # 50 abscissa_increment
            block["abscissa_increment"] = self._read_line(f)

        # 51 number_of_corresponding_variables
        block["number_of_corresponding_variables"] = int(self._read_line(f))

        corresponding_variable_labels = []
        corresponding_variable_units = []
        for _ in range(block["number_of_corresponding_variables"]):
            corresponding_variable_labels.append(self._read_line(f))
            corresponding_variable_units.append(self._read_line(f))
        # 52 corresponding_variable_labels
        if corresponding_variable_labels:
            block["corresponding_variable_labels"] = corresponding_variable_labels
        # 53 corresponding_variable_units
        if corresponding_variable_units:
            block["corresponding_variable_units"] = corresponding_variable_units

        # 54 signal_mode
        block["signal_mode"] = self._read_line(f)
        # 55 signal_collection_time
        block["signal_collection_time"] = self._read_line(f)

        # 56 number_of_scans_to_compile_this_block
        block["number_of_scans_to_compile_this_block"] = self._read_line(f)
        # 57 signal_time_correction
        block["signal_time_correction"] = self._read_line(f)

        return block

    def _get_block_info_58_71(self, f: TextIOWrapper, block: dict) -> dict:
        """Obtain additional information in the block.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.
            block (dict): Block data before item addition.

        Returns:
            dict: Block data after item addition.

        """
        technique_list = ["AES diff", "AES dir", "EDX", "ELS", "UPS", "XPS", "XRF"]
        experiment_list = ["MAPDP", "MAPSVDP", "SDP", "SDPCV"]
        technique_list = [s.upper() for s in technique_list]
        experiment_list = [s.upper() for s in experiment_list]
        if (block["technique"].upper() in technique_list) and \
                isinstance(self.meta["experiment_mode"], str) and \
                (self.meta["experiment_mode"].upper() in experiment_list):
            # 58 sputtering_source_energy
            block["sputtering_source_energy"] = self._read_line(f)
            # 59 sputtering_source_beam_current
            block["sputtering_source_beam_current"] = self._read_line(f)
            # 60 sputtering_source_width_x
            block["sputtering_source_width_x"] = self._read_line(f)
            # 61 sputtering_source_width_y
            block["sputtering_source_width_y"] = self._read_line(f)
            # 62 sputtering_source_polar_angle_of_incidence
            block["sputtering_source_polar_angle_of_incidence"] = self._read_line(f)
            # 63 sputtering_source_azimuth
            block["sputtering_source_azimuth"] = self._read_line(f)
            # 64 sputtering_mode
            block["sputtering_mode"] = self._read_line(f)

        # 65 sample_normal_polar_angle_of_tilt
        block["sample_normal_polar_angle_of_tilt"] = self._read_line(f)
        # 66 sample_normal_tilt_azimuth
        block["sample_normal_tilt_azimuth"] = self._read_line(f)
        # 67 sample_rotation_angle
        block["sample_rotation_angle"] = self._read_line(f)

        # 68 number_of_additional_numerical_parameters
        block["number_of_additional_numerical_parameters"] = int(self._read_line(f))

        additional_numerical_parameter_labels = []
        additional_numerical_parameter_units = []
        additional_numerical_parameter_values = []
        for _ in range(block["number_of_additional_numerical_parameters"]):
            additional_numerical_parameter_labels.append(self._read_line(f))
            additional_numerical_parameter_units.append(self._read_line(f))
            additional_numerical_parameter_values.append(self._read_line(f))
        if block["number_of_additional_numerical_parameters"] > 0:
            # 69 additional_numerical_parameter_labels
            block["additional_numerical_parameter_labels"] = additional_numerical_parameter_labels
            # 70 additional_numerical_parameter_units
            block["additional_numerical_parameter_units"] = additional_numerical_parameter_units
            # 71 additional_numerical_parameter_values
            block["additional_numerical_parameter_values"] = additional_numerical_parameter_values

        return block

    def _get_block_info_72_76(self, f: TextIOWrapper, block: dict) -> dict:
        """Obtain additional information in the block.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.
            block (dict): Block data before item addition.

        Returns:
            dict: Block data after item addition.

        """
        # 72 future_upgrade_block_entries
        future_upgrade_block_entries = []
        future_upgrade_block_entries_org = self.meta["number_of_future_upgrade_block_entries"] \
            if isinstance(self.meta["number_of_future_upgrade_block_entries"], int) \
            else 0
        for _ in range(future_upgrade_block_entries_org):
            future_upgrade_block_entries.append(self._read_line(f))
        if future_upgrade_block_entries:
            block["future_upgrade_block_entries"] = future_upgrade_block_entries

        # 73 number_of_ordinate_values
        block["number_of_ordinate_values"] = int(self._read_line(f))

        variables: list = []
        block["minimum_ordinate_values"] = []
        block["maximum_ordinate_values"] = []
        for _ in range(block["number_of_corresponding_variables"]):
            # 74 minimum_ordinate_values
            block["minimum_ordinate_values"].append(self._read_line(f))
            # 75 maximum_ordinate_values
            block["maximum_ordinate_values"].append(self._read_line(f))
            variables.append([])

        for _ in range(int(block["number_of_ordinate_values"] / block["number_of_corresponding_variables"])):
            for j in range(block["number_of_corresponding_variables"]):
                variables[j].append(self._read_line(f))

        # 76 ordinate_values
        block["ordinate_values"] = variables

        return block

    def _read_line(self, f: TextIOWrapper) -> str:
        """One line reads.

        Args:
            f (TextIOWrapper): Buffered text of the measurement file interface.

        Returns:
            str: One line string.

        """
        ret = f.readline()
        if ret == "":
            err_msg = f"end of file: {self.rawfile_name}"
            raise StructuredError(err_msg)

        ret = ret.rstrip().replace("\x00", "")
        return self._check_outlier(ret)

    def _check_outlier(self, _val: str) -> str:
        """Outlier Check.

        Args:
            _val(str): Character string to be checked.

        Returns:
            str: Check, and string after replacement.

        """
        # Leave blank for ex. "1e+37", "1E37", and "1e+37".
        m = re.fullmatch(r"1[eE][\+]*0*37", _val)
        if m is not None:
            _val = ""
        return _val

    def _count_decimal_places(self, num: float) -> int:
        """Convert floating point numbers to strings.

        Args:
            num (float): Floating-point number.

        Returns:
            int: Number of decimal places.

        """
        num_str = str(num)
        return len(num_str.split('.')[1]) if '.' in num_str else 0
