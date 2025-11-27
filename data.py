import time
import irsdk
from locales import L

################################################################################
# Utils
################################################################################

def time2speech(t):
    if not t is None:
        minutes = t/60
        hours = 0
        if minutes > 60:
            hours = minutes / 60
            minutes = minutes % 60
        secs = t % 60
        _, decimal = divmod(t,1)
        if hours > 0:
            return "{:02}:{:02}:{:02}.{:03}".format(int(hours),int(minutes), int(secs), int(decimal*1000))
        else:
            return "{} {} {}".format(int(minutes), int(secs), int(decimal*1000))
    

################################################################################
# iRacing Shared Mem computing
################################################################################

__ir = irsdk.IRSDK()

NO_SESSION_TIME_LIMIT = 604800
NO_SESSION_LAPS_LIMIT = 32767

def data_snapshot():
    if not __ir.is_initialized or not __ir.is_connected:
        __ir.startup()
    if __ir.is_connected:
        __ir.freeze_var_buffer_latest()
    else:
        __ir.shutdown()
    return __ir.is_initialized and __ir.is_connected and len(__ir["SessionInfo"]["Sessions"]) != 0

def data_cars():
    cars = []

    driverInfo = __ir["DriverInfo"]
    sessionInfo = __ir["SessionInfo"]["Sessions"][__ir["SessionNum"]]
    weekendInfo = __ir["WeekendInfo"]

    standings = [None]*64
    if sessionInfo["ResultsPositions"]:
        for resultPositionsStruct in sessionInfo["ResultsPositions"]:
            standings[resultPositionsStruct["CarIdx"]] = resultPositionsStruct

    for driversStruct in driverInfo["Drivers"]:
        if not driversStruct["CarIsPaceCar"] and not driversStruct["IsSpectator"]:
            idx = driversStruct["CarIdx"]
            cars.append({
                "id": idx,
                "driverName": driversStruct["UserName"],
                "lapsTravelled": __ir["CarIdxLapCompleted"][idx] + __ir["CarIdxLapDistPct"][idx],
                "bestLapTime": __ir["CarIdxBestLapTime"][idx],
                "lastLapTime": __ir["CarIdxLastLapTime"][idx],
                "number": driversStruct["CarNumberRaw"],
                "className": driversStruct["CarClassShortName"],
            })
    cars.sort(key=lambda x: x["lapsTravelled"], reverse=True)
    return cars

def data_session():
    sessionInfo = __ir["SessionInfo"]["Sessions"][__ir["SessionNum"]]

    return {
        "sessionTimeRemaining": -1 if __ir["SessionTimeRemain"] == NO_SESSION_TIME_LIMIT else __ir["SessionTimeRemain"],
        "sessionLapsRemaining": -1 if __ir["SessionLapsRemain"] == NO_SESSION_LAPS_LIMIT else __ir["SessionLapsRemain"],
        "sessionLapsLimit": NO_SESSION_LAPS_LIMIT if sessionInfo["SessionLaps"] == 'unlimited' else sessionInfo["SessionLaps"],
        "sessionTimeLimit": sessionInfo["SessionTime"],
        "sessionName": sessionInfo["SessionName"]
    }

################################################################################
# D A T A   E X P O S E D
################################################################################

DATA = {}

def clear_data():
    pass # TODO if needed

def update_data():
    DATA["timestamp"] = time.strftime("%H : %M")
    cars = data_cars()
    session = data_session()
    for i in range(0, len(cars)):
        p = i+1
        car = cars[i]
        DATA["p{}lasttime".format(p)] = time2speech(car["lastLapTime"])
        DATA["p{}besttime".format(p)] = time2speech(car["bestLapTime"])
        DATA["p{}name".format(p)] = car["driverName"]
        if car["id"] == __ir["PlayerCarIdx"]:
            DATA["playerposition"] = p
    for i in range(len(cars), 64):
        DATA["p{}lasttime".format(p)] = L("notime")
        DATA["p{}besttime".format(p)] = L("notime")
        DATA["p{}name".format(p)] = L("noone")

def get_data():
    if data_snapshot():
        update_data()
    return DATA
