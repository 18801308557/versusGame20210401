import math
#计算两点之间距离是否小于r
def distanceInR(cx,cy,r,x,y):
    dist=math.sqrt((math.pow(x-cx,2)+math.pow(y-cy,2)))
    if dist<r:
        return True
    else:
        return False

def distanceCal(cx,cy,x,y):
    dist=math.sqrt((math.pow(x-cx,2)+math.pow(y-cy,2)))
    return dist

