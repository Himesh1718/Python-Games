import socket
import threading


class TicTacToe:
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "0"
        self.winner = None
        self.gameOver = False

        self.counter = 0

    def hostGame(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()

        self.you = "X"
        self.opponent = "0"
        threading.Thread(target=self.handleConnection, args=(client,)).start()
        server.close()

    def connectToGame(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = "0"
        self.opponent = "X"
        threading.Thread(target=self.handleConnection, args=(client,)).start()

    def handleConnection(self, client):
        while not self.gameOver:
            if self.turn == self.you:
                move = input("Enter a move (row,column): ")
                if self.checkValidMove(move.split(',')):
                    client.send(move.encode('utf-8'))
                    self.applyMove(move.split(','), self.you)
                    self.turn = self.opponent
                else:
                    print('Invalid move!')
            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                    break
                else:
                    self.applyMove(data.decode(
                        'utf-8').split(','), self.opponent)
                    self.turn = self.you
        client.close()

    def applyMove(self, move, player):
        if self.gameOver:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.printBoard()
        if self.checkIfWon():
            if self.winner == self.you:
                print('You win!')
                exit()
            elif self.winner == self.opponent:
                print('You lose!')
                exit()
            else:
                if self.counter == 9:
                    print("It's a tie!")
                    exit()

    def checkValidMove(self, move):
        return self.board[int(move[0])][int(move[1])] == " "

    def checkIfWon(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.gameOver = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                self.winner = self.board[1][col]
                self.gameOver = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            self.winner = self.board[0][0]
            self.gameOver = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            self.winner = self.board[0][0]
            self.gameOver = True
            return True
        return False

    def printBoard(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print('-----------')


game = TicTacToe()
game.connectToGame('localhost', 9999)
