import pytest
from app import app

# Yahan koi fixture nahi hoga, sirf tests honge
def test_header_exists(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=15)
    assert dash_duo.find_element("h1").text.strip().upper() == "PINK MORSEL SALES ANALYSIS DASHBOARD"

def test_visualization_exists(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-graph", timeout=15)
    assert dash_duo.find_element("#sales-graph") is not None

def test_region_picker_exists(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-picker", timeout=15)
    assert dash_duo.find_element("#region-picker") is not None