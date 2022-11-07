# coding=utf-8
import json
import os
import socket
import time

import pymysql


def selectdata(conn, cur, nickname):
    sql_select = "select * from IOTMark"
    lists = []
    try:
        cur.execute(sql_select)
        rs = cur.fetchall()
        for r in rs:
            lists.append((nickname, r[0], r[7], r[1], r[2], r[5]))
        conn.commit()
        return lists
    except Exception as e:
        return lists
        conn.rollback()
        print(e)

s = socket.socket()
s.connect(('172.25.135.11', 1234))
print("----start to start program----")
print("----please input nickname:", end='')
nick = input()
s.send(("nick:" + nick).encode())
print("----connect to 172.25.215.66 success---")
while True:
    recv_msg = s.recv(1024)
    if recv_msg:
        data = str(recv_msg.decode('utf-8'))
        if "send*to*nat_behand" in data:
            lists = data.split("*")[3]
            print("----收到服务器扫描的地址：----")
            print(lists)
            listip = lists.split("\n")
            filename = '/home/ysf/nat/ipaddress'
            with open(filename, 'w') as file_object:
                for ip in listip:
                    file_object.write(ip + "\n")
            os.system('java -jar /home/ysf/nat/code/ToActivemq.jar')
        if "/get/iotmark/nat_behand" in data:
                    print("----将结果发送给服务器------")
                    conn = pymysql.Connect(host='localhost', user='root', password='123456', database='DeviceMark',
                                           port=3306)
                    cursor = conn.cursor()
                    lists = selectdata(conn, cursor, nick)
                    cursor.close()
                    conn.close()
                    print(lists)
                    data = json.dumps(lists)
                    s.send((nick+"*post*iotresult*from*nat_behand*" + data).encode())

