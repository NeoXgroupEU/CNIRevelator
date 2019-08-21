# -*- coding: utf8 -*-
"""
********************************************************************************
*                             CNIRevelator                                     *
*                                                                              *
*  Desc:       Pytesseract modification to comply with Pyinstaller             *
*                                                                              *
*  Copyright © 2017-2018 Matthias A. Lee (madmaze)                             *
*  Copyright © 2018-2019 Adrien Bourmault (neox95)                             *
*                                                                              *
*  This file is part of CNIRevelator.                                          *
*                                                                              *
*  CNIRevelator is free software: you can redistribute it and/or modify        *
*  it under the terms of the GNU General Public License as published by        *
*  the Free Software Foundation, either version 3 of the License, or           *
*  any later version.                                                          *
*                                                                              *
*  CNIRevelator is distributed in the hope that it will be useful,             *
*  but WITHOUT ANY WARRANTY*without even the implied warranty of               *
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               *
*  GNU General Public License for more details.                                *
*                                                                              *
*  You should have received a copy of the GNU General Public License           *
* along with CNIRevelator. If not, see <https:*www.gnu.org/licenses/>.         *
********************************************************************************
"""
                            
        
try:
    import Image
except ImportError:
    from PIL import Image

import os, sys, subprocess, tempfile, shlex, string
from glob import iglob
from pkgutil import find_loader
from distutils.version import LooseVersion
from os.path import realpath, normpath, normcase
numpy_installed = find_loader('numpy') is not None
if numpy_installed:
    from numpy import ndarray
tesseract_cmd = 'tesseract'
RGB_MODE = 'RGB'
OSD_KEYS = {'Page number':(
  'page_num', int), 
 'Orientation in degrees':(
  'orientation', int), 
 'Rotate':(
  'rotate', int), 
 'Orientation confidence':(
  'orientation_conf', float), 
 'Script':(
  'script', str), 
 'Script confidence':(
  'script_conf', float)}

class Output:
    STRING = 'string'
    BYTES = 'bytes'
    DICT = 'dict'


class TesseractError(RuntimeError):

    def __init__(self, status, message):
        self.status = status
        self.message = message
        self.args = (status, message)


class TesseractNotFoundError(EnvironmentError):

    def __init__(self):
        super(TesseractNotFoundError, self).__init__(tesseract_cmd + " is not installed or it's not in your path")


class TSVNotSupported(EnvironmentError):

    def __init__(self):
        super(TSVNotSupported, self).__init__('TSV output not supported. Tesseract >= 3.05 required')


def run_once(func):

    def wrapper(*args, **kwargs):
        if wrapper._result is wrapper:
            wrapper._result = func(*args, **kwargs)
        return wrapper._result

    wrapper._result = wrapper
    return wrapper


def get_errors(error_string):
    return ' '.join(line for line in error_string.decode('utf-8').splitlines()).strip()


def cleanup(temp_name):
    """ Tries to remove files by filename wildcard path. """
    for filename in iglob(temp_name + '*' if temp_name else temp_name):
        try:
            os.remove(filename)
        except OSError:
            pass


def prepare(image):
    if isinstance(image, Image.Image):
        return image
    if numpy_installed:
        if isinstance(image, ndarray):
            pass
        return Image.fromarray(image)
    raise TypeError('Unsupported image object')


def save_image(image):
    temp_name = tempfile.mktemp(prefix='tess_')
    if isinstance(image, str):
        return (temp_name, realpath(normpath(normcase(image))))
    else:
        image = prepare(image)
        img_extension = image.format
        if image.format not in frozenset({'BMP', 'JPEG', 'GIF', 'TIFF', 'PNG'}):
            img_extension = 'PNG'
        if not image.mode.startswith(RGB_MODE):
            image = image.convert(RGB_MODE)
        if 'A' in image.getbands():
            background = Image.new(RGB_MODE, image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
            image = background
        input_file_name = temp_name + os.extsep + img_extension
        (image.save)(input_file_name, format=img_extension, **image.info)
        return (
         temp_name, input_file_name)


def subprocess_args(include_stdout=True):
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}
    ret.update({'stdin':subprocess.PIPE,  'stderr':subprocess.PIPE, 
     'startupinfo':si, 
     'env':env})
    return ret


def run_tesseract(input_filename, output_filename_base, extension, lang, config='', nice=0):
    cmd_args = []
    if not sys.platform.startswith('win32'):
        if nice != 0:
            cmd_args += ('nice', '-n', str(nice))
    cmd_args += (tesseract_cmd, input_filename, output_filename_base)
    if lang is not None:
        cmd_args += ('-l', lang)
    cmd_args += shlex.split(config)
    if extension not in ('box', 'osd', 'tsv'):
        cmd_args.append(extension)
    try:
        proc = (subprocess.Popen)(cmd_args, **subprocess_args())
    except OSError:
        raise TesseractNotFoundError()

    status_code, error_string = proc.wait(), proc.stderr.read()
    proc.stderr.close()
    if status_code:
        raise TesseractError(status_code, get_errors(error_string))
    return True


def run_and_get_output(image, extension, lang=None, config='', nice=0, return_bytes=False):
    temp_name, input_filename = ('', '')
    try:
        temp_name, input_filename = save_image(image)
        kwargs = {'input_filename':input_filename, 
         'output_filename_base':temp_name + '_out', 
         'extension':extension, 
         'lang':lang, 
         'config':config, 
         'nice':nice}
        run_tesseract(**kwargs)
        filename = kwargs['output_filename_base'] + os.extsep + extension
        with open(filename, 'rb') as (output_file):
            if return_bytes:
                return output_file.read()
            return output_file.read().decode('utf-8').strip()
    finally:
        cleanup(temp_name)


def file_to_dict(tsv, cell_delimiter, str_col_idx):
    result = {}
    rows = [row.split(cell_delimiter) for row in tsv.split('\n')]
    if not rows:
        return result
    else:
        header = rows.pop(0)
        if len(rows[(-1)]) < len(header):
            rows[(-1)].append('')
        if str_col_idx < 0:
            str_col_idx += len(header)
        for i, head in enumerate(header):
            result[head] = [int(row[i]) if i != str_col_idx else row[i] for row in rows]

        return result


def is_valid(val, _type):
    if _type is int:
        return val.isdigit()
    else:
        if _type is float:
            pass
        try:
            float(val)
            return True
        except ValueError:
            return False

        return True


def osd_to_dict(osd):
    return {OSD_KEYS[kv[0]][0]:OSD_KEYS[kv[0]][1](kv[1]) for kv in (line.split(': ') for line in osd.split('\n')) if len(kv) == 2 if is_valid(kv[1], OSD_KEYS[kv[0]][1])}


@run_once
def get_tesseract_version():
    """
    Returns LooseVersion object of the Tesseract version
    """
    try:
        return LooseVersion((subprocess.check_output)([tesseract_cmd, '--version'], **subprocess_args(False)).decode('utf-8').split()[1].lstrip(string.printable[10:]))
    except OSError:
        raise TesseractNotFoundError()


def image_to_string(image, lang=None, config='', nice=0, boxes=False, output_type=Output.STRING):
    """
    Returns the result of a Tesseract OCR run on the provided image to string
    """
    if boxes:
        print("\nWarning: Argument 'boxes' is deprecated and will be removed in future versions. Use function image_to_boxes instead.\n")
        return image_to_boxes(image, lang, config, nice, output_type)
    else:
        args = [
         image, 'txt', lang, config, nice]
        if output_type == Output.DICT:
            return {'text': run_and_get_output(*args)}
        if output_type == Output.BYTES:
            args.append(True)
        return run_and_get_output(*args)


def image_to_boxes(image, lang=None, config='', nice=0, output_type=Output.STRING):
    """
    Returns string containing recognized characters and their box boundaries
    """
    config += ' batch.nochop makebox'
    args = [image, 'box', lang, config, nice]
    if output_type == Output.DICT:
        box_header = 'char left bottom right top page\n'
        return file_to_dict(box_header + run_and_get_output(*args), ' ', 0)
    else:
        if output_type == Output.BYTES:
            args.append(True)
        return run_and_get_output(*args)


def image_to_data(image, lang=None, config='', nice=0, output_type=Output.STRING):
    """
    Returns string containing box boundaries, confidences,
    and other information. Requires Tesseract 3.05+
    """
    if get_tesseract_version() < '3.05':
        raise TSVNotSupported()
    config = '{} {}'.format('-c tessedit_create_tsv=1', config.strip()).strip()
    args = [image, 'tsv', lang, config, nice]
    if output_type == Output.DICT:
        return file_to_dict(run_and_get_output(*args), '\t', -1)
    else:
        if output_type == Output.BYTES:
            args.append(True)
        return run_and_get_output(*args)


def image_to_osd(image, lang='osd', config='', nice=0, output_type=Output.STRING):
    """
    Returns string containing the orientation and script detection (OSD)
    """
    config = '{}-psm 0 {}'.format('' if get_tesseract_version() < '3.05' else '-', config.strip()).strip()
    args = [
     image, 'osd', lang, config, nice]
    if output_type == Output.DICT:
        return osd_to_dict(run_and_get_output(*args))
    else:
        if output_type == Output.BYTES:
            args.append(True)
        return run_and_get_output(*args)


def main():
    if len(sys.argv) == 2:
        filename, lang = sys.argv[1], None
    else:
        if len(sys.argv) == 4:
            if sys.argv[1] == '-l':
                filename, lang = sys.argv[3], sys.argv[2]
            sys.stderr.write('Usage: python pytesseract.py [-l lang] input_file\n')
            exit(2)
    try:
        print(image_to_string((Image.open(filename)), lang=lang))
    except IOError:
        sys.stderr.write('ERROR: Could not open file "%s"\n' % filename)
        exit(1)


if __name__ == '__main__':
    main()
