import argparse
import ConfigParser
import os
import sys

from commands import download, upload

default_pypi_name = "mininet"
# TODO: Change to Mininet repo URL once finalized
default_pypi_upload_url = "http://localhost:8000/"
default_pypi_download_url = default_pypi_upload_url.rstrip("/") + "/simple/"
pypirc = ConfigParser.ConfigParser()

def init():
    global pypirc
    global default_pypi_upload_url
    global default_pypi_download_url

    try:
        pypirc.read(os.path.join(os.path.expanduser("~"), ".pypirc"))
        default_pypi_upload_url = pypirc.get(default_pypi_name, "repository")
        default_pypi_download_url = default_pypi_upload_url.rstrip("/") + "/simple/"
    except ConfigParser.NoSectionError as e:
        print(e.message)
        print("Make sure the .pypirc file is correct.\n")
    except ConfigParser.NoOptionError as e:
        print(e.message)
        print("Make sure the .pypirc file is correct.\n")

def download_handler(args, additional_args):
    index_url = default_pypi_download_url
    if args.repository:
        index_url = pypirc.get(args.repository[0], "repository")
    elif args.index_url:
        index_url = args.index_url[0]
    download(args.packages, index_url, additional_args)

def upload_handler(args, additional_args):
    upload(args.repository[0], additional_args)

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

    result, rest = parser.parse_known_args()
    result.func(result, rest)

if __name__ == "__main__":
    main()
