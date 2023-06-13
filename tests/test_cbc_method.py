import sys
sys.path.append('..')

import cbc_methods
from unittest.mock import patch
from Crypto.Random import get_random_bytes

@patch('cbc_methods.get_random_bytes')
def test_encryption(mocked_get_random_bytes):
    mocked_get_random_bytes.return_value = b'1234567812345678'
    
    iv, cipher =  cbc_methods.encrypt_cbc("message", "abcdefghabcdefgh")
    
    assert iv == r"1234567812345678"
    assert cipher.encode('latin-1') == b'&\x85\x1d\x87$\xc8\x94\x12\xbb`\x10\xd6k\xd2?\xc4'