"""
Font utilities for RSSpythemes.

This module provides functions to register and use the bundled Source Sans Pro fonts
with matplotlib.
"""

from pathlib import Path
from typing import List, Dict, Optional

try:
    import matplotlib.font_manager as fm
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    import warnings
    warnings.warn(
        "matplotlib is not installed. Font registration features will not be available.",
        ImportWarning
    )


def get_font_path() -> Path:
    """
    Get the path to the fonts directory.

    Returns
    -------
    Path
        Path object pointing to the source_sans_pro fonts directory.

    Examples
    --------
    >>> font_path = get_font_path()
    >>> print(font_path)
    /path/to/RSSpythemes/fonts/source_sans_pro
    """
    return Path(__file__).parent / "source_sans_pro"


def list_available_fonts() -> List[str]:
    """
    List all available Source Sans Pro font files.

    Returns
    -------
    List[str]
        Sorted list of font filenames (.ttf files).

    Examples
    --------
    >>> fonts = list_available_fonts()
    >>> print(fonts)
    ['SourceSansPro-Bold.ttf', 'SourceSansPro-BoldItalic.ttf', ...]
    """
    font_dir = get_font_path()
    if not font_dir.exists():
        return []

    font_files = [f.name for f in font_dir.glob("*.ttf")]
    return sorted(font_files)


def register_source_sans_fonts(verbose: bool = False) -> bool:
    """
    Register Source Sans Pro fonts with matplotlib.

    This function registers all Source Sans Pro font files bundled with RSSpythemes
    with matplotlib's font manager, making them available for use in plots.

    Parameters
    ----------
    verbose : bool, optional
        If True, print information about registered fonts. Default is False.

    Returns
    -------
    bool
        True if at least one font was successfully registered, False otherwise.

    Examples
    --------
    >>> from RSSpythemes import register_source_sans_fonts
    >>> register_source_sans_fonts()
    True
    >>>
    >>> # Now you can use the font in matplotlib
    >>> import matplotlib.pyplot as plt
    >>> plt.rcParams['font.family'] = 'Source Sans Pro'

    Notes
    -----
    After registration, you may need to restart your Python session or rebuild
    matplotlib's font cache for the fonts to be recognized in all contexts.
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib is required to register fonts. "
            "Install it with: pip install matplotlib"
        )

    font_dir = get_font_path()
    if not font_dir.exists():
        if verbose:
            print(f"Font directory not found: {font_dir}")
        return False

    font_files = list(font_dir.glob("*.ttf"))
    if not font_files:
        if verbose:
            print(f"No font files found in: {font_dir}")
        return False

    registered_count = 0
    for font_file in font_files:
        try:
            fm.fontManager.addfont(str(font_file))
            registered_count += 1
            if verbose:
                print(f"Registered: {font_file.name}")
        except Exception as e:
            if verbose:
                print(f"Failed to register {font_file.name}: {e}")

    if registered_count > 0:
        # Rebuild the font cache
        try:
            fm._rebuild()
        except AttributeError:
            # In some matplotlib versions, _rebuild might not exist
            pass

        if verbose:
            print(f"Successfully registered {registered_count} font(s)")

    return registered_count > 0


def is_source_sans_available() -> bool:
    """
    Check if Source Sans Pro font is available in matplotlib.

    Returns
    -------
    bool
        True if Source Sans Pro is available, False otherwise.

    Examples
    --------
    >>> from RSSpythemes import is_source_sans_available, register_source_sans_fonts
    >>> if not is_source_sans_available():
    ...     register_source_sans_fonts()
    >>> is_source_sans_available()
    True
    """
    if not MATPLOTLIB_AVAILABLE:
        return False

    # Check if Source Sans Pro is in the font list
    font_names = {f.name for f in fm.fontManager.ttflist}
    return "Source Sans Pro" in font_names


def get_source_sans_weights() -> Dict[str, str]:
    """
    Get a mapping of font weight names to font filenames.

    Returns
    -------
    Dict[str, str]
        Dictionary mapping weight names to .ttf filenames.

    Examples
    --------
    >>> weights = get_source_sans_weights()
    >>> print(weights['regular'])
    SourceSansPro-Regular.ttf
    >>> print(weights['bold_italic'])
    SourceSansPro-BoldItalic.ttf
    """
    return {
        "regular": "SourceSansPro-Regular.ttf",
        "italic": "SourceSansPro-Italic.ttf",
        "bold": "SourceSansPro-Bold.ttf",
        "bold_italic": "SourceSansPro-BoldItalic.ttf",
    }


__all__ = [
    "get_font_path",
    "list_available_fonts",
    "register_source_sans_fonts",
    "is_source_sans_available",
    "get_source_sans_weights",
]
