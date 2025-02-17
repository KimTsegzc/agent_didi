import requests



GAODE_KEY = '788339595ce3232036976af44443597f'


def L0_LBS_IP2City(ip):
    url = f"https://restapi.amap.com/v3/ip?ip={ip}&output=json&key={GAODE_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        if data["status"] == "1":
            # print("[L0]>> LBS ip to location: ", data["rectangle"])
            return data["city"]
        else:
            print("[L0]!! LBS wrong status", data["info"])
    except requests.RequestException as e:
        print("[L0]!! LBS error", e)



def L0_LBS_L2A(longitude, latitude):
    url = f"https://restapi.amap.com/v3/geocode/regeo?key={GAODE_KEY}&location={longitude},{latitude}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        if data["status"] == "1":
            # print("[L0]>> LBS: formatted_address:", data["regeocode"]["formatted_address"])
            # print("[L0]>> LBS: addressComponent：", data["regeocode"]["addressComponent"])
            return data["regeocode"]["formatted_address"]
        else:
            print("[L0]!! LBS error", data["info"])
    except requests.RequestException as e:
        print("[L0]!! LBS error", e)


if __name__ == "__main__":
    city = L0_LBS_IP2City('220.198.244.234')
    print(city)
