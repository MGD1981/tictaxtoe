import json
from random import choice
import pdb
import urllib, urllib2
import socket


def resetboard():
    return [0 for x in range(0,9)]

def evalboard(board):

    if (abs((board[0] + board[1] + board[2])) == 3 or
          abs((board[3] + board[4] + board[5])) == 3 or
          abs((board[6] + board[7] + board[8])) == 3 or
          abs((board[0] + board[4] + board[8])) == 3 or
          abs((board[2] + board[4] + board[6])) == 3 or
          abs((board[0] + board[3] + board[6])) == 3 or
          abs((board[1] + board[4] + board[7])) == 3 or
          abs((board[2] + board[5] + board[8])) == 3):
        return 1
    else:
        return 0

def turn(board):
    if sum(board) == 0:
        return 1
    return -1
 
def minimax(board):

    p = turn(board)
    alpha = -10  
    best_move = -1

    for x in range(0,9):
        if board[x] != 0: continue
        board[x] = p
        if winstate(board) != 0:
            alpha = evalboard(board)
            board[x] = 0
            return (alpha, 0)
        prev_a = alpha
        alpha = max(alpha, -1 * minimax(board)[0])
        if alpha > prev_a:        
            best_move = x
        board[x] = 0
    return (alpha, best_move)


def selectmove(board):
    p = turn(board)    
    if board.count(0) == 1:
        best_move = board.index(0)
    else:
        _, best_move = minimax(board)
    board[best_move] = p
    return board

def winstate(board):
    if 0 not in board: return  2
    if evalboard(board) != 0: return 1
    return 0

def printboard(board):
    print '\n'
    s = "".join((str(board)))
    s = s.replace('-1','O').replace('1','X').replace('0','_').replace(
        ',',"").replace('[',"").replace(']', "")
    print s[0:5]
    print s[6:11]
    print s[12:17]

def req(route, board=None):
    if board:
        return json.loads(urllib2.urlopen(HOST + route,
               data=urllib.urlencode({'data':json.dumps(
               {'board':board})})).read())
    else:
        return json.loads(urllib2.urlopen(HOST + route, data=board).read())

def get_board(player_id):
    resp = req('/get_board/' + str(player_id))
    return resp['board']

def submit_board(board, player_id):
    resp = req('/submit_board/' + str(player_id), board)
    

def play_request():
    resp = req('/play_request')
    if len(resp) < 2:
        player_id = resp['player2']
    else:
        player_id = resp['player1']
    return player_id

def format_board(board):
    if len(board) < 4:
        board = board['board']
    if isinstance(board[0], unicode):
        for i in board:
            board[i] = int(board[i])
    return board

board = resetboard()
print "\nWould you like to play on a server?"
print "1) Yes"
print "2) No"
choice = raw_input("\n>> ")
print "\n"


if choice == '1': # If a server game
    HOST = raw_input("Server URL: ")
    if HOST == '':
        HOST = 'http://thomasballinger.com:8001'
    print "\nWaiting for server..."
    player_id = play_request()
    print "\nPlayer ID: %d" % player_id
    while winstate(board) == 0:
        board = format_board(get_board(player_id))
        print "\nGameboard received."
        printboard(board)
        t = turn(board)
        if t == -1:
            print "O's turn."
        else:
            print "X's turn."
        if player_id % 2 != 0:
            if t == -1:
                continue
            else:
                board = selectmove(board)
                submit_board(board, player_id)
        else:
            if t == 1:
                continue
            else:
                board = selectmove(board)
                submit_board(board, player_id)
        printboard(board)
        
else:

    while winstate(board) == 0:
        printboard(board)
        board = selectmove(board)

    if winstate(board) == 1:
        print "\nWinner!"
    else:
        print "\nStalemate!"
    printboard(board)
