import json
from datetime import datetime, timedelta
import logging
import os
import sqlite3
from abc import ABC, abstractmethod

from kivy.app import App
from kivy.clock import Clock

import requests

refresh_token = "APJWN8dOrJmWU1Wzw7Ws0l0RNbX8cRCJXnK-0av7jqIA8J_0m9dTgjFr7zONJH9JNwEY1K_vInRoCB2IoI7sgL2wxNl7gb0fNW8YxUzXXmLN610RI1SzWOnnJ8eV7-VYE77eAsXkjq3V5wa8Bk8Rpl6TkH5h06LSUKFqZw4UN3GlkXnGbOpCRL95BnsJWT6Dmo-JxxcsTmRpUdaHDouLFyFHBh6EhbmY51abbsFqwTEVKR8szlRESyg"
key = "AIzaSyCq2oNYF_aU_OhVKS6OF0uWKMlaNq8Voos"
token_path = "token.json"


class DataStorage:

    def __init__(self):
        logging.debug("Data storage is initializing")
        cred = get_credent()
        self.id_token: str = cred.get("idToken", "")
        self.params: dict = cred.get("params", {})
        self.tok_exp: datetime = datetime.fromisoformat(
            cred.get("expires_in", "2023-03-09T20:04:29.392099"))
        self.db_path = str()
        self.s = requests.Session()
        self.fresh_data = dict()
        self.app = App.get_running_app()

    def update_cred(self):
        validate_token()
        cred = get_credent()
        self.id_token: str = cred.get("idToken", "")
        self.params: dict = cred.get("params", [])
        self.tok_exp: datetime = datetime.fromisoformat(
            cred.get("expires_in", "2023-03-09T20:04:29.392099"))

    def get_values(self):
        self.update_cred()
        for i in self.params:
            res = get_values(self.id_token, i, self.s)
            if res.status_code != 200:
                logging.error(f'Invalid response {res}, {res.text}')
                continue
            self.fresh_data.update({i: res.json()})
        logging.debug(f'data is updated {self.fresh_data}')

    def dump_data(self):
        handle = SQLHandle()
        for param in self.params:
            handle.add_values(self.fresh_data.get(param))

    def get_data(self, param: str, start_date: datetime, end_date: datetime) -> list:
        handle = SQLHandle()
        start_date = int(start_date.timestamp())
        end_date = int(end_date.timestamp())
        data = handle.get_values(param, (start_date, end_date))
        logging.info(f'Data for {param}')
        return data

    def auto_refresh(self, dt=0):
        logging.debug("Auto refersh is started")
        self.get_values()
        self.app.vm.last_values.update({key: (value[0].get("data"), value[0].get("datetime")) for
                                        key, value in self.fresh_data.items()})
        Clock.schedule_once(self.auto_refresh, 300)
        logging.info(f"Data is updated, new update is scheduled")




class DBHandle(ABC):

    @abstractmethod
    def get_values(self):
        pass

    @abstractmethod
    def add_values(self):
        pass


class SQLHandle(DBHandle):

    def __init__(self):
        super(SQLHandle, self).__init__()
        self.db = os.path.join("data", "weather.db")

    def write_items(self, sql, items: list[dict] = None):
        con = self.get_connection()
        with con:
            cur = con.cursor()
            if items is None:
                cur.execute(sql)
            else:
                cur.executemany(sql, [tuple(d.values()) for d in items])
            con.commit()
            con.close()

    def get_items(self, sql) -> list:
        con = self.get_connection()
        with con:
            cur = con.cursor()
            cur.execute(sql)
            con.commit()
            data = cur.fetchall()
            con.close()
        return data

    def add_values(self, table_name, items: list[dict]):
        sql = f"""INSERT OR IGNORE INTO ({table_name}) VALUES (
        ?, ?, ?)
        """
        self.write_items(sql, items)

    def get_values(self, table_name, date_range: tuple[int]) -> list:
        sql = f"""SELECT * FROM ({table_name}) 
                          WHERE date
                        BETWEEN date_range[0] and date_range[1]
                       ORDER BY date"""
        res = self.get_items(sql)
        return res
        

    def get_connection(self):
        return sqlite3.connect(self.db, isolation_level='DEFERRED')

    def create_table(self):
        self.write_items("""CREATE TABLE IF NOT EXISTS (?) (
                        id INTEGER
                        date timestamp,
                        data REAL)""")
        



def validate_token():
    cred = get_credent()
    logging.debug(f'credeantials are {cred}')
    if datetime.now() > datetime.fromisoformat(
            cred.get("expires_in", "2023-03-09T20:04:29.392099")):
        logging.info("Token must be refreshed")
        update_credent(requests.Session()).json()
    logging.debug("Token is valid")

def get_values(token: str, param: str, s: requests.Session) -> requests.Response:
    head = {'Content-Type': 'application/x-www-form-urlencoded','charset': 'utf-8'}
    params = {"idToken": token, "value": param, "lines":20}
    url =  "https://monitor3.uedasoft.com/getValue.php"
    return s.get(url, headers=head, params=params)


def auth(s: requests.Session, refresh_token: str,
         url="https://securetoken.googleapis.com/v1/token") -> requests.Response:

    head = {'Content-Type': 'application/x-www-form-urlencoded','charset': 'utf-8'}
    data = {"grant_type": "refresh_token",
            "refresh_token": refresh_token}
    params = {"key": key}
    logging.debug("Refresh token is acquired")
    return s.post(url, params=params, data=data, headers=head)

def update_credent(s: requests.Session) -> requests.Response:
    res = auth(s, refresh_token)
    if res.status_code != 200:
        raise AssertionError(f'Invalid response {res}, {res.text}')

    if "id_token" not in res.json():
        raise AssertionError(f'Invalid json {res.json}')

    with open("token.json", "w", encoding="utf8") as f:

        json.dump({
            "idToken":       res.json().get("id_token"),
            "refresh_token": res.json().get("refresh_token"),
            "expires_in":    datetime.now()
                            + timedelta(seconds=int(res.json().get("expires_in")) - 15),
            "params": {
                "exwedjrg": "humidity",
                "orgmjnzw": "temp",
                "rjwyzjzg": "co2"
                }
            },
            f, indent=2)
    logging.debug("Credentials are updated")
    return res



def get_credent() -> dict:
    with open(token_path, encoding="utf8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            logging.exception(f"exception on reading {token_path}")
            data = dict()
        if not isinstance(data, dict):
            logging.error(f"Invalid type of data {token_path}")
            data = dict()
        logging.debug('Credentials are read')
        return data


def main():
    s = requests.Session()
    res = auth(s, refresh_token)

    if res.status_code != 200:
        raise AssertionError(f'Invalid response {res}, {res.text}')
    if not "id_token" in res.json():
        raise AssertionError(f'Invalid json {res.json}')
    with open("token.json", "w", encoding="utf8") as f:
        json.dump({"idToken": res.json().get("id_token"),
                   "refresh_token": res.json().get("refresh_token"),
                   "expires_in": datetime.isoformat(datetime.now()
                   + timedelta(seconds=int(res.json().get("expires_in")) - 15)),
                   "params": {
                        "exwedjrg": "humidity",
                        "orgmjnzw": "temp",
                        "rjwyzjzg": "co2"
                    }
                    },
                   f, indent=2)




if __name__ == '__main__':
    main()


