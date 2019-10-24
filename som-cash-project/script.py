import pandas as pd

# global settings
output = "output"
extension = ".csv"
folder = "/Users/amadu/AnacondaProjects/cash-2018/"
data_location = folder + "Somalia_CASH_3W_All_Cluster_Jan - August_2019_v1.xlsx"
pcodes = pd.read_csv('/Users/amadu/AnacondaProjects/data/new_somalia-adm1-adm2-codes.csv', usecols=['DIST_NAME', 'DIS_CODE'], sep=";")

# read the df as pandas obj called df
print("=== Getting data ===")
df = pd.read_excel(data_location)
print(df.head(10))

# upper all columns name
# list columns names
cols = df.columns
print("== columns names ==")
df.columns = ['CLUSTER', 'ORGANIZATION', 'IMPLEMENTING PARTNER', 'PROGRAMME NAME',
              'ACTIVITY DESCRIPTION', 'DONOR', 'MODALITY', 'CONDITIONALITY', 'MULTIPURPOSE CASH', 'DELIVERY MECHANISM',
              'RESTRICTION', 'TRANSFER VALUE (USD)', 'FREQUENCY', 'TOTAL TRANSFERS USD', 'REGION',
              'DISTRICT', 'SPECIFIC LOCATION', 'RURAL/URBAN', 'STATUS', 'DURATION',
              'START DATE (DD/MM/YY)', 'END DATE (DD/MM/YY)', 'Y_COORD', 'X_COORD',
              'Total # of INDIVIDUALS', '# of HOUSEHOLDS', 'Women', 'Men', 'Girls',
              'Boys', 'CHEKS', 'Additional Comments']
print(cols)

# clean conditionality
print("=== cleaning conditionality ===")
df.loc[df['CONDITIONALITY'].isin(['Yes - Cash for work', 'Yes, Cash for work', 'Cash For Work']), 'CONDITIONALITY'] = 'Yes - cash for work'
df.loc[df['CONDITIONALITY'].isin(['No - unconditional', 'Unconditional ', 'unconditional ', 'unconditional']), 'CONDITIONALITY'] = 'Unconditional'
df.loc[df['CONDITIONALITY'].isin(['Conditional ', 'conditional', 'Yes', 'Restricted', 'Food for work',
                                 'unskilled labour', 'skilled labour', 'Cash']), 'CONDITIONALITY'] = 'Conditional'
df.loc[df['CONDITIONALITY'].isin(['yes-cash for assets', 'Cash for Assets']), 'CONDITIONALITY'] = 'Yes - Cash for assets'
print(df['CONDITIONALITY'].unique())

# delivery mechanism cleaning
print("=== delivery mechanism ===")
df.loc[df['DELIVERY MECHANISM'].isin(['Cash- Mobile ', 'through mobile transfer', 'Cash- Mobile', 'Mobile transfer',
                                     ' mobile ', 'Mobile money transfer', 'Cash Mobile', 'Mobile', 'Cash - Mobile',
                                      'mobile cash', 'Mobile Transfer']), 'DELIVERY MECHANISM'] = 'Cash - mobile'
df.loc[df['DELIVERY MECHANISM'].isin(['Money/cash transfer', 'Deposit account', 'Cash - bank transfer', 'Food', 'in kind ',
                                     'EVC Plus', 'monthly', 'Agricultural input', 'other', 'Cash - Hawaala',
                                      'Woqooyi Galbeed', 'Togdheer', 'Sanaag']), 'DELIVERY MECHANISM'] = 'Unspecified'
df.loc[df['DELIVERY MECHANISM'].isin(['Voucher', 'Food Vourcher ', 'Voucher - Paper', 'Voucher-Paper']), 'DELIVERY MECHANISM'] = 'Voucher - paper'
df.loc[df['DELIVERY MECHANISM'].isin(['e-voucher', 'e-Voucher']), 'DELIVERY MECHANISM'] = 'E-voucher'
df.loc[df['DELIVERY MECHANISM'].isin(['Cash -  in hand', 'Cash in hand', 'cash in hand']), 'DELIVERY MECHANISM'] = 'Cash - In Hand'
print(df['DELIVERY MECHANISM'].unique())

# cleaning restriction
print("=== Cleaning restriction ===")
df.loc[df['RESTRICTION'].isin(['Vulnerable People', 'Unconditional', '1.2dollar per I metre of Soil bund',
                              '1 dollar per I metre of Soil bund', '65 USD ', '70 USD', '75 USD',
                               '280 USD', '40 USD']), 'RESTRICTION'] = 'Unspecified'
df.loc[df['RESTRICTION'].isin(['restricted', 'restricted ', 'yes']), 'RESTRICTION'] = 'Restricted'
df.loc[df['RESTRICTION'].isin(['unrestricted ', 'unrestricted', 'unrestricted', 'No', 'NO']), 'RESTRICTION'] = 'Unrestricted'
print(df['RESTRICTION'].unique())

# cleaning Rural/Urban
print("=== Rural/Urban ===")
df.loc[df['RURAL/URBAN'].isin(['rural', 'Rural', 'Rural ', ' Rural', 'rURAL']), 'RURAL/URBAN'] = 'RURAL'
df.loc[df['RURAL/URBAN'].isin(['urban', 'Urban ', 'Urban', 'urban ']), 'RURAL/URBAN'] = 'URBAN'
df.loc[df['RURAL/URBAN'].isin(['Xayira', 'Gumays', 'ongoing', 'planned', 'completed', 'TBC', 'Baki']), 'RURAL/URBAN'] = 'Unspecified'
df.loc[df['RURAL/URBAN'].isin(['Mixed', 'Mixed ', 'RURAL/idp']), 'RURAL/URBAN'] = 'MIXED'
df.loc[df['RURAL/URBAN'] == 'IDP', 'RURAL/URBAN'] = 'IDPs'
print(df['RURAL/URBAN'].unique())

# functions
# Fillna (here Unspecified) a given column in a given dataframe


def fillNa(df, col):
    df[col].fillna('Unspecified', inplace=True)
    return 0


# In practice
print("=== Filling NA ===")
for col in ['CONDITIONALITY', 'RESTRICTION', 'DELIVERY MECHANISM', 'RURAL/URBAN']:
    fillNa(df, col)

# getting districts and pcoding it
print("=== Cleaning districts ===")
districts = pd.DataFrame(df.DISTRICT.unique())
districts = districts.rename(columns={0: "district_name"})
# pcodes = pcodes[['DIST_NAME', 'DIS_CODE']]
districts = districts.merge(pcodes, how='left', left_on='district_name', right_on='DIST_NAME')

# sometimes missing districts codes need to be fixed
districts.loc[districts['district_name'] == 'Mogadishu/Daynile', 'DIS_CODE'] = 0
districts.loc[districts['district_name'] == 'Mogadishu', 'DIS_CODE'] = 0
districts.loc[districts['district_name'] == 'Daynile', 'DIS_CODE'] = 22
districts.loc[districts['district_name'] == 'Wadajir', 'DIS_CODE'] = 0
districts.loc[districts['district_name'] == 'Hodan', 'DIS_CODE'] = 22
districts.loc[districts['district_name'] == 'Mogadishu/Dharkenley', 'DIS_CODE'] = 0
print(districts.head(10))

# getting regions and pcoding
print("=== Cleaning regions ===")
regions = pd.DataFrame(df.REGION.unique())
regions = regions.rename(columns={0: "region_name"})
regions.loc[regions['region_name'] == 'Lower Shabelle', 'REG_CODE'] = 23
regions.loc[regions['region_name'] == 'Mudug', 'REG_CODE'] = 18
regions.loc[regions['region_name'] == 'Bakool', 'REG_CODE'] = 25
regions.loc[regions['region_name'] == 'Woqooyi Galbeed', 'REG_CODE'] = 12
regions.loc[regions['region_name'] == 'Togdheer', 'REG_CODE'] = 13
regions.loc[regions['region_name'] == 'Banadir', 'REG_CODE'] = 22
regions.loc[regions['region_name'] == 'Lower Juba', 'REG_CODE'] = 28
regions.loc[regions['region_name'] == 'Bari', 'REG_CODE'] = 16
regions.loc[regions['region_name'] == 'Gedo', 'REG_CODE'] = 26
regions.loc[regions['region_name'] == 'Sanaag', 'REG_CODE'] = 15
regions.loc[regions['region_name'] == 'Bay', 'REG_CODE'] = 24
regions.loc[regions['region_name'] == 'Galgaduud', 'REG_CODE'] = 19
regions.loc[regions['region_name'] == 'Middle Shabelle', 'REG_CODE'] = 21
regions.loc[regions['region_name'] == 'Hiraan', 'REG_CODE'] = 20
regions.loc[regions['region_name'] == 'Lower juba', 'REG_CODE'] = 28
regions.loc[regions['region_name'] == 'GEDO', 'REG_CODE'] = 26
regions.loc[regions['region_name'] == 'gedo', 'REG_CODE'] = 26
regions.loc[regions['region_name'] == 'Sool', 'REG_CODE'] = 14
regions.loc[regions['region_name'] == 'Awdal', 'REG_CODE'] = 11
regions.loc[regions['region_name'] == 'Nugaal', 'REG_CODE'] = 17
print(regions.head(10))

# adding in the dataframe the two news codes columns
print("=== Adding region and district codes columns ===")
df['REG_CODE'] = 0
df['DIS_CODE'] = 0
print(df.head())

# pcoding
print("=== Pcoding regions and districts ===")
for row in districts.iterrows():
    df.loc[df.DISTRICT == row[1].DIST_NAME, 'DIST_CODE'] = row[1].DIS_CODE

for row in regions.iterrows():
    df.loc[df.REGION == row[1].region_name, 'REG_CODE'] = row[1].REG_CODE

print(df.head())

# write to the default folder
print("========== Exporting data ==========")
df.to_csv(folder + 'monthlyData/' + output + extension)

print("<<<<< DONE ! >>>>>")
# end

