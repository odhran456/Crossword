import pygame
import pandas as pd


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
highlighted_tile = None


def get_word_coords(version):
    word_coords = []
    for count in range(169):
        word = {}
        if tiles[count] in boundaries[version]:
            continue
        elif tiles[count] == (0, 0):
            if tiles[count + 1] not in boundaries[version]:
                word.update({'across': tiles[count]})
            if tiles[count + 13] not in boundaries[version]:
                word.update({'down': tiles[count]})
        elif tiles[count][0] == 0:
            if tiles[count - 1] in boundaries[version] and tiles[count + 1] not in boundaries[version]:
                word.update({'across': tiles[count]})
            elif tiles[count + 13] not in boundaries[version]:
                word.update({'down': tiles[count]})
        elif tiles[count][1] == 0:
            if count < 168:
                if tiles[count + 1] not in boundaries[version]:
                    word.update({'across': tiles[count]})
            if count < 155:
                if tiles[count - 13] in boundaries[version] and tiles[count + 13] not in boundaries[version]:
                    word.update({'down': tiles[count]})
        if count < 168:
            if tiles[count - 1] in boundaries[version] and tiles[count + 1] not in boundaries[version]:
                word.update({'across': tiles[count]})
        if count < 155:
            if tiles[count - 13] in boundaries[version] and tiles[count + 13] not in boundaries[version]:
                word.update({'down': tiles[count]})
        count += 1
        word_coords.append(word)
    word_coords = list(filter(None, word_coords))
    words_df = pd.DataFrame(word_coords)
    return words_df


def find_end_across(start, version):
    same_row = []
    for i in range(len(boundaries[version])):
        if boundaries[version][i][0] == start[0] and boundaries[version][i][1] > start[1]:
            same_row.append(boundaries[version][i])
    if not same_row:
        end_coord = (start[0], 12)
    else:
        end_coord = (same_row[0][0], same_row[0][1] - 1)
    return end_coord


def find_end_down(start, version):
    same_column = []
    for i in range(len(boundaries[version])):
        if boundaries[version][i][1] == start[1] and boundaries[version][i][0] > start[0]:
            same_column.append(boundaries[version][i])
    if not same_column:
        end_coord = (12, start[1])
    else:
        end_coord = (same_column[0][0] - 1, same_column[0][1])
    return end_coord


def find_coords_across(start, end):
    word = []
    for i in range(start[1], end[1] + 1, 1):
        word.append((start[0], i))
    return word


def find_coords_down(start, end):
    word = []
    for i in range(start[0], end[0] + 1, 1):
        word.append((i, start[1]))
    return word


def words_full(version):
    df = get_word_coords(version=version)
    list_of_words = []
    for i in range(df.shape[0]):
        if type(df.iloc[i]['across']) is tuple:
            end = find_end_across(start=df.iloc[i]['across'], version=version)
            coords_of_word = find_coords_across(start=df.iloc[i]['across'], end=end)
            list_of_words.append([df.iloc[i]['across'], 'across', len(coords_of_word), coords_of_word])
        if type(df.iloc[i]['down']) is tuple:
            end = find_end_down(start=df.iloc[i]['down'], version=version)
            coords_of_word = find_coords_down(start=df.iloc[i]['down'], end=end)
            list_of_words.append([df.iloc[i]['down'], 'down', len(coords_of_word), coords_of_word])
    words_full_df = pd.DataFrame(list_of_words, columns=['start', 'drn', 'len', 'coords'])
    print(words_full_df)
    return words_full_df


def draw(win, height, rows, version):
    # Draw Grid Lines
    gap = height / 13
    for i in range(rows + 1):
        pygame.draw.line(win, (0, 0, 0), (0, i * gap), (height, i * gap))
        pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, height))
    # Draw black squares
    for i in range(len(boundaries[version])):
        row, col = boundaries[version][i]
        pygame.draw.rect(win, (0, 0, 0), (col * (540 / 13), row * (540 / 13), (540 / 13) + 1, (540 / 13) + 1))
    # Draw highlighted word
    if highlighted_tile is None or highlighted_tile in boundaries[version]:
        pass
    else:
        pygame.draw.rect(win, (255, 0, 0), (highlighted_tile[1] * gap, highlighted_tile[0] * gap, gap, gap), 5)


def redraw_window(win, height, rows, version):
    win.fill((255, 255, 255))
    # Draw grid and board
    draw(win, height, rows, version)


def click(pos, height):
    """
    :param: pos
    :return: (row, col)
    """
    global highlighted_tile

    if pos[0] < height and pos[1] < height:
        gap = height / 13
        x = pos[0] // gap
        y = pos[1] // gap
        highlighted_tile = (int(y), int(x))
        return int(y), int(x)
    else:
        highlighted_tile = None
        return None


def main():
    win = pygame.display.set_mode((1200, 600))
    height = 540
    width = 1200
    rows = 13
    pygame.display.set_caption("Crossword")
    run = True
    key = None
    version = 'Metro_v1'

    words_full(version=version)

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = click(pos, height)
                if clicked:
                    print(clicked[0], clicked[1])
                    key = None

        redraw_window(win=win, height=height, rows=rows, version=version)
        pygame.display.update()


main()

