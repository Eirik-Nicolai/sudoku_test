def get_table(path):
    if path != None and path != "":
        f = open(path)
        s = f.read()
        if len(s) == 0:
            return None
        s = s.replace('\n', '')
        f.close()
    out = []
    blocks_strings = s.split(';')
    for block_string in blocks_strings:
        block_info = block_string.split('-')
        tile_strings = block_info[1].split('|')
        tiles = []
        for tile_string in tile_strings:
            single_tile = tile_string.split(',')
            tiles.append(((single_tile[0],single_tile[1]),single_tile[2]))
        blocks = []
        block = []
        block.append(block_info[0].split(','))
        block.append(tiles)
        out.append(block)
    return out

def save_board(value, name):
    f = open(name, "w")
    f.write(value)
    f.close()
