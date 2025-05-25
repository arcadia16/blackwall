import struct
import io


def _parse_mysql_handshake(data: bytes) -> dict | None:
    """Parse MySQL server handshake packet"""
    # Create a stream for easier reading
    try:
        stream = io.BytesIO(data)

        # Parse header (4 bytes: length + sequence_id)
        header = stream.read(4)
        length = struct.unpack('<I', header[:3] + b'\x00')[0]
        sequence_id = header[3]

        # Parse protocol version (1 byte)
        protocol_version = struct.unpack('<B', stream.read(1))[0]

        # Parse server version (null-terminated string)
        server_version = bytearray()
        while True:
            char = stream.read(1)
            if char == b'\x00' or not char:
                break
            server_version += char

        # Parse connection ID (4 bytes)
        thread_id = struct.unpack('<I', stream.read(4))[0]

        # Read first part of scramble (8 bytes)
        scramble_part1 = stream.read(8)

        # Skip filler (1 byte)
        stream.read(1)

        # Parse capability flags (lower 2 bytes)
        capability_low = struct.unpack('<H', stream.read(2))[0]

        # Read character set (1 byte)
        charset = struct.unpack('<B', stream.read(1))[0]

        # Parse status flags (2 bytes)
        status_flags = struct.unpack('<H', stream.read(2))[0]

        # Parse capability flags (upper 2 bytes)
        capability_high = struct.unpack('<H', stream.read(2))[0]

        # Combine capability flags
        capabilities = (capability_high << 16) | capability_low

        # Read auth plugin data length (1 byte)
        auth_data_len = struct.unpack('<B', stream.read(1))[0]

        # Skip reserved bytes (10 bytes)
        stream.read(10)

        # Read second part of scramble (variable length)
        scramble_part2 = stream.read(max(13, auth_data_len - 8))

        # Read auth plugin name (null-terminated)
        auth_plugin = bytearray()
        while True:
            char = stream.read(1)
            if char == b'\x00' or not char:
                break
            auth_plugin += char

        return {
            'length': length,
            'sequence_id': sequence_id,
            'protocol_version': protocol_version,
            'server_version': server_version.decode(),
            'thread_id': thread_id,
            'scramble': (scramble_part1 + scramble_part2[:-1]).hex(),
            'capabilities': f'{capabilities:08x}',
            'charset': charset,
            'status_flags': f'{status_flags:04x}',
            'auth_plugin': auth_plugin.decode(),
            'raw_data': data.hex()
        }
    except Exception as err:
        print(f"{__name__} :: Parsing failure - {err}")
        return None


def parse_and_print(handshake) -> None:
    result = _parse_mysql_handshake(handshake)
    if result:
        for k, v in result.items():
            print(f"{k:>16}: {v}")
