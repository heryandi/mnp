import argparse
import ConfigParser
import getpass
import os
import sys

from commands import docs, download, github_upload, info, list_packages, normal_upload, search
from utils import craft_download_url

# TODO: Change github application id once finalized
pypi_github_id = "f7d6dae90c7584bb737f"
default_pypi_name = "mininet"
# TODO: Change to Mininet repo URL once finalized
default_pypi_upload_url = "http://localhost:8000/"
default_pypi_download_url = craft_download_url(default_pypi_upload_url)
pypirc = ConfigParser.ConfigParser()

def init():
    global pypirc
    global default_pypi_upload_url
    global default_pypi_download_url

    try:
        pypirc.read(os.path.join(os.path.expanduser("~"), ".pypirc"))
        default_pypi_upload_url = pypirc.get(default_pypi_name, "repository")
        default_pypi_download_url = craft_download_url(default_pypi_upload_url)
    except ConfigParser.NoSectionError as e:
        print(e.message)
        print("Make sure the .pypirc file is correct.\n")
    except ConfigParser.NoOptionError as e:
        print(e.message)
        print("Make sure the .pypirc file is correct.\n")

def download_handler(args, additional_args):
    index_url = default_pypi_download_url
    if args.repository:
        index_url = craft_download_url(pypirc.get(args.repository[0], "repository"))
    elif args.index_url:
        index_url = args.index_url[0]
    download(args.packages, index_url, additional_args)

def upload_handler(args, additional_args):
    repo = args.repository[0]
    keys = set(x[0] for x in pypirc.items(repo))
    if "username" in keys and "password" in keys:
        normal_upload(repo, additional_args)
    elif "github_username" in keys:
        password = None
        if "github_password" in keys:
            password = pypirc.get(repo, "github_password")
        else:
            password = getpass.getpass("Enter your GitHub password: ")
        github_upload(pypirc.get(repo, "repository"), pypi_github_id, pypirc.get(repo, "github_username"), password)

def list_handler(args, additional_args):
    list_packages(pypirc.get(args.repository[0], "repository"))

def search_handler(args, additional_args):
    search(pypirc.get(args.repository[0], "repository"), " ".join(args.query))

def docs_handler(args, additional_args):
    docs(pypirc.get(args.repository[0], "repository"), " ".join(args.package_name))

def info_handler(args, additional_args):
    info(pypirc.get(args.repository[0], "repository"), args.package_name[0], args.package_version)

def main():
    init()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help = "action")

    down_subp = subparsers.add_parser("download")
    down_subp.add_argument("packages", nargs = "+", help = "list of packages to download")
    down_subp_repo_group = down_subp.add_mutually_exclusive_group()
    down_subp_repo_group.add_argument("-r", "--repository", nargs = 1)
    down_subp_repo_group.add_argument("-i", "--index-url", nargs = 1)
    down_subp.set_defaults(func = download_handler)

    up_subp = subparsers.add_parser("upload")
    up_subp.add_argument("-r", "--repository", nargs = 1, default = [default_pypi_name])
    up_subp.set_defaults(func = upload_handler)

    list_subp = subparsers.add_parser("list")
    list_subp.add_argument("-r", "--repository", nargs = 1, default = [default_pypi_name])
    list_subp.set_defaults(func = list_handler)

    search_subp = subparsers.add_parser("search")
    search_subp.add_argument("query", nargs = "+", help = "search term(s)")
    search_subp.add_argument("-r", "--repository", nargs = 1, default = [default_pypi_name])
    search_subp.set_defaults(func = search_handler)

    docs_subp = subparsers.add_parser("docs")
    docs_subp.add_argument("package_name", nargs = 1, help = "package name")
    docs_subp.add_argument("-r", "--repository", nargs = 1, default = [default_pypi_name])
    docs_subp.set_defaults(func = docs_handler)

    info_subp = subparsers.add_parser("info")
    info_subp.add_argument("package_name", nargs = 1, help = "package name")
    info_subp.add_argument("package_version", nargs = "?", default = -1, help = "package version")
    info_subp.add_argument("-r", "--repository", nargs = 1, default = [default_pypi_name])
    info_subp.set_defaults(func = info_handler)

    result, rest = parser.parse_known_args()
    result.func(result, rest)

if __name__ == "__main__":
    main()
