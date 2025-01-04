import json
import requests

BLIZZARD_API_URL = "https://us.api.blizzard.com/data/wow/"
BNET_TOKEN_URI = "https://us.battle.net/oauth/token"
BNET_AUTH_URI = "	https://us.battle.net/oauth/authorize"

ITEM_ID = "82800"
CAGE_ID = "82800"
SPECIES_IDS = [3533, 3261, 3291, 3293, 3546, 3548, 3412, 1337]
REGION = "en_US"
IS_PET = True

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
    
def get_pet_prices_on_realm(r_index, species_prices, realm_name, region="en_US"):
    url = BLIZZARD_API_URL + f"connected-realm/{r_index}/auctions?namespace=dynamic-us&locale={region}"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        api_data = response.json()
        if "auctions" in api_data.keys():
            get_buyout_by_id(response.json()["auctions"], species_prices, realm_name)

    return False

def update_prices(species_id, price, realm, species_prices):

    species_data = species_prices[species_id]

    updated_price = False
    for p_index in range(0, len(species_data)):
        if price < species_data[p_index]["price"]:
            updated_price = True
            species_data.insert(p_index, {"realm": realm, "price": price})
            break
    if not updated_price:
        species_data.append({"realm": realm, "price": price})

    species_prices[species_id] = species_data
        

def get_buyout_by_id(api_response, species_prices, r_index):
    for entry in api_response:
        if int(entry['item']['id']) == int(CAGE_ID):
            for species in SPECIES_IDS:
                if int(entry["item"]["pet_species_id"]) == species:
                    update_prices(species, entry["buyout"], r_index, species_prices)
    return None

def find_pets(access_token="secret", region="en_US"):
    realm_indexes_map = get_realm_indexes(access_token=access_token)
    species_prices = {}
    for specie in SPECIES_IDS:
        species_prices[specie] = []
    for r_index, realm_name in realm_indexes_map.items():
        get_pet_prices_on_realm(r_index, species_prices, realm_name, region)

    return species_prices

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
        data = find_pets(access_token=access_token, region=REGION)

        for species, prices in data.items():
            print(f"--------------------------------------------")
            print(f"----------------{species}-------------------")
            print(f"--------------------------------------------")
            for i in range(0, 3):
                print(f"Realm: {prices[i]["realm"]} - Price: {str(prices[i]["price"])[0:-4]}")
