import StringIO
import sys
import unittest

from mock import patch

from mnp.command import *

# For tests needing subprocess
class SubprocessTest(unittest.TestCase):
    def setUp(self):
        patcher1 = patch("subprocess.check_call")
        self.addCleanup(patcher1.stop)
        self.mockSubprocess_check_call = patcher1.start()

class DownloadTest(SubprocessTest):
    def test_download_one(self):
        download(["package1"], "indexUrl1")
        self.mockSubprocess_check_call.assert_called_once_with(["pip", "install", "package1", "--extra-index-url", "indexUrl1"])

    def test_download_multiple(self):
        download(["package1", "package2", "package3"], "indexUrl1")
        self.mockSubprocess_check_call.assert_called_once_with(["pip", "install", "package1", "package2", "package3", "--extra-index-url", "indexUrl1"])

    def test_download_indexUrl2(self):
        download(["package1"], "indexUrl2")
        self.mockSubprocess_check_call.assert_called_once_with(["pip", "install", "package1", "--extra-index-url", "indexUrl2"])

    def test_download_additional_args(self):
        download(["package1"], "indexUrl1", ["-v", "-v", "-v"])
        self.mockSubprocess_check_call.assert_called_once_with(["pip", "install", "package1", "--extra-index-url", "indexUrl1", "-v", "-v", "-v"])

class NormalUploadTest(SubprocessTest):
    def test_normal_upload_simple(self):
        normal_upload("default")
        self.mockSubprocess_check_call.assert_called_once_with(["python", "setup.py", "register", "-r", "default", "sdist", "upload", "-r", "default"])

    def test_normal_upload_additional_args(self):
        normal_upload("default", ["anything", "everything"])
        self.mockSubprocess_check_call.assert_called_once_with(["python", "setup.py", "register", "-r", "default", "sdist", "upload", "-r", "default", "anything", "everything"])

class GitHubUploadTest(SubprocessTest):
    def test_github_upload_simple(self):
        github_upload("default")
        self.mockSubprocess_check_call.assert_called_once_with(["python", "setup.py", "github_register", "-r", "default", "sdist", "github_upload", "-r", "default"])

    def test_github_upload_additional_args(self):
        github_upload("default", ["anything", "everything"])
        self.mockSubprocess_check_call.assert_called_once_with(["python", "setup.py", "github_register", "-r", "default", "sdist", "github_upload", "-r", "default", "anything", "everything"])

# For tests needing xmlrpclib
class XmlRpcTest(unittest.TestCase):
    def setUp(self):
        # print method for debugging
        self.originalStdout = sys.stdout
        self._print = lambda x: self.originalStdout.write(str(x) + "\n")

        patcher1 = patch("xmlrpclib.ServerProxy")
        self.addCleanup(patcher1.stop)
        self.mockServerProxy = patcher1.start()

        patcher2 = patch("sys.stdout", new_callable = StringIO.StringIO)
        self.addCleanup(patcher2.stop)
        self.stringIO = patcher2.start()

class ListPackageTest(XmlRpcTest):
    def setUp(self):
        super(ListPackageTest, self).setUp()
        self.list_packages_return_value = ["package1", "package2", "package3"]

        self.mockServerProxy.return_value.list_packages.return_value = self.list_packages_return_value

    def test_list(self):
        list_packages("indexUrl1")
        self.mockServerProxy.assert_called_once_with("indexUrl1")
        self.mockServerProxy.return_value.list_packages.assert_called_once_with()

        self.assertEquals(self.stringIO.getvalue(), "\n".join(self.list_packages_return_value) + "\n")

class SearchPackageTest(XmlRpcTest):
    def setUp(self):
        super(SearchPackageTest, self).setUp()
        self.search_return_value = [
            {"name": "package1", "version": "1.0.0", "summary": "summary1"},
            {"name": "package1", "version": "1.1.0", "summary": "summary1"},
            {"name": "package2", "version": "1.0.0", "summary": "summary2"},
        ]

        self.mockServerProxy.return_value.search.return_value = self.search_return_value

    def test_search(self):
        search("indexUrl1", "query1")
        self.mockServerProxy.assert_called_once_with("indexUrl1")
        self.mockServerProxy.return_value.search.assert_called_once_with({"name": "query1", "summary": "query1"}, "or")

        newest_packages = [
            {"name": "package1", "version": "1.1.0", "summary": "summary1"},
            {"name": "package2", "version": "1.0.0", "summary": "summary2"},
        ]
        expected_string = "\n".join("- ".join([p["name"].ljust(20), p["summary"]]) for p in newest_packages)
        self.assertEquals(self.stringIO.getvalue(), expected_string + "\n")

class DocsTest(XmlRpcTest):
    def setUp(self):
        super(DocsTest, self).setUp()
        self.docs_return_value = "Some String"

        self.mockServerProxy.return_value.docs.return_value = self.docs_return_value

    def test_docs(self):
        docs("indexUrl1", "package1")
        self.mockServerProxy.assert_called_once_with("indexUrl1")
        self.mockServerProxy.return_value.docs.assert_called_once_with("package1")

        self.assertEquals(self.stringIO.getvalue(), self.docs_return_value + "\n")

class InfoTest(XmlRpcTest):
    def setUp(self):
        super(InfoTest, self).setUp()
        self.info_return_value = {
            "name": "name",
            "version": "version",
            "summary": "summary",
            "author": "author",
            "home_page": "home_page",
            "project_page": "project_page"
        }
        self.mockServerProxy.return_value.info.return_value = self.info_return_value

    def test_info(self):
        info("indexUrl1", "package1", "version1")
        self.mockServerProxy.assert_called_once_with("indexUrl1")
        self.mockServerProxy.return_value.info.assert_called_once_with("package1", "version1")

        expected_string = "\n".join(["Name: " + self.info_return_value["name"],
            "Version: " + self.info_return_value["version"],
            "Summary: " + self.info_return_value["summary"],
            "Author: " + self.info_return_value["author"],
            "Home page: " + self.info_return_value["home_page"],
            "Project page: " + self.info_return_value["project_page"]])
        self.assertEquals(self.stringIO.getvalue(), expected_string + "\n")

    def test_info_no_version(self):
        info("indexUrl1", "package1")
        self.mockServerProxy.assert_called_once_with("indexUrl1")
        self.mockServerProxy.return_value.info.assert_called_once_with("package1", -1)
