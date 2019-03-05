"""
filename: 2aiplaychess.py
comp (black) vs. comp (white) chess game
time to see how ai faces off itself...
time to incorporate the search tree using minimax
"""
from chesslib import *
from weightedchesslib import *
from treechesslib import *
from random import randint

#the game.
def main():
   done = False
   board = InitBoard()
   print("\nBoard indices are defined as follows:")
   ls=[" "+str(i) for i in range(0,10)]+[str(i) for i in range(10,8*8)]
   PrintBoard(ls)
   print("starting the game!") 
 
   summary=[]
   cnt=0
   while True:
      cnt+=1
      PrintBoard(board)
      summary+=[list(board)]
      #white - automatic player
      while(True):
         player=10
         opp=20
         depth=3
         move=alphabetaminimax(board,depth,player,opp)
         if move==[]:
            print("white out of moves- black wins~")
            print("INFO: number of turns = ",cnt)
            print("-------> Game board summary <-------")
            for bd in summary:
               PrintBoard(bd)
            return 20
         curr=move[0]
         dest=move[1]
         test=ProcessMove(board, curr, dest, player)
         summary+=[list(board)]
         if (test[0]==True): #successfully moved.
            if len(test)==2: #did kill something..
               if test[1] == 5+opp: #killed the king!
                  print("White killed Black king: white wins!")
                  print("INFO: number of turns = ",cnt)
                  print("-------> Game board summary <-------")
                  for bd in summary:
                     PrintBoard(bd)
                  return 10
            break
         #end of white's while loop#
      
      cnt+=1
      PrintBoard(board)

      #black - automatic player
      while(True):
         player=20
         opp=10
         depth=2
         #move=pureminimax(board,depth,player,opp)
         move=alphabetaminimax(board,depth,player,opp)
         #move=GenBestMove(board,player,opp)
         ##### ONLY AS DEBUGGER REMOVE LATER THX
         if move==False:
            print("move=False in the game and im using another so i dont crash.")
            move=[48,40]
         #####   
         print("move to process: ",move)
         if move==[]:
            print("black out of moves- white wins~")
            print("INFO: number of turns = ",cnt)
            print("-------> Game board summary <-------")
            for bd in summary: 
               PrintBoard(bd)
            return 10
         curr=move[0]
         dest=move[1]
         print("B curr=",curr," dest=",dest)
         test=ProcessMove(board, curr, dest, player)
         summary+=[list(board)]
         if (test[0]==True): #successfully moved.
            if len(test)==2: #did kill something..
               if test[1] == 5+opp: #killed the king!
                  print("Black killed White king: black wins!")
                  print("INFO: number of turns = ",cnt)
                  print("-------> Game board summary <-------")
                  for bd in summary:
                     PrintBoard(bd)
                  return 20
            break
         #end of blacks' while loop


main()
