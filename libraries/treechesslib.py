"""
filename: treechesslib.py
tree algorithms to add to my chess game...
"""
from chesslib import *
from weightedchesslib import * #i particularly want GetBoardStrength(board,player,opp)
from tree import *

################ The Minimax Method ################

"""
function: pureminimax
returns a list of 2-lists with moves evaluated to be reasonable.
starts off with a list of candidate moves, which it reduces as it goes through the tree.
when it's length 1, it's the final move. if it goes through everything and there is more
than one candidate move remaining... for now, pick a random one.
"""
def pureminimax(board,depth,player,opp):
   print("-----------pureminmax-----------")
   if depth==0:
      print("lol why.")
      return GenBestMove(board,player,opp) #dont even bother...
   TestBoard=list(board)
   pureminimaxtree=tree(TestBoard)
   out=[]
   test=pureminimaxMakeTree(pureminimaxtree,depth,player,opp)
   if test==False:
      print("no options then? uhhhh")
      #decide what to do later XD
   #note: it is in the ODD NUMBERED levels of the pureminimax tree that I will find moves
   #for player. Even-numbered levels represent potential opponent moves.
   #...also note that reducing the number of elements in potential opponent moves list will be
   #beneficial. This will be done in alpha-beta pruned minimax function.
   
   #OK. so that tree now has levels, where level 0 is current board, level 1 is after i
   #move, level 2 is after opp moves, level 3 is after i move... so my options are
   #contained in the ODD numbered levels.
   #i make the tree till depth.
   #but then, options are either at depth (if it's odd), or one above depth since depth is
   #opponents move if even).
   
   #WAIT. which move am i looking at???? I NEED THE NEXT MOVE NOT THE ONE FURTHEST DOWN IN
   #THE DAMNED LIST.
   
   print("depth level to check going into options: ",depth)
   options_treels=pureminimaxtree.GetAtLevel(depth) #list of move options- list of trees
   print("number of options = ",len(options_treels))
   print("3 of options_treels ",options_treels[:3])#should be a list of tree objects.
   options=[]
   for i in range(len(options_treels)):
      options+=[(options_treels[i]).GetVal()]
   print("3 of options ",options[:3])#should be list of boards
   optionValues=[]
   WillPick=0
   for opt in range(len(options)):
      optionValues+=[GetBoardStrength(options[opt],player,opp)]
      if optionValues[opt] > optionValues[WillPick]:
         WillPick=opt
         print("WillPick ",WillPick)
   print("that was ",options[WillPick]," with value ",optionValues[WillPick])
   
   ##so now i know which final path i want to pick. so, time to go back and figure out
   #Wwhat my NEXT move should be.
   
   tempTree=options_treels[WillPick]
   print("tempTree: ",tempTree)
   for i in range(depth):
      if (tempTree.GetParent()).GetParent() == False:
#         print("breaking out")
         break
      else:
#         print("round i: ",i)
         tempTree = tempTree.GetParent()
#   print("out of the loop: tempTree = ",tempTree)

   finalBoard=tempTree.GetVal()
   print("final board ",finalBoard)
   print("current board ",board)
   for i in range(len(board)):
      if board[i]!=finalBoard[i]:
         print("diff at ",i, "and board[i]=",board[i],"and finalBoard[i]=",finalBoard[i])
   if board==finalBoard:
      print("rip they equal?")
   move=GetMoveFromBoard_diffs(board,finalBoard)
   if move[0]==False or move[1]==False:
      print("well... interesting.")
   return move 
      


"""
function: pureminimaxMakeTree
newroot is a tree, with newroot.GetVal()=board.
test each possibility by using GetBoardStrength(newroot.GetVal(), player, opp)

"""
def pureminimaxMakeTree(newroot,depth,player,opp):
   if depth==0:
#      print("depth=0 and done!")
      return True
   options=playerMoveOptions(newroot.GetVal(),player)
   if options==[]:
      print("no options...")
      return False
#   print("pureminimaxMakeTree with depth = ",depth)
   for possibility in options:
      tstBoard=GenTestBoard(list(newroot.GetVal()),possibility[0],possibility[1])
      newbranch=tree(tstBoard)
      newroot.AddSuccessor(newbranch)
      #pureminimaxMakeTree(newbranch,depth-1,player)
   for successor in newroot.GetSuccessors():
      pureminimaxMakeTree(successor,depth-1,opp,player)
   return True


# so i need to improve pureminimax by:
# -generate the game tree
# for each successor of my initial root, pick the max or min suuccessor to traverse
# - continue until i run out of time or choose smth.
# in the interest of not running out of time, ill only make a two-level tree, which i
# shall call recursively until i have something.


################ The Minimax Method + Alpha-Beta Pruning ################

"""
function: alphabetaminimax
returns a list of 2-lists with A selected move evaluated to be reasonable.
starts off with a list of candidate moves, which it reduces as it goes through the tree.
eventually picks one board to which it'll converge, after which it goes back up the tree
and figures out the next move.

(wrote this earlier but i think its invalid rn)
when it's length 1, it's the final move. if it goes through everything and there is more
than one candidate move remaining... pick a random one.
"""
def alphabetaminimax(board,depth,player,opp):
   print("-----------alphabetaminmax-----------")
   if depth==0:
      print("lol why.")
      return GenBestMove(board,player,opp) #dont even bother...
   TestBoard=list(board)
   alphabetaminimaxtree=tree(TestBoard)
#   print("OKOKOKOKMKKOKOKOKKKKOKKOKOKOOKOK PARENT ",alphabetaminimaxtree.GetParent())
   out=[]
   test=alphabetaMakeTree(alphabetaminimaxtree,depth,player,opp)
   if test==False: #if the function failed
      print("no options then? uhhhh")
      return []  #decide what to do later XD
   print("depth level to check going into options: ",depth)

   #options_treels: list of final board options- list of trees
   options_treels=alphabetaminimaxtree.GetAtBottomLevel()
   if alphabetaminimaxtree.GetAtLevel(depth) == options_treels:
      print("checking option_treels: we ok")
   else:
      print("checking option_treels: we have a depth difference. RIP, plz fix me.")

   #may also use GetAtBottomLevel(), but then we gotta consider the change in depth- so
   #that's a cheap way to get evaluation not really up till depth.

   print("number of options = ",len(options_treels))
   print("3 of options_treels ",options_treels[:3])#should be a list of tree objects.
      

   #options: list of the actual boards stored in the trees of options_treels
   options=[]
   for i in range(len(options_treels)):
      options+=[(options_treels[i]).GetVal()]
#   print("3 of options ",options[:3])#should be list of boards
   
   #optionValues: the board value associated with each option, another parallel list..
   optionValues=[]
   #note: original move selection method was to pick the highest value of the board.
   #new idea: build a fcn which considers more than just the endvalue.
   #call this fcn Move2PickFromTree(options_treels, options, optionValues).

   #WillPick=0 #the index of the highest value in the optionValues list
   #print("WILLPICK=0 NOW")
   for opt in range(len(options)-1):
      # each opt is a board
      optionValues+=[GetBoardStrength(options[opt],player,opp)]
      #if optionValues[opt] > optionValues[WillPick]:
      #   WillPick=opt
      #   print("WillPick ",WillPick)
   #print("that was ",options[WillPick]," with value ",optionValues[WillPick])
  
   move=Move2PickFromTree(options_treels,options,optionValues,depth,board,player,opp)

   return move 

"""
function: alphabetaMakeTree
creates the game tree just as pureminimaxMakeTree does, but with alpha-beta pruning to
reduce the size of the tree and increase processing speed.
note: 
3 - black
2 - white
1 - black
0 - done
how about a convention.
odd number depths are player, even number depths are opponent (ps. human is opp)
as such, odd depths have only the HIGHEST VALUE MOVES go through. or wait.
how about at least one move per player move. But, do notice the BIG ones.
"""
def alphabetaMakeTree(newroot,depth,player,opp):
   if depth==0:
#      print("depth=0 and done!")
      return True
   options=playerMoveOptions(newroot.GetVal(),player)
   if options==[]:
      print("no options...")
      return False
#   print("alphabetaMakeTree with depth = ",depth)
   CurrentBoardStrength=GetBoardStrength(newroot.GetVal(),player,opp)
   for possibility in options:
      tstBoard=GenTestBoard(list(newroot.GetVal()),possibility[0],possibility[1])
      tstBoardStrength=GetBoardStrength(tstBoard,player,opp)

      ##### evaluate whether we ought to bother with making the enxt node...
      ##### (THIS IS THE PART TO MAKE BETTER.)
      # ->check1: if we are at the first node, consider ALL options for sure.
      #   - TODO: i dont think check1 is necessary
      # ->check2: True if the strength of the tstBoard is better (not=) to current board.
      #   ...but for check2, let's introduce a factor. with this factor, i'll allow moves
      #   which look bad for the immediate next board state, but which may end up being
      #   ok moves in the future.
      factor = 10 #currently ok with the death of a PAWN only appearing in the tree.
      
#      print("DEBUG: player=",player," CURRENT BOARD STRENGTH = ",CurrentBoardStrength,"TSTBOARDSTRENGTH=",tstBoardStrength)
      check2 = tstBoardStrength > CurrentBoardStrength - factor #is next better than this. 
      check1 = newroot.GetParent() # will =False only when this is the parent.
#      print("check1=",check1,"check2=",check2)
      check3 = (newroot.GetSuccessors==[])
      
      # if tstBoardStrength == CurrentBoardStrength, allow a max number of tree nodes 
      # to be added.
      if tstBoardStrength == CurrentBoardStrength and len(newroot.GetSuccessors()) > 50:
#         print("ok now its getting too big... hopefully limiting here is ok?")
         #lim=-1
         lim=2 #very much subject to change
      else:
         lim=-1

      if check2 or (check1==False) or check3:
#         print("adding the node with CurrentBS-factor=",CurrentBoardStrength - factor)
         newbranch=tree(tstBoard)
         newroot.AddSuccessor(newbranch)
      #####
   if lim==-1:
#      print("lim=-1, adding all")
      for successor in newroot.GetSuccessors():
         alphabetaMakeTree(successor,depth-1,opp,player) #flipping who player is
   else:
#      print("lim=",lim,"adding len successors / lim")
      for i in range(0,len(newroot.GetSuccessors()),lim):
         successor=(newroot.GetSuccessors())[i]
         alphabetaMakeTree(successor,depth-1,opp,player)
   return True


"""
function: Move2PickFromTree
helper for alphabetaminmax
takes in the options at the bottom of the tree as well as the list of trees, 
and selects a move which it will return to alphabetaminmax.
to consider in selecting a move:
   - final board value
   - board values neighboring the final board i am considering (ave value?)
      --> fcn to check average board value?
         --> pick option with highest AVERAGE, then highest BOARD in that group
"""
def Move2PickFromTree(options_treels,options,optionValues,depth,board,player,opp):
  
   ##PART 1: PICK the final board state.
  
   ## ## ## ## WORKING ON THIS CHUNK RN

   # test a few optionValues which seem to be high and have potential...
   # trying three for now.. let's see how that goes XD
   candidates = []
   # actually, let's look for all potential ways to get max value != 0.
   # figure out max board value
#   print("INFO: optionValues = ",optionValues)
   biggest = max(optionValues) # <------- i think this is wrong.
#   print("INFO: biggest = ",biggest)
   # if the best case is board value = 0, limit number of nodes considered.
   # arbitraty choice, for now.
   if biggest==0:
#      print("biggest=0")
      #errrr this leads to prob- cant evaluate each node, just picking 5 random endpoints.
      lim=-1 #nvm lets make it limitless
      #lim=5 #look at max 5 options
   else:
#      print("limitless- lets go.")
      lim=-1
   # iterate over optionValues to figure out indices at which the max value occurs, and store
   # these indices in candidates.
   for i in range(len(optionValues)):
      if optionValues[i] == biggest:
         candidates += [i]
         lim-=1
      if lim==0: 
#         print("hit limit- break")
         break #note: no longer using this method am i?
   # note candidates is a list of indices which map to board states defined in
   # option_treels, options, optionValues
#   print("INFO: len(candidates) = ",len(candidates))
#   print("INFO: candidates: ",candidates)
   #if there are no candidates? then i have a problem

   # candidates works best when the list is length max 100- reduce to list of 100. 
   if len(candidates)>500:
      #gonna pick some over intervals of list_length/2
      factor=int( len(candidates) / (len(candidates)%500) )
      
#      print("info: factor = ",factor)
      temp=[]
      for i in range(0,len(candidates),factor):
         temp+=[candidates[i]]
      candidates=temp
#      print("INFO: len(candidates) changed to ",len(candidates))


   # figure out average value between nbors of the nodes in candidates, for each
   # candidate.
   ave_ls=[]
   for move_ind in range(len(candidates)): #move_ind corresponds to ind in option_treels
      ave = GetNborMovesAve(options_treels, optionValues, player, opp, move_ind)
      ave_ls += [ave]
   # choose the highest of the average values, and store its index from ave_ls

   selection = ave_ls.index(max(ave_ls))
#   print("INFO: max ave = ",max(ave_ls))
#   print("selection index in ave_ls: ",selection)
   # ave_ls[selection] is the BOARD VALUE of options_treels which i am going to use.
   # selection is the index of the board value in the ave_ls
   # so what's the index in options_treels?
   # candidates is the list of indices im interested in. which index in candidates? well, same
   
   # convert to index as it appears in option_treels. candidates list maps the index in ave_ls 
   # to the corresponding index in option_treels.
   selection = candidates[selection]
   
   # some debugging info
#   print("INFO: selection board value = ",optionValues[selection])
   
   ##PART 2: Figure out which move to take next
   #...time to traverse back up to level 1 of the tree, where i can find the 
   # next move to take.
   
   #tempTree is the tree node to traverse back up from.
   tempTree=options_treels[selection]
#   print("tempTree: ",tempTree)
   for i in range(depth):
      if (tempTree.GetParent()).GetParent() == False:
#         print("breaking out")
         break
      else:
#         print("round i: ",i)
         tempTree = tempTree.GetParent()
#   print("out of the loop: tempTree = ",tempTree)
#   print("current level (should=1): ",tempTree.GetLevel())
   finalBoard=tempTree.GetVal()
#   print("final board ",finalBoard)
#   print("current board ",board)
#   for i in range(len(board)):
#      if board[i]!=finalBoard[i]:
#         print("diff at ",i, "and board[i]=",board[i],"and finalBoard[i]=",finalBoard[i])
#   if board==finalBoard:
#      print("rip they equal?")
   move=GetMoveFromBoard_diffs(board,finalBoard)
#   if move[0]==False or move[1]==False:
#      print("well........")
   return move


"""
function: GetNborMovesAve
returns the average Board Value of a group of nodes.
move_ind corresponds to the index of options_treesls to consider as my move.
optionValues is a list of board values with indices corresponding to options_treels
"""
def GetNborMovesAve(options_treels, optionValues, player, opp, move_ind):
   # move_ind correspo
   chosen_treenode = options_treels[move_ind]
   # calculate average value of that node
   out=0
   for nbor in chosen_treenode.GetParentalNbors():
      out += GetBoardStrength(nbor.GetVal(), player, opp)
   #print(out)
   div=len(chosen_treenode.GetParentalNbors())
   ave = out/div
#   print("ave: ",ave)
   return ave 


################# SUBMITTABLE: a combo of alphabeta to return as per nebu's wishes ################
"""
function: alphabetaeverything
returns the whole evaltree as well as move (ps i normally just return the move alone)
returns the list out:
   - out[0]: the full tree
   - out[1]: list of candidate board states
   - out[2]: list of values for each candidate board state
   - out[3]: the chosen move, which is itself represented as a 2-list
"""
def alphabetaeverything(board,depth,player,opp):
   out=[False,False]
#   print("-----------alphabetaEVERYTHING-----------")
   if depth==0:
      print("lol why.")
      return out
      #return GenBestMove(board,player,opp) #dont even bother...
   TestBoard=list(board)
   alphabetaminimaxtree=tree(TestBoard)
#   print("OKOKOKOKMKKOKOKOKKKKOKKOKOKOOKOK PARENT ",alphabetaminimaxtree.GetParent())
   test=alphabetaMakeTree(alphabetaminimaxtree,depth,player,opp)
   if test==False: #if the function failed
      print("no options then? uhhhh")
      return out  #decide what to do later XD
   # so my tree is good, and out[0] will return this tree! #
#   print("----adding to out[0]----")
   out[0]=alphabetaminimaxtree
#   print("depth level to check going into options: ",depth)

   #options_treels: list of final board options- list of trees
   options_treels=alphabetaminimaxtree.GetAtBottomLevel()
#   if alphabetaminimaxtree.GetAtLevel(depth) == options_treels:
#      print("checking option_treels: we ok")
#   else:
#      print("checking option_treels: we have a depth difference. RIP, plz fix me.")

#   print("number of options = ",len(options_treels))
#   print("3 of options_treels ",options_treels[:3])#should be a list of tree objects.
      

   #options: list of the actual boards stored in the trees of options_treels
   options=[]
   for i in range(len(options_treels)):
      options+=[(options_treels[i]).GetVal()]
#   print("3 of options ",options[:3])#should be list of boards
   
   #optionValues: the board value associated with each option, another parallel list..
   optionValues=[]

   #WillPick=0 #the index of the highest value in the optionValues list
   #print("WILLPICK=0 NOW")
   for opt in range(len(options)-1):
      # each opt is a board
      optionValues+=[GetBoardStrength(options[opt],player,opp)]
   
   move=Move2PickFromTree(options_treels,options,optionValues,depth,board,player,opp)
   
   ## out[3] = 2-list detailing the move ##
#   print("----adding to out[3]----")
   out[1]=list(move)

   return out 



