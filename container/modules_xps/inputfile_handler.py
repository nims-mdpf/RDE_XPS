import pandas as pd
from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules_xps.interfaces import IInputFileParser


class FileReader(IInputFileParser):
    """Reads and processes structured ras files into data and metadata blocks.

    This class is responsible for reading structured files which have specific patterns for data and metadata.
    It then separates the contents into data blocks and metadata blocks.

    Attributes:
        data (dict[str, pd.DataFrame]): Dictionary to store separated data blocks.

    """

    def __init__(self, config: dict):
        self.data: dict[str, pd.DataFrame] = {}
        self.config = config

    def convert_raw2txt_with_wine(self, resource_paths: RdeOutputResourcePath) -> str:
        """There is no reality in the parent method."""
        return ""
