from pathlib import Path
import re
import zipfile
import os
import shutil
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('way', metavar='path to directory', type=str, help="path to directory")
args = parser.parse_args()
way = args.way


def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    CYRILLIC_SYMBOLS = list(CYRILLIC_SYMBOLS)
    TRANS = {}
    for k, v in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(k)] = v
        TRANS[ord(k.upper())] = v.upper()
    name = name.translate(TRANS)
    name = re.sub(r'\W', '_', name)
    return name

def del_empty_dirs(way):
    for d in os.listdir(way):
        a = os.path.join(way, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)

def move_this(way):
    all_of = {'images' : ['JPEG', 'PNG', 'JPG', 'SVG'],
              'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
              'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
              'archives': ['ZIP', 'GZ', 'TAR']
              }
    for type, ext in all_of.items():
        for i in ext:
            files = glob.glob((os.path.join(way, f'*.{i}')), recursive=True)
            if not os.path.isdir(os.path.join(way, type)):
                os.mkdir(os.path.join(way, type))
            for file in files:
                basename = os.path.basename(file)
                dst = os.path.join(way, type, basename)
                shutil.move(file, dst)
    arch = os.listdir((os.path.join(way, 'archives')))
    arch_path = os.path.join(way, 'archives')
    for i in arch:
        name = Path(i)
        name = name.stem
        with zipfile.ZipFile(os.path.join(arch_path, i)) as zp:
            zp.extractall((os.path.join(arch_path, name)))
    del_empty_dirs(way)

def main(way):
    move_this(way)


if __name__ == "__main__":
    main(way)

move_this('D:\хай буде може\розібрати')









