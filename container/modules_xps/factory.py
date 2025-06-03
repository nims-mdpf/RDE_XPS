from __future__ import annotations

from pathlib import Path

import yaml
from rdetoolkit import rde2util
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.rde2util import read_from_json_file

from modules_xps.graph_handler import GraphPlotter as XpsGraphPlotter
from modules_xps.inputfile_handler import FileReader as XpsFileReader
from modules_xps.invoice_handler import InvoiceWriter
from modules_xps.meta_handler import MetaParser as XpsMetaParser
from modules_xps.scienta_omicron.vms.graph_handler import GraphPlotter as VmsGraphPlotter
from modules_xps.scienta_omicron.vms.inputfile_handler import FileReader as VmsFileReader
from modules_xps.scienta_omicron.vms.meta_handler import MetaParser as VmsMetaParser
from modules_xps.structured_handler import StructuredDataProcessor
from modules_xps.ulvac_phi.meta_handler import MetaParser as UlvacPhiMetaParser
from modules_xps.ulvac_phi.pro.graph_handler import GraphPlotter as ProGraphPlotter
from modules_xps.ulvac_phi.pro.inputfile_handler import FileReader as ProFileReader
from modules_xps.ulvac_phi.spe.graph_handler import GraphPlotter as SpeGraphPlotter
from modules_xps.ulvac_phi.spe.inputfile_handler import FileReader as SpeFileReader

SCIENTA_OMICRON_SUFFIX_CLASS_MAPPING = {
    "scienta_omicron": {
        ".vms": (VmsFileReader, VmsMetaParser, VmsGraphPlotter),
    },
}

ULVAC_PHI_SUFFIX_CLASS_MAPPING = {
    "ulvac_phi": {
        ".spe": (SpeFileReader, UlvacPhiMetaParser, SpeGraphPlotter),
        ".pro": (ProFileReader, UlvacPhiMetaParser, ProGraphPlotter),
        ".ang": (ProFileReader, UlvacPhiMetaParser, ProGraphPlotter),
    },
}


class XpsFactory:
    """Obtain a variety of data for use in the XPS's Structured processing."""

    def __init__(
        self,
        invoice_writer: InvoiceWriter,
        file_reader: XpsFileReader,
        meta_parser: XpsMetaParser,
        graph_plotter: XpsGraphPlotter,
        structured_processor: StructuredDataProcessor,
    ):
        self.invoice_writer = invoice_writer
        self.file_reader = file_reader
        self.meta_parser = meta_parser
        self.graph_plotter = graph_plotter
        self.structured_processor = structured_processor

    @staticmethod
    def get_config(invoice_org_path: Path, path_tasksupport: Path) -> dict:
        """Obtain a variety of data.

        Obtain configuration data.

        Args:
            invoice_org_path (Path): invoice file.
            path_tasksupport (Path): tasksupport path.

        Returns:
            config (dict): config data.

        """
        rdeconfig_file = path_tasksupport.joinpath("rdeconfig.yaml")

        # Get the graph scale of the representative image from rdeconfig.yaml.
        if not rdeconfig_file.exists():
            err_msg = f"File not found: {rdeconfig_file}"
            raise StructuredError(err_msg)
        try:
            with open(rdeconfig_file) as file:
                config: dict = yaml.safe_load(file)
        except Exception:
            err_msg = f"Invalid configuration file: {rdeconfig_file}"
            raise StructuredError(err_msg) from None

        invoice_obj = read_from_json_file(invoice_org_path)
        config["xps"]["no3dimage"] = invoice_obj["custom"]["no3dimage"] \
            if invoice_obj.get("custom", "").get("no3dimage") is not None \
            else False

        return config

    @staticmethod
    def get_objects(rawfile: Path, path_tasksupport: Path, config: dict) -> tuple[Path, XpsFactory, str]:
        """Obtain a variety of data.

        Retrieve the class to be executed.
        Obtain the metadata definition file to be used.

        Args:
            rawfile (Path): measurement file.
            path_tasksupport (Path): tasksupport path.
            config (dict): config data.

        Returns:
            metadata_def (Path): Metadata file path.
            module (XpsFactory): classes.
                InvoiceWriter (class): Overwrite invoice file.
                FilaReader (class): Reads and processes structured files into data and metadata blocks.
                MetaParser (class): Parses metadata and saves it to a specified path.
                GraphPlotter (class): Utility for plotting data using various types of plots.
                StructuredDataProcessor (class): Template class for parsing structured data.

        """
        suffix = rawfile.suffix.lower()

        # (Only on manufacturer: scienta_omicron, ulvac_phi) Input file extension check
        valid_extensions = {
            "scienta_omicron": {".vms"},
            "ulvac_phi": {".spe", ".pro", ".ang"},
        }
        manufacturer = config['xps']['manufacturer']
        if suffix not in valid_extensions.get(manufacturer, set()):
            err_msg = f"Format Error: Input data extension is incorrect: {suffix}"
            raise StructuredError(err_msg)

        # Obtain classes according to manufacturer and file extension.
        class_filereader, class_metaparser, class_graphplotter = get_classes(manufacturer, suffix)

        # Change the metadata definition file according to the file format.
        metadata_def = path_tasksupport.joinpath('metadata-def.json')

        # Get metadata default values
        default_value = rde2util.get_default_values(path_tasksupport.joinpath('default_value.csv'))

        module = XpsFactory(
            InvoiceWriter(config),
            class_filereader(config),
            class_metaparser(metadata_def_json_path=metadata_def, config=config, default_value=default_value),
            class_graphplotter(),
            StructuredDataProcessor(config=config),
        )

        return metadata_def, module, suffix


def get_classes(manufacturer: str, suffix: str) -> tuple[type[XpsFileReader], type[XpsMetaParser], type[XpsGraphPlotter]]:
    """Get the appropriate FileReader and MetaParser classes based on the manufacturer and file suffix."""
    try:
        match manufacturer:
            case "scienta_omicron":
                return SCIENTA_OMICRON_SUFFIX_CLASS_MAPPING[manufacturer][suffix]
            case "ulvac_phi":
                return ULVAC_PHI_SUFFIX_CLASS_MAPPING[manufacturer][suffix]
            case _:
                raise KeyError
    except KeyError:
        err_msg = f"Unsupported combination of manufacturer '{manufacturer}' and file extension '{suffix}'"
        raise StructuredError(err_msg) from None
