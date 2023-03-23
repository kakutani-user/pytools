# ---ssh接続---#
from sshtunnel import SSHTunnelForwarder
# ---MySQL---#
import MySQLdb
# ---タイムゾーン---#
import datetime
import os
import logging
import sys
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
logger.addHandler(sh)
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%dT%H:%M:%S")
sh.setFormatter(fmt)
import mysql.connector
import csv
import pandas as pd

def get_data(type=None, is_register_ownid=False):
    start_time = datetime.datetime(2020, 1, 16, 0, 0, 0, tzinfo=datetime.timezone.utc)
    tz_jst = datetime.timezone(datetime.timedelta(hours=9))
    start_time = start_time.astimezone(tz_jst)
    # table-name = 'private_lora_locamoni'
    node_id = 2001
    script = "SELECT * FROM {} WHERE created_at > '{}' AND node_id = {} ORDER BY id asc limit 10".format(table_name, start_time, node_id)
    logger.info(script)
    dataset = list(get_data_mysql(script))
    dataset.to_csv
    print(dataset)

server_ip = '133.68.31.33'
ssh_port = 22
ssh_uname = 'otsukalab'
ssh_pw = '55otsukalab!!'
mysql_uname = 'otsukalab'
mysql_pw = '55otsukalab!!'
database_name = 'lora_db'
table_name = 'private_lora_locamoni'

# --- Vigen(MySQL) --- #
def get_data_mysql(script):
    # Vigenに接続し、scriptで設定したデータを持ってくる
    # SSH jester
    server = SSHTunnelForwarder(
        (server_ip, ssh_port),
        ssh_username=ssh_uname,
        ssh_password=ssh_pw,
        remote_bind_address=('127.0.0.1', 3306)
    )
    server.start()
    # データベース接続
    cnx = MySQLdb.connect(
        host='127.0.0.1',
        port=server.local_bind_port,
        user=mysql_uname,
        passwd=mysql_pw,
        db=database_name,
        charset='utf8',
    )
    # MySQLコンソールを開く
    cursor = cnx.cursor()

    cursor.execute(script)
    dataset = cursor.fetchall()

    # MySQLコンソールを閉じる
    cursor.close()
    cnx.close()

    # SSH切断
    server.stop()

    return dataset


def hex2dec(x: str, bit: int) -> str:
    """16進数文字列xをビット数bit内の符号付10進に変換する"""
    dec = int(x, 16)
    if dec >> bit:
        raise ValueError
    return dec - (dec >> (bit - 1) << bit)


def main():
    # 接続
    server = SSHTunnelForwarder(
        (server_ip, ssh_port),
        ssh_username=ssh_uname,
        ssh_password=ssh_pw,
        remote_bind_address=('127.0.0.1', 3306)
    )
    server.start()
    # データベース接続
    cnx = MySQLdb.connect(
        host='127.0.0.1',
        port=server.local_bind_port,
        user=mysql_uname,
        passwd=mysql_pw,
        db=database_name,
        charset='utf8',
    )

    node_id_list = list(range(1001, 1006))
    # node_id_list = list(range(3001, 3004))
    # node_id_list = [2013, 2025, 2026, 2001, 2022, 2010, 2024, 2028, 2015]
    # node_id_list = list(range(2001, 2051)) + list(range(2111, 2151))
    # SQL
    for node_id in node_id_list:
        # query = "SELECT * FROM {} WHERE node_id = {} ORDER BY id asc".format(table_name, node_id)
        query = "SELECT * FROM {} WHERE node_id = {} and created_at >= '2022-11-7' and created_at <= '2022-11-15' ORDER BY id asc".format(table_name, node_id)
        # 実行結果をデータフレームへ
        df = pd.read_sql(query, cnx)
        # データフレームからCSVへ
        df.to_csv(
            path_or_buf='output/locamoni_{}_221107-221114.csv'.format(node_id),
            encoding='utf-8',
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
            escapechar='\\')

    # 後始末
    cnx.close()
    server.stop()


if __name__ == '__main__':
    main()
    sys.exit()
