## M-x conda-env-activate ret py311
## M-x run-python
## C-c C-r to evaluate

import pandas as pd
pd.set_option('display.max_columns', None)
import pathlib 
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels as sm
import statsmodels.formula.api as smf
import os
from shillerdata import ShillerData  ## filename, classname

os.system("ls -hl")




obj = ShillerData(url = "http://www.econ.yale.edu/~shiller/data/ie_data.xls")
obj.prepare_data()
obj.df

obj.columns()
obj.moments(year = 1930, inflation_threshold=3)

obj.df.loc[ (obj.df['year'].astype(int) > 1930) & (obj.df['yoy_cpi_inflation'] > 3)].loc[:, ['yoy_cpi_inflation', 'yoy_sp_return', 'long_interest_rate_gs10']].agg(['count', 'min', 'mean', 'std', 'median', 'max'])


obj.df_raw.shape
obj.df.shape

## pd.DataFrame(obj.df.columns, columns=['colname'])
## obj.df.loc[ (obj.df['year'].astype(int) > 1930) & (obj.df['yoy_cpi_inflation'] > 3)].loc[:, ['yoy_cpi_inflation', 'yoy_sp_return','long_interest_rate_gs10']].mean()
##obj.df.loc[ (obj.df['year'].astype(int) > 1930) & (obj.df['yoy_cpi_inflation'] > 3)].loc[:, ['yoy_cpi_inflation', 'yoy_sp_return', 'long_interest_rate_gs10']].median()

## TODO...



