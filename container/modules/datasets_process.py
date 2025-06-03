from __future__ import annotations

from rdetoolkit.errors import catch_exception_with_message
from rdetoolkit.models.rde2types import RdeInputDirPaths, RdeOutputResourcePath
from rdetoolkit.rde2util import Meta

from modules_xps.factory import XpsFactory


@catch_exception_with_message()
def dataset(srcpaths: RdeInputDirPaths, resource_paths: RdeOutputResourcePath) -> None:
    """Execute structured processing in XPS.

    Execute structured text processing, metadata extraction, and visualization.
    It handles structured text processing, metadata extraction, and graphing.
    Other processing required for structuring may be implemented as needed.

    Args:
        srcpaths (RdeInputDirPaths): Paths to input resources for processing.
        resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.

    Returns:
        None

    Note:
        The actual function names and processing details may vary depending on the project.

    """
    # Get config & class to use
    config = XpsFactory.get_config(resource_paths.invoice_org, srcpaths.tasksupport)
    metadata_def, module, suffix = XpsFactory.get_objects(resource_paths.rawfiles[0], srcpaths.tasksupport, config)

    # Convert from raw file to txt file by MPExport.exe
    if suffix in [".spe", ".pro", ".ang"]:
        module.file_reader.convert_raw2txt_with_wine(resource_paths)
    # Read input file
    meta, data, data_blocks, data_atoms = module.file_reader.read(resource_paths)

    # Meta parse & save
    module.meta_parser.parse(meta, data_blocks)
    module.meta_parser.save_meta(resource_paths.meta.joinpath("metadata.json"), Meta(metadata_def))

    # Save csv
    module.structured_processor.save_file(resource_paths, meta, data, data_blocks, data_atoms)

    # Plot
    module.graph_plotter.plot_main(resource_paths, meta, data, data_blocks, data_atoms, config)

    # Overwrite invoice
    if suffix in [".spe", ".pro", ".ang"]:
        module.invoice_writer.overwrite_invoice_measured_date(suffix, resource_paths, meta)
