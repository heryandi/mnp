================
Mininet Packager
================

Mininet Packager (mnp) is a wrapper script to help simplify the commands to 
download/upload packages from/to Mininet repository.

Example usage:
--------------

* Downloading:

  Download 1 package:
    mnp download <package>
  Download multiple packages:
    mnp download <package1> <package2> <package3>
  Download from custom repository:
    mnp download <package> -r <repo_name>
    mnp download <package> -i <repo_url>

* Uploading a package:

  Upload package:
    mnp upload
  Upload to custom repository:
    mnp upload -r <repo_name>

<repo_name> and <repo_url> will be read from your ~/.pypirc file, so make sure 
the file is setup properly.

Default value:

* <repo_name>: mininet

* <repo_url>: http://localhost:8000/


TODO: Update the default value of <repo_url> once finalized.
