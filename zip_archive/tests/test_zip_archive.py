#!/usr/bin/env python
# coding: utf-8

"""
Tests for the ZipArchive class
"""

from .. import ZipArchive
import pytest
from pathlib import Path


ARCHIVE = "test.zip"


@pytest.fixture
def archive_filepath(tmp_path_factory):
    a_path = tmp_path_factory.getbasetemp() / ARCHIVE
    yield a_path
    a_path.unlink()


def test_create_new_archive(archive_filepath):
    print(archive_filepath)
    archive = ZipArchive(archive_filepath)
    files_in_archive = [ f for f in archive ]
    assert len(files_in_archive) == 0


def test_store_txt_file(archive_filepath):
    archive = ZipArchive(archive_filepath)
    test_string = "abc"
    archive.add("test.txt", test_string)

    for f in archive:
        read_string = archive.get(f)
        assert read_string == test_string


def test_json_txt_file(archive_filepath):
    archive = ZipArchive(archive_filepath)
    test_json = { "a": "test"}
    archive.add("test.json", test_json)

    read_json = archive.get("test.json")
    assert read_json["a"] == test_json["a"]


def test_add_none_file(archive_filepath):
    archive = ZipArchive(archive_filepath)
    test = None
    with pytest.raises(TypeError):
        archive.add("test.json", test)


def test_add_same_filename_twice(archive_filepath):
    archive = ZipArchive(archive_filepath)

    test = "abc"
    archive.add("test.txt", test)

    test = "def"
    with pytest.raises(FileExistsError):
        archive.add("test.txt", test)


def test_append_to_existing_archive(archive_filepath):
    archive = ZipArchive(archive_filepath)
    archive.add("test.txt", "abc")

    archive2 = ZipArchive(archive_filepath)
    files_in_archive2 = [ f for f in archive2 ]
    assert files_in_archive2 == ["test.txt"]

    archive2.add("test2.json", { "a": "bc" })

    files_in_archive1 = [ f for f in archive ]
    assert files_in_archive1 == ["test.txt", "test2.json"]

def joinread(archive):
    contents = []
    for data in archive.iter_files():
        contents.append(data)
    return "".join(contents)

def test_overwrite(archive_filepath):
    archive = ZipArchive(archive_filepath)
    archive.add("test.txt", "abc")
    archive = ZipArchive(archive_filepath, overwrite=True)
    assert "test.txt" not in archive
    archive.add("test.txt", "abc")
    archive.add("test2.txt", "def")
    assert joinread(archive) == "abcdef"

def test_iter_files(archive_filepath):
    archive = ZipArchive(archive_filepath)
    archive.add("test.txt", "abc")
    archive.add("test2.txt", "def")
    assert joinread(archive) == "abcdef"

def test_custom_json_ext(archive_filepath):
    archive = ZipArchive(archive_filepath, json_ext=".foo")
    archive["bar.foo"] = [1,2,3]
    archive["bar.json"] = [1,2,3]
    assert archive["bar.foo"] == [1,2,3]
    assert archive["bar.json"] == "[\n    1,\n    2,\n    3\n]"

def test_custom_indent(archive_filepath):
    archive = ZipArchive(archive_filepath, json_indent=6)
    archive["foo.txt"] = [1,2,3]
    assert archive["foo.txt"] == "[\n      1,\n      2,\n      3\n]"


def test_contains(archive_filepath):
    archive = ZipArchive(archive_filepath)
    assert "test.json" not in archive
    archive.add("test.json", "abc")
    assert "test.json" in archive


def test_getitem_setitem(archive_filepath):
    archive = ZipArchive(archive_filepath)
    archive["test.json"] = [1,2,3]
    assert archive["test.json"] == [1,2,3]
