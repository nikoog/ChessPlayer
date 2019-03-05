"""
filename: weightedchesslib.py
adds to chesslib the method of determining player moves by board weightings.
"""
from chesslib import *

#board: 8x8
#occupied pos'n value = offset+value
#player 10 is white, 20 is black

################ The Weighted Board Method ################
"""
function: GetPieceStrength
returns relative strength of a piece
NOTE: this only returns the POSITIVE of strength. Convert within functions as necessary.
"""
def GetPieceStrength(piece):
   if piece==0:
      return 10
   elif piece==1:
      return 30
   elif piece==2:
      return 30
   elif piece==3:
      return 50
   elif piece==4: #increased queen weighting
      return 200
   elif piece==5: #...and thus king weighting as well.
      return 1500
   else:
      return -10000000000000000

"""
function: GetBoardStrength
returns BoardStrength given board, player and opp
BoardStrength is a number whose positive indiccates a good situtation for PLAYER.
negative indicates player is doing poorly, while OPP is doing well.

NOTE: this takes into the account the following in determining board strength:
   - PlayerStrength and OppStrength, which are numbers indicating strength based
     on values of pieces each respective side has.
   - (something about evaluating based on player's position on the board) (not high 
     priority but perhaps consider later)
   - (something about preserving pieces that are super important to me)(DO THIS ONE)
   - (something based on how close player's pieces are to enemy king and how close opp's
     are to player's king) (may or may not do this part)

"""
def GetBoardStrength(board,player,opp):
   PlayerInds=GetPlayerPositions(board, player)
   #print("PLAYERINDS ",PlayerInds)
   OppInds=GetPlayerPositions(board, opp)
  
   #part 1: based purely on PlayerStrength, OppStrength
   PlayerStrength=0
   for i in PlayerInds:
      PlayerStrength+=GetPieceStrength(board[i]-player)
   OppStrength=0
   for i in OppInds:
      OppStrength+=GetPieceStrength(board[i]-opp)
#   print("PlayerStrength=",PlayerStrength," OppStrength=",OppStrength)
   BoardStrength=PlayerStrength-OppStrength
#   print("BoardStrength=",BoardStrength)

   #part 2: consider how threatened i am in a current board position, and subtract value accordingly.
   for i in PlayerInds:
      #print("iiiiiii = ",i)
      if IsPositionUnderThreat(board,i,player): #lmao i wouldve thought it should be player, but its working with opp and not player?
#         print("Board Strength reduced due to position threat")
#         print("piece under threat: ",board[i]-player)
         BoardStrength -= 0.5*GetPieceStrength(board[i]-player)

   #part 3: consider value of pieces I can kill vs. value of pieces opponent can kill
   #how much value can opponent get by killing my pieces?
   opp_kill_val=0
   for i in PlayerInds:
      if IsPositionUnderThreat(board,i,player):
         opp_kill_val+=GetPieceStrength(board[i]-player)
   #how much value will I gain by killing my opponent's pieces?
   player_kill_val=0
   for i in OppInds:
      if IsPositionUnderThreat(board,i,opp):
         player_kill_val+=GetPieceStrength(board[i]-opp)
#   print("INFO: opp_kill_val=",opp_kill_val," player_kill_val=",player_kill_val)
   net_kill_val=player_kill_val-opp_kill_val
   #add to BoardStrength with a factor... (note: factor a complete guess supported by empirical observation rn)
   factor=0.25
#   print("BoardStrength before adding net_kill_val: ",BoardStrength)
   BoardStrength += factor*net_kill_val
#   print("BoardStrength after adding net_kill_val: ",BoardStrength)
   
   #lmao those parts arent happening any time soon.
   #####part 2: consider favorable positions
   #####part 3: consider nearness to king of either side

   return BoardStrength

"""
function: TestMoveWeight
returns BoardStrength as it would be if the given move were executed.
"""
def TestMoveWeight(board,curr,dest,player,opp):
   TestBoard=list(board)
   TestBoard[dest]=TestBoard[curr]
   TestBoard[curr]=0
   TstWeight=GetBoardStrength(TestBoard,player,opp)
   return TstWeight

"""
function: Move2KillHighest
returns 2-list, out, st:
 - out[0]=MoveWeight, which is the weight to be added to the BoardWeight as a result of 
   the move. This will either be 0 or positive- negative moves are not considered
   NOTE THIS MAY HAVE TO CHANGE IN THE FUTURE BUT ITS OK FOR NOW.
 - out[1]=strongestMove, a 2-list of location to be moved.
NOTE: return of [0,[]] indicates no strongest move... need to pick move by other means.
"""
def Move2KillHighest(board,player,opp):
   PlayerInds=GetPlayerPositions(board, player)
   OppInds=GetPlayerPositions(board, opp)
   BoardStrength= GetBoardStrength(board,player,opp)
   strongestMove=[]
   MoveWeight=0
   for ind in PlayerInds:
      mvs = GetPieceLegalMoves(board, ind)
      for mv in mvs:
         TstWeight=TestMoveWeight(board,ind,mv,player,opp)
         if TstWeight > MoveWeight:
            MoveWeight=TstWeight
            strongestMove=[ind,mv]
   return [MoveWeight,strongestMove]
                   
"""
function: GenBestMove
returns a 2-list of the selected move.
note: GenBestMove makes its decision for the best move based on:
   - Move2KillHighest
   - IsMoveSafe (recall that this checks whether the position to which my piece moves
     will immediately become a position under threat- and that's it.)
   - picks a random move from those remainng. 
"""
def GenBestMove(board,player,opp):
   movetst=Move2KillHighest(board,player,opp)
   if movetst[0]!=0:
      return movetst[1]
   bpos=GetPlayerPositions(board, player)
#   print("positions: ",bpos)
   accum=[] #will be a list of possible moves, which are also evaluated to be safe.
   for pos in bpos:
#      print("pos",pos)
      moves = GetPieceLegalMoves(board, pos)
#      print("moves: ",moves)
      for move in moves:
         if IsMoveSafe(board,pos,move,player):
            accum+=[pos,move]
#   print("accum: ",accum)
   if accum==[]:
      print("no moves available")
      return []
   m=randrange(0,len(accum),2) #random selection is king. prove me wrong.
#   print("m",m)
   curr=accum[m]
   dest=accum[m+1]
#   print("auto player curr=",curr," dest=",dest)
   return [curr,dest]
      


