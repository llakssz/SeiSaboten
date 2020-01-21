import sys
import random
import locations
import globals


class EnemyManager:
    enemy_count = 180

    enemy_names = []

    full_enemy_list = []
    main_enemy_list = []

    enemy_address = None
    monster_book_address = None

    # key is monster id, value is True/False, depending in monster book or not
    monster_in_book_dict = {}

    # have parameter to either load ALL 179/180 enemies, or, just the ones that are in the monster list?
    def __init__(self):
        self.enemy_address = int(locations.locations[globals.rom_region]['enemy_data'], base=16)

        monster_book_pointer = int(locations.locations[globals.rom_region]['monster_book_pointer'], base=16)
        self.monster_book_address = int.from_bytes(globals.my_file[monster_book_pointer:monster_book_pointer + 0x4],
                                                   byteorder='little') - 0x08000000

        self.get_monsters_in_book(self.monster_book_address)

        # 3rd table in master table contains the monster names
        self.enemy_names = globals.my_textman.all_entries_text_table(globals.my_textman.master_table_table_addresses[2])

        # load enemy data
        for i in range(self.enemy_count):
            temp_enemy = self.get_enemy(i)
            self.full_enemy_list.append(temp_enemy)

        # this is a shallow(?) copy, any changes to main will be reflected in full... good in a way
        # but if i shuffle main list, the order is full not changed
        # so I think I will need to make a real deep copy of this
        # or, just assign main list back to full... not a big problem i think
        self.main_enemy_list = self.full_enemy_list[1:123]

    def get_monsters_in_book(self, address):
        # hold list of monster ids that are in the book
        self.monster_in_book_dict = {}
        for i in range(self.enemy_count):
            self.monster_in_book_dict[i] = False

        # assume max of 180 monsters in book (or 180 minus 1?)
        # we just continue until we find 0xFFFF
        it = iter(globals.my_file[address:address + (0x02 * 180)])
        for x in it:
            y = next(it)
            char = (y << 8) | x
            if char == 0xFFFF:
                return True
            self.monster_in_book_dict[char] = True
        return False

    def write_monster_book(self, address):
        monster_bytes = bytearray()
        for i, monster in enumerate(self.full_enemy_list):
            if monster.in_book:
                b1, b2 = i.to_bytes(2, byteorder='little')
                monster_bytes.append(b1)
                monster_bytes.append(b2)
        monster_bytes.append(0xFF)
        monster_bytes.append(0xFF)
        monster_bytes.append(0xFF)
        monster_bytes.append(0xFF)
        globals.my_file[address:address + len(monster_bytes)] = monster_bytes

    def get_enemy(self, enemy_num):
        enemy_data = globals.my_file[
                     self.enemy_address + (enemy_num * 0x20):self.enemy_address + 0x20 + (enemy_num * 0x20)]
        return Enemy(enemy_data, self.enemy_names[enemy_num], self.monster_in_book_dict[enemy_num])

    def set_enemy(self, num, enemy):
        globals.my_file[self.enemy_address + (num * 0x20):self.enemy_address + 0x20 + (num * 0x20)] = enemy.bytes_

    # I am passing the enemy name into each enemy object, but when writing enemy back,
    # i don't do anything with the name that may have changed

    def shuffle_enemies_deep(self):
        random.shuffle(self.main_enemy_list)

    # shuffles sets of enemy names+ids+abilities+types+exp+money (not money yet!)
    # for example, lime slime could replace rabite, but keeping the rabite stats
    def shuffle_enemies_light(self):
        multi_list = [(e.name, e.id, e.type_, e.ability_prime, e.ability_sub) for e in self.main_enemy_list]
        shuffled_list = random.sample(multi_list, len(multi_list))
        for i, e in enumerate(self.main_enemy_list):
            e.name, e.id, e.type_, e.ability_prime, e.ability_sub = shuffled_list[i]

    # all these 3 functions are basically identical...
    def shuffle_stats_only(self):
        stat_list = [enemy.stats for enemy in self.main_enemy_list]
        # same as random.shuffle but not inplace
        shuffled_stat_list = random.sample(stat_list, len(stat_list))
        for i, enemy in enumerate(self.main_enemy_list):
            enemy.stats = shuffled_stat_list[i]

    def shuffle_magic_resistances_only(self):
        magic_res_list = [enemy.magic_res for enemy in self.main_enemy_list]
        shuffled_magic_res_list = random.sample(magic_res_list, len(magic_res_list))
        for i, enemy in enumerate(self.main_enemy_list):
            enemy.magic_res = shuffled_magic_res_list[i]

    def shuffle_weapon_resistances_only(self):
        weapon_res_list = [enemy.weapon_res for enemy in self.main_enemy_list]
        shuffled_weapon_res_list = random.sample(weapon_res_list, len(weapon_res_list))
        for i, enemy in enumerate(self.main_enemy_list):
            enemy.weapon_res = shuffled_weapon_res_list[i]

    # makes changes to the rom data
    def set_enemies(self):
        # write name table
        self.enemy_names = [enemy.name for enemy in self.full_enemy_list]
        # my_textman.recreate_enemy_name_table(remove_this_later, self.enemy_names)
        globals.my_textman.master_table_table_addresses[2] = self.enemy_names
        # write enemy data
        for i in range(self.enemy_count):
            self.set_enemy(i, self.full_enemy_list[i])


# class Stats:
#     hp = None
#     pow_ = None
#     def_ = None
#     int_ = None
#     mnd = None
#     agi = None
#     exp = None

# class WepResistances:
#     slash = None
#     bash = None
#     jab = None

# class MagResistances:
#     light = None
#     dark = None
#     moon = None
#     fire = None
#     water = None
#     wood = None
#     wind = None
#     earth = None

class Enemy:
    bytes_ = None
    original_bytes = None  # a backup so we can check if edited or not

    stats = None
    resistances = None

    def __init__(self, enemy_data, name, in_book):
        self.bytes_ = enemy_data
        self.original_bytes = enemy_data
        self.name = name
        self.in_book = in_book

    def bytes_as_string(self):
        string = ""
        for byte in self.bytes_:
            string += f'{byte:02X}' + ' '
        return string

    @property
    def id(self):
        # reved
        a = int.from_bytes(self.bytes_[0x0:0x0 + 0x2], byteorder='little')
        return ((a << 0x17) & 0xFFFFFFFF) >> 0x17

    @property
    def type_(self):
        # reved
        a = self.bytes_[0x1]
        return ((a << 0x1B) & 0xFFFFFFFF) >> 0x1C

    @property
    def ability_prime(self):
        # reved
        a = self.bytes_[0x1]
        return (a >> 5)

    @property
    def ability_sub(self):
        # reved
        a = self.bytes_[0x2]
        return ((a << 0x1D) & 0xFFFFFFFF) >> 0x1D

    @property
    def hp(self):
        # trouble
        a = self.bytes_[0x7]
        b = int.from_bytes(self.bytes_[0x8:0x8 + 0x2], byteorder='little')
        return (a >> 0x7) | ((b & 0x1FFF) << 1)

    @property
    def pow(self):
        # reved
        a = int.from_bytes(self.bytes_[0x8:0x8 + 0x4], byteorder='little')
        return ((a << 0xB) & 0xFFFFFFFF) >> 0x18

    @property
    def def_(self):
        # reved
        a = int.from_bytes(self.bytes_[0xA:0xA + 0x2], byteorder='little')
        return ((a << 0x13) & 0xFFFFFFFF) >> 0x18

    @property
    def int_(self):
        # trouble, but reved!
        a = self.bytes_[0xB]
        b = self.bytes_[0xC]
        return (a >> 0x5) | ((b & 0x1F) << 0x3)

    @property
    def mnd(self):
        # reved
        a = int.from_bytes(self.bytes_[0xC:0xC + 0x2], byteorder='little')
        return ((a << 0x13) & 0xFFFFFFFF) >> 0x18

    @property
    def agi(self):
        # reved
        a = int.from_bytes(self.bytes_[0xC:0xC + 0x4], byteorder='little')
        return ((a << 0xB) & 0xFFFFFFFF) >> 0x18

    @property
    def exp(self):
        # trouble
        a = self.bytes_[0x17]
        b = self.bytes_[0x18]
        return (a >> 0x4) | ((b & 0x3F) << 0x4)

    @property
    def slash(self):
        # reved
        a = self.bytes_[0x3]
        return ((a << 0x1B) & 0xFFFFFFFF) >> 0x1E

    @property
    def bash(self):
        # reved
        a = self.bytes_[0x3]
        return ((a << 0x19) & 0xFFFFFFFF) >> 0x1E

    @property
    def jab(self):
        # trouble
        a = self.bytes_[0x3]
        b = self.bytes_[0x4]
        return (a >> 0x7) | ((b & 0x1) << 0x1)

    @property
    def light(self):
        # reved
        a = self.bytes_[0xE]
        return ((a << 0x19) & 0xFFFFFFFF) >> 0x1E

    @property
    def dark(self):
        # reved
        a = int.from_bytes(self.bytes_[0xE:0xE + 0x2], byteorder='little')
        return ((a << 0x17) & 0xFFFFFFFF) >> 0x1E

    @property
    def moon(self):
        # reved
        a = self.bytes_[0xF]
        return ((a << 0x1D) & 0xFFFFFFFF) >> 0x1E

    @property
    def fire(self):
        # reved
        a = self.bytes_[0xF]
        return ((a << 0x1B) & 0xFFFFFFFF) >> 0x1E

    @property
    def water(self):
        # reved
        a = self.bytes_[0xF]
        return ((a << 0x19) & 0xFFFFFFFF) >> 0x1E

    @property
    def wood(self):
        # trouble   - still trouble..? i think i just forgot to mark as ok, but check!
        a = self.bytes_[0xF]
        b = self.bytes_[0x10]
        return (a >> 0x7) | ((b & 0x1) << 0x1)

    @property
    def wind(self):
        # reved
        a = self.bytes_[0x10]
        return ((a << 0x1D) & 0xFFFFFFFF) >> 0x1E

    @property
    def earth(self):
        # reved
        a = self.bytes_[0x10]
        return ((a << 0x1B) & 0xFFFFFFFF) >> 0x1E

    @property
    def unknown1(self):
        # reved
        # @080500AE
        a = int.from_bytes(self.bytes_[0x2:0x2 + 0x2], byteorder='little')
        return ((a << 0x15) & 0xFFFFFFFF) >> 0x18

    @property
    def unknown2(self):
        # reved
        # @08023C62
        a = self.bytes_[0x17]
        return ((a << 0x1C) & 0xFFFFFFFF) >> 0x1D

    @property
    def unknown3(self):
        # @0801Fe84
        a = int.from_bytes(self.bytes_[0x4:0x4 + 0x2], byteorder='little')
        return (a << 0x16) & 0xFFFFFFFF

    @property
    def unknown4(self):
        # @0801FEC0
        a = int.from_bytes(self.bytes_[0x4:0x4 + 0x4], byteorder='little')
        return (a << 0x0D) & 0xFFFFFFFF

    # is this speed? I changed to 6 and rabite and bebe seemed a bit slow...?
    # and when a high value, enemies were crazy, flickering back and forth.
    # although I'm not sure I'm setting/getting properly
    @property
    def q1(self):
        # @0805009A
        a = int.from_bytes(self.bytes_[0x16:0x16 + 0x2], byteorder='little')
        return ((a << 0x17) & 0xFFFFFFFF) >> 0x1C

    @property
    def lucre(self):
        # @080500BE
        a = int.from_bytes(self.bytes_[0x18:0x18 + 0x2], byteorder='little')
        return (a >> 0x6)

    @property
    def q3(self):
        # @080500CE
        a = int.from_bytes(self.bytes_[0x1A:0x1A + 0x2], byteorder='little')
        return ((a << 0x14) & 0xFFFFFFFF) >> 0x18

    @lucre.setter
    def lucre(self, value):
        a = int.from_bytes(self.bytes_[0x18:0x18 + 0x2], byteorder='little')
        a &= ~(self.lucre << 0x6)
        a |= (value << 0x6)
        self.bytes_[0x18:0x18 + 0x2] = a.to_bytes(2, byteorder='little')
        # max value is FFFF >> 6 = 3FF = 1023

    @q1.setter
    def q1(self, value):
        a = int.from_bytes(self.bytes_[0x16:0x16 + 0x2], byteorder='little')
        a &= ~(self.q1 << 0x1C) >> 0x17
        a |= (value << 0x1C) >> 0x17
        self.bytes_[0x16:0x16 + 0x2] = a.to_bytes(2, byteorder='little')

    # i am clearing for AGI but not for INT, why? are both working perfectly?

    @id.setter
    def id(self, value):
        a = int.from_bytes(self.bytes_[0x0:0x0 + 0x2], byteorder='little')
        a &= ~(self.id << 0x17) >> 0x17
        a |= (value << 0x17) >> 0x17
        self.bytes_[0x0:0x0 + 0x2] = a.to_bytes(2, byteorder='little')

    @type_.setter
    def type_(self, value):
        a = self.bytes_[0x1]
        a &= ~(self.type_ << 0x1C) >> 0x1B
        a |= (value << 0x1C) >> 0x1B
        self.bytes_[0x1] = a

    @ability_prime.setter
    def ability_prime(self, value):
        a = self.bytes_[0x1]
        a &= ~(self.ability_prime << 0x5)
        a |= (value << 0x5)
        self.bytes_[0x1] = a

    @ability_sub.setter
    def ability_sub(self, value):
        a = self.bytes_[0x2]
        a &= ~(self.ability_sub << 0x1D) >> 0x1D
        a |= (value << 0x1D) >> 0x1D
        self.bytes_[0x2] = a

    @hp.setter
    def hp(self, value):
        a = self.bytes_[0x7]
        # clear 0x7, otherwise the first bit is kept is 1 if so
        a &= ~(self.hp << 0x7)
        b = int.from_bytes(self.bytes_[0x8:0x8 + 0x2], byteorder='little')
        self.bytes_[0x7] = ((a & 0x1FFF) | (value << 0x7)) & 0xFF
        b = (b & 0xE000) | (value >> 0x1) & 0xFF
        self.bytes_[0x8:0x8 + 0x2] = b.to_bytes(2, byteorder='little')

    @pow.setter
    def pow(self, value):
        a = int.from_bytes(self.bytes_[0x8:0x8 + 0x4], byteorder='little')
        a &= ~(self.pow << 0x18) >> 0xB
        a |= (value << 0x18) >> 0xB
        self.bytes_[0x8:0x8 + 0x4] = a.to_bytes(4, byteorder='little')

    @def_.setter
    def def_(self, value):
        a = int.from_bytes(self.bytes_[0xA:0xA + 0x2], byteorder='little')
        a &= ~(self.def_ << 0x18) >> 0x13
        a |= (value << 0x18) >> 0x13
        self.bytes_[0xA:0xA + 0x2] = a.to_bytes(2, byteorder='little')

    @int_.setter
    def int_(self, value):
        self.bytes_[0xB] = ((self.bytes_[0xB] & 0x1F) | (value << 0x5)) & 0xFF
        self.bytes_[0xC] = (self.bytes_[0xC] & 0xE0) | (value >> 0x3)

    @mnd.setter
    def mnd(self, value):
        a = int.from_bytes(self.bytes_[0xC:0xC + 0x2], byteorder='little')
        a &= ~(self.mnd << 0x18) >> 0x13
        a |= (value << 0x18) >> 0x13
        self.bytes_[0xC:0xC + 0x2] = a.to_bytes(2, byteorder='little')

    @agi.setter
    def agi(self, value):
        a = int.from_bytes(self.bytes_[0xC:0xC + 0x4], byteorder='little')
        a &= ~(self.agi << 0x18) >> 0xB
        a |= (value << 0x18) >> 0xB
        self.bytes_[0xC:0xC + 0x4] = a.to_bytes(4, byteorder='little')

    @exp.setter
    def exp(self, value):
        # i need to clear the value/bits first... because for rabite, exp is 1.
        # so when setting exp to 150, the first bit is already set, and makes it 151
        self.bytes_[0x17] &= ~(self.exp << 0x4)
        # do I need to clear for 0x18 too? 
        self.bytes_[0x17] = ((self.bytes_[0x17] & 0x3F) | (value << 0x4)) & 0xFF
        self.bytes_[0x18] = (self.bytes_[0x18] & 0xC0) | (value >> 0x4) & 0xFF

    @slash.setter
    def slash(self, value):
        a = self.bytes_[0x3]
        a &= ~(self.slash << 0x1E) >> 0x1B
        a |= (value << 0x1E) >> 0x1B
        self.bytes_[0x3] = a

    @bash.setter
    def bash(self, value):
        a = self.bytes_[0x3]
        a &= ~(self.bash << 0x1E) >> 0x19
        a |= (value << 0x1E) >> 0x19
        self.bytes_[0x3] = a

    @jab.setter
    def jab(self, value):
        if (value >> 0) & 1:
            self.bytes_[0x3] |= (1 << 0x7)
        else:
            self.bytes_[0x3] &= ~(1 << 0x7)
        if (value >> 1) & 1:
            self.bytes_[0x4] |= 1
        else:
            self.bytes_[0x4] &= ~1

    @light.setter
    def light(self, value):
        self.bytes_[0xE] &= ~(self.light << 0x1E) >> 0x19
        self.bytes_[0xE] |= (value << 0x1E) >> 0x19

    @dark.setter
    def dark(self, value):
        a = int.from_bytes(self.bytes_[0xE:0xE + 0x2], byteorder='little')
        a &= ~(self.dark << 0x1E) >> 0x17
        a |= (value << 0x1E) >> 0x17
        self.bytes_[0xE:0xE + 0x2] = a.to_bytes(2, byteorder='little')

    @moon.setter
    def moon(self, value):
        self.bytes_[0xF] &= ~(self.moon << 0x1E) >> 0x1D
        self.bytes_[0xF] |= (value << 0x1E) >> 0x1D

    @fire.setter
    def fire(self, value):
        self.bytes_[0xF] &= ~(self.fire << 0x1E) >> 0x1B
        self.bytes_[0xF] |= (value << 0x1E) >> 0x1B

    @water.setter
    def water(self, value):
        self.bytes_[0xF] &= ~(self.water << 0x1E) >> 0x19
        self.bytes_[0xF] |= (value << 0x1E) >> 0x19

    @wood.setter
    def wood(self, value):
        if (value >> 0) & 1:
            self.bytes_[0xF] |= (1 << 0x7)
        else:
            self.bytes_[0xF] &= ~(1 << 0x7)
        if (value >> 1) & 1:
            self.bytes_[0x10] |= 1
        else:
            self.bytes_[0x10] &= ~1

    @wind.setter
    def wind(self, value):
        self.bytes_[0x10] &= ~(self.wind << 0x1E) >> 0x1D
        self.bytes_[0x10] |= (value << 0x1E) >> 0x1D

    @earth.setter
    def earth(self, value):
        self.bytes_[0x10] &= ~(self.earth << 0x1E) >> 0x1B
        self.bytes_[0x10] |= (value << 0x1E) >> 0x1B
