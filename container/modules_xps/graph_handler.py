from __future__ import annotations

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter

from modules_xps.interfaces import IGraphPlotter


class GraphPlotter(IGraphPlotter[pd.DataFrame]):
    """Utility for plotting data using various types of plots.

    This class provides methods to generate and save different types of plots based on provided data.
    It supports line plots, log-scale plots, and multi-plots where multiple series are plotted on the same graph.

    """

    def __init__(self) -> None:
        """Init."""

    def _set_ax_option(self, ax: Axes, plot_options: dict, graph_title: str, is_counts: bool = False) -> Axes:
        """Set matplotlib axes interface.

        Args:
            ax (Axes): Axes object.
            plot_options (dict): Plot option data.
            graph_title (str): Graph title.
            is_parent (bool): True(Y-axis 1st) or False(Y-axis 2nd).
            is_counts (bool): True(counts) or False(cps).

        Returns:
            Axes: Axes object.

        """
        formatter = ScalarFormatter(useMathText=True)
        ax.yaxis.set_major_formatter(formatter)
        if plot_options.get("axisInverse_x", False):
            ax.invert_xaxis()
        if plot_options.get("axisInverse_y", False):
            ax.invert_yaxis()
        if plot_options.get("axisScale_x", "") == "log":
            ax.set_xscale("log")
        if plot_options.get("axisScale_y", "") == "log":
            ax.set_yscale("log")
        if plot_options.get("axisFormat_y", plot_options.get("axisScale_y", "sci")) == "sci":
            ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
            ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
        if plot_options.get("grid", False):
            ax.grid(True)
        ax.set_title(graph_title)

        return self._set_ax_option_label(ax, plot_options, is_counts)

    def _set_ax_option_label(self, ax: Axes, plot_options: dict, is_counts: bool = False) -> Axes:
        """Set matplotlib axes interface.

        Args:
            ax (Axes): Axes object.
            plot_options (dict): Plot option data.
            graph_title (str): Graph title.
            is_counts (bool): True(counts) or False(cps).

        Returns:
            Axes: Axes object.

        """
        if "axisUnit_x" in plot_options:
            ax.set_xlabel(f"{plot_options['axisName_x']} ({plot_options['axisUnit_x']})")
        else:
            ax.set_xlabel(f"{plot_options['axisName_x']}")
        if "axisUnit_y" in plot_options:
            if is_counts and plot_options['axisUnit_y'] == "cps":
                ax.set_ylabel(f"{plot_options['axisName_y']} (counts)")
            else:
                ax.set_ylabel(f"{plot_options['axisName_y']} ({plot_options['axisUnit_y']})")
        else:
            ax.set_ylabel(f"{plot_options['axisName_y']}")

        return ax

    def _get_scalar_float(self, plot_options: dict, key: str) -> float | None:
        """Return the display range as a float.

        Args:
            plot_options (dict): Plot option data.
            key (str): "xmin" or "xmax".

        Returns:
            float: Display range as a float.

        """
        return float(plot_options[key][0]) if key in plot_options else None
