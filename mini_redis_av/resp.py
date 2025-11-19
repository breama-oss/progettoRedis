# Supporto bulk strings, integer, simple strings, errors, nil
import typing

class RESPParser:
    def __init__(self):
        self.buffer = b""

    def feed(self, data: bytes):
        self.buffer += data
        commands = []

        while True:
            if not self.buffer:
                break
            if self.buffer[0:1] != b'*':
                # Not an array — incomplete or protocol mismatch
                break

            try:
                line, rest = self.buffer.split(b"\r\n", 1)
            except ValueError:
                break

            try:
                num_elems = int(line[1:])
            except ValueError:
                raise ValueError("Invalid array length in RESP")

            self.buffer = rest
            array = []

            for _ in range(num_elems):
                if len(self.buffer) < 1:
                    self.buffer = b""
                    break

                if self.buffer[0:1] != b'$':
                    raise ValueError("Expected bulk string ($) in RESP")

                try:
                    length_line, rest = self.buffer.split(b"\r\n", 1)
                except ValueError:
                    # incomplete
                    self.buffer = length_line + b"\r\n" + self.buffer[len(length_line)+2:]
                    break

                length = int(length_line[1:])
                self.buffer = rest

                if len(self.buffer) < length + 2:
                    # incomplete
                    # put back and wait
                    self.buffer = b"$" + str(length).encode() + b"\r\n" + self.buffer
                    break

                bulk = self.buffer[:length]
                array.append(bulk.decode('utf-8'))
                self.buffer = self.buffer[length+2:]  # skip data + \r\n

            if len(array) == num_elems:
                commands.append(array)
            else:
                break

        return commands


class RESPWriter:
    def encode_simple_string(self, s: str) -> bytes:
        return f"+{s}\r\n".encode()

    def encode_error(self, msg: str) -> bytes:
        return f"-ERR {msg}\r\n".encode()

    def encode_integer(self, n: int) -> bytes:
        return f":{n}\r\n".encode()

    def encode_bulk_string(self, s: typing.Optional[str]) -> bytes:
        if s is None:
            return b"$-1\r\n"
        encoded = s.encode('utf-8')
        return b"$" + str(len(encoded)).encode() + b"\r\n" + encoded + b"\r\n"

    def encode_array(self, arr: typing.List[typing.Union[str,int,None]]) -> bytes:
        parts = [b"*" + str(len(arr)).encode() + b"\r\n"]
        for el in arr:
            if isinstance(el, int):
                parts.append(self.encode_integer(el))
            else:
                parts.append(self.encode_bulk_string(None if el is None else str(el)))
        return b"".join(parts)

    def encode(self, value):
        # convenience: decide representation based on Python type
        if isinstance(value, bytes):
            return self.encode_bulk_string(value.decode('utf-8'))
        if isinstance(value, str):
            # treat as bulk string for commands like GET
            return self.encode_bulk_string(value)
        if isinstance(value, int):
            return self.encode_integer(value)
        if value is None:
            return self.encode_bulk_string(None)
        if isinstance(value, list):
            return self.encode_array(value)
        return self.encode_error("Invalid response type")
