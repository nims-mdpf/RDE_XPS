from __future__ import annotations

import os.path
from pathlib import Path
from typing import cast

import pandas as pd
from matplotlib import pyplot as plt
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath

from modules_xps.graph_handler import GraphPlotter as XpsGraphPlotter


class GraphPlotter(XpsGraphPlotter):
    """Utility for plotting data using various types of plots.

    This class provides methods to generate and save different types of plots based on provided data.
    It supports line plots, log-scale plots, and multi-plots where multiple series are plotted on the same graph.

    """

    MAX_TITLE_LENGTH = 35
    REVERSE_NOT_INCLUDED = 1
    ATOMS_COUNTS_DATA = 1
    COLUMNS_COUNTS_DATA = 3
    TYPES_OF_CPS_AND_COUNTS = 2

    def __init__(self) -> None:
        super().__init__()

    def plot_main(
        self,
        resource_paths: RdeOutputResourcePath,
        _meta: MetaType,
        data: pd.DataFrame,
        data_blocks: list[dict],
        data_atoms: list[dict] | None,
        _config: dict,
    ) -> None:
        """Visualization from SPE files handled by ULVAC-PHI.

        Args:
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            _meta (MetaType): unused.
            data (pd.DataFrame): All measurement data.
            data_blocks (list[dict]): Block-by-Block additional data.
            data_atoms (list[dict] | None): Data by atomic.
            _config (dict): Configuration details.

        """
        if not isinstance(data_atoms, list):
            err_msg = "ERROR in graph_handler: No data available."
            raise StructuredError(err_msg)

        # get options
        plot_options, make_other_images = self._read_plot_options(resource_paths, data_blocks, data_atoms, data.columns.values)
        file_base_name, ____ = os.path.splitext(os.path.basename(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.csv")))

        # plot main image
        self._plot_main_image(data_atoms, resource_paths, file_base_name, plot_options)
        # plot other images
        if make_other_images:
            self._plot_other_image(data_atoms, resource_paths, file_base_name, plot_options)

    def _read_plot_options(
        self,
        resource_paths: RdeOutputResourcePath,
        data_blocks: list[dict],
        data_atoms: list[dict],
        columns: list | None = None,
    ) -> tuple[dict, bool]:
        """Set optional information necessary for plots.

        Args:
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            data_blocks (list[dict]): Block-by-Block additional data.
            data_atoms (list[dict]): Data by atomic.
            columns: (list | None): Dataframe columns.

        Return:
            tuple[dict, bool]: Information necessary for graph image.

        """
        title = resource_paths.rawfiles[0].stem
        legend_list = []
        if data_atoms is not None:
            legend_list = [
                Path(os.path.basename(str(f.get('file')))).stem.replace(resource_paths.rawfiles[0].stem + '_', '')
                for f in data_atoms
            ]
        axis = columns[0].split("(") if columns is not None else ""
        axis_name_x = axis[0].strip()
        axis_unit_x = axis[1].strip().rstrip(")")
        axis = columns[1].split("(") if columns is not None else ""
        axis_name_y = axis[0].strip()
        axis_unit_y = axis[1].strip().rstrip(")")
        # Header object list is converted to a single object.
        # Only the first object is to be retained. (From existing templates.)
        axis_inverse_x = False
        if data_blocks is not None:
            axis_inverse_x = len(data_blocks[0]['XLabel'].split(',')) > self.REVERSE_NOT_INCLUDED

        plot_options = {
            "title": title,
            "dimension": ["x", "y"],
            "axisName_x": axis_name_x,
            "axisUnit_x": axis_unit_x,
            "axisInverse_x": axis_inverse_x,
            "axisName_y": axis_name_y,
            "axisUnit_y": axis_unit_y,
            "legend": legend_list,
        }
        make_other_images = len(cast(list, plot_options["legend"])) > 1

        return plot_options, make_other_images

    def _plot_main_image(
        self,
        data_atoms: list[dict],
        resource_paths: RdeOutputResourcePath,
        file_base_name: str,
        plot_options: dict,
    ) -> None:
        """Plot main image.

        Args:
            data_atoms (list[dict]): Data by atomic.
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            file_base_name (str): Output file name.
            plot_options (dict): Plot options data.

        Raises:
            StructuredError: Error(csv columns are invalid).

        """
        if len(data_atoms) != len(plot_options["legend"]):
            err_msg = "ERROR in graph_handler: csv columns are invalid"
            raise StructuredError(err_msg)

        file_path_main_image = os.path.join(resource_paths.main_image, f"{file_base_name}.png")
        self._write_graph_main_image(data_atoms, plot_options, plot_options["title"], file_path_main_image)

    def _plot_other_image(
        self,
        data_atoms_org: list[dict],
        resource_paths: RdeOutputResourcePath,
        file_base_name: str,
        plot_options: dict,
    ) -> None:
        """Plot other image.

        Args:
            data_atoms_org (list[dict]): Data by atomic.
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            file_base_name (str): Output file name.
            plot_options (dict): Plot options data.

        Raises:
            StructuredError: Error(csv columns are invalid).

        """
        if len(data_atoms_org) != len(plot_options["legend"]):
            err_msg = "ERROR in graph_handler: csv columns are invalid"
            raise StructuredError(err_msg)

        for legend, data_atom_org in zip(plot_options["legend"], data_atoms_org):
            df_atom = data_atom_org['df'].astype(float)
            graph_title_other_image = f"{file_base_name}_{legend}"
            file_path_other_image = os.path.join(resource_paths.other_image, f"{file_base_name}_{legend}.png")
            self._write_graph_other_image(df_atom, plot_options, graph_title_other_image, file_path_other_image)

    def _write_graph_main_image(
        self,
        data_atoms: list[dict],
        plot_options: dict,
        graph_title_org: str,
        png_file_path: str,
    ) -> None:
        """Write graph image from Intensity cps.

        Args:
            data_atoms (list[dict]): Data by atomic.
            plot_options (dict): Plot options data.
            graph_title_org (str): Graph title.
            png_file_path (Path): Output file path.

        """
        # Titles should be abbreviated to no more than 35 characters.
        graph_title_short = graph_title_org[:self.MAX_TITLE_LENGTH] + "..." \
            if len(graph_title_org) > self.MAX_TITLE_LENGTH \
            else graph_title_org

        show_legend = not (len(data_atoms) <= self.ATOMS_COUNTS_DATA)

        fig = plt.figure(figsize=(6.4, 4.8))
        ax = fig.add_subplot(1, 1, 1)
        fig.subplots_adjust(left=0.17, bottom=0.155, right=0.95, top=0.9, wspace=None, hspace=None)

        ax = self._set_ax_option(ax, plot_options, graph_title_short, is_counts=False)

        x_factor = plot_options.get("scaleFactor_x", 1.0)
        y_factor = plot_options.get("scaleFactor_y", 1.0)
        min_c = 0
        max_c = 0
        for i_legend, data_atom_org in enumerate(data_atoms):
            df = data_atom_org['df'].astype(float)
            ax.plot(
                x_factor * df.iloc[:, 0],
                y_factor * df.iloc[:, 1],
                lw=1,
                label=plot_options["legend"][int(i_legend)],
            )
            temp_c = y_factor * df.iloc[:, 2].min()
            min_c = min(temp_c, min_c)
            temp_c = y_factor * df.iloc[:, 2].max()
            max_c = max(max_c, temp_c)
        if show_legend:
            ax.legend()

        ax.set_xlim(
            xmin=self._get_scalar_float(plot_options, "xmin"),
            xmax=self._get_scalar_float(plot_options, "xmax"),
        )
        ax.set_ylim(
            ymin=self._get_scalar_float(plot_options, "ymin"),
            ymax=self._get_scalar_float(plot_options, "ymax"),
        )
        fig.tight_layout()
        fig.savefig(png_file_path)
        plt.close(fig)

    def _write_graph_other_image(
        self,
        df_atom: pd.DataFrame,
        plot_options: dict,
        graph_title_org: str,
        png_file_path: str,
    ) -> None:
        """Write graph image from Intensity cps and counts.

        Args:
            df_atom (pd.DataFrame): All measurement data.
            plot_options (dict): Plot options data.
            graph_title_org (str): Graph title.
            png_file_path (Path): Output file path.

        """
        # Titles should be abbreviated to no more than 35 characters.
        graph_title_short = graph_title_org[:self.MAX_TITLE_LENGTH] + "..." \
            if len(graph_title_org) > self.MAX_TITLE_LENGTH \
            else graph_title_org

        # In the case of .spe, three columns of XY(cps)Y(counts) represent one series.
        # If the number of columns is 3, there is only one series, so the legend is not displayed.
        show_legend = not (len(df_atom.columns) <= self.COLUMNS_COUNTS_DATA)

        for i in range(self.TYPES_OF_CPS_AND_COUNTS):
            fig = plt.figure(figsize=(6.4, 4.8))
            ax = fig.add_subplot(1, 1, 1)
            fig.subplots_adjust(
                left=0.17, bottom=0.155, right=0.95, top=0.9, wspace=None, hspace=None,
            )

            is_counts = i != 0  # 0:cps, 1:counts

            ax = self._set_ax_option(ax, plot_options, graph_title_short, is_counts=is_counts)

            x_factor = plot_options.get("scaleFactor_x", 1.0)
            y_factor = plot_options.get("scaleFactor_y", 1.0)
            for i_legend in range(0, len(df_atom.columns), 3):
                ax.plot(
                    x_factor * df_atom.iloc[:, i_legend],
                    y_factor * df_atom.iloc[:, i_legend + i + 1],
                    lw=1,
                    label=plot_options["legend"][int(i_legend / 3)],
                )
            if show_legend:
                ax.legend()

            ax.set_xlim(
                xmin=self._get_scalar_float(plot_options, "xmin"),
                xmax=self._get_scalar_float(plot_options, "xmax"),
            )
            ax.set_ylim(
                ymin=self._get_scalar_float(plot_options, "ymin"),
                ymax=self._get_scalar_float(plot_options, "ymax"),
            )
            fig.tight_layout()
            if i == 0:
                fig.savefig(png_file_path)
            else:
                png_file_path_count = \
                    png_file_path.replace("main_image", "other_image").replace(".png", "_count.png")
                fig.savefig(Path(png_file_path_count))
            plt.close(fig)
