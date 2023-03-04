from pathlib import Path
import shutil
import zipfile
import os
import argparse
import threading

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='path to directory', type=str, help="path to directory")
args = parser.parse_args()
path = args.path


class Filemover():
    def __init__(self, path):
        self.path = path

    def get_files_to_move(self):
        all_of = {'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
                  'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                  'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
                  'archives': ['ZIP', 'GZ', 'TAR']
                  }
        files_to_move = []
        for type, ext in all_of.items():
            exts = [f"*.{e.lower()}" for e in ext] + [f"*.{e.upper()}" for e in ext]
            files = [f for ext in exts for f in Path(self.way).rglob(ext)]
            if files:
                files_to_move.extend(files)
        return files_to_move

    def get_file_type(file_path):
        ext = os.path.splitext(file_path)[1]
        if ext:
            return ext[1:].upper()
        else:
            return None

    def move_files(self, files_to_move):
        for f in files_to_move:
            name = normalize(f.name)
            dest = os.path.join(self.way, self.get_file_type(f))
            os.makedirs(dest, exist_ok=True)
            shutil.move(f, os.path.join(dest, name))

        arch_path = os.path.join(self.way, 'archives')
        for a in os.listdir(arch_path):
            full_path = os.path.join(arch_path, a)
            if zipfile.is_zipfile(full_path):
                with zipfile.ZipFile(full_path, 'r') as zip_ref:
                    name = Path(a).stem
                    zip_ref.extractall(os.path.join(arch_path, name))
                os.remove(full_path)


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
    name, ext = os.path.splitext(name)
    name = name.replace(' ', '_')
    return f"{name}{ext}"


def del_empty_dirs(way):
    for root, dirs, files in os.walk(way, topdown=False):
        for d in dirs:
            full_path = os.path.join(root, d)
            try:
                os.rmdir(full_path)
            except OSError:
                pass


def main(path):
    file_mover = Filemover(path)
    threads = []
    thread_get_files_to_move = threading.Thread(target=file_mover.get_files_to_move)
    threads.append(thread_get_files_to_move)
    thread_move_files = threading.Thread(target=file_mover.move_files)
    threads.append(thread_move_files)
    thread_get_files_to_move.start()
    thread_move_files.start()

    for thread in threads:
        thread.join()

    del_empty_dirs(path)


if __name__ == "__main__":
    main(path)
