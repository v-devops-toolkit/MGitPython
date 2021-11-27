import pytest
from MultiGit import *

test_items = [
    [
        {},
        { 'dir': '', 'baseUrl': '', 'repos': [] }
    ],
    [
        { 'dir': '/', 'baseUrl': '', 'repos': [] },
        { 'dir': '/', 'baseUrl': '', 'repos': [] }
    ],
    [
        { 'dir': '////', 'baseUrl': '', 'repos': [] },
        { 'dir': '/', 'baseUrl': '', 'repos': [] }
    ],
    [
        { 'dir': 'a', 'baseUrl': 'b' },
        { 'dir': 'a/', 'baseUrl': 'b', 'repos': [] }
    ],
    [
        { 'dir': 'a///', 'baseUrl': 'b' },
        { 'dir': 'a/', 'baseUrl': 'b', 'repos': [] }
    ],
    [
        { 'dir': 'a', 'baseUrl': 'b', 'repos': [{'name': 'c'}] },
        { 'dir': 'a/', 'baseUrl': 'b', 'repos': [{'name': 'c', 'dir': 'a/', 'url': 'b', 'tags': ['all']}] }
    ],
    [
        { 'dir': 'a', 'baseUrl': '', 'repos': [{'name': 'b', 'dir': 'q', 'url': '', 'tags': ['all']}] },
        { 'dir': 'a/', 'baseUrl': '', 'repos': [{'name': 'b', 'dir': 'q', 'url': '', 'tags': ['all']}] }
    ],
    [
        { 'dir': 'a', 'baseUrl': 'x{{name}}y', 'repos': [{'name': 'b'}] },
        { 'dir': 'a/', 'baseUrl': 'x{{name}}y', 'repos': [{'name': 'b', 'dir': 'a/', 'url': 'xby', 'tags': ['all']}] }
    ],
]

@pytest.fixture(params=test_items)
def next_item(request):
    return request.param

def test_process_raw_config_file(next_item):
    mgit = MultiGit()
    mgit.__set_config__(next_item[0])
    mgit.__process_raw_config_file__()
    assert mgit.__get_config__() == next_item[1]
