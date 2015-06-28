import csv
import re
from collections import Counter
from collections import defaultdict

date_dic = defaultdict(list)
# auto-align: ctrl+alt+L

# Read the dictionary from csv file
reader = csv.reader(open('dict2.csv', 'rb'))
date_dic = dict(x for x in reader)
stock_list = []
statistics = {}
# Compress the value of dictionary into a list for statistics
value_lists = date_dic.values()
for ele in value_lists:
    current_value_list = re.findall(r'\$(.*?)\'',ele)
    stock_list.extend(current_value_list)

for item in [stock_list]:
    c = Counter(item)
    most_ten = c.most_common()[:10] # top 10

for value in most_ten:
    statistics[value[0]] = value[1]

print most_ten
# Regular expression objects: https://docs.python.org/2/library/re.html
writer = csv.writer(open('Stock_most_mentioned.csv', 'wb'))
for key, value in statistics.items():
    writer.writerow([key, value])
