from .GOSTEncrypt import GOSTEncrypt

GOST = GOSTEncrypt('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef')
# Key taken from official documentation

def test_single_encryption():
    """
    Values for this test are taken from official GOST 34.12-2018 for 128bit spec
    """
    plain_text = "1122334455667700ffeeddccbbaa9988"
    target_text = "7f679d90bebc24305a468d42b9d4edcd"
    result = GOST.encrypt_single(plain_text)
    assert result == target_text

def test_single_decryption():
    # TODO
    pass

def test_json_encryption():
    """
    Values are hand-tested, full pass (18.05.2025)
    """
    plain_json = {"state": "OK", "next": "next/hop"}
    target_text = "ac361e5c72869e29a9996324b0a8cd68c9d32ceb1fb8223b94a429e791d11aa303e215085806d35a9475251a345e03e8"
    result = GOST.encrypt_json(plain_json)
    assert result == target_text

def test_json_decryption():
    """
    Values are hand-tested, full pass (18.05.2025)
    """
    encrypted_json = "ac361e5c72869e29a9996324b0a8cd68c9d32ceb1fb8223b94a429e791d11aa303e215085806d35a9475251a345e03e8"
    target_json = {"state": "OK", "next": "next/hop"}
    result = GOST.decrypt_json(encrypted_json)
    assert result == target_json