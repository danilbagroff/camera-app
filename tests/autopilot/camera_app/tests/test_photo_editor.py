# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# Copyright 2014 Canonical
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.

"""Tests for the Camera photo editor"""

from testtools.matchers import Equals, NotEquals, GreaterThan, LessThan
from autopilot.matchers import Eventually
from autopilot.exceptions import StateNotFoundError

from camera_app.tests import CameraAppTestCase

import unittest
import os
from time import sleep


class TestCameraPhotoEditor(CameraAppTestCase):
    """Tests the main camera features"""

    """ This is needed to wait for the application to start.
        In the testfarm, the application may take some time to show up."""
    def setUp(self):
        super(TestCameraPhotoEditor, self).setUp()
        self.assertThat(
            self.main_window.get_qml_view().visible, Eventually(Equals(True)))
        self.pictures_dir = os.path.expanduser("~/Pictures/com.ubuntu.camera")
        self.videos_dir = os.path.expanduser("~/Videos/com.ubuntu.camera")

    def tearDown(self):
        super(TestCameraPhotoEditor, self).tearDown()

    def delete_all_media(self):
        picture_files = os.listdir(self.pictures_dir)
        for f in picture_files:
            os.remove(os.path.join(self.pictures_dir, f))

        video_files = os.listdir(self.videos_dir)
        for f in video_files:
            os.remove(os.path.join(self.videos_dir, f))

    def add_sample_photo(self):
        # add a fake photo to pictures_dir
        photo_path = os.path.join(self.pictures_dir, "fake_photo.jpg")
        with open(photo_path, 'a'):
            os.utime(photo_path, None)

    def select_first_photo(self):
        # select the first photo
        gallery = self.main_window.get_gallery()
        photo = gallery.wait_select_single(objectName="mediaItem0")
        self.pointing_device.move_to_object(photo)

        # do a long press to enter Multiselection mode
        self.pointing_device.press()
        sleep(1)
        self.pointing_device.release()

    """Tests swiping to the gallery and pressing the back button"""
    def test_editor_appears(self):
        viewfinder = self.main_window.get_viewfinder()
        gallery = self.main_window.get_gallery()

        self.main_window.swipe_to_gallery(self)

        self.assertThat(gallery.inView, Eventually(Equals(True)))

        # open actions drawer
        opt = gallery.wait_select_single(objectName="additionalActionsButton")
        self.pointing_device.move_to_object(opt)
        self.pointing_device.click()

        edit = gallery.wait_select_single(objectName="actionButtonEdit")
        self.pointing_device.move_to_object(edit)
        self.pointing_device.click()

        editor = gallery.wait_select_single(objectName="photoEditor")
        self.assertThat(editor.visible, Eventually(Equals(True)))

        undo = gallery.wait_select_single(objectName="undoButton")
        self.assertThat(undo.visible, Eventually(Equals(True)))
        self.assertThat(undo.enabled, Eventually(Equals(False)))

        redo = gallery.wait_select_single(objectName="redoButton")
        self.assertThat(redo.visible, Eventually(Equals(True)))
        self.assertThat(redo.enabled, Eventually(Equals(False)))

        back = gallery.wait_select_single(objectName="backButton")
        self.pointing_device.move_to_object(back)
        self.pointing_device.click()

        disappeared = False
        try:
            gallery.select_single(objectName="photoEditor")
        except StateNotFoundError:
            disappeared = True
        self.assertThat(disappeared, Equals(True))