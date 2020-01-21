# coding=utf8

import sys
import itertools
import json

if __name__ != '__main__':
    pass
    # from __main__ import my_file, rom_region
    # import thegui
import locations
import globals

class TextManager:
    en_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ()[]abcdefghijklmnopqrstuvwxyz「」『』0123456789,.·"-:…⋯!? /~<>À♪★+&'
    jp_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ()[]abcdefghijklmnopqrstuvwxyz「」『』0123456789、。·"-:⋯‥!?ー/~<>♥️♪★+&'
    kanji_list = '哀愛悪握扱安暗宷闇以囲意異?遦域育一印員因引飲隠右?噂運雲影映栄英衛越延炎遠汚奥応押王屋憶桶乙俺穏恩音下化仮何価加可嫁家?果歌河火花過我画餓会解回壊怪悔改?海界開階外鎧??覚革学楽掛割活滑噛乾喚感慣換敢棺看管簡観間関館頑顔?企危喜器奇寄希揮機帰気祈記貫起輝飢騎鬼偽?技犠疑義議客逆仇休及吸宮急救求泣究給去居拠許供共協叫強恐教況狂興郷鏡?仰?琴禁近金吟苦駆具愚喰空屈掘窟君軍係刑兄形恵提?計?激決結血月件健剣???犬肩見賢険元原幻減現言個古呼孤故枯湖誇五互後御悟語誤護?光公?ロ向坑好幸広控攻構皇紅考行鉱高号合拷刻国酷黒獄骨込頃今婚根魂左差砂鎖座催最妻才歳?砕祭在材罪作策殺雑?三参山散産斬残仕使士姉姿子志思指支止死私紙視詩試資飼事似侍慈持時次治耳自識執失室質実射捨?者車蛇邪借?若弱主取守手狩酒受呪寿樹周修終習??集?住十獣垂宿出瞬準純順処初所緒?助女除傷勝召商小少床招沼消焼照硝章笑証詳障上丈乗冗城場嬢常情?状色食信侵寝心?新森深申真神臣親身進震人尋吹水衰数世制勢征性成政整晴正牲生盛精聖声西誓請静席惜昔石責?切接説絶先占戦洗染線船選前然全狙祖組阻双想早巣争相窓聡草装走送騒像増憎造側即息束足賊族続存尊村他多堕打駄体対待態替?袋貸退代台大題滝択託逹?脱竪誰単探短端鍛壇断段男談値知地置遅築茶?中仲注張彫朝町調長鳥直沈追痛通停定帝底庭弟締艇敵的溺鉄天展転伝殿吐徒渡登賭途度土?怒倒塔投東盗当等答統討踏逃頭闘動同堂導洞道得特毒独読内謎難二日乳入任認熱年念燃悩?能派破廃敗杯背配売伯泊白迫?肌発抜判反飯番否妃彼悲秘非飛備眉美必姫百氷評病品不付夫怖敷浮父腐負武舞部封風伏復服福腹沸仏物分文聞兵平閉別変片返捕歩補??母報抱放方法砲褒飽亡忘暴望冒北?本魔妹毎末万満味未魅密脈民眠務夢無霧娘冥名命明迷鳴?面盲木目戻貰問紋門治夜野役約薬訳躍油優勇友幽有由誘遊雄予余与幼妖容様用集要欲来頼落乱覧利理離陸立流竜旅了両料良?カ涙令冷礼隷霊裂恋練蓮連路浪牢老和話惑腕掟絆盾移防降灼煙雫剛黄球虫肉匕効系?類亜植昆嗅聴昼設帳標南岸司業完週扉裏捜星曜買辺図符種綿絹布甲象牙銅鋼鉛銀魚隕晶赤廊?丘半避儖倉庫橋岩潜景突板歴史衆刈勉詠唱喚耐?罰再保鍵碑録?冊棚矛称匹+.,…’濃雨雪菜響触限↑←↓→菓易荒検爆介?功日謝術誕宴収字建汝?荷払便製弓叩帽々経験操低青髪敬脅速慎更期踊排繰点島写基礎隊困縁絡久労妨示軌園表威秒副倍泡包複費柱尾弾届距杭崖率谷店貨浴夏校雷巨崩衝詮始隣己氏郎眼契比級趣胃預宝券訪超混軽俳徊努汗犯恥富?淪局珍罠清楚胸懐候詰刀拒混沌留監芸唄辛例紹刃圏些細恨歯描弁巻妙都迎焦察削膝諦永却謀覗条酔?領黙厳拾固吉蝕?漂普告陽圧剰枢胆蜂粉往際尽暖針俗訴枚酬額卒働昨第提依従塞害徴源矢枕市劇批拘拝?句棒稼挙雇欠甘桁災式殊?悴横穴米粗太宅鉢承譲寂凍?戒潮劫某継怨畜幹丸略凶紛党華肖祝微羽玉首炉師位測?隅卵折壁快績縛呂煮?疎?偏絵亀糸四浅枝疲泉津授炉忠境裕首担損箱劣培善歓墜堵瞳透薄卑?程丁皮腰臆遇隙群創千揺叶粋寒偉淵鱗宮没採棲'
    hirgana_small_a_game = 0x005b
    katakana_small_a_game = 0x00ab
    hiragana_string = ''
    katakana_string = ''
    hiragana_small_a_unicode = 0x3041
    katakana_small_a_unicode = 0x30A1

    # holds address in ROM of each table in master table
    master_table_table_addresses = []
    # will hold lists of the tables contents
    master_table_list = []

    # will hold dicts of story dialog
    story_table_list = []

    char_dict = {}
    inv_char_dict = {}

    charmap_start_u = 0xE7BB62
    charmap_length_u = 0xD6 # but there are 90, 5A letters in the char string...?
    # length is d6, ends in 0019

    charmap_length = 0xD6
    # really d6 for both usa and japan????????

    story_table_address = None

    def __init__(self):


        story_table_offset = int(locations.locations[globals.rom_region]['story_text_location'], base=16)
        self.story_table_address = int.from_bytes(globals.my_file[story_table_offset:story_table_offset + 0x4],
                                             byteorder='little') - 0x08000000

        # do Japanese first, because some kanji overwrite some english chars.
        # so, let the kanji get overwritten. only a few, but usa game does contain (placeholder) Japanese chars
        # build list containing hiragana and katakana
        for x in range(83):
            this_char = self.hiragana_small_a_unicode + x
            self.hiragana_string += chr(this_char)
        for x in range(84):
            this_char = self.katakana_small_a_unicode + x
            self.katakana_string += chr(this_char)
        # remove non-existant kana
        self.hiragana_string = self.hiragana_string.replace('ゐ', '')
        self.hiragana_string = self.hiragana_string.replace('ゑ', '')
        self.hiragana_string = self.hiragana_string.replace('ゎ', '')
        self.katakana_string = self.katakana_string.replace('ヰ', '')
        self.katakana_string = self.katakana_string.replace('ヱ', '')
        self.katakana_string = self.katakana_string.replace('ヮ', '')
        # put kana in char_dict
        for x, char in enumerate(self.hiragana_string):
            self.char_dict[self.hirgana_small_a_game + x] = char
        for x, char in enumerate(self.katakana_string):
            self.char_dict[self.katakana_small_a_game + x] = char
        # iterate through all kanji and put in char_dict
        for i, kanji in enumerate(self.kanji_list):
            # 0x010C is the value of the first kanji in game
            self.char_dict[i + 0x010C] = kanji


        # build char map from rom, from the text entry screen
        charmap_start = int(locations.locations[globals.rom_region]['charmap_start'], base=16)
        it = iter(globals.my_file[charmap_start:charmap_start+self.charmap_length])
        position = 0
        for x in it:
            y = next(it)
            # this combines to hex values, like 0xFF 0x66 into 0xFF66
            char = (x << 8) | y
            if char != 0xFFFF:
                if globals.rom_region == 'J':
                    self.char_dict[char] = self.jp_chars[position]
                elif globals.rom_region == 'E':
                    self.char_dict[char] = self.en_chars[position]
                position += 1

        # manually add some that weren't in the text entry screen
        # fatter japanese ones i guess, some dupes?
        self.char_dict[0x04a1] = '.'
        self.char_dict[0x04a2] = ','
        self.char_dict[0x04a4] = "’"
        self.char_dict[0x11ff] = '\n'
        self.char_dict[0x0093] = "'"
        self.char_dict[0x0095] = ';'
        # opening, and closing quote
        self.char_dict[0x009d] = '“'
        self.char_dict[0x000d] = '”'
        # self.char_dict[0x009d] = '"'
        # self.char_dict[0x000d] = '"'
        self.char_dict[0x0000] = ' '
        self.char_dict[0x0008] = 'ー'

        # make an inverse of the dict so that we can map characters back to their byte representation
        # if there are duplicates (there are), i guess the last key's assigned value is is used...
        self.inv_char_dict = {v: k for k, v in self.char_dict.items()}

        # read text from game
        self.story_table_list = self.read_story_table(self.story_table_address)
        self.read_master_table()


    # function to get a single string from a text table
    def get_element_text_table(self, table_start, item_num):
        # table_start is where the number of items in the table is located
        offset_start = table_start + 0x4
        start_offset_address = offset_start + (item_num*0x2)
        end_offset_address = start_offset_address + 0x2
        
        start_offset = int.from_bytes(globals.my_file[start_offset_address:start_offset_address+0x2], byteorder='little')
        end_offset = int.from_bytes(globals.my_file[end_offset_address:end_offset_address+0x2], byteorder='little')
        
        start_text_address = table_start + start_offset
        end_text_address = table_start + end_offset

        string = ""
        it = iter(globals.my_file[start_text_address:end_text_address])
        for a in it:
            b = next(it)
            char = (a << 8) | b
            letter = self.char_dict.get(char, None)
            if letter is not None:
                string += letter
            else:
                print('*******************  missing: ' + hex(char))
        return string

    # return all a list of all text entries in table
    def all_entries_text_table(self, table_start):
        num_entries = int.from_bytes(globals.my_file[table_start:table_start+0x4], byteorder='little')
        text_list = []
        for i in range(num_entries):
            temp_string = self.get_element_text_table(table_start, i)
            text_list.append(temp_string)
        return text_list

    def get_end_of_table(self, table_start):
        num_entries = int.from_bytes(globals.my_file[table_start:table_start+0x4], byteorder='little')
        offset_start = table_start + 0x4
        start_offset_address = offset_start + ((num_entries - 1) * 0x2)
        end_offset_address = start_offset_address + 0x2
        end_offset = int.from_bytes(globals.my_file[end_offset_address:end_offset_address + 0x2], byteorder='little')
        end_text_address = table_start + end_offset
        return end_text_address

    def recreate_enemy_name_table(self, table_start, name_list):
        # entry_count = len(name_list) + 1
        entry_count = len(name_list)
        if globals.my_file[table_start] != entry_count:
            print('Writing a different amount of entries, quitting')
            print(globals.my_file[table_start])
            print(entry_count)

        # table start is the number of entries in the text table, starts at 1, so I plus 1 to get the 'number'
        # 4 bytes after, the offsets for each entry is stored. each offset has 2 bytes
        # we know how long the offset block is, because it is 2 bytes * number of entries
        # by default, use the entry count, or, overwrite with custom one if specified via parameter
        offset_start = table_start + 0x4
        text_start = table_start + 0x4 + (entry_count * 0x2)

        text_start_byte_address = text_start
        text_end_byte_address = text_start
        
        for i, name in enumerate(name_list):
            name_bytes = bytearray()
            for char in name:
                char_bytes = self.inv_char_dict[char].to_bytes(2, byteorder='little')
                for byte in char_bytes:
                    name_bytes.append(byte)
            # assign name_bytes to rom at address text_start + current_text_address
            text_start_byte_address = text_end_byte_address
            text_end_byte_address += len(name_bytes)
            current_offset_address = offset_start + ((i+1)*0x2)
            current_offset_value = (text_end_byte_address-table_start).to_bytes(2, byteorder='little')
            globals.my_file[text_start_byte_address:text_end_byte_address] = name_bytes
            globals.my_file[current_offset_address:current_offset_address+0x2] = current_offset_value

    def decode_string(self, string_bytes):
        string = ""
        it = iter(string_bytes)
        for a in it:
            if a == 0x80: # single byte for newline
                string += '\n'
            elif a == 0x82: # single byte to wait until keypress
                string += '{A}'
            elif a == 0x83: # beginning of a choice
                string += '{CHOICE}'
            elif a == 0x84: # end of choices
                string += '{END_CHOICES}'
            elif a == 0x8E: # red color
                string += '{RED}'
            elif a == 0x8D: # ends color?? not 100%
                string += '{END_COLOR}'
            elif (a == 0x8B) or (a == 0x99):
                c1 = next(it)
                c2 = next(it)
                actor_id = (c1 << 8) | c1
                if a == 0x8B:
                    string += f'POS_L ACTOR_{actor_id:04X}\n'
                else:
                    string += f'POS_R ACTOR_{actor_id:04X}\n'
            else:
                try:
                    b = next(it)
                    char = (a << 8) | b

                    if a == 0x86:
                        actor = ''
                        if b == 0:
                            actor = '{HERO}'
                        elif b == 1:
                            actor = '{HEROINE}'

                        if actor:
                            string += actor
                        else:
                            string += f'ACTOR{b}'
                        continue
                    
                    
                    letter = self.char_dict.get(char, None)
                    if letter is not None:
                        string += letter
                    else:
                        pass
                        # print('*******************  missing: ' + hex(char))
                        # sys.exit(0)
                except Exception as e:
                    return "error"
        return string

    def get_dialog_entries_count(self, table_start):
        return int.from_bytes(globals.my_file[table_start+0x2:table_start+0x4], byteorder='little')

    def read_story_table(self, table_start):
        num_entries = int.from_bytes(globals.my_file[table_start+0x2:table_start+0x4], byteorder='little')
        # one more offset than sentences because there's an end offset for final sentence
        num_offsets = num_entries + 1
        offsets_block = globals.my_file[table_start+0x4:table_start+0x4+(0x2*num_offsets)]
        # build list of text offset values
        offset_list = []
        # times that offset value had overflowed 2 bytes and had to start again from 0
        overflow_count = 0
        # holds previous value, to compare if bigger (overflowed)
        prev_value = 0
        it = iter(offsets_block)
        for i, a in enumerate(it):
            b = next(it)
            value = (b << 8) | a
            if prev_value > value:
                overflow_count += 1
            prev_value = value
            value += (0x10000*overflow_count)
            value += table_start
            offset_list.append(value)

        # offsets are like s1_start, s1_end/s2_start, s2_end/s3_start, ...
        # make a list of (s1_start, s1_end/s2_start), (s1_end/s2_start, s2_end/s3_start) ...
        a, b = itertools.tee(offset_list)
        next(b, None)
        address_list = list(zip(a, b))

        story_list = []
        for i, sentences_address in enumerate(address_list):
            temp_dict = {}
            temp_dict['id'] = i
            temp_dict['start'] = sentences_address[0]
            temp_dict['end'] = sentences_address[1]
            temp_dict['actor'] = {}
            temp_dict['string'] = ''
            
            first_byte = globals.my_file[temp_dict['start']]
            # check if actor sprite is shown
            # if so, keep these first 3 bytes
            # i need to fix for the 1st sentence, because we manually look 1/2/3 ahead for the actor
            # but doing this on the 1st (0th) sentence looks into the next sentence's data
            if len(globals.my_file[sentences_address[0]:sentences_address[1]]):
                if first_byte == 0x8B or first_byte == 0x99:
                    if first_byte == 0x8B:
                        temp_dict['actor']['position'] = 'Left'
                    else:
                        temp_dict['actor']['position'] = 'Right'
                    temp_dict['actor']['id'] = int.from_bytes(globals.my_file[temp_dict['start']+0x1:temp_dict['start']+0x3], byteorder='little')
                    temp_dict['string'] = self.decode_string(globals.my_file[sentences_address[0]+0x3:sentences_address[1]])
                else:
                    temp_dict['string'] = self.decode_string(globals.my_file[sentences_address[0]:sentences_address[1]])
            else:
                temp_dict['string'] = '{BLANK}'
            story_list.append(temp_dict)
        return story_list
        # when rebuilding header, just to with other tables, but subtract 0x10000 whilst over 0xFFFF

    def read_master_table(self):
        master_table_offset = int(locations.locations[globals.rom_region]['real_master_table_location'], base=16)
        master_table_start_address = int.from_bytes(globals.my_file[master_table_offset:master_table_offset + 0x4],
                                                    byteorder='little') - 0x08000000
        # make a function for the above thing. with a parameter to return a rom address or not (-0x08000000 or not)
        # print(f'{master_table_start_address:08X}')

        # read_master_table(master_table_start_address)

        table_start = master_table_start_address
    # def read_master_table(self, table_start):
        num_entries = int.from_bytes(globals.my_file[table_start + 0x8:table_start + 0x4 + 0x8], byteorder='little')
        offset_start = table_start + 0x4 + 0x8
        table_address_list = []
        for i in range(num_entries):
            start_offset_address = offset_start + (i * 0x4)
            end_offset_address = start_offset_address + 0x4

            # print(f'{i}-08{start_offset_address:06X}
            b_str = f'08{start_offset_address:06X}'
            rev_str = b_str[6:8] + b_str[4:6] + b_str[2:4] + b_str[0:2]
            # print(f'{i}-{b_str}-{rev_str}')

            start_offset = int.from_bytes(globals.my_file[start_offset_address:start_offset_address + 0x4], byteorder='little')
            # end_offset = int.from_bytes(my_file[end_offset_address:end_offset_address + 0x4], byteorder='little')

            table_start_address = table_start + start_offset
            # table_end_address = table_start + end_offset - 8
            # print(f'ID:{i:02X}-{i} @ 0x{table_start_address:08X}:0x{table_end_address:08X}')
            # should change from a dict to a list since we are only keeping start
            # self.master_table_table_addresses.append({
            #     'start': table_start_address
            # })
            self.master_table_table_addresses.append(table_start_address)

        # last_end_address = self.get_end_of_table(self.master_table_table_addresses[-1]['start'])
        last_end_address = self.get_end_of_table(self.master_table_table_addresses[-1])
        orig_master_table_length = last_end_address - master_table_start_address


        for i, table_address in enumerate(self.master_table_table_addresses):
            if i == 43 or i == 47:
                self.master_table_list.append(['Unavailable for editing'])
            else:
                self.master_table_list.append(self.all_entries_text_table(table_address))

