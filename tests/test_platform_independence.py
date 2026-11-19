"""
Unit Tests for Star Platform Independence & PAL (Platform Abstraction Layer)
Authoritative Reference: STAR_PLATFORM_SPEC.md
"""

import unittest
import os
from star_engine.platform import Platform
from star_engine.lexer import Lexer
from star_engine.parser import Parser
from star_engine.interpreter import Interpreter


class TestPlatformIndependence(unittest.TestCase):
    def test_platform_os_and_arch_detection(self):
        os_name = Platform.os_name()
        self.assertIn(os_name, ("windows", "linux", "macos", "android"))
        self.assertIn(Platform.arch(), ("x64", "arm64", "x86", "arm"))
        self.assertTrue(Platform.is_64bit())
        self.assertGreater(Platform.cpu_count(), 0)
        self.assertIn(Platform.endian(), ("little", "big"))

    def test_universal_path_normalization(self):
        win_style = "src\\models\\user.star"
        posix_style = "src/models/user.star"
        self.assertEqual(Platform.to_posix_path(win_style), "src/models/user.star")
        self.assertEqual(Platform.to_posix_path(posix_style), "src/models/user.star")

    def test_system_directories(self):
        home = Platform.home_dir()
        temp = Platform.temp_dir()
        cwd = Platform.cwd()
        self.assertTrue(os.path.isdir(home))
        self.assertTrue(os.path.isdir(temp))
        self.assertTrue(os.path.isdir(cwd))

    def test_environment_variables(self):
        Platform.set_env("STAR_TEST_VAR", "UNIVERSAL_TEST_123")
        self.assertEqual(Platform.get_env("STAR_TEST_VAR"), "UNIVERSAL_TEST_123")

    def test_platform_star_sdk_integration(self):
        code = """
        use Platform

        show Platform.os
        show Platform.arch
        show Platform.is_64bit
        show Platform.home_dir()
        """
        out = []
        interp = Interpreter(output_handler=lambda s: out.append(s), source_code=code)
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens, source_code=code).parse()
        interp.interpret(ast)

        self.assertEqual(len(out), 4)
        self.assertEqual(out[0], Platform.os_name())
        self.assertEqual(out[1], Platform.arch())
        self.assertEqual(out[2], "true")


if __name__ == "__main__":
    unittest.main()
