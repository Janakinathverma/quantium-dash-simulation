from app import app

def test_header_exists(dash_duo):
    # Start the app
    dash_duo.start_server(app)
    
    # Wait for the header element to appear
    dash_duo.wait_for_element("h1", timeout=10)
    
    # Check if the text matches
    assert dash_duo.find_element("h1").text == "Pink Morsel Sales Visualiser"

def test_visualization_exists(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-graph", timeout=10)
    assert dash_duo.find_element("#sales-graph") is not None