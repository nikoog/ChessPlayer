"""
filename: 2playchess.py
comp vs. human chess game
using only the weighted method, comp opponent will kill highest if possible.
"""
from chesslib import *
from weightedchesslib import *
from random import randrange

"""
no idea why tf i have this fcn but ok
"""
def CheckBoard(board):
   #what does the board look like if the game has ended?
   Bs=[]
   Ws=[]
   for i in board:
      if i!=0:
         if i-20>0:
            Bs+=[i]
         elif i-10>0:
            Ws+=[i]
   if Bs==[]:
      print("no more black players")
      return [True,10]
   if Ws==[]:
      print("no more white players.")
      return [True,20]
   
   BhasK=False
   for i in Bs:
      if i==25:
         BhasK=True
   if BhasK==False:
      print("Black King gone- white wins!")
      return [True,10]
   
   WhasK=False
   for i in Ws:
      if i==15:
         WhasK=True
   if WhasK==False:
      print("White King gone- black wins!")
      return [True,20]
   return [False]

"""
function: GenBestMove
returns a 2-list of the selected move.
"""
def GenBestMove(board,player,opp):
   bpos=GetPlayerPositions(board, player)
   print("positions: ",bpos)
   accum=[]
   for pos in bpos:
#      print("pos",pos)
      moves = GetPieceLegalMoves(board, pos)
#      print("moves: ",moves)
      for move in moves:
         if IsMoveSafe(board,pos,move,player):
            accum+=[pos,move]
   print("accum: ",accum)
   if accum==[]:
      print("no moves available")
      return []
   m=randrange(0,len(accum),2)
   print("m",m)
   curr=accum[m]
   dest=accum[m+1]
   print("auto player curr=",curr," dest=",dest)
   return [curr,dest]
   

#the game.
def main():
   done = False
   board = InitBoard()
   print("\nBoard indices are defined as follows:")
   ls=[" "+str(i) for i in range(0,10)]+[str(i) for i in range(10,8*8)]
   PrintBoard(ls)
   print("starting the game!") 
   
   while True:
      PrintBoard(board)

      #white - human player
      while(True):
         legal=[]
         player=10
         opp=20
         if CheckKing(board,player)[0]==True:
            print("WCheckKing=>True")
            legal=CheckKing(board,player)[1]
            if legal==[]:
               print("no saving moves for white: black wins!")
               return 20
         print("White player: make ur move.")
         curr = input("piece to be moved? ")
         dest = input("where to? ")
         king_wont_commit_suicide=True
         if legal!=[]: #gotta save the king!
            print("king suicide...")
            print("legal=",legal)
            king_wont_commit_suicide=False
            for i in range(0,len(legal),2):
               if legal[i]==int(curr):
                  if legal[i+1]==int(dest):
                     print("okie we legally saving king!")
                     king_wont_commit_suicide=True
            if king_wont_commit_suicide==False:
               print("please try to save your king, White")
         if king_wont_commit_suicide==True: #you really want that to be True before moving. 
            #actual processing of the move.
            test=ProcessMove(board, curr, dest, player)
            if (test[0]==True): #successfully moved.
               if len(test)==2: #did kill something..
                  if test[1] == 5+opp: #killed the king!
                     print("White killed Black king: white wins!")
                     return 10
               break
         #end of white's while loop#
      
      PrintBoard(board)

      #black - automatic player
      while(True):
         player=20
         opp=10
         move=GenBestMove(board,player,opp)
         print("move to process: ",move)
         if move==[]:
            print("black out of moves- white wins~")
            return 10
         curr=move[0]
         dest=move[1]
         print("B curr=",curr," dest=",dest)
         test=ProcessMove(board, curr, dest, player)
         if (test[0]==True): #successfully moved.
            if len(test)==2: #did kill something..
               if test[1] == 5+opp: #killed the king!
                  print("Black killed White king: black wins!")
                  return 20
            break
         #end of blacks' while loop
main()
