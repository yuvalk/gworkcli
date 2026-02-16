from upload_doc import extract_title


def test_h1_heading():
    assert extract_title("# Heading", "fallback") == "Heading"


def test_h2_heading():
    assert extract_title("## Second Level", "fallback") == "Second Level"


def test_leading_blank_lines():
    assert extract_title("\n\n# Heading", "fallback") == "Heading"


def test_no_heading_returns_fallback():
    assert extract_title("Just plain text", "fallback") == "fallback"


def test_empty_string_returns_fallback():
    assert extract_title("", "fallback") == "fallback"


def test_heading_with_extra_spaces():
    assert extract_title("#   Spaced   ", "fallback") == "Spaced"
