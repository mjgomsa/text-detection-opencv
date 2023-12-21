
# Using OSC (Open Sound Control) send info in and out of Sonic Pi via the network

# By default when Sonic Pi is launched it listens to port 4560 for incoming OSC messages from programs on the same computer.

from pythonosc import udp_client

# Replace with your Sonic Pi IP and port
# '149.31.203.106', 4560
# '127.0.0.1', 4559
# sender = udp_client.SimpleUDPClient('0.0.0.0', 4560)
sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)


def send_sonic_pi_code(sonic_pi_code):
    sender.send_message('/run-code', [sonic_pi_code])
