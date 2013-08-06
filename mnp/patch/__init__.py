import ConfigParser
import hashlib
import os

from distutils.command.upload import upload
from setuptools import Command
from setuptools.command.register import register
import requests
import setuptools

from .. import pypi_github_id

def get_github_userid(github_username, github_password):
    user = requests.get("https://api.github.com/user", auth = (github_username, github_password))
    if user.status_code == 200:
        return user.json()["id"]
    elif auths.status_code == 401:
        print("Invalid username or password.")
    else:
        print(user.json()["message"])

def get_github_hashed_token(github_username, github_password):
    auths = requests.get("https://api.github.com/authorizations", auth = (github_username, github_password))
    if auths.status_code == 200:
        for token in auths.json():
            if token["app"]["client_id"] == pypi_github_id:
                hashed_token = hashlib.sha1(token["token"]).hexdigest()
                return hashed_token
        print("No matching token found. Make sure the github account is already registered with the website.")
    elif auths.status_code == 401:
        print("Invalid username or password.")
    else:
        print("Error code: %s" % auths.status_code)
        print(auths.json()["message"])
        print(auths.text)

class github_mixin(Command, object):
    def _read_pypirc(self):
        config = super(github_mixin, self)._read_pypirc()
        # Reopen pypirc file and read in additional configuration because
        # distutils implementation doesn't read in everything.
        repository = self.repository or self.DEFAULT_REPOSITORY
        rc = self._get_rc_file()
        if os.path.exists(rc):
            cp = ConfigParser.ConfigParser()
            cp.read(rc)
            github_username = cp.get(repository, "github_username")

            keys = set(x[0] for x in cp.items(repository))
            if "github_password" not in keys:
                github_password = getpass.getpass("Enter your GitHub password: ")
            else:
                github_password = cp.get(repository, "github_password")
        config["username"] = str(get_github_userid(github_username, github_password))
        config["password"] = get_github_hashed_token(github_username, github_password)
        return config

"""
    setup.py subcommand to register package using github token for authentication
"""
class github_register(github_mixin, register, object):
    pass

"""
    setup.py subcommand to upload package using github token for authentication
"""
class github_upload(github_mixin, upload, object):
    pass

"""
    Do some patching to automatically include additional commands
"""
_setup = setuptools.setup
def setup(**args):
    if "cmdclass" not in args:
        args["cmdclass"] = {}
    if "github_upload" not in args["cmdclass"]:
        args["cmdclass"]["github_register"] = github_register
        args["cmdclass"]["github_upload"] = github_upload
    print(args)
    _setup(**args)
setuptools.setup = setup
