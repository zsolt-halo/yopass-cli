

import unittest
from click.testing import CliRunner
from cli.cli import cli


class CliTestCase(unittest.TestCase):

    def setUp(self):
        super(CliTestCase, self).setUp()
        self.runner = CliRunner()

    def test_yopass_backend_should_be_defined(self):
        result = self.runner.invoke(cli, ["send", 'test-secret'])

        self.assertEqual(
            result.output,
            "YOPASS_BACKEND_URL is not defined, run export\n"
            "            YOPASS_BACKEND_URL=<your backend> first\n"
        )

        self.assertEqual(result.exit_code, 1)

    def test_yopass_frontend_should_be_defined(self):
        env = {
            "YOPASS_BACKEND_URL": "test"
        }

        result = self.runner.invoke(
            cli,
            ["send", 'test-secret, -m verbose'],
            env=env
        )

        self.assertEqual(
            result.output,
            "YOPASS_FRONTEND_URL is not defined, run export\n"
            "            YOPASS_FRONTEND_URL=<your frontend> first\n"
        )

        self.assertEqual(result.exit_code, 1)
