import collections
import hashlib
import itertools
import operator
import os
import requests
import subprocess
import xmlrpclib

import distutils.core

from pkg_resources import parse_version

def download(packages, index_url, additional_args = None):
    additional_args = [] if additional_args is None else additional_args
    subprocess.check_call(["pip", "install"] + packages + ["--extra-index-url", index_url] + additional_args)

def normal_upload(repository, additional_args = None):
    additional_args = [] if additional_args is None else additional_args
    subprocess.check_call(["python", "setup.py", "register", "-r", repository, "sdist", "upload", "-r", repository] + additional_args)

def github_upload(repository, github_id, username, password, additional_args = None):
    subprocess.check_call(["python", "setup.py", "github_register", "-r", repository, "sdist", "github_upload", "-r", repository] + additional_args)

def list_packages(index_url):
    rpc_client = xmlrpclib.ServerProxy(index_url)
    packages = rpc_client.list_packages()

    # make print function
    def _print(input):
        print(input)
    [_print(p) for p in packages]

def search(index_url, query):
    rpc_client = xmlrpclib.ServerProxy(index_url)
    packages = rpc_client.search({"name": query, "summary": query}, "or")
    packages.sort(key = lambda x: x["name"])

    # group by name
    grouped = {}
    for name, packages in itertools.groupby(packages, key = operator.itemgetter("name")):
        grouped[name] = [p for p in packages]

    # pick newest of each package for display
    for k, p in sorted(grouped.items()):
        newest_p = sorted(p, key = lambda x: parse_version(x["version"]), reverse = True)[0]
        print("- ".join([newest_p["name"].ljust(20), newest_p["summary"]]))

def docs(index_url, package_name):
    rpc_client = xmlrpclib.ServerProxy(index_url)
    response = rpc_client.docs(package_name)
    print(response)

def info(index_url, package_name, package_version = -1):
    rpc_client = xmlrpclib.ServerProxy(index_url)
    response = rpc_client.info(package_name, package_version)
    print("Name: %s" % response["name"])
    print("Version: %s" % response["version"])
    print("Summary: %s" % response["summary"])
    print("Author: %s" % response["author"])
    print("Home page: %s" % response["home_page"])
    print("Project page: %s" % response["project_page"])
