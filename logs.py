#!/usr/bin/python -u
# -*- coding: UTF-8 -*-

import argparse
import os.path
import sys
from datetime import date, timedelta
import requests
import pprint

def login(args):


    url =  "https://" + args.login_url.replace("https://", "")
    print("Login to salesforce: " + url)

    params = {
        "client_id": args.client_id,
        "client_secret": args.client_secret,
        "username": args.username,
        "password": args.password,
        "grant_type": "password"
    }

    r = requests.post(url + "/services/oauth2/token", data=params)

    access_token = r.json().get("access_token")
    instance_url = r.json().get("instance_url")

    download(instance_url, "Bearer " + access_token, args.date)

def download(instance, token, logDate):

    if logDate is None:
        yesterday = date.today() - timedelta(days=1)
        logDate = yesterday.strftime("%Y-%m-%d")

    print("Download logs from: " + logDate )

    dir_path = os.getcwd()
    logs_dir = os.path.join(*[dir_path,"logs",logDate])
    # results_dir = os.path.join(dir_path, "results")

    if os.path.exists(logs_dir) is False:
        os.makedirs(logs_dir)

    # if os.path.exists(results_dir) is False:
    #     os.mkdir(results_dir)

    url = instance + "/services/data/v34.0/query?q=Select Id,EventType,LogDate From EventLogFile Where LogDate>=" + logDate + "T00:00:00Z"

    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }
    response = requests.get(url, headers=headers)

    for logFile in response.json().get("records"):

        url = instance + "/services/data/v34.0/sobjects/EventLogFile/" +  logFile.get("Id") + "/LogFile"
        print("Download log flie: " + url)

        logResponse = requests.get(url, headers=headers)
        fileName = os.path.join(logs_dir, logFile.get("Id") + "_" + logFile.get("EventType") + '.csv' )
        print("Save log file to: " + fileName)

        with open(fileName, 'w') as file:
            file.write(logResponse.text)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Download and parse Salesforce Log file.')
    parser.add_argument('login_url', metavar = 'login_url', help = 'Login url to Salesforce (production or sandbox)')
    parser.add_argument('client_id', metavar = 'client_id', help = 'Salesforce application client_id used to login')
    parser.add_argument('client_secret', metavar = 'client_secret', help = 'Salesforce application client_secret used to login')
    parser.add_argument('username', metavar = 'username', help = 'User name for login')
    parser.add_argument('password', metavar = 'password', help = 'User password for login')
    parser.add_argument('--date', metavar = 'date', help = 'Optional date from which take logs. If not pass it is set to YESTERDAY')
    args = parser.parse_args()

    login(args)



