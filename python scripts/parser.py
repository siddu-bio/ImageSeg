import pandas as pd
import re
def parse_file(filename):
    fn = filename + ".txt" 
    file = open(fn)
    data = [[],[]]
    for line in file:
        if line.startswith("Image A:"):
            if line.find("PAC") != -1:
                antibody = "PAC "
            elif line.find("CON") != -1:
                antibody = "CON "
            ab = re.search(r"[A-Za-z0-9]{8,}",line)
            ab = ab.group()
            ab = ab[3::]
            antibody = antibody + ab
            if re.search(r"[0-9]{4,}",line) != None:
                number = re.search(r"[0-9]{4,}",line)
                number = number.group()
                slideID = str(antibody) + " " + number
                data[0].append(slideID)
            else:
                number = "0000"
                slideID = str(antibody) + " " + number
                data[0].append(slideID)
        if line.startswith("r="):
            pearsons = re.search(r"[^A-Za-z^_^=]{3,}",line)
            pearsons = pearsons.group()
            pearsons = pearsons.strip()
            data[1].append(pearsons)
    result = list(zip(data[0],data[1])) 
    return result
list_of_files = ["drg_con_nalcn_data","drg_pac_fam155a","drg_pac_nalcn","drg-con-fam_coloc_data"]
for file in list_of_files:
    data = pd.DataFrame(parse_file(file), columns = ["SlideID","PCC"])
    fname = file + ".xlsx"
    data.to_excel(fname)
