# encoding: utf-8
import paho.mqtt.client as mqtt

MQTTHOST = "120.76.100.197"
MQTTPORT = 18832
topic = "/web/public/TEST/test"
clientId = "txm_1680507023"

def test():
    client = mqtt.Client(client_id=clientId)

    client.connect(MQTTHOST, MQTTPORT, 60)

    client.publish(topic, "hello watermelon-001", 0)  # 发布一个主题为'chat',内容为‘hello liefyuan’的信息

    client.loop_forever()


if __name__ == '__main__':
    test()
