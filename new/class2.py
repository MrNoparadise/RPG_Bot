
def calc_checksum(data):
    def add(cs, ch):
        cs += ord(ch);
        if cs > 0xff:
            cs &= 0xff
            return cs + 1
        return cs
    return ~reduce(add,data,0) & 0xff

assert '%02X' % calc_checksum('\x02') == 'FD'
assert '%02X' % calc_checksum('\x02\x43') == 'BA'
