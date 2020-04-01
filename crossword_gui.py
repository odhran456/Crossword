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


# Get co-ordinate of start of every word in a list
def get_word_coords(tiles,version):
    word_coords = []
    for count in range(169):
        word = {}
        if tiles[count] in boundaries[version]:
            continue
        elif tiles[count] == (0,0):
            if tiles[count + 1] not in boundaries[version]:
                word.update({'across':tiles[count]})
            if tiles[count + 13] not in boundaries[version]:
                word.update({'down':tiles[count]})
        elif tiles[count][0] == 0:
            if tiles[count - 1] in boundaries[version] and tiles[count + 1] not in boundaries[version]:
                word.update({'across':tiles[count]})
            elif tiles[count + 13] not in boundaries[version]:
                word.update({'down':tiles[count]})
        elif tiles[count][1] == 0:
            if count < 168:
                if tiles[count + 1] not in boundaries[version]:
                    word.update({'across':tiles[count]})
            if count < 155:
                if tiles[count - 13] in boundaries[version] and tiles[count + 13] not in boundaries[version]:
                    word.update({'down':tiles[count]})
        if count < 168:
            if tiles[count - 1] in boundaries[version] and tiles[count + 1] not in boundaries[version]:
                word.update({'across':tiles[count]})
        if count < 155:
            if tiles[count - 13] in boundaries[version] and tiles[count + 13] not in boundaries[version]:
                word.update({'down':tiles[count]})
        count+=1
        word_coords.append(word)
    word_coords = list(filter(None, word_coords))
    words_df = pd.DataFrame(word_coords)
    return words_df


def find_end_across(start):
    same_row = []
    for i in range(len(boundaries['version_1'])):
        if boundaries['version_1'][i][0] == start[0] and boundaries['version_1'][i][1] > start[1]:
            same_row.append(boundaries['version_1'][i])
    if not same_row:
        end_coord = (start[0],12)
    else:
        end_coord = (same_row[0][0],same_row[0][1]-1)
    print(start,end_coord)
    return end_coord


def find_end_down(start):
    same_column = []
    for i in range(len(boundaries['version_1'])):
        if boundaries['version_1'][i][1] == start[1] and boundaries['version_1'][i][0] > start[0]:
            same_column.append(boundaries['version_1'][i])
    if not same_column:
        end_coord = (12,start[1])
    else:
        end_coord = (same_column[0][0]-1,same_column[0][1])
    print(start,end_coord)
    return end_coord


def find_coords_across(start,end):
    word = []
    for i in range(start[1],end[1]+1,1):
        word.append((start[0],i))
    return word


def find_coords_down(start,end):
    word = []
    for i in range(start[0],end[0]+1,1):
        word.append((i,start[1]))
    return word


def words_full(df):
    list_of_words = []
    for i in range(df.shape[0]):
        if type(df.iloc[i]['across']) is tuple:
            end = find_end_across(df.iloc[i]['across'])
            coords_of_word = find_coords_across(df.iloc[i]['across'],end)
            list_of_words.append([df.iloc[i]['across'],'across',len(coords_of_word),coords_of_word])
        if type(df.iloc[i]['down']) is tuple:
            end = find_end_down(df.iloc[i]['down'])
            coords_of_word = find_coords_down(df.iloc[i]['down'],end)
            list_of_words.append([df.iloc[i]['down'],'down',len(coords_of_word),coords_of_word])
    words_full_df = pd.DataFrame(list_of_words,columns=['start','drn','len','coords'])
    print(words_full_df)
    return words_full_df


a = get_word_coords(tiles,'version_1')
words_full(a)


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

