import pytest

@pytest.mark.manual
def test_manual_ui_launch():
    """Manual UI launch test for visual inspection."""
    import launch_ui
    launch_ui.launch_ui()
