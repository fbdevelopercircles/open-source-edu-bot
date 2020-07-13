from services import profile


def test_get_white_listed_urls():
    """Test the generation of white listed url"""
    white_listed_urls = profile.get_white_listed_urls()

    assert isinstance(white_listed_urls, list)
