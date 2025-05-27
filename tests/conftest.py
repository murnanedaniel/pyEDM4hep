import pytest
import os

@pytest.fixture(scope='session')
def sample_edm4hep_file():
    """Fixture to provide the path to the sample EDM4hep ROOT file."""
    # Construct the path relative to this conftest.py file
    # This makes the tests runnable from any directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data', 'sample_event.root')
    if not os.path.exists(file_path):
        pytest.fail(f"Sample data file not found: {file_path}")
    return file_path 