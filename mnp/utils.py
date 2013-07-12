def craft_download_url(upload_url):
    if upload_url.rstrip("/").endswith("pypi"):
        return upload_url[::-1].replace("pypi"[::-1], "simple"[::-1], 1)[::-1]
    else:
        return upload_url.rstrip("/") + "/simple/"
