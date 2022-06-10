'''
@author: Grant Gabrielson
@author: Kyle Hammer
Term Project Main File
'''
import shares, TPTaskUser, TPTaskData, TPTaskMotor

# Set all the shares variables
drawFlag = shares.Share(False)

#triFlag = shares.Share(False)
#
#cirFlag = shares.Share(False)
#
#sqFlag = shares.Share(False)
#
#mFlag = shares.Share(False)

datalen = shares.Share(0)

drawnum = shares.Share(0)

sendFlag = shares.Share(False)

doneFlag = shares.Share(False)

raphFlag = shares.Share(False)

penFlag = shares.Share(False)

th1 = shares.Share(0)

th2 = shares.Share(0)

if __name__ == '__main__':
    
    # Task list for main to run through
    tasklist = [TPTaskUser.TaskUserFun('Task User', 50_000,  drawnum, datalen, drawFlag),
                TPTaskData.TaskDataFun('Task Newtson Raphson', 50_000, datalen, drawnum, sendFlag, drawFlag, penFlag, th1, th2),
                TPTaskMotor.TaskMotorFun('Task Motor', 10_000, penFlag, sendFlag, th1, th2)]
    
    while True:
        try:
            for task in tasklist:
                next(task)
        except KeyboardInterrupt:
            break