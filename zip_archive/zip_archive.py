#!/usr/bin/env python
# coding: utf-8

"""
Simple Zip archvie.
Writes json/text files into zip file.
Reads files from zip file

Usage

z = ZipArchive("test.zip")

y = { ... }

if not z.contains("y.json"):
    z.add("y.json", y)

...

y = z.get("y.json")

"""

import zipfile
import json
import os

class ZipArchive:

    def __init__(self, filepath, overwrite=False):
        self.filepath = filepath
        self.overwrite = overwrite
        if not os.path.exists(self.filepath) or self.overwrite:
            archive = zipfile.ZipFile(self.filepath, "w", zipfile.ZIP_DEFLATED)
        else:
            archive = zipfile.ZipFile(self.filepath, "a", zipfile.ZIP_DEFLATED)
        archive.close()

    def _open(self):
        return zipfile.ZipFile(self.filepath, "a", zipfile.ZIP_DEFLATED)

    def add(self, filepath, data):
        """
        Add data (str, data or list) to zip file.
        """
        if isinstance(data, list) or isinstance(data, dict):
            data = json.dumps(data, indent=4)
        elif not isinstance(data, str):
            raise TypeError("ZipArchive only supports datatypes string, list and dict")

        if self.contains(filepath):
            raise FileExistsError('Filename already in archive')

        with self._open() as archive:
            archive.writestr(filepath, data)    
        

    def get(self, filepath):
        """
        Reads (text-)file from zip file.
        """
        with self._open() as archive:
            data = archive.read(filepath)

        if filepath.endswith(".json"):
            return json.loads(data.decode("utf-8"))
        else:
            return data.decode("utf-8")       

    def contains(self, filepath):
        """
        Check if zip file contains file :filepath:
        """
        with self._open() as archive:
            filelist = archive.namelist()
        
        if filepath in filelist:
            return True
        else:
            return False

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.add(key, value)

    def __iter__(self):
        with self._open() as archive:
            namelist = archive.namelist()

        for filename in namelist:
            yield filename
    
    def iter_files(self):
        for filename in self:
            data = self.get(filename)
            yield data
