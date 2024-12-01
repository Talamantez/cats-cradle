import pytest

# Configure pytest-asyncio to use auto mode
pytest_plugins = ["pytest_asyncio"]

# Set default fixture loop scope
def pytest_configure(config):
    config.option.asyncio_default_fixture_loop_scope = "function"