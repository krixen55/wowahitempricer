import json
import requests

BLIZZARD_API_URL = "https://us.api.blizzard.com/data/wow/"
BNET_TOKEN_URI = "https://us.battle.net/oauth/token"
BNET_AUTH_URI = "	https://us.battle.net/oauth/authorize"

ITEM_ID = "35226"
REGION = "en_US"

def get_realm_indexes(region="en_US", access_token="secret"):
    url = BLIZZARD_API_URL + f"realm/index?namespace=dynamic-us&locale={region}"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return {realm['id']: realm['name'] for realm in response.json()['realms']}
    else:
        print("Error:", response.status_code, response.text)
        return None
    
def get_mount_prices_on_realm(r_index, item_id, region="en_US"):
    url = BLIZZARD_API_URL + f"connected-realm/{r_index}/auctions?namespace=dynamic-us&locale={region}"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        api_data = response.json()
        if "auctions" in api_data.keys():
            return get_buyout_by_id(item_id, response.json()["auctions"])

    return False

def get_buyout_by_id(auction_id, api_response):
    for entry in api_response:
        if int(entry['item']['id']) == int(auction_id): # and int(entry['quantity']) >= 1:
            return int(entry['buyout'])
    return None

def find_mount(item_id = "49286", access_token="secret", region="en_US"):
    realm_indexes_map = get_realm_indexes(access_token=access_token)
    mount_prices = {}
    for r_index, realm_name in realm_indexes_map.items():
        value = get_mount_prices_on_realm(r_index, item_id, region)
        if value:
            print(f"Found. realm: {realm_name} - price: {value}")
            mount_prices[realm_name] = value

    return mount_prices

def get_access_token(creds):
    data = {
        "grant_type": "client_credentials",
        "client_id": creds["client_id"],
        "client_secret": creds["secret"]
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(BNET_TOKEN_URI, data=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get("access_token")
        
        if access_token:
            print("Access Token:", access_token)
            return access_token
        else:
            print("Error: Access token not found in response.")
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None

if __name__ == "__main__":

    with open("secrets.json") as f:
        creds = json.load(f)
    
    access_token = get_access_token(creds)
    if (access_token):
        prices = find_mount(access_token=access_token, item_id=ITEM_ID, region=REGION)

        sorted_data = sorted(prices.items(), key=lambda x: x[1])

        if len(sorted_data) >= 3:
            for name, value in sorted_data[:3]:
                print(f"Name: {name}, Value: {str(value)[:-4]}")
        else:
            for name, value in sorted_data:
                print(f"Name: {name}, Value: {str(value)[:-4]}")