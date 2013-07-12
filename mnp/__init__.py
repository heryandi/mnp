import argparse
import sys

from commands import download, upload

default_pypi_name = "mininet"
# TODO: Change to Mininet repo URL
default_pypi_url = "https://pypi.python.org/simple/"

def download_handler(args, additional_args):
    download(args.packages, args.index_url[0], additional_args)

def upload_handler(args, additional_args):
    upload(args.repository[0], additional_args)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help = "action")

    down_subp = subparsers.add_parser("download")
    down_subp.add_argument("packages", nargs = "+", help = "list of packages to download")
    down_subp.add_argument("-i", "--index-url", nargs = 1, default = [default_pypi_url])
    down_subp.set_defaults(func = download_handler)

    up_subp = subparsers.add_parser("upload")
    up_subp.add_argument("-r", "--repository", nargs = 1, default = [default_pypi_name])
    up_subp.set_defaults(func = upload_handler)

    result, rest = parser.parse_known_args()
    result.func(result, rest)

if __name__ == "__main__":
    main()
