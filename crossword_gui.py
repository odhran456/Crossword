import pygame
import pandas as pd

# Pick which crossword template you want to play with
boundaries = {'version_1':[(0,1),(0,3),(0,5),(0,6),(1,8),(1,10),(1,12),(2,1),(2,3),(2,5),(2,6),(3,5),(3,10),(3,12),
                  (4,4),(4,9),(5,0),(5,2),(5,7),(5,12),(6,0),(6,1),(6,11),(6,12),(7,0),(7,5),(7,10),(7,12),
                  (8,3),(8,8),(9,0),(9,2),(9,7),(10,6),(10,7),(10,9),(10,11),(11,0),(11,2),(11,4),(12,6),
                  (12,7),(12,9),(12,11)],
              'version_2':[(2,2),(2,3),(2,4),(2,5),(3,2),(4,2),(5,2),(6,2),(6,3),(6,4),(6,5),(7,2),(8,2),(9,2),
                           (10,2),(10,3),(10,4),(10,5),(2,8),(2,12),(3,9),(3,11),(4,10),(5,10),(6,10),(7,10),
                           (8,10),(9,10),(10,10)]
              }

# The grid (13x13)
tiles = [(i,j) for i in range(13) for j in range(13)]


# Get co-ordinate of start of every word
def get_word_coords(tiles,version):
    word_coords = []
    for count in range(169):
        if tiles[count] in boundaries[version]:
            continue
        elif tiles[count] == (0,0):
            word_coords.append(tiles[count])
        elif tiles[count][0] == 0:
            if tiles[count - 1] in boundaries[version] or tiles[count + 13] not in boundaries[version]:
                word_coords.append(tiles[count])
        elif tiles[count][1] == 0:
            if tiles[count - 13] in boundaries[version] or tiles[count + 1] not in boundaries[version]:
                word_coords.append(tiles[count])
        if count < 168:
            if tiles[count - 1] in boundaries[version] and tiles[count + 1] not in boundaries[version]:
                word_coords.append(tiles[count])
        if count < 155:
            if tiles[count - 13] in boundaries[version] and tiles[count + 13] not in boundaries[version]:
                word_coords.append(tiles[count])
        count+=1
    word_coords = list( dict.fromkeys(word_coords))
    return word_coords


# TODO :Get co-ordinates of all letters of word for all words
def words_full(word_coords):
    all_words = []
    for i in range(len(word_coords)):
        index = tiles.index(word_coords[i])
        cur = tiles[index]
        word_len = []
        while index % 13 <= 12 and cur not in boundaries['version_1']:
            word_len.append(cur)
            index += 1
            cur = tiles[index]
        if len(word_len) > 1:
            all_words.append(word_len)
    return all_words


class Grid:
    def __init__(self,rows,cols,width,height,win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.win = win

    def draw(self,version):
        # Draw Grid Lines
        gap = self.height / 13
        for i in range(self.rows+1):
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.height, i*gap))
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height))
        # Draw black squares
        for i in range(len(boundaries[version])):
            row, col = boundaries[version][i]
            pygame.draw.rect(self.win, (0, 0, 0), (col * (540 / 13), row * (540 / 13), (540 / 13) + 1, (540 / 13) + 1))

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.height and pos[1] < self.height:
            gap = self.height / 13
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None


def redraw_window(win, board):
    win.fill((255,255,255))
    # Draw grid and board
    board.draw('version_1')


def main():
    win = pygame.display.set_mode((1200,600))
    pygame.display.set_caption("Crossword")
    board = Grid(13, 13, 1200, 540, win)
    key = None
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    print(clicked[0], clicked[1])
                    key = None

        redraw_window(win, board)
        pygame.display.update()


main()
