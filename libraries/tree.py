from queue import *
from stack import *

"""
note: this class assumes a tree whose successors are also trees.
"""

class tree:
   def __init__(self,val):
      self.x = [val] #maybe calling it self.store would've been nice...
      self.parent=False #not yet initialized.
      self.lvl=0 #currently the root- may change level when added as a branch to another tree.

   """
   function: AddSuccessor
   adds a successor to the current tree node, while updating the parent
   and level value for each added node.
   """
   def AddSuccessor(self,x):
      self.x = self.x + [x]
      try:
         x.AddParent(self)
         x.AddLevel()
         for i in range(self.GetLevel()):
            #x.AddParent(self)
            x.AddLevel()
      except:
         print(":((((((((((")
         sad=True
         return sad 
         #note this is ok depending on the type of self.x's
         #except its not ok since this is a list of trees so DEBUG ME.
      return True

   def AddLevel(self):
      self.lvl+=1
      if len(self.x)>1:
         print("ADDED LVL????")
         for i in self.x[1:]:
            i.AddLevel()
      return True

   def GetLevel(self):
      return self.lvl

   """
   function: IsRoot
   returns True if the node is the root node of the tree, False otherwise.
   ie. if it has a parent, then this node is nothing but part of another tree.
   otherwise, it must be the root of the rest of the tree"""
   def IsRoot(self):
      if self.parent==False:
         return True
      return False

   def AddParent(self,parent):
      self.parent=parent
      return True

   def GetParent(self):
#      print("Parent: ",(self.parent).GetVal())
      return self.parent

   def GetSuccessors(self):
      if len(self.x) == 1:
         return []
      return self.x[1:]

   def GetVal(self):
      return self.x[0]

   def Print_DepthFirst(self):
      depth=self.Get_DepthOrder()
      print("-----------tree-depth-----------")
      sp=""#play with spacing later! :D
      print(depth)
      print("---------------------------------")
      return True

   def Print_BreadthFirst(self):
      breadth=self.Get_LevelOrder()
      print("-----------tree-breadth----------")
      print(breadth)
      print("--------------------------------")
      return True

   def Get_DepthOrder(self):
      accum=[]
      x=stack()
      x.push(self)
      while(1):
         r=x.pop()
         if r==False:
            break
         accum+=[r.GetVal()]
         for i in r.GetSuccessors():
            x.push(i)
      return accum

   """
   function: Get_LevelOrder
   returns a list representing the tree as traversed in level order.
   (note: this is a list of values, not trees.)
   """
   def Get_LevelOrder(self):
      accum=[]
      x=queue()
      x.enqueue(self)
      while(1):
         r=x.dequeue()
         if r==False: #nothing to dequeue - empty queue
            break
         elif r!= []:
            accum+=[r.GetVal()]
            for i in r.GetSuccessors():
               x.enqueue(i)
      return accum
  
   """
   function: Get_LevelOrder_Obj
   returns a list of trees (not their values!), as traversed in level order.
   """
   def Get_LevelOrder_Obj(self):
      accum=[]
      x=queue()
      x.enqueue(self)
      while(1):
         r=x.dequeue()
         if r==False: #nothing to dequeue - empty queue
            break
         elif r!= []:
            accum+=[r]
            for i in r.GetSuccessors():
               x.enqueue(i)
      return accum
      

   def GetAtLevel(self,lvl):
      out=[]
      if self.IsRoot()==False:
         print("call GetAtLevel() with root node only.")
         return False
      test=self.Get_LevelOrder_Obj()
      for i in test:
         if i.GetLevel()==lvl:
            out+=[i]
#      for i in out:
#         print(i.GetVal())
      return out

   def GetAtBottomLevel(self):
      lvl=-1
      out=[]
      while(True):
         lvl+=1
         tmpout=self.GetAtLevel(lvl)
         if tmpout==[]:
            break
         else:
            out=tmpout
      return out
            
   """
   function: GetParentalNbors
   returns a list of nbors who share the same parent as a given node.
   if the node is the root, it has no parents and the fcn returns [].
   if there are no nbors, returns the node itself.
   does include the node itself in the return list.
   """
   def GetParentalNbors(self):
      out=[]
      if self.IsRoot()==True or self.lvl==0:
         print("root has no nbors.")
         return []
      #find parent
      parent=self.GetParent()
      while parent.GetParent()!=False:
         parent=parent.GetParent()
      #print("out, now parent val =",parent.GetVal())
      test=parent.GetAtLevel(self.lvl)
      #print("test=",test)
      out=[]
      for i in test:
         if i.GetParent() == self.GetParent():
            out+=[i]
      return out


   def ConvertToBinaryTree(self):
      return self.BinTreeHelp([])

   def BinTreeHelp(self,sibs):
      root=self.x[0]
      #print('root ',root) 
      #left...
      x=self.GetSuccessors()
      if x==[]:
         L = []
      elif len(x)==1:
         Lsibs=[]
         L=(x[0]).BinTreeHelp(Lsibs) #flush out the sibs
      else:
         Lsibs=x[1:]
         L=(x[0]).BinTreeHelp(Lsibs)

      #right...
      if sibs==[]:
         R = []
      elif len(sibs)==1:
         Rsibs=[]
         R=(sibs[0]).BinTreeHelp(Rsibs)
      else:
         Rsibs=sibs[1:]
         R=(sibs[0]).BinTreeHelp(Rsibs)

      #print('L ',L)
      out=tree(root)

      if L!=[]:
         out.AddSuccessor(L) #now we hit the end of the tree -  yay leaves!
      if R!=[]:
         out.AddSuccessor(R)
      #print(out,out.GetVal(),out.GetSuccessors())
      return out 


#def main():
#   test=tree(0)
#   a=tree(1)
#   b=tree(2)
#   c=tree(3)
#   d=tree(4)
#   e=tree(5)
#   f=tree(6)
#   g=tree(7)
#   h=tree(8)
#   i=tree(9)
##   c.AddSuccessor(h)
##   c.AddSuccessor(i)
##   a.AddSuccessor(c)
##   a.AddSuccessor(d)
##   b.AddSuccessor(e)
##   b.AddSuccessor(f)
##   b.AddSuccessor(g)
##   test.AddSuccessor(a)
##   test.AddSuccessor(b)
##   test.Print_BreadthFirst()
#
#   test.AddSuccessor(a)
#   test.AddSuccessor(b)
#   a.AddSuccessor(c)
#   a.AddSuccessor(d)
#   b.AddSuccessor(e)
#   b.AddSuccessor(f)
#   b.AddSuccessor(g)
#   c.AddSuccessor(h)
#   c.AddSuccessor(i)
#
#   #print(a.GetParent())
#   #print(b.GetParent())
#   #print("GetLevel test")
#   #print(test.GetLevel())
#   #print(a.GetLevel())
#   #print(b.GetLevel())
#   #print(c.GetLevel())
#   #print(g.GetLevel())
#
#   test.Print_BreadthFirst()
#
#   #test.getallatLevel(2)
#   #print("h",h.GetLevel())
#   print([x.GetVal() for x in test.GetAtLevel(2)])
#   print([x.GetVal() for x in test.GetAtBottomLevel()])
#   #print("parent test: ",a.GetParent())
#
#   print("GetParentalNbors test: ",[x.GetVal() for x in e.GetParentalNbors()])
#
#   return True
#main()
