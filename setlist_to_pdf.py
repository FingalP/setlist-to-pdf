import zipfile
import os
import shutil
from PyPDF2 import PdfMerger

musicians = {
    "fingal": {"instrument": "alto", "instrument_number": 2},
    "emily": {"instrument": "alto", "instrument_number": 2},
    "alice": {"instrument": "alto", "instrument_number": 1},
    "milo": {"instrument": "tenor", "instrument_number": 1},
    "callum": {"instrument": "tenor", "instrument_number": 1},
    "peter": {"instrument": "bass", "instrument_number": 1},
    "noah": {"instrument": "guitar", "instrument_number": 1},
    "kiran": {"instrument": "guitar", "instrument_number": 1},
    "james": {"instrument": "trombone", "instrument_number": "C"},
    "freya": {"instrument": "tenor", "instrument_number": 1},
    "lizzie": {"instrument": "tenor", "instrument_number": 1},
    "nickdf": {"instrument": "trumpet", "instrument_number": 1},
    "hugh": {"instrument": "trumpet", "instrument_number": 2},
    "ella": {"instrument": "trumpet", "instrument_number": 1},
    "lois": {"instrument": "trombone", "instrument_number": "Bb"},
}

gig_name = "Fitz Conference"
musician_names = ["fingal", "alice", "lois", "callum", "hugh", "ella"]
gig_date = "2024-10-24"

def get_most_recent_sheet_music_file():
    downloads_folder = os.path.expanduser("~/Downloads")

    most_recent_file = None
    most_recent_time = 0

    for filename in os.listdir(downloads_folder):
        if filename.startswith("Sheet Music by song"):
            filepath = os.path.join(downloads_folder, filename)
            mod_time = os.path.getmtime(filepath)

            if mod_time > most_recent_time:
                most_recent_time = mod_time
                most_recent_file = filepath

    assert most_recent_file is not None, "No files starting with 'Sheet Music by song' found in the Downloads folder."

    print("Using sheet music file:", most_recent_file)
    return most_recent_file


# sheet_music_by_song_name = "Sheet Music by song-20241024T154929Z-001"


setlist_raw = ['''
Gimme Gimme Gimme
Love Machine
(This Will Be) An Everlasting Love
Tracy Beaker's Dilemma
Closer
99 Luftballons
Murder On the Dancefloor
Rasputin
Arthur
Can't Take My Eyes Off You
Foundations
Blinding Lights
Bad Touch
Tiggle Diggle Tiggle Miggle
Come On Eileen
Shregamix
Toxic
(Walking On Sunshine)
''']

os.mkdir('tmp')

try:
    with zipfile.ZipFile(get_most_recent_sheet_music_file(), 'r') as zip_ref:
        zip_ref.extractall('tmp')

    for i, single_setlist in enumerate(setlist_raw):
        setlist = [x for x in single_setlist.split('\n') if not x == '']
        if len(setlist) == 0:
            continue

        def make_minimal(song):
            # why not check if alphanumeric?
            for char in ["'", '"', " ", "(", ")", "-", "_", ",", ".", '/', '>', '+', '–', "’", "!", "…", '=', '—']:
                song = song.replace(char, "")
            return song.strip().lower()

        setlist_minimal = [make_minimal(x) for x in setlist]


        for musician_name in musician_names:
            musician = musicians[musician_name]
            instrument = musician["instrument"]
            instrument_number = musician["instrument_number"]
            file_name = f'{gig_date} {gig_name} {musician_name} {chr(65+i)}'

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
                'sreep&mreep': ('screep&mreepifs&mandcreephadababy',),
                'sreepandmreep': ('screep&mreepifs&mandcreephadababy',),
                'screepandmreep': ('screep&mreepifs&mandcreephadababy',),
                'vroomvroom': ('vroomvrooooom',),
                'tracybeakersdilemna': ('tracybeakersdilemma',),
                'tiggledigglemigglewiggle': ('tigglediggletigglemiggle',),
                'canttakemyeyesoffofyou': ('canttakemyeyesoffyou',),
                'murderonthedogsfloor': ('murderonthedancefloor',),
                'manifeellikewoman': ('manifeellikeawoman',),
                'cantstopfeelingbulliedjeansface': ('cantstopfeelingbilliejeansface',),
                'screepmreep': ('screep&mreepifs&mandcreephadababy',)
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
                # TODO: make this more general - if it's some order or other, then make the matches list ordering be the same as the string in song_minimal
                # Fiddly because we don't know where to split the strings by default
                if len(matches) == 2 and f"{matches[1][0]}{matches[0][0]}" == song_minimal:
                    matches = [*reversed(matches)]
                if len(matches) == 0 and song_minimal in manual_matches:
                    matches.append(manual_matches[song_minimal])
                if len(matches) == 0:
                    print(f'{len(matches)} matches found for `{song_minimal}`, please add to manual or otherwise fix')
                    print(matches)
                for match in matches:
                    for folder_minimal in match:
                        folder = folders_minimal_to_folder[folder_minimal]
                        if folder not in folders_to_ignore:
                            folders_in_order.append(folder)

            bad_file_names = ['Original-Tom', 'Old (musescore 2 no guitar part)', 'old - one trumpet']

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
                        matching_files = [x for x in matching_files if str(instrument_number).lower() in make_minimal(x)]
                if not len(matching_files) == 1:
                    print(f'{len(matching_files)} matches found for `{folder}` for {instrument} {instrument_number}, please fix')
                else:
                    pdfs_to_merge.append(f'tmp/Sheet Music by song/{folder}/{matching_files[0]}')

            with PdfMerger() as merger:
                for pdf in pdfs_to_merge:
                    merger.append(pdf)

                merger.write(f"{file_name}.pdf")
                merger.close()

finally:
    shutil.rmtree('tmp')
