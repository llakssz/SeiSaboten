# SeiSaboten 😇🌵

A ROM editor for the GBA game Sword of Mana/新約 聖剣伝説.

Supports editing:
- monsters and their stats, experience and Lucre given
- game dialog (story text, actor sprites, sign posts, ...)
- game text (items, place names, ...)
- monsters shown in 'Monster Album' (add unlisted monsters!)
- monster encounter tables (change enemies in areas)

Only supports editing the Japanese version and the USA version at the moment.
The European versions (the 3 of them!) are not currently supported.

Dialog can be exported to JSON, in order to edit in an external program. It can then be imported back.

Lots of reverse engineering of the game was needed to accomplish this, and without [No$GBA](https://www.nogba.com/) this wouldn't have been possible - a big thank you to that!

To handle the Japanese text, each of the 1247 kanji in the game had to be documented individually...! I didn't trust OCR with something like this, due to the low pixel density. Some kanji were hard to deduce (they were viewed all together, not in context) - so they were skipped. View the 'kanji_table.xlsx' file in the 'kanji' folder in the repo to see which kanji are missing. Screenshots of each kanji are included in case anyone wants to fill in the missing ones before I get around to it myself! Again, check the 'kanji' folder.

Sample:
![Text Editing](https://jtm.gg/files/dudbear-message4x.png)
SeiSaboten GUI:
![Editor GUI](https://jtm.gg/files/SeiSaboten0.6.png)
Edit of Rabite:
![Monster Editing](https://jtm.gg/files/rabite_edit4x.png)
Replacing Rabites with Chocobos:
![Encounter Editing](https://jtm.gg/files/chocobo4x.png)