import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import re
import random
import zlib

### fix to load pyqt5
import os
import PyQt5

import locations
import globals
import textman
import enemyman

__version__ = '0.6'

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

qt_creator_file = "gui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)

# https://stackoverflow.com/questions/52293422/pyqt4-setwindowicon-from-base64
def iconFromBase64(base64):
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

window_icon = b'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAACXBIWXMAAA7DAAAOwwHHb6hkAAAC4UlEQVR4nO3cIZOjQBCGYe7qfkAkMhKJRK5ERiKRKyNXIiORkUhkJHJlZCQSGZl/sGevP66Ym4Ns3229j+saEsh2TQ/MDJskAAAAAAAAAAAAAICv6lvogMPL7uPXuCxS0z5c7ya+vD+C3xkjdH7lfT2x5/++1YXh75AAZyTAWfQY0A/N4vFVadtDNTBUU+t6H7rERV03mTi2Rj/799MDnJEAZyTAWXAM6PLK1MCX4820p8V+8fPV63WxfVbzm9fQJa3SNWcT65ig+nOx2H6/TiZ+b3MT17eeMeBfRgKckQBnP2I/kA6Vift2NPF1mkzctrbGz8aMfRl7CavoGFNPg4m1ph+Lh4mL/d7EVWb/HkkyJjHoAc5IgDMS4Cx6DEiqNxuOUvP6kwlPx8nEb62N0330FWxKa/7puDPxrObL70+yzMZNHXV+eoAzEuCMBDiLXi/VuaGq6ewBMgb0MkZU1+W5FW99YeeuKq3xMgb0UvNDcz+KHuCMBDgjAc5W75nRMeGys3MrbS1zQdVz5/vXuvd2veDY2fWCw8POXcXWfEUPcEYCnJEAZ5vum0yS+H00Stds24ttv92Wx5A8lxp+sO2xa86x+3xi0QOckQBnJMBZ/HqA0Jqv9/2x5jX/JkeckyV6fJ7LPp0m8nrmv8c+96wcE+gBzkiAMxLgbPUYoAZZIq4jP6/37VrDw88B9nj9vlj6e7ZGD3BGApyRAGer5zWyLDP3xbO5F33H65P3gkaTvaL6jpk+p4zjyHPA/4wEOCMBzlY/B2gNHK52bkjV9bDUPKN7N0P35aVs4wm9w6ZC7xWPI+sBXwoJcEYCnG0+F/Sb+fHFMUFrttZ4rcH9sPxeb1Xa+ftSvi/2fFuvASt6gDMS4IwEONt8DFBaQ8d7asaEIbU1N/Q/4ZJp3QS/7vUc7/Z8W9/nh9ADnJEAZyTA2afWuz+h6wtbWzt/vzV6gDMS4IwEAAAAAAAAAAAAPNlPAsTmOZ3S0B4AAAAASUVORK5CYII='

rom_info = {
    'AVSJ': {
        'region': 'J',
        'name': 'Japan',
        'clean_crc32': '31B220E5'  # this is the scene dump at least, need to dump my copy
    },
    'AVSE': {
        'region': 'E',
        'name': 'USA',
        'clean_crc32': '7F1EAC75'
    },
    'AVSP': {
        'region': 'P',
        'name': 'Europe - En',
        'clean_crc32': '88E64A8A'
    }
}

class MyHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, text):
        QtGui.QSyntaxHighlighter.__init__(self, text)

    def highlightBlock(self, text):

        good_bracket_format = QtGui.QTextCharFormat()
        good_bracket_format.setForeground(QtGui.QColor('white'))
        good_bracket_format.setBackground(QtGui.QColor('black'))

        regex_num = re.compile('{\w+}')
        match_iter = regex_num.finditer(text)
        for m in match_iter:
            self.setFormat(m.start(), m.end() - m.start(), good_bracket_format)

        # nned to check if same amount of { and }
        # if not, look further to see where the problem is
        # and highlight as incorrect
        # maybe I could take the above {abc} curly bracket positions I found above
        # remove the { } chars at those start+end positions from the temp string
        # and then flag any further { } I find... sounds good I think
        # oh actually, changing the temp string is a problem because the length would be wrong, used for applying the format.
        # i can just skip the 'good' { } positions when going through the bad ones/going through all of them... no issue.
        # or, if I remove {} from the allowed chars, they will be highlighted red, but then I can after highlight good ones black..

        # check to make sure only legal characters are entered
        # don't simply check whether an illegal char exists... find where it is!
        # does this handle emoji? 😀 came up as 2 boxes (only first was highlighted) - but they are joined/grouped.. maybe the font?
        # but when adding a character/illegal char after it, it showed up properly (when formatted, shows up due to now html...?)
        # probably nothing to worry about
        allowed_chars = 'ABCDEFGHIJKLMONPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{} '
        allowed_chars += globals.my_textman.hiragana_string
        allowed_chars += globals.my_textman.katakana_string
        allowed_chars += globals.my_textman.kanji_list
        allowed_chars += globals.my_textman.jp_chars
        allowed_chars += 'ー'

        illegal_char_format = QtGui.QTextCharFormat()
        illegal_char_format.setBackground(QtGui.QColor('red'))

        regex_num = re.compile(f'[^{allowed_chars}]')
        match_iter = regex_num.finditer(text)
        for m in match_iter:
            self.setFormat(m.start(), m.end() - m.start(), illegal_char_format)


class MonsterModel(QtCore.QAbstractTableModel):
    def __init__(self, *args, monsters=None, **kwargs):
        super(MonsterModel, self).__init__(*args, **kwargs)
        self.monsters = monsters or []
        self.header = ['Name', 'in Book']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if (index.column() == 0):
                return self.monsters[index.row()].name
        elif role == QtCore.Qt.CheckStateRole:
            if index.column() == 1:
                if self.monsters[index.row()].in_book:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False
        if role == Qt.CheckStateRole and index.column() == 1:
            if value == Qt.Checked:
                self.monsters[index.row()].in_book = True
            else:
                self.monsters[index.row()].in_book = False
        return True

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return col
        return None

    def rowCount(self, index):
        return len(self.monsters)

    def columnCount(self, index):
        return len(self.header)

    def flags(self, index):
        if index.column() == 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class TextTableModel(QtCore.QAbstractListModel):
    def __init__(self, *args, text_entries=None, **kwargs):
        super(TextTableModel, self).__init__(*args, **kwargs)
        self.text_entries = text_entries or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            text = self.text_entries[index.row()]
            return text
        if role == Qt.EditRole:
            text = self.text_entries[index.row()]
            return text

    def rowCount(self, index):
        return len(self.text_entries)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            self.text_entries[index.row()] = value
            self.dataChanged.emit(index, index)
            print(globals.my_textman.master_table_list[0])
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(f'SeiSaboten v{__version__}')
        icon = iconFromBase64(window_icon)
        self.setWindowIcon(icon)

        self.monster_model = MonsterModel()
        self.text_table_model = TextTableModel()

        table_header = self.tableView.horizontalHeader()
        self.tableView.setHorizontalHeader(table_header)

        self.tableView.setModel(self.monster_model)
        self.tableView.verticalHeader().setSectionsMovable(True)
        self.tableView.verticalHeader().setDragEnabled(True)
        self.tableView.verticalHeader().setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)  # not needed?
        # self.tableView.verticalHeader().setDropIndicatorPosition(2) # drop below
        self.tableView.verticalHeader().setSectionResizeMode(3)

        self.tabletext_listview.setModel(self.text_table_model)

        self.shuffle_monsters_btn.pressed.connect(self.shuffle_monsters)
        self.randomize_weaknesses_btn.pressed.connect(self.randomize_weaknesses)
        self.export_dialog_btn.pressed.connect(self.dialog_export_json)

        self.weaknesses_not_all_none_checkbox.stateChanged.connect(self.toggleCombo)

        self.tableView.selectionModel().currentRowChanged.connect(self.process_monster_stats)

        self.highlighter = MyHighlighter(self.textEdit.document())

        self.string_bytes_convert_button.pressed.connect(self.string_2_bytes)

        self.actionLoad.triggered.connect(self.openFileNameDialog)
        self.actionSave.triggered.connect(self.saveFileDialog)
        self.actionCredits.triggered.connect(self.show_credits)

    def init_after_rom(self):
        globals.my_textman = textman.TextManager()
        globals.my_enemyman = enemyman.EnemyManager()

        self.dialogpicker_combo.addItems([str(i) for i in range(
            globals.my_textman.get_dialog_entries_count(globals.my_textman.story_table_address))])
        self.dialogpicker_combo.currentIndexChanged.connect(self.load_dialog)
        self.load_dialog(0)

        self.tablepicker_combo.addItems([str(i) for i in range(len(globals.my_textman.master_table_list))])
        self.tablepicker_combo.currentIndexChanged.connect(self.load_text_table)
        self.text_table_model.text_entries = globals.my_textman.master_table_list[0]
        self.text_table_model.layoutChanged.emit()

        self.type_combo.addItems(
            globals.my_textman.all_entries_text_table(globals.my_textman.master_table_table_addresses[46]))
        self.prime_ability_combo.addItems(
            globals.my_textman.all_entries_text_table(globals.my_textman.master_table_table_addresses[45]))
        self.sub_ability_combo.addItems(
            globals.my_textman.all_entries_text_table(globals.my_textman.master_table_table_addresses[45]))

        self.monster_model.monsters = globals.my_enemyman.full_enemy_list
        self.monster_model.layoutChanged.emit()

        table_header = self.tableView.horizontalHeader()
        self.tableView.setHorizontalHeader(table_header)
        self.tableView.setRowHidden(0, True)

        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()

        self.tabWidget.setEnabled(True)

        self.actionSave.setEnabled(True)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose your ROM file", "",
                                                  "GBA ROM Files (*.gba);;All Files (*.*)", options=options)
        if fileName:
            with open(fileName, 'rb') as fh:
                globals.my_file = fh.read()
                crc_sum = f'{zlib.crc32(globals.my_file) & 0xffffffff:08X}'
                rom_code = (globals.my_file[0xAC:0xB0]).decode('ansi')
                if rom_code in rom_info:
                    if crc_sum == rom_info[rom_code]['clean_crc32']:
                        Palette = QtGui.QPalette()
                        Palette.setColor(QtGui.QPalette.Text, QtGui.QColor('#3BB300'))
                        self.crc_display.setPalette(Palette)
                    else:
                        Palette = QtGui.QPalette()
                        Palette.setColor(QtGui.QPalette.Text, QtGui.QColor('#B30000'))
                        self.crc_display.setPalette(Palette)

                    globals.rom_region = rom_info[rom_code]['region']

            self.crc_display.setText(str(crc_sum))
            globals.my_file = bytearray(globals.my_file)

            self.init_after_rom()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save your ROM file", "",
                                                  "GBA ROM Files (*.gba);;All Files (*.*)", options=options)
        if fileName:
            # when clicked, also write the current monster values that are editing, to monster list
            self.text_table_model.layoutChanged.emit()

            globals.my_enemyman.full_enemy_list = self.monster_model.monsters
            globals.my_enemyman.set_enemies()

            # extend rom
            globals.my_file = globals.my_file + (b'\x00' * 0x01000000)
            # if we save twice, this happens twice... not good

            # extend rom
            globals.my_enemyman.write_monster_book(0x01500000)
            monster_book_pointer = int(locations.locations[globals.rom_region]['monster_book_pointer'], base=16)
            globals.my_file[monster_book_pointer:monster_book_pointer + 0x4] = (0x01500000 + 0x08000000).to_bytes(4,
                                                                                                                  byteorder='little')
            with open(fileName, 'wb') as f:
                f.write(globals.my_file)

            # disable loading and saving again, until proper re-init has been added
            self.actionLoad.setEnabled(False)
            self.actionSave.setEnabled(False)

    def show_credits(self):
        msg = QMessageBox()
        msg.setWindowTitle('Credits')
        msg.setText(f'聖覇王樹 v{__version__}\nThanks for checking it out!\nJoshua Miller - https://jtm.gg')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def string_2_bytes(self):
        input_text = self.string_input_TextEdit.document().toPlainText()
        text_bytes = bytearray()
        for char in input_text:
            char_bytes = globals.my_textman.inv_char_dict[char].to_bytes(2, byteorder='big')
            for byte in char_bytes:
                text_bytes.append(byte)
        output_string = ''
        for byte in text_bytes:
            output_string += f'{byte:02X}' + ' '
        self.string_output_TextEdit.setPlainText(output_string)

    def process_monster_stats(self, current, previous):
        # if a monster was viewed, store the stats for the one we just edited
        # then display the monster stats for the new monster id selected
        if previous.row() >= 0:
            self.store_monster_stats(self.monster_model.monsters[previous.row()])
        self.show_monster_stats(self.monster_model.monsters[current.row()])

    def show_monster_stats(self, monster):
        self.hp_lineEdit.setText(str(monster.hp))
        self.pow_lineEdit.setText(str(monster.pow))
        self.def_lineEdit.setText(str(monster.def_))
        self.agi_lineEdit.setText(str(monster.agi))
        self.int_lineEdit.setText(str(monster.int_))
        self.mnd_lineEdit.setText(str(monster.mnd))
        self.exp_lineEdit.setText(str(monster.exp))
        self.luc_lineEdit.setText(str(monster.lucre))

        self.slash_effect.setCurrentIndex(monster.slash)
        self.bash_effect.setCurrentIndex(monster.bash)
        self.jab_effect.setCurrentIndex(monster.jab)

        self.light_effect.setCurrentIndex(monster.light)
        self.dark_effect.setCurrentIndex(monster.dark)
        self.moon_effect.setCurrentIndex(monster.moon)
        self.fire_effect.setCurrentIndex(monster.fire)
        self.water_effect.setCurrentIndex(monster.water)
        self.wood_effect.setCurrentIndex(monster.wood)
        self.wind_effect.setCurrentIndex(monster.wind)
        self.earth_effect.setCurrentIndex(monster.earth)

        self.type_combo.setCurrentIndex(monster.type_)
        self.prime_ability_combo.setCurrentIndex(monster.ability_prime)
        self.sub_ability_combo.setCurrentIndex(monster.ability_sub)
        self.name_lineEdit.setText(monster.name)

    def store_monster_stats(self, monster):
        monster.hp = int(self.hp_lineEdit.text())
        monster.pow = int(self.pow_lineEdit.text())
        monster.def_ = int(self.def_lineEdit.text())
        monster.agi = int(self.agi_lineEdit.text())
        monster.int_ = int(self.int_lineEdit.text())
        monster.mnd = int(self.mnd_lineEdit.text())
        monster.exp = int(self.exp_lineEdit.text())
        monster.lucre = int(self.luc_lineEdit.text())

        monster.slash = self.slash_effect.currentIndex()
        monster.bash = self.bash_effect.currentIndex()
        monster.jab = self.jab_effect.currentIndex()

        monster.light = self.light_effect.currentIndex()
        monster.dark = self.dark_effect.currentIndex()
        monster.moon = self.moon_effect.currentIndex()
        monster.fire = self.fire_effect.currentIndex()
        monster.water = self.water_effect.currentIndex()
        monster.wood = self.wood_effect.currentIndex()
        monster.wind = self.wind_effect.currentIndex()
        monster.earth = self.earth_effect.currentIndex()

        monster.type_ = self.type_combo.currentIndex()
        monster.ability_prime = self.prime_ability_combo.currentIndex()
        monster.ability_sub = self.sub_ability_combo.currentIndex()
        monster.name = self.name_lineEdit.text()

    def load_dialog(self, i):
        this_dialog = globals.my_textman.story_table_list[i]
        self.textEdit.document().setPlainText(this_dialog['string'])
        if this_dialog['actor']:
            self.dialog_sprite_group.setChecked(True)
            if this_dialog['actor']['position'] == 'Left':
                self.dialog_sprite_pos.setCurrentIndex(0)
            else:
                self.dialog_sprite_pos.setCurrentIndex(1)
            self.dialog_sprite_id.setText(str(this_dialog['actor']['id']))

        else:
            self.dialog_sprite_group.setChecked(False)

    def load_text_table(self, i):
        self.text_table_model.text_entries = globals.my_textman.master_table_list[i]
        self.text_table_model.layoutChanged.emit()

    def toggleCombo(self, state):
        if state > 0:
            self.weaknesses_prevent_combo.setEnabled(True)
        else:
            self.weaknesses_prevent_combo.setEnabled(False)

    def shuffle_monsters(self):
        if self.shuffle_main.isChecked():
            main_enemy_list = self.monster_model.monsters[1:123]
            random.shuffle(main_enemy_list)
            self.monster_model.monsters[1:123] = main_enemy_list
        else:
            random.shuffle(globals.my_enemyman.full_enemy_list)
        self.monster_model.layoutChanged.emit()

    def dialog_export_json(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Dialog export", "",
                                                  "JSON File (*.json);;All Files (*.*)", options=options)
        if fileName:
            with open(fileName, 'w', encoding='utf-8') as json_file:
                json.dump(globals.my_textman.story_table_list, json_file, ensure_ascii=False, indent=2)

    def randomize_weaknesses(self):
        chosen_weights = []
        chosen_weights.append(self.weight_spin_circle.value())
        chosen_weights.append(self.weight_spin_dblcircle.value())
        chosen_weights.append(self.weight_spin_tri.value())
        chosen_weights.append(self.weight_spin_x.value())
        # make sure that weights are not all 0
        if all([w == 0 for w in chosen_weights]):
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Not all weights can be 0.')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            for i, enemy in enumerate(globals.my_enemyman.full_enemy_list):

                weapon_weaknesses = random.choices(population=[0, 1, 2, 3], weights=chosen_weights, k=3)
                magic_weaknesses = random.choices(population=[0, 1, 2, 3], weights=chosen_weights, k=8)
                if self.weaknesses_prevent_combo.isEnabled():
                    weapon_weaknesses_all_none = all([w == 3 for w in weapon_weaknesses])
                    magic_weaknesses_all_none = all([w == 3 for w in magic_weaknesses])

                    combo_type = self.weaknesses_prevent_combo.currentIndex()

                    if combo_type == 0:
                        # ensure weapon and magic weaknesses both have 1 not none
                        if weapon_weaknesses_all_none:
                            weapon_weaknesses[random.choice(range(3))] = 2
                        if magic_weaknesses_all_none:
                            magic_weaknesses[random.choice(range(8))] = 2
                    elif combo_type == 1:
                        # ensure weapon OR magic weaknesses have 1 not none
                        if weapon_weaknesses_all_none and magic_weaknesses_all_none:
                            if random.choice([0, 1]) == 0:
                                weapon_weaknesses[random.choice(range(3))] = 2
                            else:
                                magic_weaknesses[random.choice(range(8))] = 2
                    elif combo_type == 2:
                        # ensure weapon weaknesses have 1 not none
                        if weapon_weaknesses_all_none:
                            weapon_weaknesses[random.choice(range(3))] = 2
                    elif combo_type == 3:
                        # ensure magic weaknesses have 1 not none
                        if magic_weaknesses_all_none:
                            magic_weaknesses[random.choice(range(3))] = 2

                globals.my_enemyman.full_enemy_list[i].slash = weapon_weaknesses[0]
                globals.my_enemyman.full_enemy_list[i].bash = weapon_weaknesses[1]
                globals.my_enemyman.full_enemy_list[i].jab = weapon_weaknesses[2]

                globals.my_enemyman.full_enemy_list[i].light = magic_weaknesses[0]
                globals.my_enemyman.full_enemy_list[i].dark = magic_weaknesses[1]
                globals.my_enemyman.full_enemy_list[i].moon = magic_weaknesses[2]
                globals.my_enemyman.full_enemy_list[i].fire = magic_weaknesses[3]
                globals.my_enemyman.full_enemy_list[i].water = magic_weaknesses[4]
                globals.my_enemyman.full_enemy_list[i].wood = magic_weaknesses[5]
                globals.my_enemyman.full_enemy_list[i].wind = magic_weaknesses[6]
                globals.my_enemyman.full_enemy_list[i].earth = magic_weaknesses[7]

    def show_encounters(self):
        pass
        # starts at E3D4D8, each is 0x14 long, 10 enemies at 0x2 each


if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons
    app = QtWidgets.QApplication(sys.argv)
    # app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    window = MainWindow()
    window.show()
    app.exec_()
