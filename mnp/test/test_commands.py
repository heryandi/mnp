import unittest

from mock import patch

from mnp.commands import *

class DownloadTest(unittest.TestCase):
    @patch("subprocess.check_call")
    def test_download_one(self, mockSubprocess):
        download(["package1"], "indexUrl1")
        mockSubprocess.assert_called_once_with(["pip", "install", "package1", "--extra-index-url", "indexUrl1"])

    @patch("subprocess.check_call")
    def test_download_multiple(self, mockSubprocess):
        download(["package1", "package2", "package3"], "indexUrl1")
        mockSubprocess.assert_called_once_with(["pip", "install", "package1", "package2", "package3", "--extra-index-url", "indexUrl1"])

    @patch("subprocess.check_call")
    def test_download_indexUrl2(self, mockSubprocess):
        download(["package1"], "indexUrl2")
        mockSubprocess.assert_called_once_with(["pip", "install", "package1", "--extra-index-url", "indexUrl2"])

    @patch("subprocess.check_call")
    def test_download_additional_args(self, mockSubprocess):
        download(["package1"], "indexUrl1", ["-v", "-v", "-v"])
        mockSubprocess.assert_called_once_with(["pip", "install", "package1", "--extra-index-url", "indexUrl1", "-v", "-v", "-v"])

class NormalUploadTest(unittest.TestCase):
    @patch("subprocess.check_call")
    def test_normal_upload_simple(self, mockSubprocess):
        normal_upload("default")
        mockSubprocess.assert_called_once_with(["python", "setup.py", "register", "-r", "default", "sdist", "upload", "-r", "default"])

    @patch("subprocess.check_call")
    def test_normal_upload_additional_args(self, mockSubprocess):
        normal_upload("default", ["anything", "everything"])
        mockSubprocess.assert_called_once_with(["python", "setup.py", "register", "-r", "default", "sdist", "upload", "-r", "default", "anything", "everything"])

class GitHubUploadTest(unittest.TestCase):
    @patch("subprocess.check_call")
    def test_github_upload_simple(self, mockSubprocess):
        github_upload("default")
        mockSubprocess.assert_called_once_with(["python", "setup.py", "github_register", "-r", "default", "sdist", "github_upload", "-r", "default"])

    @patch("subprocess.check_call")
    def test_github_upload_additional_args(self, mockSubprocess):
        github_upload("default", ["anything", "everything"])
        mockSubprocess.assert_called_once_with(["python", "setup.py", "github_register", "-r", "default", "sdist", "github_upload", "-r", "default", "anything", "everything"])
