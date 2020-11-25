import pandas as pd

excel_file = "data/cval_response_list_11_25.xlsx"
responses = pd.read_excel(excel_file)

headers = responses.columns


five_resp = set()
three_resp = set()
one_resp = set()
five_com = set()
three_com = set()
one_com = set()

all_sp = set()
for key in headers[3:]:
    if key != "end":
        num_filled = 28 - (responses[key].isnull().sum())
        if ".1" in key:
            if num_filled >= 5:
                five_com.add(key.replace(".1", ''))
                three_com.add(key.replace(".1", ''))
                one_com.add(key.replace(".1", ''))
                all_sp.add(key.replace(".1", ''))
            elif num_filled >= 3:
                three_com.add(key.replace(".1", ''))
                one_com.add(key.replace(".1", ''))
                all_sp.add(key.replace(".1", ''))
            elif num_filled >= 1:
                one_com.add(key.replace(".1", ''))
                all_sp.add(key.replace(".1", ''))
        else:
            if num_filled >= 5:
                five_resp.add(key.replace(".1", ''))
                one_resp.add(key.replace(".1", ''))
                all_sp.add(key.replace(".1", ''))
            elif num_filled >= 3:
                three_resp.add(key.replace(".1", ''))
                one_resp.add(key.replace(".1", ''))
                all_sp.add(key.replace(".1", ''))
            elif num_filled >= 1:
                one_resp.add(key.replace(".1", ''))
                all_sp.add(key.replace(".1", ''))




num_users = 0
for i in range(27):
    if responses.loc[i].isnull().sum() not in [7592, 7594]:
        num_users += 1

all_sp = list(all_sp)
all_sp.sort()
five_resp = list(five_resp)
five_resp.sort()
one_resp = list(one_resp)
one_resp.sort()
five_com = list(five_com)
five_com.sort()
one_com = list(one_com)
one_com.sort()

nl = "\n"

write_string = ""
write_string += f"Number of users,{num_users}\n"
write_string += f"Number of five response C-value species,{len(five_resp)}\n"
write_string += f"Number of three response C-value species,{len(three_resp)}\n"
write_string += f"Number of one response C-value species,{len(one_resp)}\n"
write_string += f"Number of five response comment species,{len(five_com)}\n"
write_string += f"Number of three response comment species,{len(three_com)}\n"
write_string += f"Number of one response comment species,{len(one_com)}\n"
write_string += f"Number of species with values (C-val or comment),{len(all_sp)}\n\n"
write_string += f"Five response C-value species\n{nl.join(five_resp)}\n\n"
write_string += f"Three response C-value species\n{nl.join(three_resp)}\n\n"
write_string += f"One response C-value species\n{nl.join(one_resp)}\n\n"
write_string += f"Species with values (C-val or comment)\n{nl.join(all_sp)}\n\n"

write_file = open("output/11_25_stats.csv", 'w')
write_file.write(write_string)
write_file.close()

