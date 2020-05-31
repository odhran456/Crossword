import pygame
import pandas as pd


class Grid:
    # Pick which crossword template you want to play with
    boundaries = {
        'Metro_v1': [(0, 1), (0, 3), (0, 5), (0, 6), (1, 8), (1, 10), (1, 12), (2, 1), (2, 3), (2, 5), (2, 6), (3, 5),
                      (3, 10), (3, 12),
                      (4, 4), (4, 9), (5, 0), (5, 2), (5, 7), (5, 12), (6, 0), (6, 1), (6, 11), (6, 12), (7, 0), (7, 5),
                      (7, 10), (7, 12),
                      (8, 3), (8, 8), (9, 0), (9, 2), (9, 7), (10, 6), (10, 7), (10, 9), (10, 11), (11, 0), (11, 2),
                      (11, 4), (12, 6),
                      (12, 7), (12, 9), (12, 11)],
        'EY': [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (7, 2),
                      (8, 2), (9, 2),
                      (10, 2), (10, 3), (10, 4), (10, 5), (2, 8), (2, 12), (3, 9), (3, 11), (4, 10), (5, 10), (6, 10),
                      (7, 10),
                      (8, 10), (9, 10), (10, 10)]
        }

    # The grid (13x13)
    tiles = [(i, j) for i in range(13) for j in range(13)]

    def __init__(self,rows,cols,width,height,version,win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.version = version
        self.selected = None
        self.model = None
        self.win = win

    # Get co-ordinate of start of every word in a list
    def get_word_coords(self):
        word_coords = []
        for count in range(169):
            word = {}
            if self.tiles[count] in self.boundaries[self.version]:
                continue
            elif self.tiles[count] == (0, 0):
                if self.tiles[count + 1] not in self.boundaries[self.version]:
                    word.update({'across': self.tiles[count]})
                if self.tiles[count + 13] not in self.boundaries[self.version]:
                    word.update({'down': self.tiles[count]})
            elif self.tiles[count][0] == 0:
                if self.tiles[count - 1] in self.boundaries[self.version] and self.tiles[count + 1] not in self.boundaries[self.version]:
                    word.update({'across': self.tiles[count]})
                elif self.tiles[count + 13] not in self.boundaries[self.version]:
                    word.update({'down': self.tiles[count]})
            elif self.tiles[count][1] == 0:
                if count < 168:
                    if self.tiles[count + 1] not in self.boundaries[self.version]:
                        word.update({'across': self.tiles[count]})
                if count < 155:
                    if self.tiles[count - 13] in self.boundaries[self.version] and self.tiles[count + 13] not in self.boundaries[self.version]:
                        word.update({'down': self.tiles[count]})
            if count < 168:
                if self.tiles[count - 1] in self.boundaries[self.version] and self.tiles[count + 1] not in self.boundaries[self.version]:
                    word.update({'across': self.tiles[count]})
            if count < 155:
                if self.tiles[count - 13] in self.boundaries[self.version] and self.tiles[count + 13] not in self.boundaries[self.version]:
                    word.update({'down': self.tiles[count]})
            count += 1
            word_coords.append(word)
        word_coords = list(filter(None, word_coords))
        words_df = pd.DataFrame(word_coords)
        return words_df

    def find_end_across(self,start):
        same_row = []
        for i in range(len(self.boundaries[self.version])):
            if self.boundaries[self.version][i][0] == start[0] and self.boundaries[self.version][i][1] > start[1]:
                same_row.append(self.boundaries[self.version][i])
        if not same_row:
            end_coord = (start[0], 12)
        else:
            end_coord = (same_row[0][0], same_row[0][1] - 1)
        return end_coord

    def find_end_down(self,start):
        same_column = []
        for i in range(len(self.boundaries[self.version])):
            if self.boundaries[self.version][i][1] == start[1] and self.boundaries[self.version][i][0] > start[0]:
                same_column.append(self.boundaries[self.version][i])
        if not same_column:
            end_coord = (12, start[1])
        else:
            end_coord = (same_column[0][0] - 1, same_column[0][1])
        return end_coord

    def find_coords_across(self,start, end):
        word = []
        for i in range(start[1], end[1] + 1, 1):
            word.append((start[0], i))
        return word

    def find_coords_down(self,start, end):
        word = []
        for i in range(start[0], end[0] + 1, 1):
            word.append((i, start[1]))
        return word

    def words_full(self):
        df = self.get_word_coords()
        list_of_words = []
        for i in range(df.shape[0]):
            if type(df.iloc[i]['across']) is tuple:
                end = self.find_end_across(df.iloc[i]['across'])
                coords_of_word = self.find_coords_across(df.iloc[i]['across'], end)
                list_of_words.append([df.iloc[i]['across'], 'across', len(coords_of_word), coords_of_word])
            if type(df.iloc[i]['down']) is tuple:
                end = self.find_end_down(df.iloc[i]['down'])
                coords_of_word = self.find_coords_down(df.iloc[i]['down'], end)
                list_of_words.append([df.iloc[i]['down'], 'down', len(coords_of_word), coords_of_word])
        words_full_df = pd.DataFrame(list_of_words, columns=['start', 'drn', 'len', 'coords'])
        print(words_full_df)
        return words_full_df

    def draw(self):
        # Draw Grid Lines
        gap = self.height / 13
        for i in range(self.rows+1):
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.height, i*gap))
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height))
        # Draw black squares
        for i in range(len(self.boundaries[self.version])):
            row, col = self.boundaries[self.version][i]
            pygame.draw.rect(self.win, (0, 0, 0), (col * (540 / 13), row * (540 / 13), (540 / 13) + 1, (540 / 13) + 1))

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].selected = False

        self.tiles[row][col].selected = True
        self.selected = (row, col)

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
    board.draw()


def main():
    win = pygame.display.set_mode((1200,600))
    pygame.display.set_caption("Crossword")
    board = Grid(13, 13, 1200, 540,'Metro_v1', win)
    board.words_full()
    key = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    key = 'a'
                if event.key == pygame.K_b:
                    key = 'b'
                if event.key == pygame.K_c:
                    key = 'c'
                if event.key == pygame.K_d:
                    key = 'd'
                if event.key == pygame.K_e:
                    key = 'e'
                if event.key == pygame.K_f:
                    key = 'f'
                if event.key == pygame.K_g:
                    key = 'g'
                if event.key == pygame.K_h:
                    key = 'h'
                if event.key == pygame.K_i:
                    key = 'i'
                if event.key == pygame.K_j:
                    key = 'j'
                if event.key == pygame.K_k:
                    key = 'k'
                if event.key == pygame.K_l:
                    key = 'l'
                if event.key == pygame.K_m:
                    key = 'm'
                if event.key == pygame.K_n:
                    key = 'n'
                if event.key == pygame.K_o:
                    key = 'o'
                if event.key == pygame.K_p:
                    key = 'p'
                if event.key == pygame.K_q:
                    key = 'q'
                if event.key == pygame.K_r:
                    key = 'r'
                if event.key == pygame.K_s:
                    key = 's'
                if event.key == pygame.K_t:
                    key = 't'
                if event.key == pygame.K_u:
                    key = 'u'
                if event.key == pygame.K_v:
                    key = 'v'
                if event.key == pygame.K_w:
                    key = 'w'
                if event.key == pygame.K_x:
                    key = 'x'
                if event.key == pygame.K_y:
                    key = 'y'
                if event.key == pygame.K_z:
                    key = 'z'

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
