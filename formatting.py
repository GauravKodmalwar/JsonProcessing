import json
from re import compile, sub, match


input = """{"win_iis_agent": {"Default Web Site" :{"_id": "Memory Usage", "Memory Usage": 2713.0, "Memory Usage2": 2713.0, "Memory Usage3": 2713.0},"dotnettest" :{"_id": "Memory Usage", "Memory Usage": 2713.0,"Memory Usage2": 2713.0 },"Default Web Site" :{"_id": "Free Memory percent", "Free Memory percent": 41.0},"dotnettest" :{"_id": "Free Memory percent", "Free Memory percent": 41.6},"Default Web Site" :{"_id": "Used Memory percent", "Used Memory percent": 67.0},"dotnettest" :{"_id": "Used Memory percent", "Used Memory percent": 67.0},"Default Web Site" :{"_id": "Total (Mb)", "Total (Mb)": 4095.0},"dotnettest" :{"_id": "Total (Mb)", "Total (Mb)": 4095.0}},"Linux_java_agent": {"Default Web Site" :{"_id": "Memory Usage", "Memory Usage": 2713.0, "Memory Usage2": 2713.0, "Memory Usage3": 9713.0},"dotnettest" :{"_id": "Memory Usage", "Memory Usage": 2713.0, "Memory Usage2": 713.0},"Default Web Site" :{"_id": "Free Memory percent", "Free Memory percent": 41.0},"dotnettest" :{"_id": "Free Memory percent", "Free Memory percent": 41.6},"Default Web Site" :{"_id": "Used Memory percent", "Used Memory percent": 67.0},"dotnettest" :{"_id": "Used Memory percent", "Used Memory percent": 67.0},"Default Web Site" :{"_id": "Total (Mb)", "Total (Mb)": 4095.0},"dotnettest" :{"_id": "Total (Mb)", "Total (Mb)": 9095.0}}}"""

pattern1 = compile(r'[{}]')
pattern2 = compile(r'[":,\s]')
pattern3 = compile(r'["]')
matchNum = compile(r"[\d]+\.*[\d]*")

# For Handeling Duplicate Keys and adding to a list with that key

class ModifiedDict:
    def __init__(self):
        self.dict = {}

    def add(self, key, dictionary):
        keys = list(self.dict.keys())
        if key in keys:
            self.dict[key].append(dictionary)
        else:
            self.dict[key] = []
            self.dict[key].append(dictionary)


# To Update The Json Data

def Update_Json(data_Dict, mInput, json_loadedString):
    formatted_data = json_loadedString
    toplevel_keys = list(formatted_data.keys())
    updatekey = 0
    for dataDict in data_Dict:
        for key in formatted_data[toplevel_keys[updatekey]].keys():
            formatted_data[toplevel_keys[updatekey]
                           ][key] = dataDict[sub(pattern2, '', key)]
        updatekey += 1
    return formatted_data


# To Extract Duplicate keys value pairs

def Extract_Update(mInput):
    lines = []
    top_level_keys = []
    lines = [line for line in sub(pattern1, '\n', input).split('\n')]

    json_loadedString = json.loads(mInput)
    top_level_keys = list(json_loadedString.keys())

    lines.append('"optional_key":')
    top_level_keys = top_level_keys[1:]
    top_level_keys.append("optional_key")

    dataDict = ModifiedDict()
    keys = []
    values = []
    dict_list = []
    for line in lines:
        line = line.strip()

        if line != '' and line != ',' and line != ' ':
            if (line[0] == '"' or line[0] == ',') and line[-1] == ':' and line != '':
                key = sub(pattern2, '', line)
                keys.append(key)

                if key in [k.strip() for k in top_level_keys]:
                    dict_list.append(dataDict.dict)
                    dataDict = ModifiedDict()
            else:
                values.extend(line.split(':'))
                newvalues = list()
                newvalues.append(sub(pattern3, '', values[0].strip()))
                for val in values[1:-1]:
                    doubleValues = val.split(',')
                    newvalues.append(
                        sub(pattern3, '', doubleValues[0].strip()))
                    newvalues.append(
                        sub(pattern3, '', doubleValues[1].strip()))
                newvalues.append(sub(pattern3, '', values[-1].strip()))
                updateIndex = 0
                tempdict = {}
                while updateIndex < len(newvalues):
                    key = float(newvalues[updateIndex]) if matchNum.match(
                        newvalues[updateIndex]) else newvalues[updateIndex]
                    value = float(newvalues[updateIndex+1]) if matchNum.match(
                        newvalues[updateIndex+1]) else newvalues[updateIndex+1]
                    if key == "_id":
                        dataDict.add(keys[-1], tempdict)
                        tempdict[key] = value
                    else:
                        tempdict[key] = value
                    updateIndex += 2
                    
                values = []
    return Update_Json(dict_list, mInput, json_loadedString)


if __name__ == '__main__':
    data = Extract_Update(input)
    with open(r"C:\PYTHON\JsonProcessing\OutPut.json", 'w') as f:
        json.dump(data, f, indent=4)
    print(data)
