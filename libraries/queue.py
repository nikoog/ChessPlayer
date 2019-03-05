class queue:
   def __init__(self):
      self.x=[]
      self.len=0
   def getLen(self):
      return self.len
   def enqueue(self,val):
      self.x=self.x+[val]
      self.len+=1
      return True
   def dequeue(self):
      if self.len==0:
         return False
      r=self.x[0]
      self.x = self.x[1:]
      self.len-=1
      return r
