from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path, PureWindowsPath

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

    COLUMNS_CPS_DATA = 2
    MPEXPORT_BINPATH = Path(__file__).parent.parent.joinpath("MPExport.exe")

    def __init__(self, config: dict):
        super().__init__(config)
        self.meta: MetaType = {}

    def read(self, resource_paths: RdeOutputResourcePath) -> tuple[MetaType, pd.DataFrame, list[dict], list[dict]]:
        """Read the structured file and returns separated data and metadata.

        Args:
            resource_paths (RdeOutputResourcePath): The path of the structured file to read.

        Returns:
            MetaType: Meta data.
            pd.DataFrame: All measurement data.
            list[dict]: Block-by-Block additional data.
            list[dict]: Data by atomic.
                file_cps: Intensity(cps) file name.
                df_cps: Intensity(cps) dataframe.
                file_counts: Intensity(counts) file name.
                df_counts: Intensity(counts) dataframe.

        Raises:
            StructuredError: If the file is formatted incorrectly.

        """
        self.meta, data_org, data_blocks = self._read_tmp_txt(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.txt"))

        # Merge profile data for all energy levels
        df_singles = []
        for data_block, data_single in zip(data_blocks, data_org):
            if data_block["is_profile"]:
                file_name_ext = data_block["AtomicName"]

                # convert numerical data from csv-text to data frame
                zlabel = ""
                if isinstance(self.meta["zlabelname"], str) and isinstance(self.meta["zlabelunit"], str):
                    zlabel = self.meta["zlabelname"] + " (" + self.meta["zlabelunit"] + ")"
                columns = [zlabel, file_name_ext + "_Intensity (arb.units)"]
                df_single = pd.DataFrame(data_single, columns=columns)
                df_singles.append(df_single)

        if len(df_singles) == 0:
            err_msg = "Profile mode was selected, but not found profile data"
            raise StructuredError(err_msg)

        # Merge all data frames using the first column of each data frame as a common index
        data = pd.concat(
            [df.set_index(df.columns[0]) for df in df_singles], axis=1,
        )
        # Insert index column into data
        data.reset_index(inplace=True)

        # save spectrum data for each energy level
        z_list = data.iloc[:, 0].values

        data_atoms = []
        for data_block, data_single in zip(data_blocks, data_org):
            if not data_block["is_profile"]:
                atomic_data = self._save_spectrum_data(
                    data_block,
                    data_single,
                    resource_paths,
                    z_list,
                )
                data_atoms.append(atomic_data)

        return self.meta, data, data_blocks, data_atoms

    def convert_raw2txt_with_wine(self, resource_paths: RdeOutputResourcePath) -> str:
        """Convert XPS raw data of PHI to txt.

        Args:
            resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.

        Returns:
            bytes: Standard output of execution results.

        """
        if os.name != "nt":
            cmds = ["wine"]
            # It seems that even via wine, the delimiter character must be a backslash for windows to be accepted.
            file_path_input = PureWindowsPath(resource_paths.rawfiles[0])
            log_dir = PureWindowsPath(resource_paths.logs)
            out_dir = PureWindowsPath(resource_paths.struct)
        else:
            cmds = []
            file_path_input = resource_paths.rawfiles[0]  # type: ignore
            log_dir = resource_paths.logs  # type: ignore
            out_dir = resource_paths.struct  # type: ignore

        cmds += [
            str(self.MPEXPORT_BINPATH),
            f"-LogFolder:{log_dir}",
            f"-Filename:{file_path_input}",
            f"-OutputFolder:{out_dir}",
        ]
        # .ang and .pro needs "-ExportProfile"
        if resource_paths.rawfiles[0].suffix.lower() in [".ang", ".pro"]:
            cmds += ["-ExportProfile"]

        res = subprocess.run(
            cmds,
            encoding="utf_8",
            capture_output=True,
            check=True,
        )
        return res.stdout

    def _read_tmp_txt(self, txt_file_path: Path) -> tuple[MetaType, pd.DataFrame, list[dict]]:
        """Split a text file into multiple data blocks.

        The header information is then obtained from the first block,
        and the other blocks are obtained as numerical data blocks.

        Args:
            txt_file_path (Path): Txt data file path.

        Returns:
            dict[str, ExtendMetaType]: Meta data.
            pd.DataFrame: All measurement data.
            list[dict]: Block-by-Block additional data.

        """
        # Split a text file into multiple data blocks
        text_blocks = self._split_text_file(txt_file_path, "//Area Comment")

        # Get meta information from text_block_list[0]
        self.meta = self._text_block_to_meta(text_blocks[0])

        data = []
        data_blocks = []
        for text_block in text_blocks[1:]:
            # Decompose into header and numeric data
            spectral_data_meta = self._data_block_to_meta(text_block)
            num_header = len(spectral_data_meta)

            prefixes = ("Angle", "Sputter")
            spectral_data_meta["is_profile"] = \
                spectral_data_meta["XLabel"].startswith(prefixes) \
                if isinstance(spectral_data_meta["XLabel"], str) \
                else False

            # Convert numerical data from csv-text to data frame
            numerical_data = [text.split(",") for text in text_block[num_header + 1:] if text != ""]

            data_array = np.array(numerical_data)

            # Store in data, data_blocks
            data.append(data_array)
            data_blocks.append(spectral_data_meta)

        for spectral_data_meta in data_blocks:
            # Obtain meta-information about the x-, y- and z-axes
            # and merge it into self.meta.
            if spectral_data_meta["is_profile"] and isinstance(spectral_data_meta["XLabel"], str):
                zlabel_name, zlabel_unit, zoption, zlabel = self._read_label_text(
                    spectral_data_meta["XLabel"],
                )
                dict_axis = {
                    "zlabelname": zlabel_name,
                    "zlabelunit": zlabel_unit,
                    "zoption": zoption,
                    "zlabel": zlabel,
                }
            else:
                if isinstance(spectral_data_meta["XLabel"], str):
                    xlabel_name, xlabel_unit, xoption, xlabel = self._read_label_text(
                        spectral_data_meta["XLabel"],
                    )
                if isinstance(spectral_data_meta["YLabel"], str):
                    ylabel_name, ylabel_unit, yoption, ylabel = self._read_label_text(
                        spectral_data_meta["YLabel"],
                    )
                dict_axis = {
                    "xlabelname": xlabel_name,
                    "xlabelunit": xlabel_unit,
                    "xoption": xoption,
                    "xlabel": xlabel,
                    "ylabelname": ylabel_name,
                    "ylabelunit": ylabel_unit,
                    "yoption": yoption,
                    "ylabel": ylabel,
                }
            self.meta.update(dict_axis)

        return self.meta, data, data_blocks

    def _split_text_file(self, filename: Path, separator: str) -> list[list[str]]:
        """Split a text file into multiple data blocks using a specified separator.

        Args:
            filename (Path): Txt data file path.
            separator (str): Separator.

        Returns:
            list[list[str]]: Txt data block.

        """
        text_blocks = []
        enc = CharDecEncoding.detect_text_file_encoding(filename)
        with open(filename, encoding=enc) as file:
            lines = file.readlines()
            sublist: list = []
            for line in lines:
                if line.startswith(separator):
                    if sublist:
                        text_blocks.append(sublist)
                    sublist = [line.rstrip()]
                else:
                    sublist.append(line.rstrip())
            if sublist:
                text_blocks.append(sublist)
        return text_blocks

    def _text_block_to_meta(self, text_block: list[str]) -> dict:
        """Get meta information from a text data block.

        Args:
            text_block (list[str]): Text data blocks separated by newlines.

        Returns:
            list[dict[str, str]]: Meta information.

        """
        dct_hdr_one: dict = {}

        for line in text_block:
            tokens = [t.strip() for t in line.split(":", 1)]
            if len(tokens) != self.COLUMNS_CPS_DATA:
                continue
            k, v = tokens
            match k:
                case "AcqFileDate":
                    yy, mm, dd = v.split()[:3]
                    dct_hdr_one[k] = yy + mm.zfill(2) + dd.zfill(2)
                case "SpectralRegDef" | "SpectralRegDef2" | "DepthCalDef":
                    v_split = v.split()
                    if k == "SpectralRegDef" and v_split[2] == "Su1s":
                        v_split[2] = "Survey"
                    if k not in dct_hdr_one:
                        dct_hdr_one[k] = []
                    dct_hdr_one[k].append(v_split)
                case "SpatialAreaDesc":
                    # If the item consists of multiple lines,
                    # it is overwritten by the value of the last line. (RDE 1.0 compliant)
                    dct_hdr_one[k] = v
                case "FileType":
                    ...  # print(v)
                case _:
                    if v != "":
                        dct_hdr_one[k] = v

        return dct_hdr_one

    def _data_block_to_meta(self, text_block: list[str]) -> dict[str, str | bool]:
        """Extract metadata from txt data blocks converted from PHI XPS raw data.

        Args:
            text_block (list(str)): Text data blocks separated by newlines.

        Returns:
            dict(str, str): Metadata extracted from the header section.

        """
        header_list = text_block[0].removesuffix("//").split(",")
        spectral_data_meta: dict = {}
        for i, header in enumerate(header_list):
            spectral_data_meta[header] = text_block[1 + i]
        return spectral_data_meta

    def _read_label_text(self, text: str) -> tuple[str, str, str, str]:
        """Extract axis information from text.

        axis information are
            label: axis labels
            unit: axis unit
            option: axis options
        Converted to "cps" if axis unit is "c/s"

        Args:
            text (str): Text containing axis information. \
                        Examples: \
                            "Binding Energy(eV),reverse"
                            "Intensity(cps)"
                            "Intensity"

        Returns:
            tuple(str, str, str, str): Axis information.
                1. label name
                2. label unit
                3. label option
                4. label name and bracketed label unit

        """
        # Extract label
        label = ""
        axis_info = re.search(r"^([^,(]+)", text)
        if isinstance(axis_info, re.Match):
            label = axis_info.group(1).strip()

        # Extract unit
        unit_match = re.search(r"\((.*?)\)", text)
        unit = unit_match.group(1).strip() if unit_match else ""
        if unit == "c/s":
            unit = "cps"

        # Extract option
        option_match = re.search(r",([^,]+)$", text)
        option = option_match.group(1).strip() if option_match else ""

        label_unit = label + " (" + unit + ")"

        return label, unit, option, label_unit

    def _save_spectrum_data(
            self,
            data_block: dict,
            data_single: pd.DataFrame,
            resource_paths: RdeOutputResourcePath,
            z_list: list[str],
    ) -> dict[str, Path | pd.DataFrame]:
        """Save spectrum data block in CSV format.

        Args:
            data_block (dict): Additional data per atomic.
            data_single (pd.DataFrame): Dataframe per atomic.
            resource_paths (RdeOutputResourcePath): For path where structuredtext is saved.
            z_list (list(str)): Z values for multiple spectral data.

        Returns:
            file_cps: Intensity(cps) file name.
            df_cps: Intensity(cps) dataframe.
            file_counts: Intensity(counts) file name.
            df_counts: Intensity(counts) dataframe.

        """
        file_name_ext = data_block["AtomicName"]

        # Create column names; 2nd and subsequent columns are based on z_list
        xlabel = str(self.meta.get("xlabel", "x"))
        ylabel = str(self.meta.get("ylabel", "y"))
        zlabel_unit = str(self.meta["zlabelunit"])

        columns = [xlabel] + [f"{float(z):.6g}" + zlabel_unit + "_" + ylabel for z in z_list]

        df_cps = pd.DataFrame(data_single, columns=columns)

        # Output string data while keeping the number of significant digits
        file_cps = resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_{file_name_ext}.csv")

        if "(cps)" in ylabel:
            ylabel = ylabel.replace('(cps)', '(counts)')
            columns = [xlabel] + [f"{float(z):.6g}" + zlabel_unit + "_" + ylabel for z in z_list]
            df_counts_org = pd.DataFrame(data_single, columns=columns)
            df_counts = df_counts_org.iloc[:, 0]  # df_counts_x
            if isinstance(self.meta["SpectralRegDef"], list):
                collection_time = [tokens[10] for tokens in self.meta["SpectralRegDef"] if tokens[2] == file_name_ext]
            df_counts_y = df_counts_org.iloc[:, 1:].astype("float") * float(collection_time[0])
            for col in df_counts_y.columns:
                df_counts_y_float = df_counts_y[col].map(lambda x: f'{x:.4f}')
                df_counts = pd.concat([df_counts, df_counts_y_float], axis=1)
            file_counts = resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_{file_name_ext}_count.csv")

        return {"file_cps": file_cps, "df_cps": df_cps, "file_counts": file_counts, "df_counts": df_counts}
