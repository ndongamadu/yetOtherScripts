import pandas as pd
from script import *

# global settings
output = "February"
extension = ".csv"
folder = "/Users/amadu/AnacondaProjects/cash-2019/"
data_location = folder + "Somalia_CASH_3W_All_Cluster_January - September_2019.xlsx"
pcodes = pd.read_csv('/Users/amadu/AnacondaProjects/data/new_somalia-adm1-adm2-codes.csv', usecols=['DIST_NAME', 'DIS_CODE'], sep=";")


# read the df as pandas obj called df
print("=== Getting data ===")
df = pd.read_excel(data_location, sheet_name=output)
print(df.head(10))

print("=== Pcodes are ===")
print(pcodes)

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

cleanConditionality(df)
cleanDeliveryMechanism(df)
cleanRestriction(df)
cleanRuralUrban(df)
fillingNA(df)

districts = DistrictsPcoder(df, pcodes)
print(districts)
print(" === Fixing missing districts ===")
# sometimes missing districts codes need to be fixed
# districts.loc[districts['district_name'] == 'Baydhaba', 'DIS_CODE'] = 0

print(districts)

regions = RegionsPcoder(df)
print(regions)

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
