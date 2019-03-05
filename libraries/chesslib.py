"""
filename: chesslib.py
defines all the functions necessary to play a basic game of chess.
"""
from random import randrange
#board: 8x8
#occupied pos'n value = offset+value
#player 10 is white, 20 is black

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
 - evalTree can be None (no tree); a tree indicated by a list which is the level-traversal
   of the tree.
"""
def chessPlayer(board,player):
   #combining ProcessMove and such?
   #0 ON BOTTOM RIGHT- FLIP BOARD HERE.
   #TODO: complete me later!
  return True #no idea what im doing XD 



###################### print that board! ######################
"""
function: GetWhiteTiles
returns a list of white tiles
"""
def GetWhiteTiles():
   out=[]
   cnt=-1
   start=-8
   end=0
   while(1):
      cnt+=1
      start+=8
      end+=8
      if end>8*8:
         break
      for i in range(start,end):
          if cnt%2==0:#even row
            if i%2!=0:
               out+=[i]
          else:
            if i%2==0:
               out+=[i]
   return out

"""
function: GetBlackTIles
returns a list of black tiles
"""
def GetBlackTiles():
   out=[]
   cnt=-1
   start=-8
   end=0
   while(1):
      cnt+=1
      start+=8
      end+=8
      if end>8*8:
         break
      for i in range(start,end):
          if cnt%2==0:#even row
            if i%2==0:
               out+=[i]
          else:
            if i%2!=0:
               out+=[i]
   return out

"""
function: PrintBoard
prints the chessboard
"""
def PrintBoard(board):
   #note: row 0 is the BOTTOM row
   print("")
   start=63+8
   end=63
   cnt=8
   Binds = GetBlackTiles()
   Winds = GetWhiteTiles()
   while(1):
      cnt-=1
      start-=8
      end-=8
      if end<-1:
         break
      b="  "
      for i in range(start,end,-1):
         if board[i]==0:
            if i in Binds:
               b="__ "+b
            elif i in Winds:
               b="## "+b
         else:
            b=str(board[i])+" "+b
      b="  "+b
      print(cnt, b)
   print("")
   return True

"""
function: InitBoard
returns a list (the 8x8 board) which has the pieces in their proper starting positions.
"""
def InitBoard():
   board=[0 for x in range(8*8)]
   board[0]=13
   board[1]=11
   board[2]=12
   board[3]=14
   board[4]=15
   board[5]=12
   board[6]=11
   board[7]=13

   for i in range(8,16):
      board[i]=10

   board[56]=23
   board[57]=21
   board[58]=22
   board[59]=24
   board[60]=25
   board[61]=22
   board[62]=21
   board[63]=23

   for i in range(55,56-9,-1):
      board[i]=20

   return board


###################### Basic Game Infos ######################
"""
function: GetPlayerPositions
retuns a list of positions occupied by player
"""
def GetPlayerPositions(board, player):
   out=[]
   if board==[]:
      return []
   for i in range(len(board)):
      if board[i]-player >= 0 and board[i]-player <= 5:
         out+=[i]
   return out

"""
function: GetPieceLegalMoves
retuns a list of indices to which the piece occupying a certain position
may legally move to.
"""
def GetPieceLegalMoves(board, position):
   moves=[]
   if board==[]:
      return []
   
   if board[position]==0:
      print("no pieces here")
      return []
   
   if board[position]-20>=0:
      player=20
      offset=20
      opp=10
      mult=-1 #black pawns move down
   elif board[position]-10>=0:
      player=10
      offset=10
      opp=20
      mult=+1 #white pawns move up
   else:
      return []
   piece = board[position]-offset
  
   ###pawn###
   if piece==0: 
      #print("pawn")
      if position+8*mult < len(board) and position+8*mult >= 0:
         if board[position+8*mult]==0:
            moves+=[position+8*mult]
      if position+9*mult < len(board) and position+9*mult >= 0:
         if ((mult==1 and (position+1)%8==0) or (mult==-1 and position%8==0)):
            rip=True
#            print("rip")
         elif board[position+9*mult]!=0:
            #verify its not a friendly piece...
#            print("pawn verify friendly")
#            print(board[position+9*mult]-player)
            if board[position+9*mult]-opp <= 5 and board[position+9*mult]-opp >= 0:
#               print("added")
               moves+=[position+9*mult]
      if position+7*mult < len(board) and position+7*mult >= 0:
         if (mult==1 and position%8==0) or (mult==-1 and (position+1)%8==0):
            rip=True
#            print("rip")
         elif board[position+7*mult]!=0:
            if board[position+7*mult]-opp <= 5 and board[position+7*mult]-opp >= 0:
               moves+=[position+7*mult]
   
   ###knight###
   if piece==1:
#      print("knight")
      tst = [-17,-15,-10,-6,6,10,15,17]
      rm=[]
      #check wall limitations
      if (position+1)%8==0:#right wall
         rm+=[17,10,-6,-15]
      elif (position+2)%8==0:
         rm+=[10,-6]
      elif (position)%8==0:#left wall
         rm+=[15,6,-10,-17]
      elif (position-1)%8==0:
         rm+=[6,-10]

      if (position+8)>=8*8:
         rm+=[6,15,17,10]
      elif (position+8*2)>=8*8:
         rm+=[15,17]
      elif (position-8)<0:
         rm+=[-17,-15,-10,-6]
      elif (position-8*2)<0:
         rm+=[-17,-15]
         
#      print("position=",position," rm=",rm)
      test=[]
      for i in tst:
         if i not in rm:
            test+=[i]
#      print("test=",test)
      for i in test:
         if board[position+i]==0 or (board[position+i]-opp <= 5 and board[position+i]-opp >= 0):
#            print("added ",position+i)
            moves+=[position+i]
   
   ###bishop or queen###
   if piece==2 or piece==4: 
      #print("bishop/queen")
      cnt=0
      while(True): #top +ve slope
         cnt+=1
         if (position+9*cnt)%8==0:
            break
         if position+9*cnt < len(board) and position+9*cnt>=0 and (position+1)%8 != 0:
            #if occupied
            if board[position+9*cnt]!=0:
               #check if pos'n occupied by friendly piece...
               if board[position+9*cnt]-player <= 5 and board[position+9*cnt]-player >= 0:
                  break
               #not friendly, so it's an enemy.
               else:
#                  print("top+ ",position+9*cnt) ##
                  moves+=[position+9*cnt]
                  break
            #not occupied; may move there.
            else:
#               print("top++ ",position+9*cnt) ##
               moves+=[position+9*cnt]
         else:
            break
      cnt=0
      while(True): #bot +ve slope
         cnt+=1
         if position-9*cnt < len(board) and position-9*cnt>=0 and position%8 != 0:
            if board[position-9*cnt]!=0:
               if board[position-9*cnt]-player <= 5 and board[position-9*cnt]-player >= 0:
                  break
               else:
#                  print("bot+ ",position-9*cnt) ##
                  moves+=[position-9*cnt]
                  break
            else:
#               print("bot++ ",position-9*cnt) ##
               moves+=[position-9*cnt]
            if (position-9*cnt)%8==0:
               break
         else:
            break
      cnt=0
      while(True): #top -ve slope
         cnt+=1
         if position+7*cnt < len(board) and position+7*cnt>=0 and position+7*cnt!=7 and position%8 != 0:
            if board[position+7*cnt]!=0:
               if board[position+7*cnt]-player <= 5 and board[position+7*cnt]-player >=0:
                  break
               else:
#                  print("top- ",position+7*cnt) ##
                  moves+=[position+7*cnt]
                  break
            else:
#               print("top-- ",position+7*cnt) ##
               moves+=[position+7*cnt]
            if (position+7*cnt)%8==0:
               break
         else:
            break
      cnt=0
      while(True): #bot -ve slope
         cnt+=1
         if (position-7*cnt) %8 == 0:
            break
         if position-7*cnt < len(board) and position-7*cnt>=0 and (position+1)%8 != 0:
            if board[position-7*cnt]!=0:
               if board[position-7*cnt]-player<=5 and board[position-7*cnt]-player>=0:
                  break
               else:
#                  print("bot- ",position-7*cnt) ##
                  moves+=[position-7*cnt]
                  break
            else:
#               print("bot-- ",position-7*cnt) ##
               moves+=[position-7*cnt]
         else:
            break
   
   ###rook or queen###
   if piece==3 or piece==4: 
      #print("rook/queen")
      cnt=0
      while(cnt<8): #up
         cnt+=1
         if position+8*cnt < len(board) and position+8*cnt>0:
            if board[position+8*cnt]!=0:
               if board[position+8*cnt]-player<=5 and board[position+8*cnt]-player>=0:
                  break
               else:
#                  print("adding up ",position+8*cnt)
                  moves+=[position+8*cnt]
                  break
#            print("adding upp ",position+8*cnt)
            moves+=[position+8*cnt]
         else:
            break
      cnt=0
      while(cnt<8): #dn
         cnt+=1
         if position-8*cnt < len(board) and position-8*cnt>0:
            if board[position-8*cnt]!=0:
               if board[position-8*cnt]-player<=5 and board[position-8*cnt]-player>=0:
                  break
               else:
#                  print("adding dn ",position-8*cnt)
                  moves+=[position-8*cnt]
                  break
            moves+=[position-8*cnt]
#            print("adding dnn ",position-8*cnt)
         else:
            break
      cnt=0
      while(True): #right
         cnt+=1
#         print("position=",position)
#         print("cnt=",cnt)
         if (position+cnt)%8==0:
#            print("left R cnt=",cnt)
            break
         if position+cnt< len(board) and position+cnt>=0:
            if board[position+cnt]!=0:
               if board[position+cnt]-player <= 5 and board[position+cnt]-player >= 0:
                  break
               else:
#                  print("adding r ",position+cnt)
                  moves+=[position+cnt]
                  break
#            print("adding rr ",position+cnt)
            moves+=[position+cnt]
         else:
            break
      cnt=0
      while(True): #left
         cnt+=1
         if (position+1-cnt)%8==0:
#            print("left L")
            break
         if position-cnt< len(board) and position-cnt>=0:
            if board[position-cnt]!=0:
               if board[position-cnt]-player <= 5 and board[position-cnt]-player>=0:
                  break
               else:
#                  print("adding L", position-cnt)
                  moves+=[position-cnt]
                  break
#            print("adding LL ",position-cnt)
            moves+=[position-cnt]
         else:
            break
   
   ###king###
   if piece==5:
      #print("king")
      rm=[]
      tst=[-9,-8,-7,-1,1,7,8,9]
      if (position+1)%8==0:#wall on right
         rm+=[9,1,-7]
      elif (position)%8==0:#left
         rm+=[7,-1,-9]
      if (position+8)>8*8:
         rm+=[7,8,9]
      elif (position-8)<0:
         rm+=[-9,-8,-7]
      test=[]
      for i in tst:
         if i not in rm:
            test+=[i]
      for i in test:
         if position+i < len(board) and position+i >= 0:
            if board[position+i]-player > 5 or board[position+i]-player < 0:
               moves+=[position+i]
   return moves

"""
function: IsPositionUnderThreat
returns True is the piece at the position is under threat by the opponent,
False otherwise
"""
def IsPositionUnderThreat(board, position, player):
   #if position==False:
   #   print("err: invalid position in fcn IsPositionUnderThreat")
   #   return False
#   print("DEBUG: position = ",position)
   if player==10:
      opp=20
   else:
      opp=10
   oppinds= GetPlayerPositions(board,opp)
   for ind in oppinds:
      oppmoves=GetPieceLegalMoves(board,ind)
      for i in oppmoves:
         if i==position: #my position is an option for opponent
            return True
   return False
   


###################### More Game Functions ######################
"""
function: ProcessMove
takes in the current position and the destination which has been requested
if the move is valid, returns an array [True,opp] where opp is the opposing piece which has
been eliminated by the move, if applicable.
Else if the move is invalid, returns [False]
note: return value will be length 1 list if no kills, length 2 if there are kills.
"""
def ProcessMove(board, curr, dest, player): #payer is 10 or 20
   #returns an array: 
   #0: True/False for success/failure
   #1: value of piece killed, if applicable. (note: 10<=value<=25)
   
   out=[False]
   
   #convert inputs from float default to integers.
   try:
      curr=int(curr)
      dest=int(dest)
   except:
      print("err: invalid location or destination.")
      return [False]
   
   #check if board curr location is empty
   if board[curr]==0:
      print("err: specified location empty to start")
      return [False]
   else:
      #check if piece belongs to player
      piece=board[curr]-player
      if piece > 5 or piece < 0:
         print("err: invalid piece")
         return [False]

   #check the destination is valid and make the move.
   moves = GetPieceLegalMoves(board, curr)
   #print("valid moves: ",moves)
   if dest in moves:
      out+=[board[dest]] #opposing piece (including the 10 or 20)
      board[dest]=board[curr]
      board[curr]=0
      out[0]=True
      return out
   else:
      print("err: destination not a valid one.")
      return [False]

"""
function: playerMoveOptions
returns a list of 2-lists of moves a player can make
"""
def playerMoveOptions(board,player):
   out=[]
   positions=GetPlayerPositions(board, player)
   for pos in positions:
      moves=GetPieceLegalMoves(board, pos)
      for mv in moves:
         out+=[[pos,mv]]
   return out

"""
function: CheckKing
returns [False] is king not under attack.
else, returns [True, savemoves], where savemoves is a list of pairs of current indices 
occupied by a given piece, and a list of moves the piece can make to save the king.
"""
def CheckKing(board,player):
   savemoves=[]
   pos=GetPlayerPositions(board, player)
   #print("pos",pos)
   KingPos=False
   for i in pos:
      if board[i]==5+player:
         KingPos=i
   print("KingPos=",KingPos)
   threat=IsPositionUnderThreat(board, KingPos, player)
   if threat==False:
      return [False]
   #oof not safe...
   for ind in pos: #occupied indices
      moves=GetPieceLegalMoves(board, ind)
#      print("ind=",ind)
#      print("moves=",moves)
      for dest in moves:
         mvtst=WillMoveSaveKing(board, ind, dest, player, KingPos)
         if mvtst==True:
            print("savemove: ind=",ind,"dest=",dest)
            savemoves+=[ind,dest]
   return [True,savemoves]
     
"""
function: WillMoveSaveKing
a helper for CheckKing.
returns True if the piece at curr (a board index) being moved to dest will save the king.
returns False otherwise.
"""
def WillMoveSaveKing(board, curr, dest, player, KingPos):
   TestBoard=list(board)
   if curr==KingPos:
      KingPos=dest
   if player==10:
      opp=20
   else:
      opp=10
   if TestBoard[dest]==opp+5: #ie the other king, which i would be killing
      return True
   TestBoard[dest]=TestBoard[curr]
   TestBoard[curr]=0
   if IsPositionUnderThreat(TestBoard, KingPos, player) == False:
      #print("TESTBOARD")
      #PrintBoard(TestBoard)
      return True
   else:
      return False

"""
function: IsMoveSafe
returns True if moving to a position does not endanger the piece which MOVED,
(no other checks).
returns False otherwise.
"""
def IsMoveSafe(board,curr,dest,player):
   TestBoard=list(board)
   TestBoard[dest]=TestBoard[curr]
   TestBoard[curr]=0
   if IsPositionUnderThreat(TestBoard, dest, player):
      return False
   return True



###################### Functions to help in Testing Potential Moves ######################
"""
function: GenTestBoard
returns a TestBoard representing the making of a given move.
"""
def GenTestBoard(board,curr,dest):
   TestBoard=list(board)
   TestBoard[dest]=TestBoard[curr]
   TestBoard[curr]=0
   return TestBoard


"""
function: GetMoveFromBoard_diffs
returns the one move (represented by a 2-list) that changed board to finalBoard.
if this fails, returns [False]
"""
def GetMoveFromBoard_diffs(board,finalBoard):
   move=[False,False]
   if len(board)!=len(finalBoard):
      print("u gave me diff len boards... why.")
      return [False,False]
   num_differences=0 #should be 2 if the boards differ by one move.
   for i in range(len(board)):
      if board[i]!=finalBoard[i]:
         num_differences+=1
#         print("SHOULD BE OK")
         if finalBoard[i]==0:
#            print("000000000000000000")
            move[0]=i
         else:
#            print("111111111111111111")
            move[1]=i
         #if board[i]==0 and finalBoard[i]!=0: #must have moved TO here.
         #   print("i=",i)
         #   print("board[i]=",board[i]," and finalBoard[i]=",finalBoard[i])
         #   move[1]=i
         #elif board[i]!=0 and finalBoard[i]==0:
         #   print("i=",i)
         #   print("board[i]=",board[i]," and finalBoard[i]=",finalBoard[i])
         #   move[0]=i
   print("MOVE : ",move)
   if num_differences!=2:
      print("expected boards differing by one move; but not the case.")
      return [False,False]
   if move[0]==move[1]==False:
      print("Failure - GetMoveFromBoard")
      return move
   return move


###################### Board Weighting Evaluation Functions ########################
## i dont really like this.. maybe come back to it l8r if u want, but let's ignore it for
## now bc its not high priority and can be done later... yep.
"""
function: GetPiecePositionEvaluation
"""
def GetPiecePositionEvaluation(board, position, player):
   piece=board[position]-player
   if piece==0:
      out=PawnPosEval(position,player)
   elif piece==1:
      out=KnightPosEval(position,player)
   elif piece==2:
      out=BishopPosEval(position,player)
   elif piece==3:
      out=RookPosEval(position,player)
   elif piece==4:
      out=QueenPosEval(position,player)
   elif piece==5:
      out=KingPosEval(position,player)
   else:
      print("i have no idea what that piece is..")
      return False
   return out

def PawnPosEval(position,player):
   row0=[0,0,0,0,0,0,0,0]
   row1=[]
   row2=[]
   row3=[]
   row4=[]
   row5=[]
   row6=[]
   row7=[0,0,0,0,0,0,0,0]
   if player==10:
      evalboard=row0+row1+row2+row3+row4+row5+row6+row7
   elif player==20:
      evalboard=row7+row6+row5+row4+row3+row2+row1+row0
   else: 
      print("who is this mysterious player",player)
      return False
   return evalboard[position]

def KnightPosEval(position,player):
   row0=[]
   row1=[]
   row2=[]
   row3=[]
   row4=[]
   row5=[]
   row6=[]
   row7=[]
   if player==10:
      evalboard=row0+row1+row2+row3+row4+row5+row6+row7
   elif player==20:
      evalboard=row7+row6+row5+row4+row3+row2+row1+row0
   else: 
      print("who is this mysterious player",player)
      return False
   return evalboard[position]


def BishopPosEval(position,player):
   row0=[]
   row1=[]
   row2=[]
   row3=[]
   row4=[]
   row5=[]
   row6=[]
   row7=[]
   if player==10:
      evalboard=row0+row1+row2+row3+row4+row5+row6+row7
   elif player==20:
      evalboard=row7+row6+row5+row4+row3+row2+row1+row0
   else: 
      print("who is this mysterious player",player)
      return False
   return evalboard[position]


def RookPosEval(position,player):
   row0=[]
   row1=[]
   row2=[]
   row3=[]
   row4=[]
   row5=[]
   row6=[]
   row7=[]
   if player==10:
      evalboard=row0+row1+row2+row3+row4+row5+row6+row7
   elif player==20:
      evalboard=row7+row6+row5+row4+row3+row2+row1+row0
   else: 
      print("who is this mysterious player",player)
      return False
   return evalboard[position]


def QueenPosEval(position,player):
   row0=[]
   row1=[]
   row2=[]
   row3=[]
   row4=[]
   row5=[]
   row6=[]
   row7=[]
   if player==10:
      evalboard=row0+row1+row2+row3+row4+row5+row6+row7
   elif player==20:
      evalboard=row7+row6+row5+row4+row3+row2+row1+row0
   else: 
      print("who is this mysterious player",player)
      return False
   return evalboard[position]


def KingPosEval(position,player):
   row0=[]
   row1=[]
   row2=[]
   row3=[]
   row4=[]
   row5=[]
   row6=[]
   row7=[]
   if player==10:
      evalboard=row0+row1+row2+row3+row4+row5+row6+row7
   elif player==20:
      evalboard=row7+row6+row5+row4+row3+row2+row1+row0
   else: 
      print("who is this mysterious player",player)
      return False
   return evalboard[position]



######################

"""
function: (evaluating nearness to king, inp = player/opp, board)
"""

"""
function: (who am i about to lose/kill and how much do i care)
if queen is in danger, move is not favorable.
is_queen_in_danger...
"""


