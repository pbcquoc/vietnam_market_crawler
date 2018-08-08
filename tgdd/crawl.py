import requests
from bs4 import BeautifulSoup
import re
import json

url = 'https://www.thegioididong.com/aj/CategoryV5/Product/'
comment_api = 'https://www.thegioididong.com/aj/ProductV4/RatingCommentList/'
spec = 'https://www.thegioididong.com/aj/ProductV4/GetFullSpec/'
domain = 'https://www.thegioididong.com'

outcomment = open('comment', 'w')
specfile = open('spec', 'w')
page_idx =-1 
while True: 
    page_idx += 1
    form = {"Category":42, "Manufacture":0, "PriceRange":0, "Feature":0, "Property":0,"OrderBy":0,"PageSize":30,"PageIndex":page_idx,"ClearCache":0}
    page_text = requests.post(url,params=form).text
    if "Không tìm thấy" in page_text: break
    soup = BeautifulSoup(page_text, 'lxml')

    for link in soup.find_all('a'):
        product_url = link.get('href')
        product_name = link.find('h3')
        if product_name != None:
            product_name = product_name.text
            print(product_name)
            product_page = requests.post(domain+product_url).text
            product_soup = BeautifulSoup(product_page, 'lxml')
            try:
                product_description = product_soup.find('article', {'class':'area_article'}).text
            except:
                print('product invalid')
                continue
            m = re.search('var productID = \'(.+)\'[,;]{1}', product_page)
            if m:
                product_id = int(m.group(1))

                spec_params = {'productID':product_id}                
                spec_page = requests.post('https://www.thegioididong.com/aj/ProductV4/GetFullSpec/', params=spec_params).text
                spec_json = json.loads(spec_page)
                spec_soup = BeautifulSoup(spec_json['spec'], 'lxml')
                spec_tags = spec_soup.find_all('li')
                spec_dict = {}
                spec_dict['productID'] = product_id
                spec_dict['description'] = product_description
                key, value = '', ''
                for tag in spec_tags:    
                    if 'label' in str(tag):
                        key = tag.text
                    else:
                        value = tag.find('span').text + ':' + tag.find('div').text
                        spec_dict[key] = spec_dict.get(key, '') + ' . '+ value

                specfile.write(json.dumps(spec_dict)+'\n')

                cmt_page = 0
                comment_text = "init"
                while comment_text != "":
                    cmt_page += 1
                    comment_form = {"productid":product_id, "page":cmt_page, "score":0};
                    comment_text = requests.post(comment_api, params=comment_form).text
                    comment_soup = BeautifulSoup(comment_text, 'lxml')
                    for cmt in comment_soup.select('div.rc > p'):
                        data = cmt.select('i')
                        stars = [r for r in data if 'iconcom-txtstar' in str(r)]
                        nstar = len(stars)
                        user_cmt = data[-1].text
                        
                        features = [product_name, product_id, nstar, user_cmt]
                        features = map(str, features)
                        features = [re.sub('\n|\|', ' ', feature) for feature in features]
                        features = [re.sub('\s\s+', ' ', feature) for feature in features]

                        strcomment = '|'.join(features)
                        outcomment.write(strcomment+'\n')

outcomment.close()                       
specfile.close()
