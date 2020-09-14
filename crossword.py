import pygame
import pandas as pd
from random import randrange
import time


pygame.font.init()

boundaries = {
    'Metro_v1': [(0, 1), (0, 3), (0, 5), (0, 6), (1, 8), (1, 10), (1, 12), (2, 1), (2, 3), (2, 5), (2, 6), (3, 5),
                 (3, 10), (3, 12), (4, 4), (4, 9), (5, 0), (5, 2), (5, 7), (5, 12), (6, 0), (6, 1), (6, 11), (6, 12),
                 (7, 0), (7, 5), (7, 10), (7, 12), (8, 3), (8, 8), (9, 0), (9, 2), (9, 7), (10, 6), (10, 7), (10, 9),
                 (10, 11), (11, 0), (11, 2), (11, 4), (12, 6), (12, 7), (12, 9), (12, 11)],
    'EY': [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (4, 2), (5, 2), (6, 2), (6, 3), (6, 4), (6, 5), (7, 2), (8, 2),
           (9, 2), (10, 2), (10, 3), (10, 4), (10, 5), (2, 8), (2, 12), (3, 9), (3, 11), (4, 10), (5, 10), (6, 10),
           (7, 10), (8, 10), (9, 10), (10, 10)]
}

# The grid (13x13)
tiles = [(i, j) for i in range(13) for j in range(13)]

highlighted_tile = None
previous_tile = None
current_tile = None
current_board = None


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

    return words_full_df


def show_highlighted_word(version):
    df = words_full(version=version)
    if previous_tile != highlighted_tile:
        for x, y in df.iterrows():
            if highlighted_tile in y['coords']:
                highlighted_word = y
                # highlighted_word = y['coords']
                break
    # if you click on the same tile twice, swap from vertical word to horizontal word
    elif previous_tile == highlighted_tile:
        df = df.iloc[::-1]
        for x, y in df.iterrows():
            if highlighted_tile in y['coords']:
                highlighted_word = y
                # highlighted_word = y['coords']
                break
    return highlighted_word


def get_clue_nums(version):
    df = words_full(version)
    num = 1
    num_col = []
    for row in df.itertuples():
        # do a check here to see if any tuple from cur row is in prev row, if so dont increase num +1
        num += 1
        num_col.append(num)
    return num_col


def draw(win, height, rows, version):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 40)
    fnt_digits = pygame.font.SysFont("comicsans", 20)

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
        for i in show_highlighted_word(version=version)['coords']:
            pygame.draw.rect(win, (255, 0, 0), (i[1] * gap, i[0] * gap, gap, gap), 5)
    # Draw filled in letters
    for tile_loc, letter in current_board.items():
        text = fnt.render(letter, 1, (0, 0, 0))
        if letter is not None:
            win.blit(text, (tile_loc[1] * gap + (gap / 3), tile_loc[0] * gap + (gap / 4)))
    # Draw the clue numbers
    for row in words_full(version).itertuples():
        # ill implement get_clue_num() instead of words_full().itertuples()
        clue_num = fnt_digits.render(str(row.Index), 1, (0, 0, 0))
        win.blit(clue_num, (row.start[1] * gap, row.start[0] * gap))


def click(pos, height, version):
    global highlighted_tile
    global previous_tile
    # This is a measure to swap from vertical word to horizontal word
    previous_tile = highlighted_tile

    if pos[0] < height and pos[1] < height:
        gap = height / 13
        x = pos[0] // gap
        y = pos[1] // gap
        highlighted_tile = (int(y), int(x))

        if highlighted_tile in boundaries[version]:
            highlighted_tile = None
        else:
            return int(y), int(x)
    else:
        highlighted_tile = None
        return None


def auto_complete(version, word_num, trial):
    # some sort of back tracker algo . . .
    curr_word_coords = words_full(version).iloc[word_num]['coords']

    # pick a random word from the appropriate list of english words of the correct length
    curr_word_len = words_full(version).iloc[word_num]['len']
    n_letter_words = pd.read_csv('words/' + str(curr_word_len) + '.csv')

    # Check if your trial num is out of bounds due to iterations
    if trial > n_letter_words.shape[0] - 1:
        # TODO: put function in here that removes last crossword entry and continues onto next suitable word.
        #  This function will need to pick up from where auto_complete() left off in trial num. Also needs to know
        #  what was the last word played to remove those letters.
        pass

    word_candidate = n_letter_words.iloc[trial][0]
    print(word_candidate, str(trial) + '/' + str(n_letter_words.shape[0]))

    # see are any letters filled into that word already
    for count in range(len(curr_word_coords)):
        if current_board[curr_word_coords[count]] is None or current_board[curr_word_coords[count]] == word_candidate[count]:
            continue
        else:
            # if the word does not fit, recursively run the function until a word down the line fits. The whole function
            # will just return the first word it comes across that fits, and the co-ordinates of where to put that word.
            # When you are iterating through the trial word in 3.csv etc, your trial+=1 will eventually lead to out of
            # range error. Near the start of auto_complete(), check is trial in bounds!
            word_candidate, curr_word_coords = auto_complete(version, word_num, trial + 1)

    return word_candidate, curr_word_coords


def main():
    win = pygame.display.set_mode((1200, 600))
    height = 540
    width = 1200
    rows = 13
    pygame.display.set_caption("Crossword")
    run = True
    key = None
    version = 'Metro_v1'

    iteration_count = 0

    # Make a dict storing the value for each tile
    global current_board
    # Whenever you click a square, the current tile you can edit will become the first tile in that word. If you type in
    # a letter, the current tile will become the next letter in that word. If you click on a new square, you will jump
    # to the first tile of the next word.
    global current_tile
    current_board = dict.fromkeys([x for x in tiles if x not in boundaries[version]], None)

    while run:
        # Slowing down the loop to save my CPU resources!!!!
        time.sleep(0.2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = click(pos, height, version)
                if clicked:
                    # this tracks what letter in the word you are
                    list_position = 0
                    current_tile = show_highlighted_word(version=version)['coords'][list_position]
                    key = None

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

                # Autocomplete the grid
                if event.key == pygame.K_0:
                    # if the word fits, move onto the next empty slot. Otherwise, if it returns false, it won't move on
                    # and it will just try another word in there. Cycle through the words in the n_letter.csv, if a
                    # word fits reset the trial count, but otherwise keep going until you try all the words in the csv
                    trial_count = 0
                    word, coords = auto_complete(version=version, word_num=iteration_count, trial=trial_count)
                    print(word, coords)
                    # put that word in the slot, by putting each letter into each slot in the whole board view
                    for i in range(len(coords)):
                        current_board[coords[i]] = word[i]

                    if iteration_count < words_full(version).shape[0] - 1:
                        iteration_count += 1

        # When you type in a key, update that value in the dictionary of letters, and turn off the key and clicked.
        # Pressing a key or clicking somewhere will lead to the next letter.
        if key:
            current_board[current_tile] = key
            key = None
            # if you haven't reached the end of the word yet, move on step farther
            if show_highlighted_word(version=version)['len'] > list_position + 1:
                list_position += 1
                current_tile = show_highlighted_word(version=version)['coords'][list_position]

        draw(win=win, height=height, rows=rows, version=version)
        pygame.display.update()


main()
