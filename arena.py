import math
ball_x=180
ball_y=-200
car_front_x=180
car_front_y=-15
car_back_x=200
car_back_y=-15
goal_x=0
goal_y=200
img_x=ball_x
img_y=ball_y
ext=50
start=True

if (ball_x-goal_x)==0:
    mbg=(ball_y-car_front_y)/abs(ball_y-car_front_y)*math.inf
else:
    mbg=(ball_y-goal_y)/(ball_x-goal_x)
#ambc=math.degrees(math.atan(abs((mbc-mc)/(1+mbc*mc))))




def dis_ball_goal():
    dbg=math.sqrt(abs(pow((goal_x-ball_x),2)-pow((goal_y-ball_y),2)))
    return dbg
def imp():
    dbg=(dis_ball_goal())
    dgp=dbg+ext
    rx=int(((dgp*ball_x)-(ext*goal_x))/(dbg))
    ry=int(((dgp*ball_y)-(ext*goal_y))/(dbg))
    return rx, ry
def ang_car_imgp():
    if (car_front_x-car_back_x)==0:
        mc=(car_front_y-car_back_y)/abs((car_front_x-car_back_x))*math.inf
    else:
        mc=(car_front_y-car_back_y)/(car_front_x-car_back_x)
    if (img_x-car_front_x)==0:
        mbc=(img_y-car_front_y)/abs((img_x-car_front_x))*math.inf
    else:
        mbc=(img_y-car_front_y)/(img_x-car_front_x)
    ambc=abs(abs(math.degrees(math.atan(mc)))-abs(math.degrees(math.atan(mbc))))
    return ambc
def dis_ball_imp():
    dimpc=math.sqrt(abs(pow((img_x-car_front_x),2)-pow((img_y-car_front_y),2)))
    return dimpc
def ang_car_goal():
    if (car_front_x-car_back_x)==0:
        mc=(car_front_y-car_back_y)/abs((car_front_x-car_back_x))*math.inf
    else:
        mc=(car_front_y-car_back_y)/(car_front_x-car_back_x)
    if (goal_x-ball_x)==0:
        mbc=(goal_y-ball_y)/abs((goal_x-ball_x))*math.inf
    else:
        mbc=(goal_y-ball_y)/(goal_x-ball_x)
    ambc=abs(abs(math.degrees(math.atan(mc)))-abs(math.degrees(math.atan(mbc))))
    return ambc
def dis_car_goal():
    dimpc=math.sqrt(abs(pow((goal_x-car_front_x),2)-pow((goal_y-car_front_y),2)))
    return dimpc 

  
img_x,img_y = imp()
if start==True:
    while ang_car_imgp()<175 and ang_car_imgp()>185:
        command = 'R'
    while dis_ball_imp()>10:
        command ='F'
    while ang_car_goal()<175 and ang_car_goal()>185:
        command = 'L'
    while dis_car_goal()>10:
        command = 'F'