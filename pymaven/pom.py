from lxml import objectify

from pymaven.artifact import Artifact
from pymaven.packaging import Packaging
from pymaven.scope import Scope


def parse(_file: str) -> Artifact:
    with open(_file) as f:
        # force utf-8, otherwise fromstring throws the following error
        # Unicode strings with encoding declaration are not supported
        xml_string = f.read().encode("utf-8")

    if not xml_string:
        print("pom file is empty: {}".format(_file))
        return Artifact()

    try:
        xml_obj = objectify.fromstring(xml_string)
    except Exception as err:
        print(err)
        return Artifact()

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

            version = dep.version.text.translate(str.maketrans(dict.fromkeys("[]")))

            # we need to pull this from properties
            if "$" in version:
                version = version.translate(str.maketrans(dict.fromkeys("${}")))
                version = xml_obj.properties[version].text

            d = Artifact(dep.groupId.text,
                         dep.artifactId.text,
                         version)
            d.scope = Scope[dep.scope.text.lower()]

            artifact.dependencies.append(d)
    except AttributeError:
        pass

    return artifact
