# utils/environment.py

import os
import sys
import ctypes.util
from dataclasses import dataclass
from typing import Optional


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class EnvironmentConfig:
    """
    Configuration for external dependencies (TiXI / TiGL).
    """

    tixi_bin: str
    tigl_bin: str
    tixi_python: str
    tigl_python: str


def default_config() -> EnvironmentConfig:
    """
    Default configuration.

    Priority:
        1. Environment variables
        2. Fallback to local paths
    """

    base = os.environ.get(
        "AEROFRAME_LIBS",
        r"C:\Users\hemra\source\repos\Libs"
    )

    return EnvironmentConfig(
        tixi_bin=os.path.join(base, "TIXI-3.3.1", "bin"),
        tigl_bin=os.path.join(base, "TIGL-3.4.1", "bin"),
        tixi_python=os.path.join(base, "TIXI-3.3.1", "share", "tixi3", "python"),
        tigl_python=os.path.join(base, "TIGL-3.4.1", "share", "tigl3", "python"),
    )


# ============================================================
# ENVIRONMENT SETUP
# ============================================================

_ENV_INITIALIZED = False


def setup_environment(config: Optional[EnvironmentConfig] = None) -> None:
    """
    Configure runtime environment for TiXI and TiGL.

    Safe to call multiple times.
    """
    global _ENV_INITIALIZED

    if _ENV_INITIALIZED:
        return

    if config is None:
        config = default_config()

    _validate_paths(config)
    _add_dll_directories(config)
    _patch_find_library(config)
    _add_python_paths(config)

    _ENV_INITIALIZED = True


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _validate_paths(config: EnvironmentConfig) -> None:
    """
    Ensure required paths exist.
    """

    paths = [
        config.tixi_bin,
        config.tigl_bin,
        config.tixi_python,
        config.tigl_python,
    ]

    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Required path not found: {path}\n"
                "Check your EnvironmentConfig or AEROFRAME_LIBS."
            )


def _add_dll_directories(config: EnvironmentConfig) -> None:
    """
    Add DLL directories (Windows-specific).
    """
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(config.tixi_bin)
        os.add_dll_directory(config.tigl_bin)


def _patch_find_library(config: EnvironmentConfig) -> None:
    """
    Patch ctypes.find_library for TiXI/TiGL resolution.
    """

    original_find_library = ctypes.util.find_library

    def custom_find_library(name: str):
        if name == "tixi3":
            return os.path.join(config.tixi_bin, "tixi3.dll")
        if name == "tigl3":
            return os.path.join(config.tigl_bin, "tigl3.dll")

        return original_find_library(name)

    ctypes.util.find_library = custom_find_library


def _add_python_paths(config: EnvironmentConfig) -> None:
    """
    Add Python bindings to sys.path.
    """

    if config.tixi_python not in sys.path:
        sys.path.append(config.tixi_python)

    if config.tigl_python not in sys.path:
        sys.path.append(config.tigl_python)
