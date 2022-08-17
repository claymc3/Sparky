"""
Functions for reading and writing Sparky (.ucsf) files.
"""

from __future__ import print_function

__developer_info__ = """
Sparky file format information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Information on the Sparky file format can be found online at:
http://www.cgl.ucsf.edu/home/sparky/manual/files.html
and in the Sparky source file ucsffile.cc.

"""

import os
import struct
import datetime
from warnings import warn
try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

import numpy as np

from . import fileiobase


# unit conversion function
def make_uc(dic, data, dim=-1):
    """
    Create a unit conversion object.
    Parameters
    ----------
    dic : dict
        Dictionary of Sparky parameters.
    data : ndarray
        Array of NMR data.
    dim : int, optional
        Dimension number to create unit conversion object for.  Default is for
        last dimension.
    Returns
    -------
    uc : unit conversion object.
        Unit conversion object for given dimension.

    """
    if dim == -1:
        dim = data.ndim - 1  # last dimention

    wdic = dic["w" + str(int(1 + dim))]

    size = float(wdic["npoints"])
    cplx = False
    sw = wdic["spectral_width"]
    obs = wdic["spectrometer_freq"]
    car = wdic["xmtr_freq"] * obs

    return fileiobase.unit_conversion(size, cplx, sw, obs, car)


# dictionary/data creation
def create_data(data):
    """
    Create a Sparky data array (recast into float32 array)
    """
    return np.array(data, dtype="float32")


def guess_udic(dic, data):
    """
    Guess parameter of universal dictionary from dic,data pair.
    Parameters
    ----------
    dic : dict
        Dictionary of Sparky parameters.
    data : ndarray
        Array of NMR data.
    Returns
    -------
    udic : dict
        Universal dictionary of spectral parameter.
    """
    # create an empty universal dictionary
    udic = fileiobase.create_blank_udic(data.ndim)

    # update default values
    for i in range(data.ndim):
        adic = dic["w" + str(i + 1)]
        udic[i]["size"] = data.shape[i]
        udic[i]["sw"] = adic['spectral_width']
        udic[i]["obs"] = adic['spectrometer_freq']
        udic[i]["car"] = adic['xmtr_freq'] * adic['spectrometer_freq']
        udic[i]["label"] = adic['nucleus']
        udic[i]["complex"] = False
        udic[i]["time"] = False
        udic[i]["freq"] = True

    return udic


def create_dic(udic, datetimeobj=datetime.datetime.now(), user='user'):
    """
    Create a Sparky parameter dictionary from universal dictionary.
    Parameters
    ----------
    udic : dict
        Universal dictionary of spectral parameters.
    datatimeobj : datetime object, optional
        Datetime to record in Sparky dictionary
    user : str, optional
        Username to record in Sparky dictionary. Default is 'user'
    Returns
    -------
    dic : dict
        Dictionary of Sparky parameters.
    """
    dic = dict()

    # determind shape of array
    shape = [udic[k]["size"] for k in range(udic["ndim"])]

    # populate the dictionary
    dic["ident"] = 'UCSF NMR'
    dic["naxis"] = udic["ndim"]
    dic["ncomponents"] = 1
    dic["encoding"] = 0
    dic["version"] = 2
    dic["owner"] = user
    dic["date"] = datetimeobj.ctime()
    dic["comment"] = ''
    dic["scratch"] = ''

    # calc a good tile shape
    tshape = calc_tshape(shape)

    # total number of tiles
    ntiles = 1
    for tlen, slen in zip(tshape, shape):
        ntiles *= np.ceil(float(slen) / tlen)

    # points in tile
    tpoints = np.array(tshape).prod()

    # data bytes
    dbytes = tpoints * ntiles * 4

    # total file size if data size plus leaders
    dic["seek_pos"] = int(dbytes + 180 + 128 * len(shape))

    # populate the dictionary with axis dictionaries
    for i, (tlen, dlen) in enumerate(zip(tshape, shape)):
        dic["w" + str(i + 1)] = create_axisdic(udic[i], tlen, dlen)
    return dic


def create_axisdic(adic, tlen, dlen):
    """
    Make an Sparky axis dictionary from a universal axis dictionary.

    Parameters
    ----------
    adic : dict
        Axis dictionary from a universal dictionary.
    tlen : int
        Tile length of axis.
    dlen : int
        Data length of axis.

    Returns
    -------
    sdic : dict
        Sparky axis dictionary

    """
    dic = dict()
    dic["nucleus"] = adic["label"]
    dic["spectral_shift"] = 0
    dic["npoints"] = int(dlen)
    dic["size"] = int(dlen)
    dic["bsize"] = int(tlen)
    dic["spectrometer_freq"] = float(adic["obs"])
    dic["spectral_width"] = float(adic["sw"])
    dic["xmtr_freq"] = float(adic["car"]) / dic["spectrometer_freq"]
    dic["zero_order"] = 0.0
    dic["first_order"] = 0.0
    dic["first_pt_scale"] = 0.0
    dic["extended"] = b'\x80'  # transform bit set
    return dic


def datetime2dic(datetimeobj, dic):
    """
    Add datetime object to dictionary
    """
    dic["date"] = datetimeobj.ctime()
    return dic


def dic2datetime(dic):
    """
    Create a datetime object from a Sparky dictionary
    """
    return datetime.datetime.strptime(dic["date"], "%a %b %d %H:%M:%S %Y")


def calc_tshape(shape, kbyte_max=128):
    """
    Calculate a tile shape from data shape.


    Parameters
    ----------
    shape : tuple
        Shape of NMR data (data.shape).
    kbyte_max : float or int
        Maximum tile size in Kilobytes.

    Returns
    -------
    tshape : tuple
        Shape of tile.

    """
    # Algorithm divides each dimention by 2 until under kbyte_max tile size.
    s = np.array(shape, dtype="int")
    i = 0
    while (s.prod() * 4. / 1024. > kbyte_max):
        s[i] = np.floor(s[i] / 2.)
        i = i + 1
        if i == len(s):
            i = 0
    return tuple(s)


# global read/write functions
def read(filename):
    """
    Read a Sparky file.
    Parameters
    ----------
    filename : str
        Filename of Sparky file to read.
    Returns
    -------
    dic : dict
        Dictionary of Sparky parameters.
    data : ndarray
        Array of NMR data.
    See Also
    --------
    read_lowmem : Sparky file reading with minimal memory usage.
    write : Write a Sparky file.
    """
    # open the file
    f = open(filename, 'rb')

    # determind the dimentionality
    n = fileheader2dic(get_fileheader(f))["naxis"]
    f.close()

    if n == 2:
        return read_2D(filename)
    if n == 3:
        return read_3D(filename)
    if n == 4:
        return read_4D(filename)

    raise ValueError("unknown dimentionality: %s" % n)


# dimension specific reading/writing functions
def read_2D(filename):
    """
    Read a 2D sparky file. See :py:func:`read` for documentation.
    """
    seek_pos = os.stat(filename).st_size
    with open(filename, 'rb') as f:

        # read the file header
        dic = fileheader2dic(get_fileheader(f))

        # check for file size mismatch
        if seek_pos != dic["seek_pos"]:
            warn('Bad file size in header %s vs %s' %
                 (seek_pos, dic['seek_pos']))

        # read the axis headers...
        for i in range(dic['naxis']):
            dic["w" + str(i + 1)] = axisheader2dic(get_axisheader(f))

        # read the data and untile
        lenY = dic["w1"]["npoints"]
        lenX = dic["w2"]["npoints"]
        lentY = dic["w1"]["bsize"]
        lentX = dic["w2"]["bsize"]
        data = get_data(f)
        data = untile_data2D(data, (lentY, lentX), (lenY, lenX))

        return dic, data

def read_3D(filename):
    """
    Read a 3D Sparky file. See :py:func:`read` for documentation.
    """
    seek_pos = os.stat(filename).st_size
    with open(filename, 'rb') as f:

        # read the file header
        dic = fileheader2dic(get_fileheader(f))

        # check for file size mismatch
        if seek_pos != dic["seek_pos"]:
            warn('Bad file size in header %s vs %s' %
                 (seek_pos, dic['seek_pos']))

        # read the axis headers...
        for i in range(dic['naxis']):
            dic["w" + str(i + 1)] = axisheader2dic(get_axisheader(f))

        # read the data and untile
        lenZ = dic["w1"]["npoints"]
        lenY = dic["w2"]["npoints"]
        lenX = dic["w3"]["npoints"]
        lentZ = dic["w1"]["bsize"]
        lentY = dic["w2"]["bsize"]
        lentX = dic["w3"]["bsize"]
        data = get_data(f)
        data = untile_data3D(data, (lentZ, lentY, lentX), (lenZ, lenY, lenX))

        return dic, data


def read_4D(filename):
    """
    Read a 3D Sparky file. See :py:func:`read` for documentation.
    """
    seek_pos = os.stat(filename).st_size
    with open(filename, 'rb') as f:

        # read the file header
        dic = fileheader2dic(get_fileheader(f))

        # check for file size mismatch
        if seek_pos != dic["seek_pos"]:
            warn('Bad file size in header %s vs %s' %
                 (seek_pos, dic['seek_pos']))

        # read the axis headers...
        for i in range(dic['naxis']):
            dic["w" + str(i + 1)] = axisheader2dic(get_axisheader(f))

        # read the data and untile
        lenW = dic["w1"]["npoints"]
        lenZ = dic["w2"]["npoints"]
        lenY = dic["w3"]["npoints"]
        lenX = dic["w4"]["npoints"]
        lentW = dic["w1"]["bsize"]
        lentZ = dic["w2"]["bsize"]
        lentY = dic["w3"]["bsize"]
        lentX = dic["w4"]["bsize"]
        data = get_data(f)
        data = untile_data4D(data, (lentW, lentZ, lentY, lentX), (lenW, lenZ, lenY, lenX))

        return dic, data


# tile and data get/put functions
def get_tilen(f, n_tile, tw_tuple):
    """
    Read a tile from a Sparky file object.

    Parameters
    ----------
    f : file object
        Open file object pointing to a Sparky file.
    n_tile : int
        Tile number to read
    tw_tuple : tuple of ints
        Tile size

    Returns
    -------
    tile : ndarray
        Tile of NMR data. Data is returned as a 1D array.

    Notes
    -----
    Current file position is loss. In can be stored before calling if the
    position is later needed.

    """
    # determind the size of the tile in bytes
    tsize = 4
    for i in tw_tuple:
        tsize = tsize * i

    # seek to the beginning of the tile
    f.seek(int(180 + 128 * len(tw_tuple) + n_tile * tsize))
    return np.frombuffer(f.read(tsize), dtype='>f4')


def get_tile(f, num_points):
    """
    Read the next tile from a Sparky file object.

    Parameters
    ----------
    f : file object
        Open file object pointing to a Sparky file.
    num_points : int
        Number of points in the tile.

    Returns
    -------
    tile : ndarray
        Tile of NMR data. Data is returned as a 1D array.

    """
    bsize = num_points * 4        # size in bytes
    return np.frombuffer(f.read(bsize), dtype='>f4')


def put_tile(f, tile):
    """
    Put a tile to a Sparky file object.

    Parameters
    ----------
    f : file object
        Open file object pointing to a Sparky file, to be written to.
    tile : ndarray
        Tile of NMR data to be written.

    """
    f.write(tile.astype('>f4').tostring())
    return


def get_data(f):
    """
    Read all data from sparky file object.
    """
    return np.frombuffer(f.read(), dtype='>f4')


def put_data(f, data):
    """
    Put data to a Sparky file object.

    This function does not untile data. This should be done before calling
    this function

    """
    f.write(data.astype('>f4').tostring())
    return



def untile_data2D(data, tile_size, data_size):
    """
    Rearrange 2D Tiled/Sparky formatted data into standard format.

    Parameters
    ----------
    data : 1D ndarray
        Tiled/Sparky formatted 2D NMR data.
    (lentY, lenX) : tuple of ints
        Size of tile.
    (lenY, lenX) : tuple of ints
        Size of NMR data.

    Returns
    -------
    sdata : 2D ndarray
        NMR data, untiled/standard format.

    """
    lentY, lentX = tile_size
    lenY, lenX = data_size
    # determind the number of tiles in data
    ttX = int(np.ceil(lenX / float(lentX)))  # total tiles in X dim
    ttY = int(np.ceil(lenY / float(lentY)))  # total tiles in Y dim
    tt = ttX * ttY

    # calc some basic parameter
    tsize = lentX * lentY  # number of points in one tile
    t_tup = (lentY, lentX)  # tile size tuple

    # create an empty array to store file data
    out = np.empty((ttY * lentY, ttX * lentX), dtype="float32")

    for iY in range(int(ttY)):
        for iX in range(int(ttX)):
            minX = iX * lentX
            maxX = (iX + 1) * lentX

            minY = iY * lentY
            maxY = (iY + 1) * lentY

            ntile = iY * ttX + iX
            minT = ntile * tsize
            maxT = (ntile + 1) * tsize

            # DEBUG
            # print("ntile",ntile)
            # print("minX",minX,"maxX",maxX)
            # print("minY",minY,"maxY",maxY)
            # print("minT",minT,"maxT",maxT)

            # print(out[minY:maxY,minX:maxX].shape)
            # print(data[minT:maxT].reshape(t_tup).shape)

            out[minY:maxY, minX:maxX] = data[minT:maxT].reshape(t_tup)

    return out[:lenY, :lenX]

def untile_data3D(data, tile_size, data_size):
    """
    Rearrange 3D tiled/Sparky formatted data into standard format.

    Parameters
    ----------
    data : 1D ndarray
        Tiled/Sparky formatted 2D NMR data.
    (lentZ, lentY, lentX) : tuple of ints
        Size of tile
    (lenZ, lenY, lenX) : tuple of ints
        Size of NMR data.

    Returns
    -------
    sdata : 3D ndarray
        NMR data, untiled/standard format.

    """
    lentZ, lentY, lentX = tile_size
    lenZ, lenY, lenX = data_size

    # determind the number of tiles in data
    ttX = int(np.ceil(lenX / float(lentX)))  # total tiles in X dim
    ttY = int(np.ceil(lenY / float(lentY)))  # total tiles in Y dim
    ttZ = int(np.ceil(lenZ / float(lentZ)))  # total tiles in Z dim
    tt = ttX * ttY * ttZ

    # calc some basic parameter
    tsize = lentX * lentY * lentZ  # number of points in one tile
    t_tup = (lentZ, lentY, lentX)  # tile size tuple

    # create an empty array to store file data
    out = np.empty((ttZ * lentZ, ttY * lentY, ttX * lentX), dtype="float32")

    for iZ in range(int(ttZ)):
        for iY in range(int(ttY)):
            for iX in range(int(ttX)):

                minX = iX * lentX
                maxX = (iX + 1) * lentX

                minY = iY * lentY
                maxY = (iY + 1) * lentY

                minZ = iZ * lentZ
                maxZ = (iZ + 1) * lentZ

                ntile = iZ * ttX * ttY + iY * ttX + iX
                minT = ntile * tsize
                maxT = (ntile + 1) * tsize

                out[minZ:maxZ, minY:maxY, minX:maxX] =  \
                    data[minT:maxT].reshape(t_tup)

    return out[:lenZ, :lenY, :lenX]


def untile_data4D(data, tile_size, data_size):
    """
    Rearrange 3D tiled/Sparky formatted data into standard format.

    Parameters
    ----------
    data : 1D ndarray
        Tiled/Sparky formatted 2D NMR data.
    (lentZ, lentY, lentX) : tuple of ints
        Size of tile
    (lenZ, lenY, lenX) : tuple of ints
        Size of NMR data.

    Returns
    -------
    sdata : 3D ndarray
        NMR data, untiled/standard format.

    """
    lentZ, lentY, lentX = tile_size
    lenZ, lenY, lenX = data_size

    # determind the number of tiles in data
    ttX = int(np.ceil(lenX / float(lentX)))  # total tiles in X dim
    ttY = int(np.ceil(lenY / float(lentY)))  # total tiles in Y dim
    ttZ = int(np.ceil(lenZ / float(lentZ)))  # total tiles in Z dim
    ttW = int(np.ceil(lenW / float(lentW)))  # total tiles in Z dim

    tt = ttX * ttY * ttZ * ttW

    # calc some basic parameter
    tsize = lentX * lentY * lentZ * lentW # number of points in one tile
    t_tup = (lentW,lentZ, lentY, lentX, lentW)  # tile size tuple

    # create an empty array to store file data
    out = np.empty((ttW*lentW, ttZ * lentZ, ttY * lentY, ttX * lentX), dtype="float32")

    for iW in range(int(ttW)):
        for iZ in range(int(ttZ)):
            for iY in range(int(ttY)):
                for iX in range(int(ttX)):

                    minX = iX * lentX
                    maxX = (iX + 1) * lentX

                    minY = iY * lentY
                    maxY = (iY + 1) * lentY

                    minZ = iZ * lentZ
                    maxZ = (iZ + 1) * lentZ

                    minW = iW * lentW
                    maxW = (iW + 1) * lentW

                    ntile = iW * ttW * iZ * ttX * ttY + iY * ttX + iX

                    minT = ntile * tsize
                    maxT = (ntile + 1) * tsize

                    out[minW:maxW, minZ:maxZ, minY:maxY, minX:maxX] =  \
                        data[minT:maxT].reshape(t_tup)

    return out[:lenW, :lenZ, :lenY, :lenX]

# fileheader functions
def get_fileheader(f):
    """
    Get fileheader from file and return a list.

    Reads the 180 byte file header of a Sparky file

    """
    # file header as descriped in ucsffile.cc of sparky source
    # header is packed as follows:
    # ident(10s),naxis(c),ncomponents(c),encoding(c),version(c)
    # owner(9s),date(26s),comment(80s),pad(3x),seek_pos(l),scratch(40s),
    # pad(4x)

    # note that between comment and seek_pos is a 3 byte pad
    # so that the long is @ a multiple of 4
    # also sparky always packs big-endian, hence >
    return struct.unpack('>10s 4c 9s 26s 80s 3x l 40s 4x', f.read(180))


def put_fileheader(f, fl):
    """
    Write fileheader list to file (180-bytes).
    """
    f.write(struct.pack('>10s 4c 9s 26s 80s 3x l 40s 4x', *fl))
    return


def fileheader2dic(header):
    """
    Convert a fileheader list into a Sparky parameter dictionary.
    """
    dic = dict()
    dic["ident"] = str(header[0].decode()).strip('\x00')
    dic["naxis"] = ord(header[1].decode())
    dic["ncomponents"] = ord(header[2].decode())
    dic["encoding"] = ord(header[3].decode())
    dic["version"] = ord(header[4].decode())
    dic["owner"] = str(header[5].decode()).strip('\x00')
    dic["date"] = str(header[6].decode()).strip('\x00')
    dic["comment"] = str(header[7].decode()).strip('\x00')
    dic["seek_pos"] = header[8]     # eof seek position
    dic["scratch"] = str(header[9].decode()).strip('\x00')
    return dic


def dic2fileheader(dic):
    """
    Convert a Sparky parameter dictionary into a fileheader list.
    """
    fl = [0] * 10
    fl[0] = dic["ident"].encode()
    fl[1] = chr(dic["naxis"]).encode()
    fl[2] = chr(dic["ncomponents"]).encode()
    fl[3] = chr(dic["encoding"]).encode()
    fl[4] = chr(dic["version"]).encode()
    fl[5] = dic["owner"].encode()
    fl[6] = dic["date"].encode()
    fl[7] = dic["comment"].encode()
    fl[8] = dic["seek_pos"]
    fl[9] = dic["scratch"].encode()
    return fl


# axisheader functions
def get_axisheader(f):
    """
    Get an axisheader from file and return a list.

    Only the first 44 bytes are examined, the NMR_PROCESSED and other header
    parameters are ignored since the current version of Sparky does not use
    them.

    """
    # axis header is described in ucsffile.cc
    # axis header is packed as follows
    # nucleus(6s),spectral_shift(h),npoints(I),size(I),bsize(I)
    # spectrometer_freq(f),spectral_width(f),xmtr_freq(f),zero_order(f),
    # first_order(f),first_pt_scale(f),ZEROS
    return struct.unpack('>6s h 3I 6f 84s', f.read(128))


def put_axisheader(f, al):
    """
    Write an axisheader list to file (128-bytes written).
    """
    f.write(struct.pack('>6s h 3I 6f 84s', *al))
    return


def axisheader2dic(header):
    """
    Convert an axisheader list into Sparky parameter axis dictionary.
    """
    dic = dict()
    dic["nucleus"] = str(header[0].decode()).strip('\x00')
    dic["spectral_shift"] = header[1]
    dic["npoints"] = header[2]
    dic["size"] = header[3]
    dic["bsize"] = header[4]
    dic["spectrometer_freq"] = header[5]
    dic["spectral_width"] = header[6]
    dic["xmtr_freq"] = header[7]
    dic["zero_order"] = header[8]
    dic["first_order"] = header[9]
    dic["first_pt_scale"] = header[10]
    dic["extended"] = header[11]
    return dic


def dic2axisheader(dic):
    """
    Convert a Sparky parameter axis diction into a axisherder list.
    """
    al = [0] * 12
    al[0] = dic["nucleus"].encode()
    al[1] = dic["spectral_shift"]
    al[2] = dic["npoints"]
    al[3] = dic["size"]
    al[4] = dic["bsize"]
    al[5] = dic["spectrometer_freq"]
    al[6] = dic["spectral_width"]
    al[7] = dic["xmtr_freq"]
    al[8] = dic["zero_order"]
    al[9] = dic["first_order"]
    al[10] = dic["first_pt_scale"]
    al[11] = dic["extended"]
    return al
