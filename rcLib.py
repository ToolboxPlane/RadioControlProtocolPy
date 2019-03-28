import math


class Package:
    __START_BYTE = 0xC9
    __END_BYTE = 0x93
    __globalPackageUid = 0
    transmitter_id = 0
    __error_count = 0
    __resolution_steps_to_key = {
        32: 0b000,
        64: 0b001,
        128: 0b010,
        256: 0b011,
        512: 0b100,
        1024: 0b101,
        2048: 0b110,
        4096: 0b111
    }
    __channel_count_to_key = {
        0: 0b000,
        1: 0b000,
        2: 0b001,
        4: 0b010,
        8: 0b011,
        16: 0b100,
        32: 0b101,
        64: 0b110,
        256: 0b111
    }

    __key_to_resolution_steps = {
        0b000: 32,
        0b001: 64,
        0b010: 128,
        0b011: 256,
        0b100: 512,
        0b101: 1024,
        0b110: 2048,
        0b111: 4096
    }
    __key_to_channel_count = {
        0b000: 1,
        0b001: 2,
        0b010: 4,
        0b011: 8,
        0b100: 16,
        0b101: 32,
        0b110: 64,
        0b111: 256
    }

    def __init__(self, resolution, channel_count):
        self.resolution = resolution
        self.channel_count = channel_count
        self.mesh = False
        self.discover_state = 0
        self.tid = Package.transmitter_id
        self.routing_len = 1
        self.channel_data = []
        self.__receive_state = 0
        self.__data_byte_count = 0
        self.uid = 0
        self.checksum = 0
        self.buf = bytearray()

    def encode(self):
        res_bits = math.log2(self.resolution)
        data_size = math.ceil((res_bits * self.channel_count) / 8)
        package_len = data_size + 5
        if self.mesh:
            package_len += 1

        buf = bytearray(package_len)

        buf[0] = Package.__START_BYTE
        Package.__globalPackageUid += 1
        buf[1] = Package.__globalPackageUid
        buf[2] = self.tid
        buf[3] = Package.__resolution_steps_to_key[self.resolution] | \
                 Package.__channel_count_to_key[self.channel_count] << 3 | \
                 (1 if Package.__error_count > 0 else 0) << 6 | \
                 self.mesh << 7
        offset = 4

        if self.mesh:
            offset += 1
            buf[offset] = self.routing_len | (1 if self.discover_state == 1 else 0) << 5 | \
                          (1 if self.discover_state == 2 else 0) << 6

        for c in range(0, data_size):
            buf[offset + c] = 0
            for b in range(0, min(8, res_bits * self.channel_count - c * 8)):
                bit = self.channel_data[int((c * 8 + b) / res_bits)] & (0b1 << int((c * 8 + b) % res_bits))
                bit = bit != 0
                buf[offset + c] |= bit << b

        buf[offset + data_size] = Package.__calculate_checksum(buf)
        buf[offset + data_size + 1] = Package.__END_BYTE

        return buf

    def decode(self, data):
        if self.__receive_state == 0:  # Start byte
            if data == Package.__START_BYTE:
                self.__receive_state = 1
                self.buf = bytearray()
                self.__data_byte_count = 0
        elif self.__receive_state == 1:  # UID
            self.uid = data
            Package.__globalPackageUid = data
            self.__receive_state = 2
        elif self.__receive_state == 2:  # TID
            self.tid = data
            self.__receive_state = 3
        elif self.__receive_state == 3:  # Configuration
            self.resolution = Package.__key_to_resolution_steps[data & 0b111]
            self.channel_count = Package.__key_to_channel_count[(data & 0b111000) >> 3]
            self.channel_data = [0] * self.channel_count

            self.__receive_state = 4 if data & (1 << 7) else 5
        elif self.__receive_state == 4:  # Mesh
            self.routing_len = data & 0b1111
            self.discover_state = (data >> 5) & 0b11
            self.mesh = self.routing_len > 0
            self.__receive_state = 6 if self.discover_state == 1 else 5
        elif self.__receive_state == 5:  # Data
            res_bits = math.log2(self.resolution)
            data_size = math.ceil((res_bits * self.channel_count)/8)
            for c in range(0, 8):
                bit = int((self.__data_byte_count * 8 + c) % res_bits)
                self.channel_data[int((self.__data_byte_count * 8 + c) / res_bits)] |= ((data >> c) & 1) << bit

            self.__data_byte_count += 1
            if self.__data_byte_count >= data_size:
                self.__receive_state = 6
        elif self.__receive_state == 6:  # Checksum
            self.checksum = data
            self.__receive_state = 7
            if Package.__calculate_checksum(self.buf) != self.checksum:
                Package.__error_count += 4
            else:
                Package.__error_count -= 1
        elif self.__receive_state == 7:  # End byte
            self.__receive_state = 0
            if data == Package.__END_BYTE:
                Package.__error_count -= 1
                return True
            else:
                Package.__error_count += 4
        else:
            self.__receive_state = 0

        self.buf.append(data)
        return False

    @staticmethod
    def __calculate_checksum(buf):
        checksum = 0
        for c in range(1, len(buf)):
            checksum ^= buf[c]

        return checksum
