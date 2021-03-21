import requests as rq
import re
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

# Requesting url and creating soup object
url = ''
r = rq.get(url)
soup = bs(r.content, 'html.parser')

# Using regex to find the html division with JSON data
pattern = re.compile(r".*window.initData.screener_type = 'stock';")
script = soup.find('script', text=pattern).contents[0]

# Splitting the retrieved block by newline character to get the specific line with JSON data.
data = str(script).split('\n')[4][34:-2].replace("\\", '')  # Cleaning JSON format.
jsn = json.loads(data)

data_list = []  # Empty list that will be used to create a DataFrame.

# Looping over the data key (list) of the JSON, every index is a JSON dict containing data for one stock.
for item in range(len(jsn['data'])):
    item_data = jsn['data'][item]['d']
    data_dic = {'short_name': item_data[1], 'name': item_data[12], 'sector': item_data[11], 'last': item_data[2],
                'change_per': item_data[3], 'change_price': item_data[4], 'recommendation': item_data[5],
                'vol': item_data[6], 'mrkt_cap': item_data[7]}
    data_list.append(data_dic)

cols = ['short_name', 'name', 'sector', 'last',
        'change_per', 'change_price', 'recommendation', 'vol', 'mrkt_cap']
df = pd.DataFrame(data_list, columns=cols)
# Saving Data.
df.to_csv('stock_data.csv', index=False)

