from __future__ import annotations

import io
import re
from pathlib import Path

import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath

from modules_xps.interfaces import IStructuredDataProcessor


class StructuredDataProcessor(IStructuredDataProcessor):
    """Template class for parsing structured data.

    This class serves as a template for the development team to read and parse structured data.
    It implements the IStructuredDataProcessor interface. Developers can use this template class
    as a foundation for adding specific file reading and parsing logic based on the project's
    requirements.

    Attributes:
        df_series_1 (pd.DataFrame): The first series of data.
        df_series_2 (pd.DataFrame): The second series of data.

    Example:
        csv_handler = StructuredDataProcessor()
        df = pd.DataFrame([[1,2,3],[4,5,6]])
        loaded_data = csv_handler.to_csv(df, 'file2.txt')

    """

    DELIMITER = "="
    EXCLUSIONS = ("blocks", "experiment_terminator", "file", "ordinate_values")

    def __init__(self, config: dict[str, str | None]) -> None:
        self.df_series_1 = pd.DataFrame()
        self.df_series_2 = pd.DataFrame()
        self.config: dict = config

    def save_file(
            self,
            resource_paths: RdeOutputResourcePath,
            meta: MetaType,
            data: pd.DataFrame,
            data_blocks: list | None,
            data_atoms: list | None,
    ) -> None:
        """Save the given DataFrame to a csv file.

        Args:
            resource_paths (RdeOutputResourcePath): Standard output of execution results.
            meta (dict[str, ExtendMetaType]): Metadata.
            data (pd.DataFrame): All measurement data.
            data_blocks (list | None): Block-by-Block additional data.
            data_atoms (list | None): Data by atomic.

        """
        match resource_paths.rawfiles[0].suffix.lower():
            case ".vms":
                txt_file = resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.txt")
                if isinstance(data_blocks, list):
                    self._write_txt_file(txt_file, meta, data_blocks)
                else:
                    err_msg = "Error: No data is output."
                    raise StructuredError(err_msg)

                pretreated_data = self._pretreatment_saving_csv_file(data, data_blocks)

                csv_file = resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.csv")
                pretreated_data.to_csv(csv_file, index=False)

            case ".spe":
                if isinstance(data_atoms, list):
                    for atomic_data in data_atoms:
                        atomic_data.get('df').to_csv(atomic_data.get('file'), index=False, lineterminator="\r\n")

            case ".pro" | ".ang":
                if isinstance(data_atoms, list):
                    for atomic_data in data_atoms:
                        atomic_data['df_cps'].to_csv(atomic_data['file_cps'], index=False, lineterminator="\r\n")
                        atomic_data['df_counts'].to_csv(atomic_data['file_counts'], index=False, lineterminator="\r\n")

                csv_file = resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.csv")
                data.to_csv(csv_file, index=False, lineterminator="\r\n")

    def _pretreatment_saving_csv_file(self, data: pd.DataFrame, data_blocks: list | None) -> pd.DataFrame:
        """Pretreatment saving csv file from vms file.

        Args:
            data (pd.DataFrame): All measurement data.
            data_blocks (list | None): Block-by-Block additional data.

        Returns:
            pd.DataFrame: Pretreated data.

        """
        if isinstance(data_blocks, list):
            data_copy = data.copy()
            axis_name_x = data_blocks[0].get("abscissa_label", [""]).strip()
            axis_name_y = ",".join(data_blocks[0].get("corresponding_variable_labels", [""])).strip()
            axis_unit_x = data_blocks[0].get("abscissa_units", [""]).strip()
            axis_unit_y = ",".join(data_blocks[0].get("corresponding_variable_units", [""])).strip()

            for index_legend in range(len(data_blocks)):
                if len(data_blocks) == 1:
                    data_copy.rename(columns={
                        index_legend * 2: axis_name_x + "(" + axis_unit_x + ")",
                        index_legend * 2 + 1: axis_name_y + "(" + axis_unit_y + ")",
                    }, inplace=True)
                else:
                    data_copy.rename(columns={
                        index_legend * 2: "(data" + str(index_legend + 1) + ")" + axis_name_x + "(" + axis_unit_x + ")",
                        index_legend * 2 + 1: "(data" + str(index_legend + 1) + ")" + axis_name_y + "(" + axis_unit_y + ")",
                    }, inplace=True)

        return data_copy

    def _write_txt_file(self, txt_file_path: Path, meta: MetaType, data_blocks: list) -> None:
        """Write metadata and numeric data to TXT files.

        Args:
            txt_file_path (Path): Txt file path.
            meta (dict[str, ExtendMetaType]): Meta data.
            data_blocks (list): Numeric data.

        """
        with open(txt_file_path, "w") as f:
            i = 0
            self._write_header_infomation(f, meta)
            for i, data_block in enumerate(data_blocks):
                self._write_nemeric_data_infomation(f, i + 1, data_block)
                self._write_nemeric_data(f, i + 1, data_block)

    def _write_header_infomation(self, f: io.TextIOWrapper, meta: MetaType) -> None:
        """Write metadata.

        Args:
            f (io.TextIOWrapper): Buffered text of the txt file interface.
            meta (dict[str, ExtendMetaType]): Meta data.

        """
        print("//HEADER INFORMATION", file=f)
        for key, value in meta.items():
            if key not in self.EXCLUSIONS:
                if key == "comment" and \
                        isinstance(value, str) and \
                        isinstance(meta["number_of_lines_in_comment"], int) and \
                        meta["number_of_lines_in_comment"] > 1:
                    value_str = '"' + value + '"'
                if type(value) is list:
                    v = [str(i) for i in value]
                    value_str = ",".join(v)
                else:
                    value_str = str(value)
                value_str = self._check_outlier(value_str)
                print(key, self.DELIMITER, value_str, sep="", file=f)

    def _write_nemeric_data_infomation(self, f: io.TextIOWrapper, i: int, block_info: dict) -> None:
        """Output additional information data.

        Args:
            f (io.TextIOWrapper): Buffered text of the txt file interface.
            i (int): Block number.
            block_info (dict): Additional information in block data

        """
        print("//Numeric Data Info", i, file=f)
        for key, value in block_info.items():
            if key not in self.EXCLUSIONS:
                if key == "block_comment" and block_info["number_of_lines_in_block_comment"] > 1:
                    value_str = '"' + value + '"'
                if type(value) is list:
                    v = [str(i) for i in value]
                    value_str = ",".join(v)
                else:
                    value_str = str(value)
                value_str = re.sub("[\r\n]+$", "", value_str)
                value_str = self._check_outlier(value_str)
                print(key, self.DELIMITER, value_str, sep="", file=f)

    def _write_nemeric_data(self, f: io.TextIOWrapper, i: int, block_info: dict) -> None:
        """Output neweric data.

        Args:
            f (io.TextIOWrapper): Buffered text of the txt file interface.
            i (int): Block number.
            block_info (dict):Numeric information in block data.

        """
        print("//Numeric Data", i, file=f)
        for data1 in block_info["ordinate_values"]:
            for val in data1:
                print(str(val), file=f)

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
