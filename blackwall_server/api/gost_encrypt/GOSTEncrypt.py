from .auxillary import split_by, block_zerofill_to, json_to_hex, hex_to_json
from .gost_functions import encrypt, decrypt, generate_key
from .gost_exceptions import GOSTBlockLengthError


class GOSTEncrypt:
    """
       A class implementation of GOST 34-12.2018 128-bit cypher

       Attributes:
           key (str): str
               a hex-formatted string which will be used in encryption
    """
    key: int

    def __init__(self, key: str = None):
        """
        You can provide a 256-bit (64 char hex) key yourself, or have class generate it for you.

        It that case key will be written in ``gost_key.txt`` file in same directory.

        :param key: 64 char hex string which will be used in encryption

        Example of key: ``8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef``
        """
        if key:
            self.key = int(key, 16)
        else:
            self.key = int(generate_key(), 16)
            print(f"WARNING: No key was specified at initiation, generated key : {self.key}")
            with open("gost_key.txt", 'w', encoding='utf-8') as file_output:
                file_output.write(hex(self.key))

    def encrypt_single(self, block: str, mode: str = "strict") -> str:
        """
            :param block: Hex string of fixed length of 128 bits, or 32 chars
            :param mode: Block handling mode. ``strict`` mode will throw ``GOSTBlockLengthError`` exception if block length is less than 32. ``lazy`` mode will not throw an exception and will zerofill your block till needed length
            :returns: encrypted hex string of 32 chars
            :raises GOSTBlockLengthError: Block length is less than 32

            WARNING: Python is a pussy and will eat up zeros in the beginning of the block
        """
        # TODO: Add additional checks for hex and format
        if len(block) == 32:
            return hex(encrypt(int(block, 16), self.key))[2:]
        # noinspection PyUnreachableCode
        match mode:
            case "strict":
                raise GOSTBlockLengthError
            case "lazy":
                block = block_zerofill_to(block, 32, debug=True)
                return hex(encrypt(int(block, 16), self.key))[2:]
            case _:
                raise ValueError("No such mode")

    def encrypt_json(self, json_object: dict):
        encrypted_blocks = []
        hexed_json = json_to_hex(json_object)
        print("Open text:", hexed_json)
        block_container = [int(block, 16) for block in split_by(hexed_json, 32, 'lazy')]
        for block in block_container:
            encrypted_block = encrypt(block, self.key)
            encrypted_blocks.append(block_zerofill_to(hex(encrypted_block)[2:], 32, True))
        print("Encrypted blocks:", encrypted_blocks)
        return ''.join(encrypted_blocks)

    def decrypt_json(self, encrypted_json: str):
        decrypted_blocks = []
        block_container = [int(block, 16) for block in split_by(encrypted_json, 32, 'lazy')]
        print(block_container)
        for block in block_container:
            decrypted_block = decrypt(block, self.key)
            decrypted_blocks.append(hex(decrypted_block)[2:])
        print("Decrypted blocks:", decrypted_blocks)
        return hex_to_json(''.join(decrypted_blocks))
