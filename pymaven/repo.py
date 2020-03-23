import os
import urllib
import urllib.error
import urllib.request
from urllib import parse

from pymaven import pom
from pymaven.artifact import Artifact
from pymaven.packaging import Packaging

repo_urls = ["https://maven.google.com", "https://jcenter.bintray.com"]


def fetch_file(_url: str, _dest: str):
    # print("fetching {} to {}".format(_url, _dest))

    if os.path.exists(_dest):
        print("skipping: {}".format(_dest))
        return

    for repo in repo_urls:
        try:
            # print("requesting {}".format(_url))
            urllib.request.urlretrieve(parse.urljoin(repo, _url), _dest)
            break
        except urllib.error.HTTPError as err:
            # file may never exist, touch something
            if err.code == 404:
                open(_dest, "a").close()
            else:
                print(err)


def fetch_artifact_files(_dest_root_dir: str, artifact: Artifact, parent: Artifact = None):
    print("fetching artifacts : {}".format(artifact))

    _dest_dir = os.path.join(_dest_root_dir, artifact.dir_format())

    os.makedirs(_dest_dir, exist_ok=True)

    # group_id/artifact_id/version/artifact_id-version.pom
    # .pom, .{packaging}, -sources.jar

    base_url = artifact.dir_format()

    _dest_file = os.path.join(_dest_dir, artifact.pom_file())

    fetch_file(base_url + "/" + artifact.pom_file(), _dest_file)

    pom_artifact = pom.parse(_dest_file)

    if pom_artifact.packaging != Packaging.pom:
        # artifact file (e.g. jar)
        artifact_file = pom_artifact.filename()
        _dest_file = os.path.join(_dest_dir, artifact_file)

        fetch_file(base_url + "/" + artifact_file, _dest_file)

        # sources file (e.g. *-sources.jar)
        artifact_file = pom_artifact.sources_file()
        _dest_file = os.path.join(_dest_dir, artifact_file)

        fetch_file(base_url + "/" + artifact_file, _dest_file)

    for dependency in pom_artifact.dependencies:
        print("fetching dependency: {}".format(dependency))

        if parent is not None and parent.equals(dependency):
            print("circular dependency detected {} to {}".format(parent, dependency))
            continue

        try:
            fetch_artifact_files(_dest_root_dir, dependency, parent=pom_artifact)
        except RecursionError as err:
            print(err)
            pass
