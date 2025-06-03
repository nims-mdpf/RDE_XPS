from __future__ import annotations

import datetime as dt
import zoneinfo
from collections import defaultdict
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

    def __init__(self, *, metadata_def_json_path: Path | None = None, config: dict[str, str | None], default_value: dict):
        super().__init__(metadata_def_json_path=metadata_def_json_path, config=config, default_value=default_value)
        self.repeated_meta_info: RepeatedMetaType = defaultdict(list)

    def parse(
            self,
            meta: MetaType,
            data_blocks_with_numeric_data: list[dict],
    ) -> tuple[MetaType, RepeatedMetaType]:
        """Parse and extract constant and repeated metadata from the provided data.

        Args:
            meta (dict[str, ExtendMetaType]): Meta data.
            data_blocks_with_numeric_data (list[dict]): Data per block (with numeric data).

        Returns:
            tuple[MetaType, RepeatedMetaType]: Metadata divided into 'constant' and 'variable'.

        """
        data_blocks: list = self._set_data_blocks(data_blocks_with_numeric_data)

        # Items for which header information can be used as is
        self.const_meta_info = {k: v for k, v in meta.items() if not isinstance(v, list)}

        if len(data_blocks) > 0:
            # Use last block value (RDE 1.0 compliant)
            self.const_meta_info["measurement.measured_date"] = dt.datetime(
                int(data_blocks[-1]["year_in_full"]),
                int(data_blocks[-1]["month"]),
                int(data_blocks[-1]["day_of_month"]),
            ).astimezone(tz=zoneinfo.ZoneInfo(key='Asia/Tokyo')).isoformat()

        abscissa_ends = []
        abscissa_labels = []
        corresponding_variables_labels = []
        for data_block in data_blocks:
            abscissa_start = float(data_block["abscissa_start"])
            abscissa_increment = float(data_block["abscissa_increment"])
            decimal_point = self._count_decimal_places(abscissa_increment)
            number_of_ordinate_values = float(data_block["number_of_ordinate_values"])
            abscissa_end = round(float(abscissa_start + abscissa_increment * (number_of_ordinate_values - 1)), decimal_point)
            abscissa_ends.append(abscissa_end)

            label1 = data_block["abscissa_label"]
            unit1 = data_block["abscissa_units"]
            abscissa_labels.append(f"{label1} ({unit1})")

            label2 = data_block["corresponding_variable_labels"]
            unit2 = data_block["corresponding_variable_units"]
            corresponding_variables_labels.append(f"{label2} ({unit2})")
        self.const_meta_info["abscissa_end"] = abscissa_ends
        self.const_meta_info["abscissa_label"] = abscissa_labels
        self.const_meta_info["corresponding_variables_label"] = corresponding_variables_labels

        # Items to be stored in 'variable' type. (derived from data_blocks)
        var_keys: set = set()
        for data_block in data_blocks:
            var_keys = var_keys | set(data_block.keys())
        self.repeated_meta_info = {
            k: [data_block.get(k) for data_block in data_blocks]
            for k
            in var_keys
            if k not in self.const_meta_info
        }

        return self.const_meta_info, self.repeated_meta_info

    def _set_data_blocks(self, data_blocks_with_numeric_data: list[dict]) -> list[dict]:
        """Set block data to exclude numeric data.

        Args:
            data_blocks_with_numeric_data (list[dict]): Data per block (with numeric data).

        Returns:
            list[dict]: Data per block.

        """
        data_blocks = []
        for data_block0 in data_blocks_with_numeric_data:
            data_block2 = {}
            for k in data_block0:
                if k in ["ordinate_values"]:
                    continue
                v = data_block0[k]
                if isinstance(v, list):
                    v = ",".join([str(e) for e in v]) if len(v) != 0 else ""
                data_block2[k] = v
            data_blocks.append(data_block2)

        return data_blocks

    def _count_decimal_places(self, num: float) -> int:
        """Convert floating point numbers to strings.

        Args:
            num (float): Floating-point number.

        Returns:
            int: Number of decimal places.

        """
        num_str = str(num)
        return len(num_str.split('.')[1]) if '.' in num_str else 0
