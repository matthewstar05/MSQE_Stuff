#Compute log(x)+log(y) if defined
import math
x=4
y=-2

if(x>0):
    if(y>0):
        z=math.log(x)+math.log(y)
    else:
        z=math.log(x)
elif y>0:
    z=math.log(y)
else:
    z=0
    
if(x>0)and(y>0):
    w=math.log(x)+math.log(y)
elif(x>0):
    w=math.log(x)
elif(y>0):
    w=math.log(y)
else:
    w=0    