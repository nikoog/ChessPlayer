from chesslib import *

def main():
   board=InitBoard()
   pos=47
   moves = GetPieceLegalMoves(board, pos)
   print(moves)

   board[54]=0
   board[55]=0
   board[46]=0
   board[47]=22

   #board[41]=board[49]
   #board[49]=0
   #board[42]=board[50]
   #board[50]=0
   #board[20]=24
   #board[49]=board[58]
   #board[58]=0
   
   #board[44]=board[52]
   #board[52]=0
   #board[23]=23
   #board[20]=15
   #board[17]=board[9]
   #board[9]=0
   PrintBoard(board)
   moves = GetPieceLegalMoves(board, pos)
   print("piece: ",board[pos]-20)
   print(moves)
   for mv in moves:
      board[mv]="<>"
   PrintBoard(board)
#   board[16]=board[8]
#   board[8]=0
#   board[47]=board[55]
#   board[55]=0
#   board[17]=board[9]
#   board[9]=0
#   board[46]=board[54]
#   board[54]=0
#   board[18]=board[10]
#   board[10]=0
#   board[44]=board[52]
#   board[52]=0
#   board[19]=board[11]
#   board[11]=0
#   PrintBoard(board)
#   player=20
#   opp=10
#   bpos=GetPlayerPositions(board, player)
#   print("Black's positions: ",bpos)
#   accum=[]
#   for pos in bpos:
#      print("pos",pos)
#      moves = GetPieceLegalMoves(board, pos)
#      print("moves: ",moves)
#      for move in moves:
#         if IsMoveSafe(board,pos,move,player):
#            accum+=[pos,move]
#   print("B accum: ",accum)
#
#   curr=56
#   dest=54
#   print(GetPieceLegalMoves(board, 56))
#   #54 shoudlnt be there
#   #PrintBoard(board)
   return True

main()

