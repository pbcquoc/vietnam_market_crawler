import json
import requests
from time import sleep
from tqdm import tqdm

df = json.load(open("all_location.json"))
ids = [(item['Id'], item['RestaurantCount']) for item in df['AllLocations']]

data = []
for cityid, count in ids:
    headers = {
        'Pragma': 'no-cache',
        'DNT': '1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,ja;q=0.7',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 
        'Accept': 'application/json, text/plain, */*',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'flg=vn; __ondemand_sessionid=z3s1lfqdsyds3c1yhkx5jpug; gcat=food; xfci=UFEFTVQQYQSMYBZ; floc={}'.format(cityid),
        'Connection': 'keep-alive'
    } 
    
    size = min(12, count)
    for i in tqdm(range(count//size), desc='City: {}'.format(cityid)):
        url = 'https://www.foody.vn/__get/Place/HomeListPlace?t=1562771365533&page={}&lat=15.121387&lon=108.804415&count={}&districtId=&cateId=&cuisineId=&isReputation=&type=1'.format(i, size)
        r = requests.get(url, headers=headers)
        p = json.loads(r.text)
        data.append(p)
        sleep(0.2)

