from __future__ import annotations

import re
import zoneinfo
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from rdetoolkit.models.rde2types import MetaType, RepeatedMetaType

from modules_xps.meta_handler import MetaParser as XrdMetaParser


class MetaParser(XrdMetaParser):
    """Parses metadata and saves it to a specified path.

    This class is designed to parse metadata from a dictionary and save it to a specified path using
    a provided Meta object. It can handle both constant and repeated metadata.

    Attributes:
        const_meta_info (MetaType | None): Dictionary to store constant metadata.
        repeated_meta_info (RepeatedMetaType | None): Dictionary to store repeated metadata.

    """

    # List of positions in array
    # SpectralRegDef
    POS_PEAK_NAME_TRANSITIONS = 2
    POS_ABSCISSA_INCREMENT = 5
    POS_ABSCISSA_START = 6
    POS_ABSCISSA_END = 7
    POS_COLLECTION_TIME = 10
    POS_PASS_ENERGY = 11
    # SpectralRegDef2
    POS_TOTAL_ACQUISITION_NUMBER = 2
    POS_PEAK_SWEEP_NUMBER = 2
    # DepthCalDef
    POS_SPUTTERING_LAYER_PRESET_INTERVAL_TIME = 7
    POS_SPUTTERING_LAYER_PRESET_CYCLE_NUMBER = 8

    CONST_EXCEPTION_LIST = [
        "ImageSizeXY",  # original
        "SpectralRegDef",  # original
        "SpectralRegDef2",  # original
        "DepthCalDef",  # original
        "XraySource",
        "XrayPower",
        "XrayBeamDiameter",
        "AnalyserMode",
        "AnalyserWorkFcn",
        "SourceAnalyserAngle",
        "AnalyserSolidAngle",
        "SputterEnergy",
        "ProfSputterDelay",
        "SurvNumCycles",
    ]
    CONST_VALUE_WITH_UNIT = [
        "SputterEnergy",
        "ProfSputterDelay",
    ]
    VARIABLE_TARGET_LIST = [
        "XraySource",
        "AnalyserMode",
        "SurvNumCycles",
    ]
    VARIABLE_VALUE_WITH_UNIT = [
        "XrayPower",
        "XrayBeamDiameter",
        "AnalyserWorkFcn",
        "SourceAnalyserAngle",
        "AnalyserSolidAngle",
    ]

    def __init__(
            self,
            *,
            metadata_def_json_path: Path | None = None,
            config: dict[str, str | None],
            default_value: dict,
    ):
        super().__init__(metadata_def_json_path=metadata_def_json_path, config=config, default_value=default_value)
        self.repeated_meta_info: RepeatedMetaType = defaultdict(list)

    def parse(
            self,
            meta: MetaType,
            _: list[dict],
    ) -> tuple[MetaType, RepeatedMetaType]:
        """Parse and extract constant and repeated metadata from the provided data.

        Args:
            meta (dict[str, ExtendMetaType]): Meta data.

        Returns:
            tuple[MetaType, RepeatedMetaType]: Metadata divided into 'constant' and 'variable'.

        """
        # Items for which meta information can be used as is.
        self.const_meta_info = {
            k: v
            for k, v in meta.items()
            if k not in self.CONST_EXCEPTION_LIST
        }

        for k, v in meta.items():
            if k in self.CONST_VALUE_WITH_UNIT and isinstance(v, str):
                self.const_meta_info[k] = v.split()[0]

        # Processing of items requiring calculation from meta information.
        if "AcqFileDate" in meta and isinstance(meta["AcqFileDate"], str):
            dt_measured = datetime.strptime(meta["AcqFileDate"], "%Y%m%d").astimezone(tz=zoneinfo.ZoneInfo(key='Asia/Tokyo'))
            self.const_meta_info["measurement.measured_date"] = dt_measured.isoformat()

        # MEMO: Items that were variable length in the VAMAS format
        #       should also be variable length in the Other format instead of fixed length.
        basic_meta_var: dict = {}
        basic_meta_var = self._set_metadata_basic(meta, basic_meta_var)

        depth_meta_var: dict = {}
        depth_meta_var = self._set_metadata_using_depth_cal_def_1(meta, depth_meta_var)
        depth_meta_var = self._set_metadata_using_depth_cal_def_2(meta, depth_meta_var)

        # Items that should be stored in 'variable' type.
        spectral_meta_var: dict = {}
        spectral_meta_var = self._set_metadata_using_spectral_reg_def_1(meta, spectral_meta_var)
        spectral_meta_var = self._set_metadata_using_spectral_reg_def_2(meta, spectral_meta_var)
        spectral_meta_var = self._set_metadata_using_spectral_reg_def_3(meta, spectral_meta_var)

        # Create a dictionary that looks like a multiplication of 'spectral_meta_var' and 'depth_meta_var'.
        self._make_cross_dict(spectral_meta_var, depth_meta_var)
        self._make_cross_dict_2(basic_meta_var)

        return self.const_meta_info, self.repeated_meta_info

    def _set_metadata_basic(self, meta: MetaType, basic_meta_var: dict) -> dict:
        """Set basic variable-length metadata.

        Args:
            meta (MetaType): Meta data.
            basic_meta_var (dict): Basic variables meta.

        Returns:
            dict: Basic variables meta.

        """
        # Items for which meta information can be used as is.
        basic_meta_var = {
            k: [v]
            for k, v in meta.items()
            if k in self.VARIABLE_TARGET_LIST
        }

        for k, v in meta.items():
            if k in self.VARIABLE_VALUE_WITH_UNIT and isinstance(v, str):
                basic_meta_var[k] = [v.split()[0]]

        if "ImageSizeXY" in meta and isinstance(meta["ImageSizeXY"], str):
            xyr = meta["ImageSizeXY"].split()
            basic_meta_var["analysis_width_x"] = [xyr[0]]
            basic_meta_var["analysis_width_y"] = [xyr[1]]
            basic_meta_var["analysis_region"] = [xyr[2]]

        return basic_meta_var

    def _set_metadata_using_depth_cal_def_1(self, meta: MetaType, depth_meta_var: dict) -> dict:
        """Depth variable-length metadata settings part 1.

        Args:
            meta (MetaType): Meta data.
            depth_meta_var (dict): Depth variables meta.

        Returns:
            dict: Depth variables meta.

        """
        if "DepthCalDef" in meta and isinstance(meta["DepthCalDef"], list):
            cycle_list = [int(tok[8]) for tok in meta["DepthCalDef"] if len(tok) > self.POS_SPUTTERING_LAYER_PRESET_CYCLE_NUMBER]
            total_cycle_number = sum(cycle_list)
            self.const_meta_info["total_cycle_number"] = total_cycle_number

            cycle_control_list = [
                f"{tok[7]}min {tok[8]}cyc" for tok in meta["DepthCalDef"] if len(tok) > self.POS_SPUTTERING_LAYER_PRESET_CYCLE_NUMBER
            ]
            depth_meta_var["cycle_control_preset"] = cycle_control_list

        return depth_meta_var

    def _set_metadata_using_depth_cal_def_2(self, meta: MetaType, depth_meta_var: dict) -> dict:
        """Depth variable-length metadata settings part 2.

        Args:
            meta (MetaType): Meta data.
            depth_meta_var (dict): Depth variables meta.

        Returns:
            dict: Depth variables meta.

        """
        if "DepthCalDef" in meta and isinstance(meta["DepthCalDef"], list):
            depth_meta_var["software_preset_sputtering_layer_name"] = [
                f"{tok[1]}" for tok in meta["DepthCalDef"] if len(tok) > 1
            ]
            depth_meta_var["sputtering_layer_preset_interval_time"] = [
                f"{tok[7]}" for tok in meta["DepthCalDef"] if len(tok) > self.POS_SPUTTERING_LAYER_PRESET_INTERVAL_TIME
            ]
            depth_meta_var["sputtering_layer_preset_cycle_number"] = [
                f"{tok[8]}" for tok in meta["DepthCalDef"] if len(tok) > self.POS_SPUTTERING_LAYER_PRESET_CYCLE_NUMBER
            ]

        return depth_meta_var

    def _set_metadata_using_spectral_reg_def_1(self, meta: MetaType, spectral_meta_var: dict) -> dict:
        """Set spectral variable-length metadata part 1.

        Args:
            meta (MetaType): Meta data.
            spectral_meta_var (dict): Spectral variables meta.

        Returns:
            dict: Spectral variables meta.

        """
        if "SpectralRegDef" in meta and isinstance(meta["SpectralRegDef"], list):
            spectral_meta_var["peak_name"] = []
            spectral_meta_var["transitions"] = []
            spectral_meta_var = self._set_metadata_using_spectral_reg_def_tok(meta, spectral_meta_var)
            spectral_meta_var["abscissa_increment"] = [tokens[5] for tokens in meta["SpectralRegDef"] if len(tokens) > self.POS_ABSCISSA_INCREMENT]
            spectral_meta_var["abscissa_start"] = [tokens[6] for tokens in meta["SpectralRegDef"] if len(tokens) > self.POS_ABSCISSA_START]

        return spectral_meta_var

    def _set_metadata_using_spectral_reg_def_2(self, meta: MetaType, spectral_meta_var: dict) -> dict:
        """Set spectral variable-length metadata part 2.

        Args:
            meta (MetaType): Meta data.
            spectral_meta_var (dict): Spectral variables meta.

        Returns:
            dict: Spectral variables meta.

        """
        if "SpectralRegDef" in meta and isinstance(meta["SpectralRegDef"], list):
            spectral_meta_var["abscissa_end"] = [tokens[7] for tokens in meta["SpectralRegDef"] if len(tokens) > self.POS_ABSCISSA_END]
            spectral_meta_var["collection_time"] = [tokens[10] for tokens in meta["SpectralRegDef"] if len(tokens) > self.POS_COLLECTION_TIME]
            spectral_meta_var["pass_energy"] = [tokens[11] for tokens in meta["SpectralRegDef"] if len(tokens) > self.POS_PASS_ENERGY]

        return spectral_meta_var

    def _set_metadata_using_spectral_reg_def_3(self, meta: MetaType, spectral_meta_var: dict) -> dict:
        """Set spectral variable-length metadata part 3.

        Args:
            meta (MetaType): Meta data.
            spectral_meta_var (dict): Spectral variables meta.

        Returns:
            dict: Spectral variables meta.

        """
        if "SpectralRegDef2" in meta and isinstance(meta["SpectralRegDef2"], list):
            surv_num_cycles_str = meta.get("SurvNumCycles", "1")
            if isinstance(surv_num_cycles_str, str):
                surv_num_cycles = int(surv_num_cycles_str)
            spectral_meta_var["total_acquisition_number"] = \
                [surv_num_cycles * int(tokens[2]) for tokens in meta["SpectralRegDef2"] if len(tokens) > self.POS_TOTAL_ACQUISITION_NUMBER]
            spectral_meta_var["peak_sweep_number"] = \
                [tokens[2] for tokens in meta["SpectralRegDef2"] if len(tokens) > self.POS_PEAK_SWEEP_NUMBER]

        return spectral_meta_var

    def _set_metadata_using_spectral_reg_def_tok(self, meta: MetaType, spectral_meta_var: dict) -> dict:
        """Set spectral variable-length metadata (for peak_name, transitions).

        Args:
            meta (MetaType): Meta data.
            spectral_meta_var (dict): Spectral variables meta.

        Returns:
            dict: Spectral variables meta.

        """
        if "SpectralRegDef" in meta and isinstance(meta["SpectralRegDef"], list):
            for str_src in [tok[2] for tok in meta["SpectralRegDef"] if len(tok) > self.POS_PEAK_NAME_TRANSITIONS]:
                p_tokens1 = re.findall(r"(\d+|\D+)", str_src)
                if p_tokens1[0] == "Su":
                    val1 = "Survey"
                    val2 = ""
                elif p_tokens1[0] == "Va":  # Does not appear in CSV but only in metadata (RDE 1.0 compliant).
                    val1 = "Valence"
                    val2 = ""
                elif "_" in p_tokens1[0]:
                    p_tokens2 = p_tokens1[0].split("_", 1)
                    val1 = p_tokens2[0]
                    val2 = p_tokens2[1]
                else:
                    val1 = p_tokens1[0]
                    val2 = "".join(p_tokens1[1:])
                spectral_meta_var["peak_name"].append(val1)
                spectral_meta_var["transitions"].append(val2)

        return spectral_meta_var

    def _make_cross_dict(self, spectral_meta_var: dict, depth_meta_var: dict) -> None:
        """Create a cross dictionary by repeating the arrays in Spectral metadata and Depth metadata.

        Args:
            spectral_meta_var (dict): Spectral metadata.
            depth_meta_var (dict): Depth metadata.

        """
        num_spectral_meta_var = 1 if len(spectral_meta_var) == 0 else len(list(spectral_meta_var.values())[0])
        num_depth_meta_var = 1 if len(depth_meta_var) == 0 else len(list(depth_meta_var.values())[0])

        self.repeated_meta_info = {}
        # Repeat spectral_meta_var array block num_depth_meta_var times.
        for key, value in spectral_meta_var.items():
            self.repeated_meta_info[key] = [x for _ in range(num_depth_meta_var) for x in value]
        # Repeat depth_meta_var array block num_spectral_meta_var times, element by element.
        for key, value in depth_meta_var.items():
            self.repeated_meta_info[key] = [x for x in value for _ in range(num_spectral_meta_var)]

    def _make_cross_dict_2(self, basic_meta_var: dict) -> None:
        """Add basic metadata to all variable length data.

        Args:
            basic_meta_var (dict): Basic metadata.

        """
        num_repeated_meta = 1 if len(self.repeated_meta_info) == 0 else len(list(self.repeated_meta_info.values())[0])

        # MEMO: Set in the basic items of all arrays.
        for key, value in basic_meta_var.items():
            self.repeated_meta_info[key] = [x for _ in range(num_repeated_meta) for x in value]
