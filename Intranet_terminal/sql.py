# coding=utf-8

import pymysql
import re



def selectdata(conn, cur, nickname):
    sql_select = "select * from IOTMark"
    lists = []
    try:
        cur.execute(sql_select)
        rs = cur.fetchall()
        # print("**")
        # print(rs)
        flag = 0
        for r in rs:
            lists.append((nickname, r[0], r[7], r[1], r[4], r[5]))

        conn.commit()
        return lists

    except Exception as e:
        return lists
        conn.rollback()
        print(e)


if __name__ == '__main__':
    conn = pymysql.Connect(host='localhost', user='root', password='123456', database='DeviceMark',
                           port=3306)
    cursor = conn.cursor()

    listiot = selectdata(conn, cursor, "ysf")
    print(listiot)
    cursor.close()
    conn.close()

