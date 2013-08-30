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
