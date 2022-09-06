"""Main format functionalities dispatcher based on factory pattern."""

from ..image.image import Image
from ..parser.factory import ParserFactory
from .utils import determine_color_format
from ..image.color_format import PixelFormat, PixelPlane

import numpy as np
from fcntl import ioctl
from select import select
import mmap
from pyrav4l2 import *


def parse_image(data_buffer, color_format, width, reverse_bytes=0):
    try:
        image = Image(data_buffer)
        parser = ParserFactory.create_object(
            determine_color_format(color_format))
    except Exception as e:
        print(type(e).__name__, e)
    #Stride image
    image = parser.parse(image.data_buffer,
                         determine_color_format(color_format), width,
                         reverse_bytes)

    return image


def load_image(file_path):
    with open(file_path, 'rb') as f:
        data_buffer = bytearray(f.read())
    image = Image(data_buffer)
    return image


def load_from_camera(camera, num_of_frames):
    with open(camera, "rb+", buffering=0) as cam:
        req = v4l2_requestbuffers()
        req.count = 1
        req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        req.memory = V4L2_MEMORY_MMAP
        ioctl(cam, VIDIOC_REQBUFS, req)

        buf = v4l2_buffer()
        buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        buf.memory = V4L2_MEMORY_MMAP
        buf.index = 0
        ioctl(cam, VIDIOC_QUERYBUF, buf)

        buffer = mmap.mmap(cam.fileno(),
                           length=buf.length,
                           flags=mmap.MAP_SHARED,
                           prot=mmap.PROT_READ,
                           offset=buf.m.offset)
        ioctl(cam, VIDIOC_QBUF, buf)

        ioctl(cam, VIDIOC_STREAMON, ctypes.c_int(V4L2_BUF_TYPE_VIDEO_CAPTURE))
        select((cam, ), (), ())

        frames = bytearray()
        for _ in range(num_of_frames):
            buf = v4l2_buffer()
            buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
            buf.memory = V4L2_MEMORY_MMAP
            ioctl(cam, VIDIOC_DQBUF, buf)

            frames += buffer.read()
            buffer.seek(0)
            ioctl(cam, VIDIOC_QBUF, buf)

        ioctl(cam, VIDIOC_STREAMOFF, ctypes.c_int(V4L2_BUF_TYPE_VIDEO_CAPTURE))

        return Image(frames)


def set_camera_format(camera, color_format, framesize):
    with open(camera) as f_cam:
        fmt = v4l2_format()
        fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE
        ioctl(f_cam, VIDIOC_G_FMT, fmt)

        fmt.fmt.pix.width = framesize[0]
        fmt.fmt.pix.height = framesize[1]
        fmt.fmt.pix.pixelformat = color_format
        fmt.fmt.pix.bytesperline = 0
        fmt.fmt.pix.field = V4L2_FIELD_ANY
        ioctl(f_cam, VIDIOC_S_FMT, fmt)


def get_displayable(image,
                    height=0,
                    channels={
                        "r_y": True,
                        "g_u": True,
                        "b_v": True,
                        "a_v": True
                    }):

    if image.color_format is None:
        raise Exception("Image should be already parsed!")
    parser = ParserFactory.create_object(image.color_format)

    if image.color_format.pixel_format == PixelFormat.MONO:
        return parser.get_displayable(image)
    elif image.color_format.pixel_plane in [
            PixelPlane.SEMIPLANAR, PixelPlane.PLANAR
    ]:
        return parser.get_displayable(image, height, channels=channels)
    else:
        return parser.get_displayable(image, channels=channels)


"""Resolve picked pixel's raw integrants."""


def get_pixel_raw_components(image: Image, row: int, column: int,
                             pixel_index: int):
    """
    Keyword arguments:
        Image: Image instance
        row: row number on the plot
        column: column number on the plot
        pixel_index: relative pixel position from the first one
    """
    parser = ParserFactory.create_object(image.color_format)
    return parser.get_pixel_raw_components(image, row, column, pixel_index)


"""Crop selected area to raw format."""


def crop_image2rawformat(image: Image, up_row: int, down_row: int,
                         left_column: int, right_column: int):
    """
    Keyword arguments:
        Image: Image instance 
        up_row:  position of up row within a selected area
        down_row: position of down row within a selected area
        left_column: position of left column within a selected area
        right_column: position of right column within a selected area.   
    """
    parser = ParserFactory.create_object(image.color_format)
    return parser.crop_image2rawformat(image, up_row, down_row, left_column,
                                       right_column)


def align_image(data_buffer, nnumber, nvalues=0, frame_num=1):
    """ Add or skip data at the beginning of every frame in the data
    Keyword arguments:
        data_buffer (bytearray): byte array containing raw image data
        nnumber (int): number of bytes to append (or skip)
        nvalues (int): value of bytes to append
        frame_num (int): number of frames
    Returns:
        bytearray: aligned buffer
    """

    raw_data = np.array(data_buffer)
    frames = np.array_split(raw_data, frame_num)
    new_frames = [None] * len(frames)

    if nnumber > 0:
        values_to_insert = np.repeat(nvalues, nnumber)
        for i, frame in enumerate(frames):
            new_frames[i] = np.insert(frame, 0, values_to_insert)
    else:
        frame_len = len(raw_data) // frame_num
        if abs(nnumber) > frame_len:
            return
        for i, frame in enumerate(frames):
            new_frames[i] = frame[abs(nnumber):]

    return bytearray(np.concatenate(new_frames).tobytes())
