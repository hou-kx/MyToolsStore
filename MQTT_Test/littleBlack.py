# encoding:utf-8
# Author:"hou-kx"
# Date:2023/04/06
# MQTT
import random
import threading
from paho.mqtt import client as mqtt_client
from threading import Thread, Timer
import time


def connect_mqtt(broker, port, client_id) -> mqtt_client:
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
            print(f"Connected to MQTT Broker! {threading.current_thread()}")
        else:
            print("Failed to connect, return code %d\n", rc)
        pass

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic, from_topic, qos=0):
    """
    订阅某个主体
    :param from_topic:
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
        # print(f"{msg.topic} -> say [{time.strftime('%Y-%m-%d %H:%M:%S')}]: {msg.payload.decode('UTF-8')}")
        print(f"{from_topic} -> say [{time.strftime('%Y-%m-%d %H:%M:%S')}]: {msg.payload.decode('UTF-8')}")
        pass

    client.subscribe(topic, qos)
    client.on_message = on_message
    pass


def publish(client, topic, to_topic, payload, qos=0):
    """
    以某个主体发布消息
    """
    time.sleep(1)
    result = client.publish(to_topic, payload, qos)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"You [{topic}] said to {to_topic} [{time.strftime('%Y-%m-%d %H:%M:%S')}]: {payload} ")
    else:
        print(f"Failed to send message to topic {topic}")


class MyProducer(Thread):
    """
    生产者 发送
    """

    def __init__(self, broker, port, from_topic, to_topic, client_id, qos=0):
        super().__init__()
        self.from_topic = from_topic
        self.to_topic = to_topic
        self.qos = qos
        self.client_id = client_id
        self.port = port
        self.broker = broker

    def run(self):
        print("输入 '$' 结束对话")
        client = connect_mqtt(self.broker, self.port, self.client_id)
        # 使用同一个连接，既是发布者又是订阅者
        subscribe(client, self.from_topic, self.to_topic, self.qos)

        # 启动连接
        client.loop_start()

        while True:
            payload = input()
            if payload == '$':
                break
            publish(client, self.from_topic, self.to_topic, payload, qos=0)
            pass
        # 关闭链接
        client.disconnect()
        # loop_stop() 不能写在on_disconnect 回调里, 否则 threading.current_thread() == client._thread，\
        # 客户端无法清除client._thread 子进程，以后再使用loop_start()就无效了
        client.loop_stop()


class MyConsumer(Thread):
    """
    消费者 守护线程
    """

    def __init__(self, broker, port, topic, client_id, qos=0):
        super().__init__()
        self.topic = topic
        self.qos = qos
        self.client_id = client_id
        self.port = port
        self.broker = broker

    def run(self):
        client = connect_mqtt(self.broker, self.port, self.client_id)
        subscribe(client, self.topic, self.qos)
        client.loop_forever()


if __name__ == '__main__':
    broker = '43.142.91.235'
    port = 1883
    my_name = "小黑子"
    to_name = "watermelon"
    # generate client ID with pub prefix randomly
    client_id = f'python-mqtt-{random.randint(0, 1000)}'

    t1 = MyProducer(broker, port, my_name, to_name, client_id)
    # t2 = MyConsumer(broker, port, my_name, client_id)
    # t2.setDaemon(True)  # 设置为守护线程
    t1.start()
    # t2.start()
    pass