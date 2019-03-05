class stack:
   def __init__(self):
      self.x=[]
      self.len=0
   def push(self,val):
      self.x = [val] + self.x
      self.len+=1
      return True
   def pop(self):
      if self.len==0:
         return False
      r = self.x[0]
      self.x = self.x[1:]
      self.len-=1
      return r

