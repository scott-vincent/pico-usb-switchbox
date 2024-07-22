import board
import digitalio
import rotaryio
import analogio
from joystick_xl.inputs import Axis, Button, Hat
from joystick_xl.joystick import Joystick

def initEncoders():
    global encoders
    global encoderOldVal
    global encoderCentre

    # Add click (push)
    # Buttons 0 to 3
    js.add_input(
        Button(board.GP15),
        Button(board.GP3),
        Button(board.GP7),
        Button(board.GP11)
    )
    
    # Add axes X, Y, Z and X Rot
    js.update_axis((0, 0), (1, 0), (2, 0), (3, 0), defer=True)

    encoders = []
    encoders.append(initEncoder(board.GP1, board.GP0))
    encoders.append(initEncoder(board.GP4, board.GP5))
    encoders.append(initEncoder(board.GP8, board.GP9))
    encoders.append(initEncoder(board.GP13, board.GP12))

    encoderOldVal = []
    encoderOldVal.append(-1)
    encoderOldVal.append(-1)
    encoderOldVal.append(-1)
    encoderOldVal.append(-1)

    encoderCentre = 32768

def initEncoder(input0, input1):
    encoder = rotaryio.IncrementalEncoder(input0, input1)
    encoder.divisor = 4
    return encoder

def initButtons():
    # Buttons 4 to 7
    js.add_input(
        Button(board.GP2),
        Button(board.GP10),
        Button(board.GP6),
        Button(board.GP14)
    )

def initHat():
    global hatDelay
    
    # Hat is used for Cessna ignition key (potentiometer)
    js.update_hat((0, 8), defer=True)
    hatDelay = 0
    
def pressHat(state, delay):
    global hatDelay
    
    js.update_hat((0, state), defer=True)
    
    # If delay > 0 then hat will be released after specified time
    hatDelay = delay

def releaseHat():
    global hatDelay
    
    js.update_hat((0, 8), defer=True)
    hatDelay = 0

def initIgnition():
    global ignitionPot
    global prevIgnitionState

    # Potentiometer is on pin 28
    ignitionPot = analogio.AnalogIn(board.GP28)

    prevIgnitionState = -1

def readIgnition():
    global ignitionPot
    global ignitionState
    
    ignitionVal = ignitionPot.value
    # print("IgnitionVal", ignitionVal)

    if ignitionVal > 49000:
        ignitionState = 0
    elif ignitionVal > 38000 and ignitionVal < 45000:
        ignitionState = 1
    elif ignitionVal > 29000 and ignitionVal < 36000:
        ignitionState = 2
    elif ignitionVal > 23000 and ignitionVal < 26000:
        ignitionState = 3
    elif ignitionVal < 21500:
        ignitionState = 4
    else:
        ignitionState = -1
        
def doIgnition():
    global ignitionState
    global prevIgnitionState
    global hatDelay
    
    if hatDelay > 0:
        hatDelay -= 1
        if hatDelay == 0:
            releaseHat()
            
    readIgnition()
        
    if ignitionState != -1 and ignitionState != prevIgnitionState:
        print("Ignition", ignitionState)
        prevIgnitionState = ignitionState
        if ignitionState == 4:
            # Spring loaded start so hold until key returned to Both Mags position
            pressHat(ignitionState, 0)
        else:
            pressHat(ignitionState, 40)

def doEncoder(num):
    oldVal = encoderOldVal[num]
    newVal = encoders[num].position
    
    if oldVal == newVal:
        return

    encoderOldVal[num] = newVal

    axisVal = encoderCentre + newVal    
    # print("Axis", num, "=", axisVal)
    js.update_axis((num, axisVal), defer=True)


# Main
print("Starting")
js = Joystick()
refreshPush = False
refreshDelay = 0

initEncoders()
initButtons()
initHat()
initIgnition()

while True:
    # Ignition refers to the key in a Cessna that controls
    # the magnetos and starts the engine.
    doIgnition()

    for i in range(len(encoders)):
        doEncoder(i)
        
    # Force joystick axes to refresh
    if refreshDelay > 0:
        refreshDelay -= 1
    else:
        refreshDelay = 200
        js.update_button((8, refreshPush), defer=True)
        refreshPush = not refreshPush
    
    js.update()