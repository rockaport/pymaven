from lxml import objectify

from pymaven.artifact import Artifact
from pymaven.packaging import Packaging
from pymaven.scope import Scope


def parse(_file: str) -> Artifact:
    with open(_file) as f:
        # force utf-8, otherwise fromstring throws the following error
        # Unicode strings with encoding declaration are not supported
        xml_string = f.read().encode("utf-8")

    xml_obj = objectify.fromstring(xml_string)

    # build artifact
    artifact = Artifact()

    try:
        artifact.group_id = xml_obj.groupId.text
    except AttributeError:
        artifact.group_id = xml_obj.parent.groupId.text

    artifact.artifact_id = xml_obj.artifactId.text

    try:
        artifact.version = xml_obj.version.text
    except AttributeError:
        artifact.version = xml_obj.parent.version.text

    artifact.version = artifact.version.translate(str.maketrans(dict.fromkeys("[]")))

    try:
        artifact.packaging = Packaging[xml_obj.packaging.text.lower()]
    except AttributeError:
        pass

    try:
        for dep in xml_obj.dependencies:
            dep = dep.dependency

            d = Artifact(dep.groupId.text,
                         dep.artifactId.text,
                         dep.version.text.translate(str.maketrans(dict.fromkeys("[]"))))
            d.scope = Scope[dep.scope.text.lower()]

            artifact.dependencies.append(d)
    except AttributeError:
        pass

    return artifact
