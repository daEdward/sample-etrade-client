"""This Python script provides examples on using the E*TRADE API endpoints"""
from __future__ import print_function
import webbrowser
import json
import logging
import configparser
import sys
import requests
from rauth import OAuth1Service

CONSUMER_KEY = 'insert_key'
CONSUMER_SECRET = 'insert_secret'
CONSUMER_KEY = '446d4733ce18ece2205c1e1ee1d4578e'
CONSUMER_SECRET = '03e240c0c40806996007316b2310c00316b4fa5a52b3170c660a263d443dc906'

def oauth():
    """Allows user authorization for the sample application with OAuth 1"""
    etrade = OAuth1Service(
        name="etrade",
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com")

    menu_items = {"1": "Sandbox Consumer Key",
                  "2": "Live Consumer Key",
                  "3": "Exit"}
    while True:
        print("")
        options = menu_items.keys()
        for entry in options:
            print(entry + ")\t" + menu_items[entry])
        selection = input("Please select Consumer Key Type: ")
        if selection == "1":
            base_url = 'https://apisb.etrade.com'
            break
        elif selection == "2":
            base_url = 'https://api.etrade.com'
            break
        elif selection == "3":
            break
        else:
            print("Unknown Option Selected!")
    print("")

    # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"})

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a text code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    webbrowser.open(authorize_url)
    text_code = input("Please accept agreement and enter text code from browser: ")

    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={"oauth_verifier": text_code})


    # Step 4: Call Accounts > List Accounts API to show it works and get first accountIdKey
    print('')
    url = base_url + "/v1/accounts/list"
    response = session.get(url, header_auth=True, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    print("Request URL: {}".format(url))
    print("Request Header: {}".format(response.request.headers))
    print("Response Body: {}".format(response.text))
    parsed = json.loads(response.text)
    accounts = parsed["AccountListResponse"]["Accounts"]["Account"]
    accountIdKey = accounts[0]['accountIdKey']

    # Step 5: Call Accounts > Get Account Balance API to show it breaks with 500 instead of error
    print('')
    url = base_url + f"/v1/accounts/{accountIdKey}/balance"
    response = session.get(url, header_auth=True, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    print("Request URL: {}".format(url))
    print("Request Header: {}".format(response.request.headers))
    print("Response Body: {}".format(response.text))

    # Step 6: Call Accounts > Get Account Balance API to show it breaks again with signature_invalid
    print('')
    url = base_url + f"/v1/accounts/{accountIdKey}/balance?instType=BROKERAGE"
    response = session.get(url, header_auth=True, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    print("Request URL: {}".format(url))
    print("Request Header: {}".format(response.request.headers))
    print("Response Body: {}".format(response.text))

    # Step 7: Call Accounts > List Transactions API to show it works
    print('')
    url = base_url + f"/v1/accounts/{accountIdKey}/transactions"
    response = session.get(url, header_auth=True, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    print("Request URL: {}".format(url))
    print("Request Header: {}".format(response.request.headers))
    print("Response Body: {}".format(response.text))

    # Step 8: Call Market > Get Option Chain API to show it breaks again with signature_invalid
    print('')
    url = base_url + f"/v1/market/optionchains?symbol=IBM"
    response = session.get(url, header_auth=True, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    print("Request URL: {}".format(url))
    print("Request Header: {}".format(response.request.headers))
    print("Response Body: {}".format(response.text))

    # Step 9: Call Market > Get Option Expire Dates API to show it breaks again with signature_invalid
    print('')
    url = base_url + f"/v1/market/optionexpiredate?symbol=IBM"
    response = session.get(url, header_auth=True, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    print("Request URL: {}".format(url))
    print("Request Header: {}".format(response.request.headers))
    print("Response Body: {}".format(response.text))

if __name__ == "__main__":
    oauth()
