"""Control home bridge hue lighting
"""
from phue import Bridge

bridge = Bridge('192.168.1.213')
bridge.connect()
bridge.get_api()

if __name__ == '__main__':
    # pp(bridge.get_group())
    if bridge.get_group(3, 'on'):
        bridge.set_group(3, 'on', False)
        exit()
    bridge.set_group(3, 'on', True)
