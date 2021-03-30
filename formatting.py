import json
from re import compile, sub

input = """
{
    "win_iis_agent": {
        "Default Web Site": {
            "_id": "Memory Usage",
            "Memory Usage": 2713.0
        },
        "dotnettest": {
            "_id": "Memory Usage",
            "Memory Usage": 2713.0
        },
        "Default Web Site": {
            "_id": "Free Memory percent",
            "Free Memory percent": 41.0
        },
        "dotnettest": {
            "_id": "Free Memory percent",
            "Free Memory percent": 41.6
        },
        "Default Web Site": {
            "_id": "Used Memory percent",
            "Used Memory percent": 67.0
        },
        "dotnettest": {
            "_id": "Used Memory percent",
            "Used Memory percent": 67.0
        },
        "Default Web Site": {
            "_id": "Total (Mb)",
            "Total (Mb)": 4095.0
        },
        "dotnettest": {
            "_id": "Total (Mb)",
            "Total (Mb)": 4095.0
        }
    },
    "Linux_java_agent": {}
}
"""
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
def Update_Json(data_Dict, mInput):
    formatted_data = json.loads(mInput)
    toplevel_keys = list(formatted_data.keys())
    updatekey =0
    for dataDict in data_Dict:
        done = False
        uniQKeys = dataDict.keys()
        for key in toplevel_keys:
            if formatted_data[key].keys():
                for key1 in formatted_data[key].keys():
                    if key1.replace(' ', '') in uniQKeys:
                        formatted_data[key][key1] = dataDict[key1.replace(
                            ' ', '')]
                done = True
            if done:
                updatekey += 1
                break
    return formatted_data


# To Extract Duplicate keys value pairs
def Extract_Update(mInput, output_file_name=None):
    lines = []
    top_level_keys = []
    lines = [sub(pattern1, '', line.replace('\n', '').replace('\t', ''))
                 for line in mInput.split('\n')]

    top_level_keys = list(json.loads(mInput).keys())

    lines[-1] = '"optional_key":'
    top_level_keys = top_level_keys[1:]
    top_level_keys.append("optional_key")

    dataDict = ModifiedDict()
    keys = []
    values = []
    dict_list = []
    for line in lines:
        line = line.strip()
        if line != '' and line != ',' and line != '':
            if line[0] == '"' and line[-1] == ':' and line != '':
                key = sub(pattern2, '', line)
                keys.append(key)

                if key in [k.strip() for k in top_level_keys]:
                    dict_list.append(dataDict)
                    dataDict = ModifiedDict()
            else:
                values.extend(line.split(':'))
                values[-2] = sub(pattern3, '', values[-2])
                values[-1] = sub(pattern3, '', values[-1])
                if len(values) == 4:
                    dataDict[keys[-1]] = dict({values[0]: values[1], values[2]: float(values[3])})
                    values = []
    return Update_Json(dict_list, mInput)

if __name__ == '__main__':
    print(Extract_Update(input))