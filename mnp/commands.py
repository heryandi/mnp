import subprocess

def download(packages, index_url, additional_args = None):
    additional_args = [] if additional_args is None else additional_args
    subprocess.check_call(["pip", "install"] + packages + ["--extra-index-url", index_url] + additional_args)

def upload(repository, additional_args = None):
    additional_args = [] if additional_args is None else additional_args
    subprocess.check_call(["python", "setup.py", "register", "-r", repository, "sdist", "upload", "-r", repository] + additional_args)
