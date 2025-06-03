from __future__ import annotations

from typing import Any

from rdetoolkit.invoicefile import InvoiceFile, overwrite_invoicefile_for_dpfterm
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath
from rdetoolkit.rde2util import read_from_json_file


class InvoiceWriter:
    """Invoice overwriter.

    Overwrite invoice.json files depending on conditions.

    """

    def __init__(self, config: dict):
        self.config: dict = config

    def overwrite_invoice_measured_date(
        self,
        suffix: str,
        resource_paths: RdeOutputResourcePath,
        meta: MetaType,
    ) -> None:
        """Overwrite invoice if needed.

        The date is to be obtained from the output device and output to invoice.
        The measurement date and time are written automatically to the invoice.json file
        # based on the file meta data output from the device, so I added a process to write it to invoice.json.

        Args:
            suffix (str): Input file extension.
            resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.
            meta: (dict[str, ExtendMetaType]): Metadata.

        """
        invoice_obj = read_from_json_file(resource_paths.invoice_org)
        update_invoice_term_info = self._get_update_mesurement_date_dpf_metadata(
            suffix,
            invoice_obj,
            meta,
        )
        if update_invoice_term_info:
            overwrite_invoicefile_for_dpfterm(
                invoice_obj,
                resource_paths.invoice_org,
                resource_paths.invoice_schema_json,
                update_invoice_term_info,
            )
            invoice_org_obj = InvoiceFile(resource_paths.invoice_org)
            invoice_org_obj.overwrite(resource_paths.invoice.joinpath("invoice.json"))

    def _get_update_mesurement_date_dpf_metadata(
        self,
        suffix: str,
        invoice_obj: dict[str, Any],
        meta: MetaType,
    ) -> dict[str, str]:
        """Update metadata information about the measurement date and time.

        This function works exclusively with ulvac_phi.
        Due to the different vocabulary used in ulvac_phi to indicate the measurement date and time,
        the process is specifically defined for these formats.

        Args:
            suffix (str): file extension.
            invoice_obj (dict[str, Any]): Object of ivnoice.json or invoice_org.json.
            meta: (dict[str, ExtendMetaType]): Metadata.

        Returns:
            dict[str, str]: Metadata information updated with the measurement date and time

        """
        update_invoice_term_info: dict[str, str] = {}
        if "measurement_measured_date" not in invoice_obj["custom"]:
            return update_invoice_term_info

        keywd: str = ""
        match suffix.lower():
            case ".spe" | ".pro" | ".ang":
                keywd = "AcqFileDate"

        mesurement_date_value = invoice_obj["custom"].get("measurement_measured_date")
        if meta.get(keywd) and not mesurement_date_value:
            update_invoice_term_info["measurement_measured_date"] = str(meta[keywd])
        # MEMO: "AcqFileDate" is only in 'const_meta', so 'repeat_meta' is not considered.
        return update_invoice_term_info
