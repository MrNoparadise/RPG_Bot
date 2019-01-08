import os

class Params:
    host = 'localhost'
    port = 5001

    autotest = 3     # minutes
    pmax_count = 128
    serial_range = (0x500000, 0x503000)
    # If printing interval is 0, don't print periodical statistics
    time_window = 10

    eprom_file = os.path.join( os.path.dirname(__file__), "eprom0" )
    eprom_version = 0x0406  # 4.6

    # Count of sessions to run: 0 -> infinity
    session_count = 0
