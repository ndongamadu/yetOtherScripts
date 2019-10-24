import pandas as pd

pop_cod_location = "/Users/amadu/Downloads/POP_COD/"
pop_cod_name = "gin_population_statistic_2019_unfpa_v2.xlsx"

# Global settings for each sheet
sheets = ["GIN_ADM0_POP", "GIN_ADM1_POP", "GIN_ADM2_POP", "GIN_ADM3_POP"]  # list of sheet name starting to the first one
start = [5, 7, 10, 11]  # list of start column
core_tag = "#population"
#


def cleanSADD(sex, ageRange):
    sex = str(sex).lower()
    if sex == '#m':
        sex = 'm'
    else:
        if sex == '#f':
            sex = 'f'
        else:
            sex = 'all'

    ageRanges = ageRange.split("age")[1].split("-")
    if len(ageRanges) == 1:
        ageRanges[0] = ageRanges[0].split("+")[0]
        ageRanges.append("plus")
    age_ = "age_" + ageRanges[0] + "_" + ageRanges[1]
    # if age_ == "age_0_1":
    #     age_ = "infants +" + age_
    # else:
    #     if age_ in ["age_0_4", "age_1_4", "age_5_9", "age_10_14"]:
    #         age_ = "children +" + age_
    #     else:
    #         if age_ == "age_15_19":
    #             age_ = "adolescents +" + age_
    #         else:
    #             if age_ in ["age_20_24", "age_25_29", "age_30_34", "age_35_39", "age_40_44", "age_45_49", "age_50_54", "age_55_59"]:
    #                 age_ = "adults +" + age_
    #             else:
    #                  age_ = "elderly +" + age_
    
    saddTag = sex + " +" + age_
    return saddTag


def hxlate(cell):
    c = cell.split("+")
    return core_tag + " +" + cleanSADD(c[0], c[1])


indice = 0
for tab in sheets:
    data = pd.read_excel(pop_cod_location + pop_cod_name, sheet_name=tab)
    data.iloc[0, start[indice]:] = data.iloc[0, start[indice]:].apply(hxlate)
    data.to_excel(pop_cod_location + tab + ".xlsx", sheet_name=tab)
    indice = indice + 1




