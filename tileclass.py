
import pygame as pg
import filehelper

BG_GREY     = (230,230,230)
BG_WHITE    = (255,255,255)

TEXT_BLACK  = (0,0,0)
TEXT_GRAY   = (70,70,70)
TEXT_ORANGE = (255,140,0)
TEXT_BLUE   = (0,50,255)

number_keys = [
    pg.K_0,
    pg.K_1,
    pg.K_2,
    pg.K_3,
    pg.K_4,
    pg.K_5,
    pg.K_6,
    pg.K_7,
    pg.K_8,
    pg.K_9,
    pg.K_KP0,
    pg.K_KP1,
    pg.K_KP2,
    pg.K_KP3,
    pg.K_KP4,
    pg.K_KP5,
    pg.K_KP6,
    pg.K_KP7,
    pg.K_KP8,
    pg.K_KP9
]

class SudokuTile(pg.Surface):
    def __init__(self, width, height, border_width):
        self.background_colour = BG_WHITE
        self.WIDTH = width
        self.HEIGHT = height
        self.value_colour = TEXT_BLACK;
        super(SudokuTile, self).__init__((self.WIDTH, self.HEIGHT))
        self.BORDER_WIDTH = border_width
        border = pg.Surface(super().get_size())
        backgroundH = border.get_size()[0] - self.BORDER_WIDTH*2
        backgroundW = border.get_size()[1] - self.BORDER_WIDTH*2
        self.background = pg.Surface((backgroundH,backgroundW))
        border.fill((0,0,0))
        super().blit(border.convert(), (0,0))

        self.value = None

        self.upper_left_corner_values = []
        self.upper_right_corner_values = []

    def write_to_value(self, key):
        if self.value_colour != TEXT_GRAY:
            print(key)
            self.value = key

    def write_to_corner(self, which_corner, key):
        if which_corner == "upper_left":
            if key not in self.upper_left_corner_values:
                self.upper_left_corner_values.append(key)
        elif which_corner == "upper_right":
            if key not in self.upper_right_corner_values:
                self.upper_right_corner_values.append(key)

    def write_values(self):
        self.set_background()
        if self.value != None:
            self.set_text(self.value, int(self.HEIGHT/2), self.value_colour, "middle")

        if len(self.upper_left_corner_values) != 0:
            s = ""
            for n in self.upper_left_corner_values:
                s += f"{n}"
            self.set_text(s, int(self.HEIGHT/6), TEXT_ORANGE, "upper_left")

        if len(self.upper_right_corner_values) != 0:
            s = ""
            for n in self.upper_right_corner_values:
                s += f"{n}"
            self.set_text(s, int(self.HEIGHT/6), TEXT_BLUE, "upper_right")

    def click(self):
        self.background_colour = BG_GREY
        self.set_background()

    def clear(self):
        self.background_colour = BG_WHITE

    def is_init_value(self):
        self.value_colour = TEXT_GRAY

    def set_background(self):
        self.background.fill(self.background_colour)
        super().blit(self.background.convert(), (self.BORDER_WIDTH,self.BORDER_WIDTH))

    def set_text(self, value, font_size, colour, text_pos):
        font = pg.font.Font("freesansbold.ttf", font_size)
        txt_surf = font.render(value, True, colour)
        if text_pos == "middle":
            pos = ((self.WIDTH/2)-font_size/4, (self.HEIGHT/2)-font_size/3)
        elif text_pos == "upper_left":
            pos = (self.BORDER_WIDTH,self.BORDER_WIDTH)
        elif text_pos == "upper_right":
            pos = ((self.WIDTH-(font_size*0.6)*len(self.upper_right_corner_values)-self.BORDER_WIDTH,
                    self.BORDER_WIDTH))
        super().blit(txt_surf, pos)


class SudokuBlock(pg.Surface):
    def __init__(self, tile_size):
        self.TILE_SIZE = tile_size
        self.WIDTH = tile_size*3;
        self.HEIGHT = self.WIDTH
        self.BORDER_WIDTH = 2
        super().__init__((self.WIDTH+self.BORDER_WIDTH,self.HEIGHT+self.BORDER_WIDTH))
        self.tiles = [[SudokuTile for x in range(3)] for y in range(3)]
        self.displaytiles = [[pg.Rect for x in range(3)] for y in range(3)]
        for i in range(3):
            for ii in range(3):
                self.tiles[i][ii] = SudokuTile(self.TILE_SIZE,self.TILE_SIZE,1)
        self.selected_tile = None
        self.blit_tiles()

    def set_tile_values(self, tile_values):
        for tile_value in tile_values:
            self.tiles[int(tile_value[0][0])][int(tile_value[0][1])].write_to_value(f"{tile_value[1]}")
            self.tiles[int(tile_value[0][0])][int(tile_value[0][1])].is_init_value()
        self.blit_tiles()

    def get_tile_values(self):
        return_value = ""
        for i in range(3):
            for ii in range(3):
                if self.tiles[i][ii].value != None:
                    return_value += f"{i},{ii},{self.tiles[i][ii].value}|"
        return_value = return_value[:-1]
        return return_value

    def blit_tiles(self):
        for i in range(3):
            for ii in range(3):
                pos = self.tiles[i][ii].get_rect()
                pos.move_ip(self.TILE_SIZE*i,self.TILE_SIZE*ii)
                self.tiles[i][ii].write_values()
                self.displaytiles[i][ii] = super().blit(self.tiles[i][ii].convert(), pos)

    def click(self, mouse_pos):
        for x in range(3):
            for y in range(3):
                if self.displaytiles[x][y].collidepoint(mouse_pos):
                    self.tiles[x][y].click()
                    self.selected_tile = self.tiles[x][y]
                    self.blit_tiles()

    def keypress(self, key, ctrl_pressed, shift_pressed):
        if ctrl_pressed:
            self.selected_tile.write_to_corner("upper_left", key)
        elif shift_pressed:
            self.selected_tile.write_to_corner("upper_right", key)
        else:
            self.selected_tile.write_to_value(key)
        self.blit_tiles()

    def clear_selection(self):
        if self.selected_tile != None:
            self.selected_tile.clear()
            self.blit_tiles()

class SudokuBoard(pg.Surface):
    def __init__(self, size):
        self.SIZE = size
        tile_size = self.SIZE/9
        self.BORDER_WIDTH = 2
        super().__init__((self.SIZE+self.BORDER_WIDTH*2, self.SIZE+self.BORDER_WIDTH*2))
        self.ctrl_pressed = False
        self.shift_pressed = False

        background = pg.Surface(super().get_size())
        background = background.convert()
        background.fill((0,0,0))
        super().blit(background, (0,0))

        self.blocks = [[SudokuBlock for x in range(3)] for y in range(3)]
        self.displayblocks = [[pg.Rect for x in range(3)] for y in range(3)]
        for i in range(3):
            for ii in range(3):
                self.blocks[i][ii] = SudokuBlock(tile_size)
        self.blit_blocks()
        self.selected_block = None

    def setup_board(self, board_values):
        for block_indexes in board_values:
            block = self.blocks[int(block_indexes[0][0])][int(block_indexes[0][1])]
            block.set_tile_values(block_indexes[1])
        self.blit_blocks()

    def save_board(self):
        board_value = ""
        for i in range(3):
            for ii in range(3):
                board_value += f"{i},{ii}-"
                board_value += self.blocks[i][ii].get_tile_values()
                board_value += ";"
        board_value = board_value[:-1]
        filehelper.save_board(board_value, "new file.txt")

    def blit_blocks(self):
        for i in range(3):
            for ii in range(3):
                self.displayblocks[i][ii] = super().blit(self.blocks[i][ii].convert(),
                                                         (((self.SIZE/3)*i)+self.BORDER_WIDTH*i,
                                                          ((self.SIZE/3)*ii)+self.BORDER_WIDTH*ii))

    def check_click(self, mouse_pos):
        for x in range(3):
            for y in range(3):
                if self.displayblocks[x][y].collidepoint(mouse_pos):
                    if self.selected_block != None:
                        equal = False
                        #if self.selected_block == self.blocks[x][y]:
                            #equal = True
                        self.selected_block.clear_selection()
                        if equal:
                            self.selected_block.selected_tile = None
                            self.selected_block = None
                            self.blit_blocks()
                            return
                    #translate mouse pos for blocks
                    mposx = mouse_pos[0]-(self.SIZE/3)*x
                    mposy = mouse_pos[1]-(self.SIZE/3)*y
                    self.blocks[x][y].click((mposx,mposy))
                    self.selected_block = self.blocks[x][y]
                    self.blit_blocks()
                    return
        if self.selected_block != None:
            self.selected_block.clear_selection()
            self.blit_blocks()

    def keypress(self, key, type):
        if key == pg.K_LCTRL or key == pg.K_RCTRL:
            if self.ctrl_pressed:
                self.ctrl_pressed = False
            elif not self.ctrl_pressed:
                self.ctrl_pressed = True;
        elif key == pg.K_LSHIFT:
            if self.shift_pressed:
                self.shift_pressed = False
            elif not self.shift_pressed:
                self.shift_pressed = True;
        else:
            if type != pg.KEYDOWN:
                return
            for numberkey in number_keys:
                if key == numberkey:
                    if self.selected_block != None:
                        self.selected_block.keypress(
                            pg.key.name(numberkey),
                            self.ctrl_pressed,
                            self.shift_pressed)
                        self.blit_blocks()
