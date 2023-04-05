# -*- coding: utf-8 -*-
# python 3.6
import random
import time
import asyncio
from paho.mqtt import client as mqtt_client

broker = 'localhost'
port = 1883
my_topic = "/python/mqtt/watermelon"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt() -> mqtt_client:
    """
    连接 mqtt 服务器
    :return: 返回 client 句柄
    """

    def on_connect(client, userdata, flags, rc):
        """
        重写 client 的连接方法
        :param client:
        :param userdata: 用户隐私数据
        :param flags:
        :param rc: 连接 mqtt 服务器的返回状态
        """
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        pass

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic, qos=0):
    """
    订阅某个主体
    :param topic:
    :param client:
    :param qos:
    :return: None 打印输出收到相关主体的发布的消息
    """

    def on_message(client, userdata, msg):
        """
        重写 client 的收到消息的方法
        :param client:
        :param userdata:
        :param msg: 消息主体
        :return:
        """
        # 传输消息内容转换编码
        print(f"{msg.topic}` -> say: {msg.payload.decode('UTF-8')} [{time.strftime('%Y%m%d-%H%M%S')}]")
        pass

    client.subscribe(topic, qos)
    client.on_message = on_message
    pass


def publish(client, topic, payload, qos=0):
    """
    以某个主体发布消息
    :param client:
    :param topic:
    :param payload:
    :param qos:
    :return:
    """
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {topic}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def once_publish(client):
    con = 'Watermelon !'
    for _ in range(0, 1):
        time.sleep(1)
        msg = f"messages: {con, _}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def run(sel):
    client = connect_mqtt()
    client.loop_start()
    if sel == 1:
        once_publish(client)
    else:
        publish(client)


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()client.loop_start()

count = 0
while True:
    data = str(time.time())
    print('state: ', client._state, 'loop进程：', client._thread, end='  ')
    if client._state != 2:
        client.publish(TOPIC, data, qos=0)
        print(client._state, '发布: ', data)
    else:
        print('\n客户端已断开,')
    if count == 4:
        print('disconnect.................')
        client.disconnect()
        # loop_stop() 不能写在on_disconnect 回调里, 否则 threading.current_thread() == client._thread，\
        # 客户端无法清除client._thread 子进程，以后再使用loop_start()就无效了
        client.loop_stop()
    if count == 8:
        print('尝试重连')
        client.reconnect()  # 必须重连将 client._state 从断开状态切换为初始化状态
        client.loop_start()
    count += 1
    time.sleep(1)


if __name__ == '__main__':
    run(0)
