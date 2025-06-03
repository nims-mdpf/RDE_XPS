from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

import pandas as pd
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath, RepeatedMetaType
from rdetoolkit.rde2util import Meta

from modules_xps.models import MeasurementConditions

T = TypeVar("T")
ExtendMetaType = MetaType | MeasurementConditions


class IInputFileParser(ABC):
    """Abstract base class (interface) for input file parsers.

    This interface defines the contract that input file parser
    implementations must follow. The parsers are expected to read files
    from a specified path, parse the contents of the files, and provide
    options for saving the parsed data.

    Methods:
        read: A method expecting a file path and responsible for reading a file.

    Example implementations of this interface could be for parsing files
    of different formats like CSV, Excel, JSON, etc.

    """

    @abstractmethod
    def read(
        self,
        resource_paths: RdeOutputResourcePath,
    ) -> tuple[MetaType, pd.DataFrame, list[dict], list[dict] | None]:
        """Read."""
        raise NotImplementedError


class IStructuredDataProcessor(ABC):
    """Abstract base class (interface) for structured data parsers.

    This interface defines the contract that structured data parser
    implementations must follow. The parsers are expected to transform
    structured data, such as DataFrame, into various desired output formats.

    Methods:
        to_csv: A method that saves the given data to a CSV file.

    Implementers of this interface could transform data into various
    formats like CSV, Excel, JSON, etc.

    """

    @abstractmethod
    def save_file(
        self,
        resource_paths: RdeOutputResourcePath,
        meta: MetaType,
        data: pd.DataFrame,
        data_blocks: list | None,
        data_atoms: list | None,
    ) -> None:
        """Save file."""
        raise NotImplementedError


class IMetaParser(Generic[T], ABC):
    """Abstract base class (interface) for meta information parsers.

    This interface defines the contract that meta information parser
    implementations must follow. The parsers are expected to save the
    constant and repeated meta information to a specified path.

    Method:
        save_meta: Saves the constant and repeated meta information to a specified path.
        parse: This method returns two types of metadata: const_meta_info and repeated_meta_info.

    """

    @abstractmethod
    def parse(
        self,
        meta: MetaType,
        data_blocks_with_numeric_data: list[dict],
    ) -> tuple[MetaType, RepeatedMetaType]:
        """Parse."""
        raise NotImplementedError

    @abstractmethod
    def save_meta(
        self,
        save_path: Path,
        meta: Meta, *,
        const_meta_info: MetaType | None = None,
        repeated_meta_info: RepeatedMetaType | None = None,
    ) -> None:
        """Save meta."""
        raise NotImplementedError


class IGraphPlotter(Generic[T], ABC):
    """Abstract base class (interface) for graph plotting implementations.

    This interface defines the contract that graph plotting
    implementations must follow. The implementations are expected
    to be capable of plotting a simple graph using a given pandas DataFrame.

    Methods:
        simple_plot: Plots a simple graph using the provided pandas DataFrame.

    """

    @abstractmethod
    def plot_main(
        self,
        resource_paths: RdeOutputResourcePath,
        meta: MetaType,
        data: pd.DataFrame,
        data_blocks: list[dict],
        data_atoms: list[dict] | None,
        config: dict,
    ) -> None:
        """Plot main."""
        raise NotImplementedError
