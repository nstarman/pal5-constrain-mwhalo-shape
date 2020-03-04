# -*- coding: utf-8 -*-

"""Data.

Storage location for "static" data -- data which will not change
over the course of the research. This is the desired location for external data
which is used in notebooks and scripts. Data generated by a script is
contained within the relevant folder.

Routine Listings
----------------
module

"""

__author__ = "Nathaniel Starkman"
# __copyright__ = "Copyright 2018, "

__all__ = [
    "read_bovyrix13kzdata",
    "readClemens",
    "readMcClureGriffiths",
    "readMcClureGriffiths16",
]

##############################################################################
# IMPORTS

# GENERAL
import numpy as np
from collections import namedtuple

# typing
from typing import Sequence, Tuple

# CUSTOM

# PROJECT-SPECIFIC


##############################################################################
# PARAMETERS

BovyRix13Tuple = namedtuple("BovyRix13Data", ["surfrs", "kzs", "kzerrs"])
TermVelTuple = namedtuple("TerminalVelocityData", ["glon", "vterm", "corr"])

##############################################################################
# CODE
##############################################################################


def readBovyRix13kzdata() -> BovyRix13Tuple:
    """Read Data from BovyRix2013.

    The file is in data/mwpot14data/bovyrix13kzdata.csv
    it has three columns: surfrs, kzs, kzerrs

    Returns
    -------
    namedtuple
        surfrs, kzs, kzerrs

    """
    file: str = "mwpot14data/bovyrix13kzdata.csv"

    surf = np.loadtxt(file, delimiter=",")
    surfrs = surf[:, 2]
    kzs = surf[:, 6]
    kzerrs = surf[:, 7]

    return BovyRix13Tuple(surfrs=surfrs, kzs=kzs, kzerrs=kzerrs)


# /def


##########################################################################
# terminal velocity data


def _calc_corr(singlon: Sequence, dsinl: float) -> np.ndarray:
    """Calculate correlation matrix."""
    corr = np.zeros((len(singlon), len(singlon)))
    for ii in range(len(singlon)):
        for jj in range(len(singlon)):
            corr[ii, jj] = np.exp(-np.fabs(singlon[ii] - singlon[jj]) / dsinl)
    corr = 0.5 * (corr + corr.T)
    return corr + 10.0 ** -10.0 * np.eye(len(singlon))  # for stability


# /def


def _binlbins(
    glon: float, vterm: float, dl: float = 1.0
) -> Tuple[Sequence, Sequence]:
    """Bin l bins."""
    minglon, maxglon = (
        np.floor(np.amin(glon)),
        np.floor(np.amax(glon)),
    )
    minglon, maxglon = int(minglon), int(maxglon)
    nout = maxglon - minglon + 1
    glon_out = np.zeros(nout)
    vterm_out = np.zeros(nout)
    for ii in range(nout):
        indx = (glon > minglon + ii) * (glon < minglon + ii + 1)
        glon_out[ii] = np.mean(glon[indx])
        vterm_out[ii] = np.mean(vterm[indx])

    return glon_out, vterm_out


# /def


# ------------------------------------------------------------------------


def readClemens(dsinl: float = 0.5 / 8.0,) -> TermVelTuple:
    """Read Clemens 1985 table 2 data.

    Parameters
    ----------
    dsinl: float

    Returns
    -------
    namedtuple
        TermVelTuple(glon, vterm, err)

    """
    file: str = "mwpot14data/clemens1985_table2.dat"

    data = np.loadtxt(file, delimiter="|", comments="#",)
    glon = data[:, 0]
    vterm = data[:, 1]
    # Remove l < 40 and l > 80
    indx = (glon > 40.0) * (glon < 80.0)
    glon = glon[indx]
    vterm = vterm[indx]

    if bin:  # Bin in l=1 bins
        glon, vterm = _binlbins(glon, vterm, dl=1.0)
        # Remove nan, because 1 bin is empty
        indx = ~np.isnan(glon)
        glon = glon[indx]
        vterm = vterm[indx]

    # Calculate correlation matrix
    singlon = np.sin(glon / 180.0 * np.pi)
    corr = np.linalg.inv(_calc_corr(singlon, dsinl))

    return TermVelTuple(glon=glon, vterm=vterm, corr=corr)


# /def


# ------------------------------------------------------------------------


def readMcClureGriffiths07(
    dsinl: float = 0.5 / 8.0, bin: bool = True
) -> TermVelTuple:
    """Read McClure & Griffiths 2007 data.

    Parameters
    ----------
    dsinl: float
    bin: bool

    Returns
    -------
    namedtuple
        TermVelTuple(glon, vterm, err)

    """
    file: str = "mwpot14data/McClureGriffiths2007.dat"

    data = np.loadtxt(file, comments="#")
    glon = data[:, 0]
    vterm = data[:, 1]
    # Remove l > 320 and l > 80
    indx = (glon < 320.0) * (glon > 280.0)
    glon = glon[indx]
    vterm = vterm[indx]

    if bin:  # Bin in l=1 bins
        glon, vterm = _binlbins(glon, vterm, dl=1.0)

    # Calculate correlation matrix
    singlon = np.sin(glon / 180.0 * np.pi)
    corr = np.linalg.inv(_calc_corr(singlon, dsinl))

    return TermVelTuple(glon=glon, vterm=vterm, corr=corr)


# /def


def readMcClureGriffiths16(
    dsinl: float = 0.5 / 8.0, bin: bool = True
) -> TermVelTuple:
    """Read McClure & Griffiths 2016 data.

    Parameters
    ----------
    dsinl: float
    bin: bool

    Returns
    -------
    namedtuple
        TermVelTuple(glon, vterm, err)

    """
    file: str = "mwpot14data/McClureGriffiths2016.dat"

    data = np.loadtxt(file, comments="#", delimiter="&",)
    glon = data[:, 0]
    vterm = data[:, 1]
    # Remove l < 30 and l > 80
    indx = (glon > 40.0) * (glon < 80.0)
    glon = glon[indx]
    vterm = vterm[indx]

    if bin:  # Bin in l=1 bins
        glon, vterm = _binlbins(glon, vterm, dl=1.0)

    # Calculate correlation matrix
    singlon = np.sin(glon / 180.0 * np.pi)
    corr = np.linalg.inv(_calc_corr(singlon, dsinl))

    return TermVelTuple(glon=glon, vterm=vterm, corr=corr)


# /def


def readallMcClureGriffiths(
    dsinl: float = 0.5 / 8.0, bin: bool = True
) -> Tuple:

    termdata: tuple = (
        *readMcClureGriffiths07(dsinl=dsinl, bin=bin),
        *readMcClureGriffiths16(dsinl=dsinl, bin=bin),
    )

    return termdata


# ------------------------------------------------------------------------


##############################################################################
# END
