#!/usr/bin/env python
# coding: utf-8

"""
Tests for the ZipArchive class
"""

from .. import ZipArchive
import pytest
from pathlib import Path

ARCHIVE = "test.zip"

@pytest.fixture(scope="function")
def archive_filepath(tmp_path_factory):
    base_path = tmp_path_factory.getbasetemp()
    return base_path / ARCHIVE

def test_create_new_archive(archive_filepath):
    print(archive_filepath)
    archive = ZipArchive(archive_filepath)
    files_in_archive = [ f for f in archive ]
    assert len(files_in_archive) == 0
    archive_filepath.unlink()

def test_store_txt_file(archive_filepath):
    archive = ZipArchive(archive_filepath)
    test_string = "abc"
    archive.add("test.txt", test_string)

    for f in archive:
        read_string = archive.get(f)
        assert read_string == test_string
    archive_filepath.unlink()

def test_json_txt_file(archive_filepath):
    archive = ZipArchive(archive_filepath)
    test_json = { "a": "test"}
    archive.add("test.json", test_json)

    read_json = archive.get("test.json")
    assert read_json["a"] == test_json["a"]
    archive_filepath.unlink()

def test_add_none_file(archive_filepath):
    archive = ZipArchive(archive_filepath)
    test = None
    with pytest.raises(TypeError):
        archive.add("test.json", test)
    archive_filepath.unlink()        

def test_add_same_filename_twice(archive_filepath):
    archive = ZipArchive(archive_filepath)

    test = "abc"
    archive.add("test.txt", test)

    test = "def"
    with pytest.raises(FileExistsError):
        archive.add("test.txt", test)
    archive_filepath.unlink()

def test_append_to_existing_archive(archive_filepath):
    archive = ZipArchive(archive_filepath)
    archive.add("test.txt", "abc")

    archive2 = ZipArchive(archive_filepath)
    files_in_archive2 = [ f for f in archive2 ]
    assert files_in_archive2 == ["test.txt"]

    archive2.add("test2.json", { "a": "bc" })

    files_in_archive1 = [ f for f in archive ]
    assert files_in_archive1 == ["test.txt", "test2.json"]

    archive_filepath.unlink()


def test_iter_files(archive_filepath):
    archive = ZipArchive(archive_filepath)
    archive.add("test.txt", "abc")
    archive.add("test2.txt", "def")

    read = []
    for data in archive.iter_files():
        read.append(data)

    assert "".join(read) == "abcdef"