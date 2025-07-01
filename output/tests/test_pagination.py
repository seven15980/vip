import importlib
import pytest

mod = importlib.import_module("openapi_server.utils.pagination")
paginate = mod.paginate

def test_paginate_basic():
    items = list(range(25))
    result = paginate(items, page=2, page_size=10)
    assert result["total"] == 25
    assert result["total_pages"] == 3
    assert result["page"] == 2
    assert result["page_size"] == 10
    assert result["data"] == list(range(10, 20))

def test_paginate_last_page():
    items = list(range(23))
    result = paginate(items, page=3, page_size=10)
    assert result["data"] == list(range(20, 23))
    assert result["total_pages"] == 3

def test_paginate_page_out_of_range():
    items = list(range(5))
    result = paginate(items, page=2, page_size=10)
    assert result["data"] == []
    assert result["total_pages"] == 1

def test_paginate_empty():
    result = paginate([], page=1, page_size=10)
    assert result["total"] == 0
    assert result["data"] == []
    assert result["total_pages"] == 0

def test_paginate_page_size_one():
    items = [1, 2, 3]
    result = paginate(items, page=2, page_size=1)
    assert result["data"] == [2]
    assert result["total_pages"] == 3

@pytest.mark.parametrize("page,page_size", [(1, 5), (2, 2), (3, 1)])
def test_paginate_various(page, page_size):
    items = list(range(6))
    result = paginate(items, page=page, page_size=page_size)
    assert result["page"] == page
    assert result["page_size"] == page_size 