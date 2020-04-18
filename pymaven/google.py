import os
from typing import List

from lxml import objectify

from pymaven import repo
from pymaven.artifact import Artifact

master_index = "master-index.xml"
group_index = "group-index.xml"


def fetch_master_index(_dest_dir: str) -> str:
    master_index_file = os.path.join(_dest_dir, master_index)

    repo.fetch_file(master_index, master_index_file, overwrite=True)

    return master_index_file


def parse_master_index(_file: str) -> List[str]:
    with open(_file) as f:
        # force utf-8, otherwise fromstring throws the following error
        # Unicode strings with encoding declaration are not supported
        xml_string = f.read().encode("utf-8")

    xml_obj = objectify.fromstring(xml_string)

    return sorted(list(map(lambda x: x.tag, xml_obj.getchildren())))


def to_url_path(_group_id: str) -> str:
    return _group_id.replace(".", "/")


def fetch_group_index(_dest_root_dir: str, _group_id: str) -> str:
    print("fetching group: {}".format(_group_id))

    _group_id_url = to_url_path(_group_id)

    _dest_dir = os.path.join(_dest_root_dir, _group_id_url)

    # ensure the destination dir exists
    os.makedirs(_dest_dir, exist_ok=True)

    group_index_file = os.path.join(_dest_dir, group_index)

    repo.fetch_file(_group_id_url + "/" + group_index, group_index_file, overwrite=True)

    return group_index_file


def parse_group_index(_file: str) -> List[Artifact]:
    print("parsing group: {}".format(_file))

    with open(_file) as f:
        # force utf-8, otherwise fromstring throws the following error
        # Unicode strings with encoding declaration are not supported
        xml_string = f.read().encode("utf-8")

    xml_obj = objectify.fromstring(xml_string)

    group_id = xml_obj.tag

    artifacts = []
    for artifact in xml_obj.getchildren():
        for version in artifact.attrib["versions"].split(","):
            artifacts.append(Artifact(group_id, artifact.tag, version))

    return artifacts
