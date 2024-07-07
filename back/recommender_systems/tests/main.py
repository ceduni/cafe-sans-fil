import unittest

# Discover and run all tests in the specified directory
if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='recommender_systems.tests', pattern='test_*.py')

    runner = unittest.TextTestRunner()
    runner.run(suite)