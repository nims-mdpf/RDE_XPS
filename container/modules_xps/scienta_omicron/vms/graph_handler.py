from __future__ import annotations

import os.path

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
    COLUMNS_CPS_DATA = 2

    def __init__(self) -> None:
        super().__init__()

    def plot_main(
        self,
        resource_paths: RdeOutputResourcePath,
        _meta: MetaType,
        data: pd.DataFrame,
        data_blocks: list[dict],
        _data_atoms: list[dict] | None,
        config: dict,
    ) -> None:
        """Visualization from VMS files.

        Args:
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            _meta (MetaType): unused.
            data (pd.DataFrame): All measurement data.
            data_blocks (list[dict]): Block-by-Block additional data.
            _data_atoms (list[dict] | None): unused.
            config (dict): Configuration details.

        """
        # Get options
        opt_org, make_other_images = self._read_plot_options(resource_paths, data_blocks, config)
        file_base_name, ____ = os.path.splitext(os.path.basename(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.csv")))

        # Main image
        self._plot_image(data, resource_paths, file_base_name, opt_org, is_main_image=True)
        # Other images
        if make_other_images:
            self._plot_image(data, resource_paths, file_base_name, opt_org, is_main_image=False)

    def _read_plot_options(self, resource_paths: RdeOutputResourcePath, data_blocks: list[dict], config: dict) -> tuple[dict, bool]:
        """Obtain the information necessary for graph image drawing from the block data.

        Args:
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            data_blocks (list[dict]): Block-by-Block additional data.
            config (dict): Configuration details.

        Returns:
            tuple[dict, bool]: Information necessary for graph image.

        """
        title = os.path.splitext(os.path.basename(resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}.csv")))[0]
        legend_list = []
        for idx, data_block in enumerate(data_blocks):
            legend = data_block.get("species_label", "")
            if not legend:
                legend = f"data{idx + 1}"
            legend_list.append(legend)
        if not legend_list:
            legend_list.append("data1")
        axis_name_x = data_blocks[0].get("abscissa_label", [""]).strip()
        axis_name_y = ",".join(data_blocks[0].get("corresponding_variable_labels", [""])).strip()
        axis_unit_x = data_blocks[0].get("abscissa_units", [""]).strip()
        axis_unit_y = ",".join(data_blocks[0].get("corresponding_variable_units", [""])).strip()
        axis_xnverse_x = config["xps"].get('axis_inverse_x', False)

        plot_options = {
            "title": title,
            "dimension": ["x", "y"],
            "axisName_x": axis_name_x,
            "axisUnit_x": axis_unit_x,
            "axisInverse_x": axis_xnverse_x,
            "axisName_y": axis_name_y,
            "axisUnit_y": axis_unit_y,
            "legend": legend_list,
        }
        make_other_images = len(plot_options["legend"]) > 1

        return plot_options, make_other_images

    def _plot_image(
        self,
        df: pd.DataFrame,
        resource_paths: RdeOutputResourcePath,
        file_base_name: str,
        plot_options: dict,
        is_main_image: bool,
    ) -> None:
        """Plot graph image.

        Args:
            df (pd.DataFrame): All measurement data.
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            file_base_name (str): Output image file name.
            plot_options (dict): Information necessary for graph image.
            is_main_image (bool): True(main image) or False(other image).

        Raises:
            StructuredError: Error (csv columns are invalid error).

        """
        if len(df.columns) == len(plot_options["legend"]) * (len(plot_options["dimension"])):
            column_names = []
            for col in plot_options["legend"]:
                column_names += [f"{col}_{i}" for i in range(len(plot_options["dimension"]) - 1)] + [col]
            df_image = df.rename(columns={i: column_names[i] for i in range(len(column_names))})
        else:
            err_msg = "ERROR in graph_handler: csv columns are invalid"
            raise StructuredError(err_msg)

        if is_main_image:
            file_path_main_image = os.path.join(resource_paths.main_image, f"{file_base_name}.png")
            self._write_graph_img_file(df_image, plot_options, plot_options["title"], file_path_main_image, is_parent=True)
        else:
            for index_legend in range(0, len(df_image.columns), 2):
                df_single = df_image.iloc[:, index_legend:index_legend + 2]
                legend = df_image.columns[index_legend + 1]
                graph_title_other_image = f'{plot_options["title"]}_{legend}'
                file_path_other_image = os.path.join(resource_paths.other_image, f"{file_base_name}_{legend}.png")
                self._write_graph_img_file(df_single, plot_options, graph_title_other_image, file_path_other_image, is_parent=False)

    def _write_graph_img_file(self, df: pd.DataFrame, plot_options: dict, graph_title_org: str, png_file_path: str, is_parent: bool) -> None:
        """Write graph image.

        Args:
            df (pd.DataFrame): All measurement data.
            plot_options (dict): Information necessary for graph image.
            graph_title_org (str): Graph title.
            png_file_path (Path): Output image file path.
            is_parent (bool): True(main image) / False(other image).

        """
        # Titles should be abbreviated to no more than 35 characters.
        graph_title_short = graph_title_org[:self.MAX_TITLE_LENGTH] + "..." \
            if len(graph_title_org) > self.MAX_TITLE_LENGTH \
            else graph_title_org

        if "show_legend" in plot_options:
            show_legend = plot_options["show_legend"]
        elif len(df.columns) <= self.COLUMNS_CPS_DATA:
            # In the case of .vms, two columns of XY represent one series.
            # If two columns, there is only one series, so the legend is not displayed.
            show_legend = False
        else:
            show_legend = True

        fig = plt.figure(figsize=(6.4, 4.8))
        ax = fig.add_subplot(1, 1, 1)
        fig.subplots_adjust(left=0.17, bottom=0.155, right=0.95, top=0.9, wspace=None, hspace=None)

        ax = self._set_ax_option(ax, plot_options, graph_title_short, is_counts=False)
        x_factor = plot_options.get("scale_factor_x", 1.0)
        y_factor = plot_options.get("scale_factor_y", 1.0)

        for i_legend in range(0, len(df.columns), 2):
            ax.plot(
                x_factor * df.iloc[:, i_legend],
                y_factor * df.iloc[:, i_legend + 1],
                lw=1,
                label=df.columns[i_legend + 1],
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

        fig.savefig(png_file_path)
        plt.close(fig)
