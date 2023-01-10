from datetime import datetime as dt
from time import time
from random import choice, sample

def t():
    return dt.now().strftime('%D\t%H:%M:%S')

def write_log(*params):
    with open("tictactoe.log", 'a', encoding='utf-8') as logfile:
        logfile.write('\t'.join(list(map(lambda x: str(x), params)))+'\n')


def check_4_win(fld: list):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),  # кортеж выигрышных комбинаций
                 (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for winrec in win_coord:                                 # сравниваем текущее поле с выигрышными комбинациями
        if (fld[winrec[0]] == fld[winrec[1]] == fld[winrec[2]]) and fld[winrec[0]] != ' ':
            return True #fld[winrec[0]]
    return False

def isfull(fld: list):
    for itm in fld:
        if itm == ' ':
            return False
    return True


def bot_choice(gf: list, cia, smart = False):
    if smart:
        oc = '\U00002B55' if cia else '\U0000274C' #opponent_char
        pre_win_dict = {0:((3,6), (4,8), (1,2)), 1:((0,2), (4,7)), 2:((0,1),(6,4), (5,8)),
                        3:((0,6), (4,5)), 4: ((1,7), (2,6), (5,3), (8,0)), 5:((2,8),(3,4)),
                        6:((3,0), (7,8), (4,2)), 7:((4,1), (6,8)), 8:((2,5), (6,7), (0,4))}
        #если на поле есть предвыигрышная ситуация - занимаем это место
        for key, v in pre_win_dict.items():
            for i in range(len(v)):
                if (gf[v[i][0]] == gf[v[i][1]]) and gf[v[i][0]] != ' ' and gf[key] == ' ':
                    return key
        #иначе - занимаем смежные углы
        pos = -1
        for i in sample((0,2,6,8), k=4):
            if gf[i] != oc:
                match i:
                    case 0|8:
                        if gf[2] == ' ' and gf[6] == ' ':
                            pos = choice([2,6])
                            break
                        elif gf[2] == ' ':
                            pos = 2
                            break
                        elif gf[6] == ' ':
                            pos = 6
                            break
                    case 2|6:
                        if gf[0] == ' ' and gf[8] == ' ':
                            pos = choice([0,8])
                            break
                        elif gf[0] == ' ':
                            pos = 0
                            break
                        elif gf[8] == ' ':
                            pos = 8
                            break
        #Если и свободных углов не нашлось - берем любую свободную ячейку
        if pos == -1:
            tmp_l = []
            for i in range(len(gf)):
                if gf[i] == ' ':
                    tmp_l.append[i]
            pos = choice(tmp_l)
    else:
        #Глупый бот - простой рандом из свободных ячеек
        tmp_l = []
        for i in range(len(gf)):
            if gf[i] == ' ':
                tmp_l.append(i)
                pos = choice(tmp_l)
    return pos

def bot_turn(gf: list, cia: bool, smart = False):
        pos = bot_choice(gf, cia, smart)
        gf[pos] = '\U0000274C' if cia else '\U00002B55'
        return (gf, not cia)

if __name__ == '__main__':
    pass