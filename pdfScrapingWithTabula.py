import pandas as pd
import tabula
# import os

pdf = 'data/Burkina Projection_com_Burkina_2007_2020.pdf'

df = tabula.read_pdf(pdf, pages=9, multiple_tables=True, encoding='utf-8')
# print(df)
pd.DataFrame(df).to_excel('data/page9.xlsx', encoding='utf-8')
# tabula.convert_into(df, "page9.csv", output_format="csv")
