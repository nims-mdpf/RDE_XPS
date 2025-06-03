from __future__ import annotations

import os.path
import re
from collections.abc import Iterable
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import matplotlib.ticker as ptick
import numpy as np
import pandas as pd
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.mplot3d import Axes3D
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath

from modules_xps.graph_handler import GraphPlotter as XpsGraphPlotter


class GraphPlotter(XpsGraphPlotter):
    """Utility for plotting data using various types of plots.

    This class provides methods to generate and save different types of plots based on provided data.
    It supports line plots, log-scale plots, and multi-plots where multiple series are plotted on the same graph.

    """

    MAX_TITLE_LENGTH = 35

    def __init__(self) -> None:
        super().__init__()

    def plot_main(
        self,
        resource_paths: RdeOutputResourcePath,
        meta: MetaType,
        data: pd.DataFrame,
        _data_blocks: list[dict],
        data_atoms: list[dict] | None,
        config: dict,
    ) -> None:
        """Visualization from PRO or ANG files handled by ULVAC-PHI.

        Args:
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            meta (dict[str, ExtendMetaType]): Meta data.
            data (pd.DataFrame): All measurement data.
            _data_blocks (list[dict]): unused.
            data_atoms (list[dict]): Data by atomic.
            config (dict): Configuration details.

        """
        # Intensity
        plot_options = self._read_plot_options(meta, resource_paths, "intensity")
        self._plot_profile_intensity(data, plot_options)

        # Spectrum - By atomic
        if data_atoms is not None:
            for data_atomic_org in data_atoms:
                df_cps_org = data_atomic_org.get('df_cps')
                if df_cps_org is not None:
                    data_atomic = df_cps_org.astype(float)
                plot_options = self._read_plot_options(
                    meta,
                    resource_paths,
                    "spectrum",
                    file_cps=data_atomic_org.get('file_cps'),
                    columns=data_atomic.columns[1:],
                )
                self._plot_profile_spectrum_2d(data_atomic, plot_options)
                if not config["xps"]["no3dimage"]:
                    self._plot_profile_spectrum_3d(data_atomic, plot_options)

        # Spectrum - All
        plot_options = self._read_plot_options(meta, resource_paths, "spectrum_all")
        if data_atoms is not None:
            self._plot_profile_spectrum_all_2d(data_atoms, plot_options)
            if not config["xps"]["no3dimage"]:
                self._plot_profile_spectrum_all_3d(data_atoms, plot_options)

    def _read_plot_options(
            self,
            meta: MetaType,
            resource_paths: RdeOutputResourcePath,
            plot_type: str,
            *,
            file_cps: Path | None = None,
            columns: list | None = None,
    ) -> dict:
        """Set optional information necessary for plots.

        Args:
            meta (dict[str, ExtendMetaType]): Meta data.
            resource_paths (RdeOutputResourcePath): List of RDE output paths.
            plot_type (str): "intensity" or "spectrum" or "spectrum_all"
            file_cps (str | None): Cps file path.
            columns: (list | None): Dataframe columns.

        Return:
            dict: Plot options data.

        """
        writefile_2d = ""
        writefile_3d = ""
        x_label = meta.get("xlabel", "x")
        y_label = meta.get("ylabel", "y")
        z_label = meta.get("zlabel", "z")
        axis_inverse_x = meta["xoption"] == "reverse"
        collection_time = 0
        z_list = []

        match plot_type:
            case "intensity":
                title = resource_paths.rawfiles[0].stem
                writefile_2d = os.path.join(resource_paths.main_image, f"{title}.png")
                y_label = "Intensity (arb.units)"

            case "spectrum":
                if file_cps is not None:
                    title, _ = os.path.splitext(os.path.basename(file_cps))
                    file_name_ext = Path(os.path.basename(file_cps)).stem.replace(resource_paths.rawfiles[0].stem + '_', '')
                writefile_2d = os.path.join(resource_paths.other_image, f"{title}.png")
                writefile_3d = os.path.join(resource_paths.other_image, f"{title}_3d.png")
                if isinstance(meta["SpectralRegDef"], list):
                    collection_time = [tokens[10] for tokens in meta["SpectralRegDef"] if tokens[2] == file_name_ext][0]
                if isinstance(columns, Iterable):
                    for v in columns:
                        col_number = re.match(r"^([\d.]+)", v)
                        if isinstance(col_number, re.Match):
                            z_list.append(float(col_number.group(1)))

            case "spectrum_all":
                title = resource_paths.rawfiles[0].stem[:self.MAX_TITLE_LENGTH] + "..." + "_spectraAll" \
                    if len(resource_paths.rawfiles[0].stem) > self.MAX_TITLE_LENGTH \
                    else resource_paths.rawfiles[0].stem + "_spectraAll"
                writefile_2d = os.path.join(resource_paths.other_image, f"{resource_paths.rawfiles[0].stem}_speall.png")
                writefile_3d = os.path.join(resource_paths.other_image, f"{resource_paths.rawfiles[0].stem}_speall_3d.png")

        return {
            "title": title,
            "writefile_2d": writefile_2d,
            "writefile_3d": writefile_3d,
            "xlabel": x_label,
            "ylabel": y_label,
            "zlabel": z_label,
            "axisInverse_x": axis_inverse_x,
            "collection_time": collection_time,
            "zList": z_list,
        }

    def _plot_profile_intensity(self, data: pd.DataFrame, plot_options: dict) -> None:
        """Plot profile data for all energy levels based on data.

        Args:
            data (pd.DataFrame): Profile data.
            plot_options (dict): Plot options data.

        """
        legend = [v.split("_")[0] for v in data.columns[1:]]
        df = data.astype(float)
        ax = df.plot(x=0, legend=False, title=plot_options["title"])
        ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
        # To the nearest 10^6 (sixth power of 10) units.
        ax.ticklabel_format(style="sci", axis="y", scilimits=(6, 6))

        ax.set_xlabel(plot_options["zlabel"])
        ax.set_ylabel("Intensity (arb.units)")
        ax.axis("tight")
        plt.legend(legend)
        plt.savefig(plot_options["writefile_2d"])
        plt.close()

    def _plot_profile_spectrum_2d(self, df: pd.DataFrame, plot_options: dict) -> None:
        """Plot multiple spectra simultaneously for different z-values, 2D plot.

        Args:
            df (pd.DataFrame): Atomic data per block.
            plot_options (dict): Plot options data.

        """
        min_value = df.iloc[:, 0].min()
        max_value = df.iloc[:, 0].max()
        ax = df.plot(x=0, legend=False, title=plot_options["title"], grid=False, xlim=[min_value, max_value])
        fig = ax.get_figure()
        # Why two Y-axes(cps,counts)? Because they have different viewpoints. From Curator(Y).
        ax2 = ax.twinx()
        if plot_options["axisInverse_x"]:
            ax.invert_xaxis()
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
        ax2.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
        ax.set_xlabel(plot_options["xlabel"])
        ax.set_ylabel(plot_options["ylabel"])
        ax2.set_ylabel(plot_options["ylabel"].replace("(cps)", "(counts)"))

        min_cps, max_cps = ax.get_ylim()
        ax.margins(y=0)
        min_counts, max_counts = ax.get_ylim()
        min_c = min_counts * float(plot_options["collection_time"])
        max_c = max_counts * float(plot_options["collection_time"])
        margin = (max_c - min_c) * 0.05
        ax.set_ylim(min_cps, max_cps)
        ax2.set_ylim(min_c - margin, max_c + margin)
        fig.tight_layout()
        plt.savefig(plot_options["writefile_2d"])
        plt.close()

    def _plot_profile_spectrum_3d(self, df_org: pd.DataFrame, plot_options: dict) -> None:
        """Plot multiple spectra simultaneously for different z-values, 3D plot.

        Args:
            df_org (pd.DataFrame): Atomic data per block.
            plot_options (dict): Plot options data.

        Raises:
            StructuredError: Data mismatch.

        """
        if df_org.shape[1] - 1 != len(plot_options["zList"]):
            err_msg = "Data mismatch in plot_profile_spectrum_3d"
            raise StructuredError(err_msg)

        zvalues = np.array(plot_options["zList"], dtype=np.float64)
        zmin = zvalues.min()
        zmax = zvalues.max()
        df = df_org.copy()
        df.columns = [df.columns[0]] + list(plot_options["zList"])
        x = df.iloc[:, 0].values
        xmin = x.min()
        xmax = x.max()
        ymin = df.iloc[:, 1:].min().min()
        ymax = df.iloc[:, 1:].max().max()
        fig = plt.figure()
        ax = cast(Axes3D, fig.add_subplot(projection='3d'))

        # Plot the second and subsequent columns in reverse order
        for col in df.columns[1:][::-1]:
            y = df[col]
            zvalue = float(col)
            ax.plot(x, y, zs=zvalue, zdir="y")

        ax.set_title(plot_options["title"])
        ax.set_xlim(xmin, xmax)
        if plot_options["axisInverse_x"]:
            ax.invert_xaxis()
        ax.set_ylim(zmin, zmax)
        ax.set_zlim(ymin, ymax)
        ax.zaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.set_xlabel(plot_options["xlabel"])
        ax.set_ylabel(plot_options["zlabel"])
        ax.set_zlabel(plot_options["ylabel"])
        ax.ticklabel_format(style="sci", axis="z", scilimits=(0, 0))  # Index part is hidden (layout problem?)
        fig.savefig(plot_options["writefile_3d"])
        plt.close()

    def _plot_profile_spectrum_all_2d(self, data_atoms: list[dict], plot_options: dict) -> None:
        """Plot profile spectra all at once, 2D-plot.

        Args:
            data_atoms (list[dict]): All atoms data.
            plot_options (dict): Plot options data.

        """
        fig, ax = plt.subplots()
        fig2, ax2 = plt.subplots()

        for _, data_atomic in enumerate(data_atoms):
            df_cps_org = data_atomic.get('df_cps')
            if df_cps_org is not None:
                df = df_cps_org.astype(float)
            df_counts_org = data_atomic.get('df_counts')
            if df_counts_org is not None:
                df_counts = df_counts_org.astype(float)
            x = df.iloc[:, 0].values
            x_counts = df_counts.iloc[:, 0].values

            for i, col_name in enumerate(df.columns[1:][::-1]):
                ax.plot(x, df[col_name].values, color=f"C{i}")
                col_name_counts = col_name.replace("cps", "counts")
                ax2.plot(x_counts, df_counts[col_name_counts].values, color=f"C{i}")

        if plot_options["axisInverse_x"]:
            ax.invert_xaxis()
            ax2.invert_xaxis()

        ax.set_title(plot_options["title"])
        ax.set_xlabel(plot_options["xlabel"])
        ax.set_ylabel(plot_options["ylabel"])
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

        ax2.set_title(plot_options["title"])
        ax2.set_xlabel(plot_options["xlabel"])
        ax2.set_ylabel(plot_options["ylabel"].replace('(cps)', '(counts)'))
        ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax2.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

        fig.tight_layout()
        fig2.tight_layout()
        fig.savefig(plot_options["writefile_2d"])
        writefile = plot_options["writefile_2d"].replace("speall.png", "speall_count.png")
        fig2.savefig(writefile)

    def _plot_profile_spectrum_all_3d(self, data_atoms: list[dict], plot_options: dict) -> None:
        """Plot profile spectra all at once, 3D-plot.

        Args:
            data_atoms (list[dict]): All atoms data.
            plot_options (dict): Plot options data.

        """
        fig = plt.figure()
        ax = cast(Axes3D, fig.add_subplot(projection='3d'))
        x_list = []
        y_list = []
        z_list = []

        for _, data_atomic in enumerate(data_atoms):
            df_cps_org = data_atomic.get('df_cps')
            if df_cps_org is not None:
                df = df_cps_org.astype(float)
            x = df.iloc[:, 0].values
            x_list += list(x)

            for i, col_name in enumerate(df.columns[1:][::-1]):
                y = df[col_name].values
                y_list += list(y)
                # Extract the leading numbers from col as z value
                col_begin_float = re.match(r"^([\d.]+)", col_name)
                if col_begin_float is not None:
                    z = float(col_begin_float.group(1))
                    z_list += [z]
                ax.plot(x, y, zs=z, color=f"C{i}", zdir="y")

        x_list = np.array(x_list)
        y_list = np.array(y_list)
        z_list = np.array(z_list)
        ax.set_xlim(x_list.min(), x_list.max())
        ax.set_ylim(z_list.min(), z_list.max())
        ax.set_zlim(y_list.min(), y_list.max())

        if plot_options["axisInverse_x"]:
            ax.invert_xaxis()

        ax.set_title(plot_options["title"])
        ax.zaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.set_xlabel(plot_options["xlabel"])
        ax.set_zlabel(plot_options["ylabel"])
        ax.set_ylabel(plot_options["zlabel"])
        ax.ticklabel_format(style="sci", axis="z", scilimits=(0, 0))
        fig.savefig(plot_options["writefile_3d"])
