#DES File tools
import re
import os

UNKNOWN_TILE = "unknown"

tile_pattern = re.compile(r'DES[0-9][0-9][0-9][0-9][+-][0-9][0-9][0-9][0-9]')
def find_tilename(name):
    m = tile_pattern.search(name)
    if m is None:
        return UNKNOWN_TILE
    return m.group()


class TileCollection(object):
    "A directory with lots of files or subdirectories which have tiles in their names"
    def __init__(self, path=None, files=None):
        if files is not None:
            self.files = files
        elif path is not None:
            self.files = self.find_files(path)
        else:
            raise ValueError("Must initialize a TileCollection with either path or files")

    def find_files(self, path):
        all_files = os.listdir(path)
        files = {}
        for filename in all_files:
            tile = find_tilename(filename)
            if tile==UNKNOWN_TILE:
                continue
            files[tile] = filename
        return files

    def __contains__(self, tile):
        return tile in self.files

    def files_with_path(self, path):
        for tile, filename in self.files.items():
            yield tile, os.path.join(path, tile)

    def existing_files_with_path(self, path):
        for tile, filename in self.files_with_path(path):
            if os.path.exists(filename):
                yield tile, filename
    
    def filter(self, other):
        files = {}
        for tile, filename in self.files.items():
            if tile in other:
                files[tile] = filename
        return TileCollection(files=files)
