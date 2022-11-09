import zipfile
import os
import shutil
from PyPDF2 import PdfMerger

instrument = 'alto'
instrument_number = 2

gig_name = '2022-11-10-Junction'
setlist_raw = '''
Toxic
10/10 -> Sweet Dreams
Sell Out
Love Never Felt So Good
Don't Start Now
Tears Dry On Their Own
Video Killed the Radiostar
Bad Guy
Vengabus
Lean On
Titanium
It's Raining Men
Crazy In Love
'''

setlist = [x for x in setlist_raw.split('\n') if not x == '']

def make_minimal(song):
    for char in ["'", '"', " ", "(", ")", "-", "_", ",", ".", '/', '>']:
        song = song.replace(char, "")
    return song.strip().lower()

setlist_minimal = [make_minimal(x) for x in setlist]

os.mkdir('tmp')

with zipfile.ZipFile('/home/fingal/Downloads/Sheet Music by song-20221109T211720Z-001.zip', 'r') as zip_ref:
    zip_ref.extractall('tmp')

folders = os.listdir('tmp/Sheet Music by song/')
folders_minimal_to_folder = {make_minimal(x): x for x in folders}
folders_minimal = list(folders_minimal_to_folder.keys())

manual_matches = {
    'vengabus': ('vengaboysmashup', ),
    '1010sweetdreams': ('tenoutoften', 'sweetdreamsaremadeofthis')
}

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
    if not len(matches) == 1:
        print(f'{len(matches)} matches found for `{song_minimal}`, please add to manual or otherwise fix')
    match = matches[0]
    for folder_minimal in match:
        folder = folders_minimal_to_folder[folder_minimal]
        folders_in_order.append(folder)

pdfs_to_merge = []
for folder in folders_in_order:
    files = os.listdir(f'tmp/Sheet Music by song/{folder}/')
    matching_files = [x for x in files if instrument in make_minimal(x)]
    if len(matching_files) > 1:
        matching_files = [x for x in matching_files if str(instrument_number) in x]
    if not len(matching_files) == 1:
        print(f'{len(matching_files)} matches found for `{folder}`, please fix')
    pdfs_to_merge.append(f'tmp/Sheet Music by song/{folder}/{matching_files[0]}')

with PdfMerger() as merger:
    for pdf in pdfs_to_merge:
        merger.append(pdf)

    merger.write(f"{gig_name}.pdf")
    merger.close()

shutil.rmtree('tmp')
