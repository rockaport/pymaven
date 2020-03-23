import os
import unittest
from tempfile import gettempdir

from pymaven import google, pom, repo
from pymaven.packaging import Packaging


class TestPomParser(unittest.TestCase):
    def test_pom_aar(self):
        artifact = pom.parse("resources/interpolator-1.0.0.pom")
        self.assertEqual(Packaging.aar, artifact.packaging)


class TestGoogleMaven(unittest.TestCase):
    def test_parse_master(self):
        groups = google.parse_master_index(os.path.join("resources", google.master_index))
        print("\n".join(groups))

    def test_fetch_master(self):
        # given
        tempdir = gettempdir()
        master_index_file = os.path.join(tempdir, google.master_index)

        try:
            os.remove(master_index_file)
        except OSError:
            pass

        # when
        google.fetch_master_index(tempdir)

        # then
        self.assertTrue(os.path.exists(master_index_file))

    def test_fetch_group_index(self):
        # given
        tempdir = gettempdir()
        group_id = "com.android.tools.ddms"

        group_index_file = os.path.join(tempdir,
                                        google.to_url_path(group_id),
                                        google.group_index)

        try:
            os.remove(group_index_file)
        except OSError:
            pass

        # when
        google.fetch_group_index(tempdir, group_id)

        # then
        self.assertTrue(os.path.exists(group_index_file))

    def test_fetch_google_maven_xml_files(self):
        # given
        tempdir = os.path.join(gettempdir(), "pymaven")

        os.makedirs(tempdir, exist_ok=True)

        # when
        master_index = google.fetch_master_index(tempdir)
        groups = google.parse_master_index(master_index)

        for group in groups:
            group_index = google.fetch_group_index(tempdir, group)
            artifacts = google.parse_group_index(group_index)

            for artifact in artifacts:
                repo.fetch_artifact_files(tempdir, artifact)

    def test_parse_group_index(self):
        artifacts = google.parse_group_index("resources/group-index.xml")

    def test_fecth_artifact_files(self):
        # given
        tempdir = os.path.join(gettempdir(), "pymaven")

        os.makedirs(tempdir, exist_ok=True)

        # when
        artifacts = google.parse_group_index("resources/group-index.xml")

        for artifact in artifacts:
            google.fetch_artifact_files(tempdir, artifact)

    if __name__ == '__main__':
        unittest.main()
