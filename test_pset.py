#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_4` package."""

import os
from unittest import TestCase

import boto3
from luigi import LuigiStatusCode, build
from moto import mock_s3

from pset_4.tasks.data import ContentImage, SavedModel, DownloadImage, DownloadModel
from pset_4.tasks.stylize import Stylize


def assert_and_delete(filepath):
    """This functions asserts that the file exists.
    After that the file is removed"""
    if os.path.exists(filepath):
        os.path.os.remove(filepath)
        return True
    else:
        return False


@mock_s3
class TestLuigi(TestCase):
    conn = None

    def setUp(self):
        """Mock the S3 connection"""
        self.conn = boto3.resource('s3', region_name='us-east-1')
        self.conn.create_bucket(Bucket='pset4-gabrielbg010')
        tmpluigi = os.path.join(os.path.curdir, "test/test_files/test_luigi.jpg")
        tmpmodel = os.path.join(os.path.curdir, "test/test_files/test_rain_princess.pth")
        s3 = boto3.client('s3')
        s3.upload_file(tmpluigi, 'pset4-gabrielbg010', "pset4/images/luigi.jpg")
        s3.upload_file(tmpmodel, 'pset4-gabrielbg010', "pset4/saved_models/rain_princess.pth")

    def test_ContentImage(self):
        """
        Check that the luigi task is done:
        In other words, it checks that the image exists
        """
        self.assertEqual(build([ContentImage(image="luigi.jpg")], local_scheduler=True,
                               detailed_summary=True).status, LuigiStatusCode.SUCCESS)

    def test_SavedModel(self):
        """
        Check that the luigi task is done:
        In other words, it checks that the model exists
        """
        self.assertEqual(build([SavedModel(model="rain_princess.pth")], local_scheduler=True,
                               detailed_summary=True).status, LuigiStatusCode.SUCCESS)

    def test_DownloadImage(self):
        """
        Check that the luigi task is done:
        In other words, it checks that the image can be downloaded
        """
        image = "luigi.jpg"
        self.assertEqual(build([DownloadImage(image=image)], local_scheduler=True,
                               detailed_summary=True).status, LuigiStatusCode.SUCCESS)
        assert assert_and_delete(os.path.join("images", image))

    def test_DownloadModel(self):
        """
        Check that the luigi task is done:
        In other words, it checks that the model can be downloaded
        """
        model = "rain_princess.pth"
        self.assertEqual(build([DownloadModel(model=model)], local_scheduler=True,
                               detailed_summary=True).status, LuigiStatusCode.SUCCESS)
        assert assert_and_delete(os.path.join("saved_models", model))

    def test_Stylize(self):
        """
        Check that the stilize image is made.
        """
        image = "luigi.jpg"
        model = "rain_princess.pth"
        self.assertEqual(build([Stylize(image=image, model=model)], local_scheduler=True,
                               detailed_summary=True).status, LuigiStatusCode.SUCCESS)
