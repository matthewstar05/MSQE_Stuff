"""Offline checks for complete scans and preservation of course materials."""

import base64
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import canvas_sync as sync


class CanvasSyncTests(unittest.TestCase):
    def setUp(self):
        sync.API_CACHE.clear()
        sync.SCAN_WARNINGS.clear()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        setting = patch.object(sync, "REPO_ROOT", str(self.root))
        setting.start()
        self.addCleanup(setting.stop)

    def response(self, data, status=200, link=""):
        return json.dumps({"status": status, "body": json.dumps(data), "link": link})

    def test_pagination_follows_opaque_next_even_on_a_short_page(self):
        next_url = sync.CANVAS_ORIGIN + "/api/v1/courses/1/files?cursor=opaque"
        with patch.object(sync, "arc_eval", side_effect=[
                self.response([{"id": 1}], link=f'<{next_url}>; rel="next"'),
                self.response([{"id": 2}])]) as browser:
            self.assertEqual(sync.canvas_api_list("/api/v1/courses/1/files?per_page=100"), [{"id": 1}, {"id": 2}])
        self.assertIn(next_url, browser.call_args_list[1].args[0])

    def test_pagination_does_not_follow_an_external_origin(self):
        with patch.object(sync, "arc_eval", return_value=self.response([], link='<https://example.org/api/v1/files>; rel="next"')):
            with self.assertRaisesRegex(RuntimeError, "outside"):
                sync.canvas_api_list("/api/v1/courses/1/files")

    def test_login_html_is_an_error_rather_than_an_empty_course(self):
        response = json.dumps({"status": 200, "body": "<html>Login</html>", "link": ""})
        with patch.object(sync, "arc_eval", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "login page"):
                sync.canvas_api_get("/api/v1/users/self")

    def test_transient_read_error_recovers_and_is_cached(self):
        with patch.object(sync, "arc_eval", side_effect=[self.response({}, 503), self.response({"id": 1})]) as browser, \
                patch.object(sync.time, "sleep") as wait:
            self.assertEqual(sync.canvas_api_get("/api/v1/users/self"), {"id": 1})
            self.assertEqual(sync.canvas_api_get("/api/v1/users/self"), {"id": 1})
        self.assertEqual(browser.call_count, 2)
        wait.assert_called_once_with(1)

    def test_incomplete_download_does_not_replace_an_existing_document(self):
        dest = self.root / "notes.pdf"
        dest.write_bytes(b"Existing notes")
        with patch.object(sync, "arc_eval", return_value=base64.b64encode(b"partial").decode()):
            with self.assertRaisesRegex(RuntimeError, "Incomplete download"):
                sync.download_file_to("https://canvas.calpoly.edu/files/1/download", str(dest), expected_size=100)
        self.assertEqual(dest.read_bytes(), b"Existing notes")
        self.assertEqual(list(self.root.glob(".canvas-*")), [])

    def test_content_hash_confirms_a_renamed_duplicate(self):
        data = b"Same file under another name"
        dest = self.root / "new-name.pdf"
        with patch.object(sync, "arc_eval", return_value=base64.b64encode(data).decode()):
            result = sync.download_file_to("https://canvas.calpoly.edu/files/1/download", str(dest), len(data),
                                           {hashlib.sha256(data).hexdigest(): "existing.pdf"})
        self.assertIsNone(result)
        self.assertFalse(dest.exists())

    def test_valid_download_replaces_only_after_validation(self):
        data = b"New lecture notes"
        dest = self.root / "notes.pdf"
        dest.write_bytes(b"Old notes")
        with patch.object(sync, "arc_eval", return_value=base64.b64encode(data).decode()):
            self.assertEqual(sync.download_file_to("https://canvas.calpoly.edu/files/1/download", str(dest), len(data)), len(data))
        self.assertEqual(dest.read_bytes(), data)
        self.assertEqual(list(self.root.glob(".canvas-*")), [])

    def test_model_selection_assignment_goes_into_homeworks(self):
        path = sync.target_dest_for_file("SS1-ECON5015-ComputingMLEcon", "model_selection_assignment_2026.docx", "files_api")
        self.assertIn("/Homeworks/Model_Selection/", path)

    def test_week11_is_not_mistaken_for_week1(self):
        course = "SS1-ECON5040-DynamicStochasticModeling"
        for filename, folder in (("Week11_Lecture_1_Euler_to_Lucas_Tree.ipynb", "/In_Class_Notebooks/Week11_Asset_Pricing/"),
                                 ("Week11_Markov_Asset_Pricing_Problem_Set.pdf", "/ProblemSets/ProblemSet10/"),
                                 ("Week11_Markov_Asset_Pricing_Starter.ipynb", "/ProblemSets/ProblemSet10/"),
                                 ("Week11_Lecture_Notes.pdf", "/Lecture_Notes/Week11_Lucas_Tree/")):
            with self.subTest(filename=filename):
                self.assertIn(folder, sync.target_dest_for_file(course, filename, "module:Week 11"))

    def test_filename_cannot_escape_a_course_folder(self):
        for filename in ("../notes.pdf", "..\\notes.pdf", "/tmp/notes.pdf"):
            with self.subTest(filename=filename), self.assertRaises(RuntimeError):
                sync.target_dest_for_file("SS1-ECON5015-ComputingMLEcon", filename, "files_api")

    def test_same_size_with_a_different_name_is_not_silently_skipped(self):
        folder = "SS1-ECON5021-AdvEconometrics1"
        existing = self.root / folder / "Lecture_Notes" / "old.pdf"
        existing.parent.mkdir(parents=True)
        existing.write_bytes(b"x" * 6000)
        metadata = {"id": 1, "display_name": "new.pdf", "size": 6000,
                    "url": "https://canvas.calpoly.edu/files/1/download"}
        with patch.object(sync, "COURSE_MAP", {1: folder}), \
                patch.object(sync, "find_canvas_tab", return_value=sync.CANVAS_ORIGIN), \
                patch.object(sync, "canvas_api_get", return_value={"id": 1}), \
                patch.object(sync, "canvas_api_list", side_effect=lambda path: [metadata] if "/files?" in path else []), \
                patch.object(sync.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout=b"")), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            sync.run_sync(dry_run=True)
        self.assertIn("DIFFERENTIALS FOUND: 1", output.getvalue())
        self.assertEqual(existing.read_bytes(), b"x" * 6000)
        self.assertFalse((existing.parent / "new.pdf").exists())

    def test_updated_document_preserves_existing_local_edits(self):
        folder = "SS1-ECON5021-AdvEconometrics1"
        relative = folder + "/Lecture_Notes/notes.pdf"
        existing = self.root / relative
        existing.parent.mkdir(parents=True)
        existing.write_bytes(b"My local edits")
        metadata = {"id": 7, "display_name": "notes.pdf", "size": 100,
                    "url": "https://canvas.calpoly.edu/files/7/download"}

        def git_result(command, **kwargs):
            paths = (relative + "\0").encode() if "-m" in command else b""
            return subprocess.CompletedProcess(command, 0, stdout=paths)

        with patch.object(sync, "COURSE_MAP", {1: folder}), \
                patch.object(sync, "find_canvas_tab", return_value=sync.CANVAS_ORIGIN), \
                patch.object(sync, "canvas_api_get", return_value={"id": 1}), \
                patch.object(sync, "canvas_api_list", side_effect=lambda path: [metadata] if "/files?" in path else []), \
                patch.object(sync.subprocess, "run", side_effect=git_result), contextlib.redirect_stdout(io.StringIO()) as output:
            sync.run_sync(dry_run=True)
        self.assertIn("notes (Canvas 7).pdf", output.getvalue())
        self.assertEqual(existing.read_bytes(), b"My local edits")

    def test_module_items_omitted_from_inline_response_are_still_scanned(self):
        folder = "SS1-ECON5040-DynamicStochasticModeling"
        endpoints = []

        def listing(path):
            endpoints.append(path)
            if "/modules?" in path:
                return [{"id": 2, "name": "Week 11", "items_count": 1, "items": None}]
            if "/modules/2/items?" in path:
                return [{"type": "File", "content_id": 7, "title": "Week11_notes.pdf"}]
            return []

        metadata = {"7": {"id": 7, "display_name": "Week11_notes.pdf", "size": 100,
                          "url": "https://canvas.calpoly.edu/files/7/download"}}
        with patch.object(sync, "COURSE_MAP", {1: folder}), \
                patch.object(sync, "find_canvas_tab", return_value=sync.CANVAS_ORIGIN), \
                patch.object(sync, "canvas_api_get", return_value={"id": 1}), \
                patch.object(sync, "canvas_api_list", side_effect=listing), \
                patch.object(sync, "arc_eval", return_value=json.dumps(metadata)), \
                patch.object(sync.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout=b"")), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            sync.run_sync(dry_run=True)
        self.assertIn("/api/v1/courses/1/modules/2/items?per_page=100", endpoints)
        self.assertIn("Week11_Lucas_Tree/Week11_notes.pdf", output.getvalue())


if __name__ == "__main__":
    unittest.main()
