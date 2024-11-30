import csv
import math
import re

THRESHOLD = 500
BASE = '''
grf {
    grfid: "\42\4f\48\1";
    name: string(STR_GRF_NAME);
    desc: string(STR_GRF_DESCRIPTION);
    version: 1;
    min_compatible_version: 1;
}
'''

populations = {}

def convertfunc(pop):
  try:
    return max(math.floor(math.log(pop / 1000, 1.2)),0) + 1
  except ValueError as err:
    return 1

def clean_name(name):
  name = re.sub(r'\s?\(.*\)', '', name)
  name = re.sub(r'\s?Township', '', name)
  return name

townst = '\ntown_names {\n\tstyles : string(STR_STYLES);\n{\n'


with open("cityquiz_us_cities.csv", encoding="utf-8-sig") as f:
    data = csv.DictReader(f)
    for i in data:
        if i["archived"] == "FALSE":
            town_name = clean_name(i["name"])
            town_population = int(i["population"])
            if town_population >= THRESHOLD:
              try:
                  populations[town_name] += town_population
              except KeyError:
                  populations[town_name] = town_population

for k, v in populations.items(): 
  townst += f"\t\ttext(\"{k}\",{min(convertfunc(v), 127)}),\n"

open("names.nml","w").write(BASE+townst+'\n}}')
