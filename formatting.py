import json
from re import compile, sub


input = """{"win_iis_agent": {"Default Web Site" :{"_id": "Memory Usage", "Memory Usage": 2713.0},"dotnettest" :{"_id": "Memory Usage", "Memory Usage": 2713.0},"Default Web Site" :{"_id": "Free Memory percent", "Free Memory percent": 41.0},"dotnettest" :{"_id": "Free Memory percent", "Free Memory percent": 41.6},"Default Web Site" :{"_id": "Used Memory percent", "Used Memory percent": 67.0},"dotnettest" :{"_id": "Used Memory percent", "Used Memory percent": 67.0},"Default Web Site" :{"_id": "Total (Mb)", "Total (Mb)": 4095.0},"dotnettest" :{"_id": "Total (Mb)", "Total (Mb)": 4095.0}},"Linux_java_agent": {}}"""

# Patterns To Deal With Keys
# Patterns To Deal With Keys

pattern1 = compile(r'[{}]')
pattern2 = compile(r'[":,\s]')
pattern3 = compile(r'[":,]')

# For Handeling Duplicate Keys and adding to a list with that key
class ModifiedDict(dict):
    def __setitem__(self, key, value):
        try:
            self[key].append(value)
        except KeyError:
            super(ModifiedDict, self).__setitem__(key, value)
        except AttributeError:
            super(ModifiedDict, self).__setitem__(key, [self[key], value])

# To Update The Json Data
def Update_Json(data_Dict, mInput, json_loadedString):
    formatted_data = json_loadedString
    toplevel_keys = list(formatted_data.keys())
    updatekey =0
    for dataDict in data_Dict:
        for key in formatted_data[toplevel_keys[updatekey]].keys():
            formatted_data[toplevel_keys[updatekey]][key] = dataDict[sub(pattern2,'',key)]
        updatekey +=1
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
                    dict_list.append(dataDict)
                    dataDict = ModifiedDict()
            else:
                values.extend(line.split(':'))
                midValues = values[1].split(',')
                key1 = sub(pattern3, '', values[0])
                val1 = sub(pattern3, '', midValues[0])
                key2 = sub(pattern3, '', midValues[1])
                val2 = sub(pattern3, '', values[2])

                if len(values) == 3:
                    dataDict[keys[-1]] = dict({key1: val1[1:],
                                               key2[1:]: float(val2)})
                    values = []
    return Update_Json(dict_list, mInput,json_loadedString)

if __name__ == '__main__': 
    print(Extract_Update(input))