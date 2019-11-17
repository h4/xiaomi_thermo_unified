from xiaomi_thermo_unified import XiaomiThermo

addresses = ('58:2D:34:10:4E:86', '4C:65:A8:DC:0D:AF', '3F:59:C8:80:70:BE', )

for a in addresses:
    c = XiaomiThermo(a)
    print(c.device_name)
    print(c.temperature, c.humidity)
    print('---')
