import subprocess
import unittest


class TestMain(unittest.TestCase):
    def test_main(self):
        # Run the application
        process = subprocess.run(
            ["python3", "main.py", "--fingerprint", "198e9fe586114844f6a4eaca5069b41a7ed43fb5a2df84892b69826d64573e39",
             "--path-license", "examples/license.lic", "--path-machine", "examples/machine.lic"], stdout=subprocess.PIPE)

        # Assert the output is what we expected
        output = process.stdout.decode("utf-8")
        expected_output = "Hello, World!"
        assert expected_output in output
