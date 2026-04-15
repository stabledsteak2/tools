import unittest

from motion_tools.cli import _build_parser


class TestCli(unittest.TestCase):
    def test_list_tools_command_parses(self):
        parser = _build_parser()
        args = parser.parse_args(["list-tools"])
        self.assertEqual(args.command, "list-tools")

    def test_submit_wan_defaults(self):
        parser = _build_parser()
        args = parser.parse_args(["submit-wan", "--prompt", "test"])
        self.assertEqual(args.motion_strength, 0.6)
        self.assertEqual(args.duration_seconds, 5)


if __name__ == "__main__":
    unittest.main()
