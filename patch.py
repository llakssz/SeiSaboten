if __name__ != '__main__':
    from __main__ import my_file

import re

# table_start = 0xD434DC - 0x8

# a list of current offset values inside the master table
# we later search to see what points to these values in rom
offset_list = []
# areas in rom that point to the above values
# we then change to point to the new updated location in rom
offset_addresses_list = []

def get_direct_offsets_master_table(table_start):
    num_entries = int.from_bytes(my_file[table_start + 0x8:table_start + 0x4 + 0x8], byteorder='little')
    offset_start = table_start + 0x4 + 0x8
    for i in range(num_entries):
        start_offset_address = offset_start + (i * 0x4)
        offset_list.append(start_offset_address)

def find_offsets():
    for i, offset in enumerate(offset_list):
        # convert to rom address
        offset = offset + 0x08000000
        # convert number to bytes
        offset = offset.to_bytes(4, byteorder='little')
        # result = [f'{m.start():08X}' for m in re.finditer(re.escape(offset), my_file)]
        result = [m.start() for m in re.finditer(re.escape(offset), my_file)]
        offset_addresses_list.append(result)
    print(offset_addresses_list)

# combines above two functions
# a list of addresses that point to each table start
def get_master_table_pointers(master_table_start):
    num_entries = int.from_bytes(my_file[master_table_start + 0x8:master_table_start + 0xC], byteorder='little')
    offset_start = master_table_start + 0xC
    for i in range(num_entries):
        start_offset_address = offset_start + (i * 0x4)
        #convert to game space
        start_offset_address += 0x08000000
        # convert to bytes
        start_offset_address = start_offset_address.to_bytes(4, byteorder='little')
        # search for the offset in rom
        result = [m.start() for m in re.finditer(re.escape(start_offset_address), my_file)]
        offset_addresses_list.append(result)





# write new data to the end of the file
# for each address in my list,
#     write the new offset's address to the address
# done.

import locations

new_master_table_address = 0x1000000

def patch_offsets(master_table_offset, xyz):
    table_start = new_master_table_address
    offset_start = table_start + 0xC
    for i, addresses in enumerate(offset_addresses_list):
        # address that we want to point to
        start_offset_address = offset_start + (i * 0x4) + 0x08000000
        # if we have any addresses that need patching
        if addresses:
            for address in addresses:
                print(f'address to patch:{address:08X}, value to use:{start_offset_address:08X}')
                # address/value we want to patch
                my_file[address:address+0x4] = start_offset_address.to_bytes(4, byteorder='little')

    # patch two 4 byte values before the table, that we copied over
    # my_file[0x65D8:0x65D8+0x4] = (table_start + 0x08000000).to_bytes(4, byteorder='little')
    my_file[master_table_offset:master_table_offset+0x4] = (table_start + 0x08000000).to_bytes(4, byteorder='little')
    my_file[master_table_offset+0x4:master_table_offset+0x8] = (table_start + 0x6 + 0x08000000).to_bytes(4, byteorder='little')


# two methods to move the master table...
# 1 - how I'm doing it now, move the table data contents, the header (num of items and offsets) plus the 8 bytes at the very start
# remember, the 8 bytes at the start is where the table must actually start, because the first offset of 000000F0 shows that
# the first table is F0 away from when those two 4 bytes values begin.
# 2 - move only the table contents as in the data itself, but leave the header where is is.
# just adjust the offsets in the table header so that they point to the new location
# neater in the respect that I don't need to patch out about 50 values, addresses that directly point to table offset values for some reason.
# but it will be strange in the sense that the header is separate from the data... but probably won't cause a problem