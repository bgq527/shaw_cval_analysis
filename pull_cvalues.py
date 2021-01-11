import pandas as pd

excel_file = "data/cval_response_list_11_25.xlsx"
responses = pd.read_excel(excel_file)

phenology_file = "data/TNKY-Plants 12082020_8 _Dax Phenology columns.xlsx"
TNKY_db = pd.read_excel(phenology_file)

headers = responses.columns

index_to_species_cv = {k: v for k, v in enumerate(headers) if v != '' and ".1" not in v and "Unnamed" not in v}
# index_to_species_co = {k: v for k, v in enumerate(headers) if ".1" in v}
# print(index_to_species_co)

species_col = None
for idx, v in enumerate(TNKY_db.columns):
    if "sci_name" in list(TNKY_db[v]):
        species_col = v
        break
else:
    raise KeyError("Scientific name column not automatically found")

coc_col = None
for idx, v in enumerate(TNKY_db.columns):
    if "Coefficient of Conservatism" in list(TNKY_db[v]):
        coc_col = v
        break
else:
    raise KeyError("Scientific name column not automatically found")

c_value_col = None
for idx, v in enumerate(TNKY_db.columns):
    if "c_value" in list(TNKY_db[v]):
        c_value_col = v
        break
else:
    raise KeyError("Scientific name column not automatically found")

orig_values = {}
for idx, species_name in enumerate(TNKY_db[species_col]):
    species_name = str(species_name).lower()
    orig_value = list(TNKY_db.iloc[idx][-3:-1])

    to_dict = []
    for v in orig_value:
        if str(v) == "nan":
            to_dict.append("")
        else:
            to_dict.append(v)

    orig_values[species_name] = to_dict

print(orig_values)


c_values_dict = {}
for v in index_to_species_cv.values():
    species_name = v
    v = responses[v]
    c_values = []
    for cval in v:
        try:
            c_values.append(int(cval))
        except ValueError:
            continue

    if len(c_values) == 0:
        continue

    c_values_dict[species_name] = sum(c_values) / len(c_values)

new_str = ",\n"
for species_name in TNKY_db[species_col]:
    species_name = str(species_name).lower()
    c_value = c_values_dict.get(species_name)

    # if c_value is None:
    #     orig_value = orig_values.get(species_name)
    #     new_str += f"{orig_value[0]},{orig_value[1]}\n"
    # else:
    #     new_str += f"{round(c_value)},{round(c_value, 1)}\n"

    if c_value is None:
        orig_value = orig_values.get(species_name)
        new_str += f",\n"
    else:
        new_str += f"{round(c_value)},{round(c_value, 1)}\n"

output_file = open("output/cvalues_12_11.csv", 'w')
output_file.write(new_str)
output_file.close()