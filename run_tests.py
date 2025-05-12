import pytest
import sys

if __name__ == "__main__":
    # Running all the units test
    print("Runnning the unit test...")
    exit_code = pytest.main(["-v", "tests/unit/"])
    sys.exit(exit_code)