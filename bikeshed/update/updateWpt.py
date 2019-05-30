# -*- coding: utf-8 -*-

import io
import json
import os
import urllib.request, urllib.error, urllib.parse
from contextlib import closing

from ..messages import *

def update(path, dryRun=False):
    try:
        say("Downloading web-platform-tests data...")
        with closing(urllib.request.urlopen("https://wpt.fyi/api/manifest")) as fh:
            sha = fh.info().getheader("x-wpt-sha")
            jsonData = json.load(fh, encoding="utf-8")
    except Exception as e:
        die("Couldn't download web-platform-tests data.\n{0}", e)
        return

    paths = []
    for testType, typePaths in list(jsonData["items"].items()):
        if testType not in ("manual", "reftest", "testharness", "wdspec"):
            # Not tests
            continue
        paths.extend((testType, path) for path in list(typePaths.keys()))

    if not dryRun:
        try:
            with io.open(os.path.join(path, "wpt-tests.txt"), 'w', encoding="utf-8") as f:
                f.write("sha: {0}\n".format(sha))
                for path in sorted(paths):
                    f.write("{0} {1}\n".format(*path))
        except Exception as e:
            die("Couldn't save web-platform-tests data to disk.\n{0}", e)
            return
    say("Success!")
