# def getline(filename, convert=False, codec='UTF-8'):
#     with open(filename) as source:
#         line = source.readline()
#     if convert:
#         return bytearray(line, codec).hex()
#     return line
import json


def json_to_hex(json_obj: dict) -> str:
    return json.dumps(json_obj).encode().hex()


def hex_to_json(hex_str: str) -> dict:
    return json.loads(bytes.fromhex(hex_str).decode())


def split_by(text, size, mode='strict'):
    """ modes = ['strict', 'lazy']"""

    # noinspection PyUnreachableCode
    match mode:
        case "strict":
            return [text[i * size:(i + 1) * size] for i in range(len(text) // size)]
        case "lazy":
            text_len = len(text)
            number_of_valid_blocks = text_len // size
            container = [text[i * size:(i + 1) * size] for i in range(number_of_valid_blocks)]
            container.append(text[number_of_valid_blocks * size:])
            for block in container:
                if block == '': container.remove(block)
            return container
        case _:
            raise ValueError('Wrong split mode')


def block_zerofill_to(hex_block: str, length: int, debug: bool = False) -> str:
    """
    This function is vital because Python is a bitch and eats up zeros in blocks in str->int->str conversion.
    :param hex_block: Your hex block you are trying to fix
    :param length: Size to fill block to
    :param debug: Whether you want to log fixing triggers, I do recommend going ``True`` while testing
    :return: Zero-filled block with size of 32 chars
    """
    if len(hex_block) == length:
        return hex_block
    fixed_block = hex_block.zfill(length)
    if debug:
        print('\n' + '-' * 14 + 'BLOCK ERROR IN' + '-' * 14)
        print(f"Block {hex_block} length is not {length}, filling")
        print(f"Returning {fixed_block}")
        print('-' * 14 + 'BLOCK ERROR OUT' + '-' * 13 + '\n')
    return fixed_block
