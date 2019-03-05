"""
filename: 3playchess.py
comp (black) vs. human (white) chess game
improving the previous thing... ______
time to incorporate the search tree using minimax
"""
#from chesslib import *
#from weightedchesslib import *
from treechesslib import *

#from chessPlayer import *

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
         depth=2
         #move=pureminimax(board,depth,player,opp)
         move=alphabetaminimax(board,depth,player,opp)
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
