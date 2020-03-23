from typing import List

from pymaven.packaging import Packaging
from pymaven.scope import Scope


class Artifact:
    group_id: str
    artifact_id: str
    version: str
    packaging: Packaging
    scope: Scope
    dependencies: List['Artifact']

    def __init__(self, group_id: str = "", artifact_id: str = "", version: str = "") -> None:
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.packaging = Packaging.jar
        self.scope = Scope.compile
        self.dependencies = []

    def __str__(self) -> str:
        return ":".join([self.group_id, self.artifact_id, self.version])

    def dir_format(self) -> str:
        return "/".join([self.group_id.replace(".", "/"), self.artifact_id, self.version])

    def base_filename(self) -> str:
        return self.artifact_id + "-" + self.version

    def filename(self) -> str:
        return self.base_filename() + "." + str(self.packaging.value)

    def pom_file(self) -> str:
        return self.base_filename() + ".pom"

    def sources_file(self) -> str:
        return self.base_filename() + "-sources.jar"

    def equals(self, other: 'Artifact') -> bool:
        if self.group_id != other.group_id:
            return False
        if self.artifact_id != other.artifact_id:
            return False
        if self.version != other.version:
            return False

        return True


def sort(artifacts: List[Artifact]):
    artifacts.sort(key=lambda artifact: (artifact.group_id, artifact.artifact_id, artifact.version))
