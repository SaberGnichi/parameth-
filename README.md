# Parameth++

This tool can be used to brute discover GET parameters using 2 techniques,
the first: simple brute force attack using common keywords such as cmd, file, to, etc ..
the second: read the html content of the file and then extract tags names 

# Usage

usage: parameth++.py [-h] [-f FILE] [-u URL] [-s SOURCE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  the file that contains urls
  -u URL, --url URL     the url
  -s SOURCE, --source SOURCE
                        the source file that contains common words to be used
                        as params

