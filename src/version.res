# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
filevers=(3, 1, 4, 0),
prodvers=(3, 1, 4, 0),
# Contains a bitmask that specifies the valid bits 'flags'r
mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
subtype=0x0,
# Creation date and time stamp.
date=(0, 0)
),
  kids=[
StringFileInfo(
  [
  StringTable(
    u'040904B0',
    [StringStruct(u'CompanyName', u'Adrien Bourmault (neox95)'),
    StringStruct(u'FileDescription', u'This file is part of CNIRevelator.'),
    StringStruct(u'FileVersion', u'3.1.4'),
    StringStruct(u'InternalName', u'CNIRevelator'),
    StringStruct(u'LegalCopyright', u'Copyright (c) Adrien Bourmault (neox95)'),
    StringStruct(u'OriginalFilename', u'CNIRevelator.exe'),
    StringStruct(u'ProductName', u'CNIRevelator 3.1'),
    StringStruct(u'ProductVersion', u'3.1.4')])
  ]),
VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)