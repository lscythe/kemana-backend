import tempfile
import unittest
from pathlib import Path
from unittest import mock

from commit_scope import allowed_scopes, check_message, first_message_line

SINGLE_PACKAGE = '[package]\nname = "kemana-backend"\nversion = "0.1.0"\n'
WORKSPACE = """
[workspace]
members = ["crates/accounts", "crates/community", "tools/*"]

[package]
name = "kemana-backend"
"""
SCOPES = allowed_scopes(WORKSPACE)


class AllowedScopesTest(unittest.TestCase):
    def test_package_name_and_areas_are_allowed(self):
        scopes = allowed_scopes(SINGLE_PACKAGE)
        for s in ["kemana-backend", "build", "ci", "deps", "tooling", "docs", "release"]:
            self.assertIn(s, scopes)

    def test_workspace_member_names_are_allowed(self):
        for s in ["accounts", "community", "kemana-backend"]:
            self.assertIn(s, SCOPES)

    def test_glob_members_are_not_expanded(self):
        self.assertNotIn("tools", SCOPES)
        self.assertNotIn("tools/*", SCOPES)

    def test_member_directories_are_not_scopes_by_themselves(self):
        self.assertNotIn("crates", SCOPES)
        self.assertNotIn("crates/accounts", SCOPES)

    def test_workspace_without_root_package_is_supported(self):
        scopes = allowed_scopes('[workspace]\nmembers = ["crates/moderation"]\n')
        self.assertIn("moderation", scopes)
        self.assertNotIn("kemana-backend", scopes)


class CheckMessageTest(unittest.TestCase):
    def test_package_scope_passes(self):
        self.assertIsNone(check_message("feat(accounts): add sign up", SCOPES))

    def test_area_scope_passes(self):
        self.assertIsNone(check_message("build(tooling): add service skeleton", SCOPES))

    def test_breaking_marker_passes(self):
        self.assertIsNone(check_message("feat(accounts)!: drop v0 sessions", SCOPES))

    def test_unknown_scope_fails_naming_it(self):
        self.assertIn("acounts", check_message("fix(acounts): typo", SCOPES))

    def test_missing_scope_fails(self):
        self.assertIsNotNone(check_message("fix: something", SCOPES))

    def test_ci_and_docs_may_omit_scope(self):
        for m in ["ci: add workflows", "docs: add adrs"]:
            self.assertIsNone(check_message(m, SCOPES))

    def test_git_generated_messages_pass(self):
        for m in [
            "Merge branch 'develop' into feature/x",
            'Revert "feat(accounts): x"',
            "fixup! feat(accounts): x",
            "squash! feat(accounts): x",
            "amend! feat(accounts): x",
        ]:
            self.assertIsNone(check_message(m, SCOPES))

    def test_unknown_type_fails_naming_it(self):
        self.assertIn("feature", check_message("feature(accounts): x", SCOPES))

    def test_uppercase_summary_fails(self):
        self.assertIsNotNone(check_message("feat(accounts): Add sign up", SCOPES))

    def test_trailing_period_fails(self):
        self.assertIsNotNone(check_message("feat(accounts): add sign up.", SCOPES))

    def test_missing_space_after_colon_fails(self):
        self.assertIsNotNone(check_message("feat(accounts):add sign up", SCOPES))

    def test_empty_summary_fails(self):
        self.assertIsNotNone(check_message("feat(accounts): ", SCOPES))

    def test_header_length_limit_is_72(self):
        prefix = "feat(accounts): "
        at_limit = prefix + "a" * (72 - len(prefix))
        self.assertEqual(72, len(at_limit))
        self.assertIsNone(check_message(at_limit, SCOPES))
        self.assertIsNotNone(check_message(at_limit + "a", SCOPES))


class FirstMessageLineTest(unittest.TestCase):
    def test_file_is_read_as_utf_8(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "COMMIT_EDITMSG"
            path.write_text("# café comment\nfeat(accounts): add sign up\n", encoding="utf-8")
            with mock.patch("io.text_encoding", side_effect=lambda encoding, stacklevel=2: encoding or "ascii"):
                self.assertEqual("feat(accounts): add sign up", first_message_line(str(path)))


if __name__ == "__main__":
    unittest.main()
