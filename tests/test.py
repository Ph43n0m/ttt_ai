import unittest

from test_play import *


class AllTests:
    @staticmethod
    def run():
        unittest.main(module=None, verbosity=2)


class BoardTests:
    @staticmethod
    def run():
        suite = unittest.TestLoader().loadTestsFromModule(__import__("test_board"))
        unittest.TextTestRunner(verbosity=2).run(suite)


class PlayTests:
    @staticmethod
    def run():
        suite = unittest.TestLoader().loadTestsFromModule(__import__("test_play"))
        unittest.TextTestRunner(verbosity=2).run(suite)


class AgentTests:
    @staticmethod
    def run():
        suite = unittest.TestLoader().loadTestsFromModule(__import__("test_agent"))
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    # Run all tests by default
    AllTests.run()
