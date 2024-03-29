import zipfile
import os
import shutil
from PyPDF2 import PdfMerger

musicians = {
    "fingal": {"instrument": "alto", "instrument_number": 2},
    "alice": {"instrument": "alto", "instrument_number": 1},
    "milo": {"instrument": "tenor", "instrument_number": 1},
    "annamaria": {"instrument": "bass", "instrument_number": 1},
    "noah": {"instrument": "guitar", "instrument_number": 1},
    "nick": {"instrument": "trombone", "instrument_number": 1},
    "freya": {"instrument": "trombone", "instrument_number": "baritone"},
    "lizzie": {"instrument": "tenor", "instrument_number": 1},
    "nick-df": {"instrument": "trumpet", "instrument_number": 1},
}

musician_name = "fingal"
gig_name = "Norfolk wedding"
gig_date = "2023-09-09"

musician = musicians[musician_name]


instrument = musician["instrument"]
instrument_number = musician["instrument_number"]

sheet_music_by_song_name = "Sheet Music by song-20230729T173444Z-001"

file_name = f'{gig_date} {gig_name} {musician_name} A'
setlist_raw = '''
Rasputin
Love Never Felt So Good
Brown Eyed Girl
Don't Start Now
10/10 --> Sweet Dreams
99 Luftballons
Put Your Records On
Escape (Pina Colada)
Sax
All I Want For Xmas Is You
This Girl
Voulez Vous
Toxic
(Walking On Sunshine)'''

# file_name = f'{gig_date} {gig_name} {musician_name} B'
# setlist_raw = '''
# Pencil Full Of Lead
# 9 to 5
# Watermelon Sugar
# Forget You
# I Will Survive
# Don't Start Now
# Shregamix
# Bad Guy
# Son Of A Preacher
# Take On Me
# This Girl
# Vengabus
# Gimme Gimme Gimme
# Video KIlled The Radiostar
# Crazy In Love
# (Walking On Sunshine)
# '''

setlist = [x for x in setlist_raw.split('\n') if not x == '']

def make_minimal(song):
    for char in ["'", '"', " ", "(", ")", "-", "_", ",", ".", '/', '>', '+', '–', "’", "!", "…", '=']:
        song = song.replace(char, "")
    return song.strip().lower()

setlist_minimal = [make_minimal(x) for x in setlist]

os.mkdir('tmp')

try:
    with zipfile.ZipFile(f'/home/fingal/Downloads/{sheet_music_by_song_name}.zip', 'r') as zip_ref:
        zip_ref.extractall('tmp')

    folders = os.listdir('tmp/Sheet Music by song/')
    folders_minimal_to_folder = {make_minimal(x): x for x in folders}
    folders_minimal = list(folders_minimal_to_folder.keys())

    manual_matches = {
        'vengabus': ('vengaboysmashup', ),
        'vengabusboomboomboom': ('vengaboysmashup', ),
        '1010sweetdreams': ('tenoutoften', 'sweetdreamsaremadeofthis'),
        'sweetdreamaremadeofthis': ('sweetdreamsaremadeofthis', ),
        'thinkaboutthingstreasure': ('thinkaboutthings', 'treasure'),
        'fivecoloursinherhair': ('5coloursinherhair', ),
        'alliwantforxmasisyou': ('alliwantforchristmasisyou', ),
        'twistshout': ('twistandshout',),
        'aintgotno': ('aintgotnoigotlife',),
        'staceysmom': ('stacysmom',),
        'raspuntin': ('rararasputin',),
        'vengabusmashup': ('vengaboysmashup',),
        '99luftballoons': ('99luftballons',),
        'shrektacular': ('shregamix',),
        'manifeellikeawomen': ('manifeellikeawoman',),
        'cantgetyououtofmyhead': ('cantgetyououttamyhead',),
        'brooklyn': ('brooklynupdated',),
        'livinglavidaloca': ('livinlavidaloca', ),
    }

    folders_to_ignore = [
        # "Walking On Sunshine",
    ]

    def song_and_folder_match(song_minimal, folder_minimal):
        if song_minimal in folder_minimal:
            return True
        if folder_minimal in song_minimal:
            return True
        return False

    folders_in_order = []
    for song_minimal in setlist_minimal:
        matches = [(folder_minimal, ) for folder_minimal in folders_minimal if song_and_folder_match(song_minimal, folder_minimal)]
        if len(matches) == 0 and song_minimal in manual_matches:
            matches.append(manual_matches[song_minimal])
        if len(matches) == 0:
            print(f'{len(matches)} matches found for `{song_minimal}`, please add to manual or otherwise fix')
        for match in matches:
            for folder_minimal in match:
                folder = folders_minimal_to_folder[folder_minimal]
                if folder not in folders_to_ignore:
                    folders_in_order.append(folder)

    bad_file_names = ['Original-Tom', 'Old (musescore 2 no guitar part)']

    pdfs_to_merge = []
    for folder in folders_in_order:
        files = os.listdir(f'tmp/Sheet Music by song/{folder}/')
        good_files = [x for x in files if x not in bad_file_names]
        matching_files = [x for x in good_files if instrument in make_minimal(x)]
        if len(matching_files) == 0:
            matching_files = [x for x in good_files if 'usemescript' in make_minimal(x)]
        if len(matching_files) > 1:
            if instrument == 'guitar':
                matching_files = [x for x in matching_files if 'bass' not in make_minimal(x) and 'tab' not in make_minimal(x)]
            else:
                matching_files = [x for x in matching_files if str(instrument_number) in make_minimal(x)]
        if not len(matching_files) == 1:
            print(f'{len(matching_files)} matches found for `{folder}`, please fix')
        pdfs_to_merge.append(f'tmp/Sheet Music by song/{folder}/{matching_files[0]}')

    with PdfMerger() as merger:
        for pdf in pdfs_to_merge:
            merger.append(pdf)

        merger.write(f"{file_name}.pdf")
        merger.close()

finally:
    shutil.rmtree('tmp')
