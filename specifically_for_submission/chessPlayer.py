"""
filename: chessPlayer.py
contains the chessPlayer function as required by Assignment A CSC 190
"""

#from chessPlayer_chesslib import *
#from chessPlayer_weightedchesslib import *
from chessPlayer_treechesslib import *
#check, but all should come from treechesslib

"""
function: chessPlayer
returns [status, move, candidateMoves, evalTree]
 - status=True indicates function succeeded; status=False indicates function cannot
   compute move.
 - move is a 2-list of indices (0-63)
   - move[0] is current location
   - move[1] is destination
 - candidateMoves is a list of 2-lists where
   - candidateMoves[i][0] is 2-list corresponding to move
   - candidateMoves[i][1] is some float indicating how good/bad the move is
 - evalTree is my alphabetaminmax tree- the tree of trees, traversed in LEVEL ORDER 
"""
def chessPlayer(board,player):
   #out = [status,move,candidateMoves,evalTree]
   out=[False,False,False,False]
   if player==10:
      opp=20
   elif player==20:
      opp=10
   else: #...lol who're u playing with?
      print("invalid player")
      return out 
   
   depth=2
   alphabeta = alphabetaeverything(board,depth,player,opp)
#   print("INFO: len(alphabeta)=",len(alphabeta))
   # alphabeta[0]: the full tree
   # alphabeta[1]: the chosen move, which is itself represented as a 2-list
   
   #if any returned false then we have a problem
   
   if alphabeta[0]==False:
      print("ERR: no tree?")
      return out
   traverse = (alphabeta[0]).Get_LevelOrder()
#   print("Level-Order Traversal: ",traverse)

   ## add the traversal of the tree to return list! ##
   out[3] = traverse

   if (alphabeta[1])[0] == False or (alphabeta[1])[1] == False:
      print("ERR: weird move")
      return out
   
   ## add move to return list! ##   
   out[1]=alphabeta[1]

   ## get all potential moves and add each move + board value to return list! ##
   move_options=playerMoveOptions(board,player)
   candidateMoves=[]
   for mv in move_options:
      candidateMoves+=[[mv,TestMoveWeight(board,mv[0],mv[1],player,opp)]]
   out[2]=list(candidateMoves)

   ## now that all else is ok, status is True! ##
   out[0]=True

#   print("=====CHESS PLAYER=====")
#   print("++++status: out[0] = ",out[0])
#   print("++++move: out[1] = ",out[1])
#   print("++++candidate moves: out[2] = ",out[2])
#   print("++++evalTree: out[3] = ",out[3])
#lmao also get rid of ALL YOUR PRINTS girl XD   
   return out


   

