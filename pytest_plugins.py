"""Pytest configuration hooks for better test reporting"""
import pytest
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def pytest_configure(config):
    """Configure pytest with custom markers and settings"""
    config.addinivalue_line(
        "markers", "smoke: mark test as a smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as a regression test"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical"
    )
    
    # Create reports directory if it doesn't exist
    Path("reports").mkdir(exist_ok=True)
    Path("reports/screenshots").mkdir(exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test outcome available to fixtures"""
    outcome = yield
    rep = outcome.get_result()
    
    # Store the test result in the item
    setattr(item, f"rep_{rep.when}", rep)


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add markers based on test name patterns
        if "smoke" in item.nodeid.lower():
            item.add_marker(pytest.mark.smoke)
        if "regression" in item.nodeid.lower():
            item.add_marker(pytest.mark.regression)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add custom summary to terminal output"""
    terminalreporter.write_sep("=", "Test Automation Summary", bold=True)
    
    # Add custom message
    if exitstatus == 0:
        terminalreporter.write("\n✅ All tests passed!\n", green=True, bold=True)
    else:
        terminalreporter.write("\n❌ Some tests failed!\n", red=True, bold=True)
    
    terminalreporter.write_sep("=", "HTML Report: reports/report.html")
