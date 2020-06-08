import tileclass

def check_solution(board):
    #CHECK BLOCKS
    blocks = []
    for block_column in board.blocks:
        for block in block_column:
            tile_list = []
            for tile_column in block.tiles:
                for tile in tile_column:
                    if tile.value != None:
                        tile_list.append(tile.value)
                    else:
                        return False
            blocks.append(tile_list)

    for block in blocks:
        for tile in block:
            if block.count(tile) > 1:
                print()
                return False

    #CHECK COLUMNS
    columns = []
    for block_column in range(3):
        for tile_column in range(3):
            column = []
            for block in range(3):
                for tile in range(3):
                    column.append(board.blocks[block_column][block].tiles[tile_column][tile].value)
            columns.append(column)

    for column in columns:
        for tile in column:
            if column.count(tile) > 1:
                return False


    #CHECK ROWS
    rows = []
    for block in range(3):
        for tile in range(3):
            row = []
            for block_column in range(3):
                for tile_column in range(3):
                    row.append(board.blocks[block_column][block].tiles[tile_column][tile].value)
            rows.append(row)

    for row in rows:
        for tile in row:
            if row.count(tile) > 1:
                return False

    return True
