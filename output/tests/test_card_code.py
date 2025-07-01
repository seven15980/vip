import importlib
import string
import pytest

mod = importlib.import_module("openapi_server.utils.card_code")
generate_card_code = mod.generate_card_code
batch_generate_card_codes = mod.batch_generate_card_codes

def test_generate_card_code_basic():
    code = generate_card_code()
    assert isinstance(code, str)
    assert len(code) == 12
    assert all(c in string.ascii_uppercase + string.digits for c in code)

def test_generate_card_code_with_prefix():
    code = generate_card_code(length=8, prefix="VIP-")
    assert code.startswith("VIP-")
    assert len(code) == 4 + 8  # prefix + length

def test_generate_card_code_charset():
    code = generate_card_code(length=6, charset="ABC123")
    assert all(c in "ABC123" for c in code)

def test_batch_generate_card_codes_unique():
    codes = batch_generate_card_codes(100, length=10)
    assert len(codes) == 100
    assert len(set(codes)) == 100

def test_batch_generate_card_codes_prefix():
    codes = batch_generate_card_codes(10, length=5, prefix="PRE-")
    for code in codes:
        assert code.startswith("PRE-")
        assert len(code) == 4 + 5

def test_batch_generate_card_codes_charset():
    codes = batch_generate_card_codes(10, length=6, charset="XYZ")
    for code in codes:
        assert all(c in "XYZ" for c in code[0:])

def test_batch_generate_card_codes_zero():
    codes = batch_generate_card_codes(0)
    assert codes == []

@pytest.mark.parametrize("count,length", [(1, 1), (5, 2), (20, 3)])
def test_batch_generate_card_codes_various(count, length):
    codes = batch_generate_card_codes(count, length=length)
    assert len(codes) == count
    for code in codes:
        assert len(code) == length 