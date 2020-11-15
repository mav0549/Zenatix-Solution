import time
import json
import random as rand
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

myMQTTClient = AWSIoTMQTTClient("clientid")

myMQTTClient.configureEndpoint("a3itj121xmscfn-ats.iot.ap-south-1.amazonaws.com", 8883) 
myMQTTClient.configureCredentials("C:/Users/LENOVO/Desktop/AWSIot/root-ca.pem", "C:/Users/LENOVO/Desktop/AWSIot/private.pem.key", "C:/Users/LENOVO/Desktop/AWSIot/certificate.pem.crt")

#Timout Settings
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

myMQTTClient.connect()


def generateData():
    temp = round(rand.uniform(20.5, 40.5), 2)
    humid = round(rand.uniform(60, 100), 2)
    ph = round(rand.uniform(5, 10), 1)

    return (temp, humid, ph)

def getData(timeout):
    if(timeout > 0 and timeout < 100):
        try:
            while 1:
                t, h, p = generateData()
                output = "Temperature: {}\nHumidity: {}\npH: {}".format(t, h, p)
                print(output)
                data = '''{"Timestamp": "","Temperature": "","Humidity": "", "pH": ""}'''
                data = json.loads(data)
                data['Timestamp'] = time.strftime("%Y%m%d-%H%M%S")
                data['Temperature'] = t
                data['Humidity'] = h
                data['pH'] = p
                data = json.dumps(data)       
                myMQTTClient.publish(
                    topic="sensor_data",
                    QoS=1,
                    payload=data
                )
                time.sleep(timeout)

        except KeyboardInterrupt:
            pass
    else:
        print("Input time must be a positive integer")
        return

getData(5)
time.sleep(60)

myMQTTClient.disconnect()
