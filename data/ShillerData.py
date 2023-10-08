## M-x conda-env-activate ret py311
## M-x run-python
## C-c C-r to evaluate

import pandas as pd
        
class ShillerData:
    def __init__(self, url: str, sheet_name = 'Data', skip_rows = 7, parse_dates = True) -> None:
        self.url = url,
        self.sheet_name = sheet_name,
        self.df_raw = pd.read_excel(url, sheet_name = sheet_name, skiprows = skip_rows, parse_dates = parse_dates)

    def prepare_data(self) -> None:
        ## Compute New Columns
        self.df = self.df_raw.copy()

        self.df[['year', 'month']] = self.df['Date'].map(str).str.split(pat = '\.', expand = True)
        self.df['datestamp'] =  pd.to_datetime( self.df['year'] + "-" + self.df['month'], errors='coerce')
        self.df.rename( columns={
            "Date" : "YYYYMM",
            "Fraction": "date_fraction",
            "Rate GS10": "long_interest_rate_gs10",
            "Price": "real_price",
            "Dividend": "real_dividend",
            "Price.1": "real_total_return_price",
            "Earnings": "real_earnings",
            "Earnings.1": "real_tr_scaled_earnings",
            "CAPE": "cape",
            "TR CAPE": "tr_cape"
        }, inplace=True)
        self.df.drop(['Unnamed: 13', 'Unnamed: 15', 'Yield', 'Returns', 'Returns.1',
                 'Real Return', 'Real Return.1', 'Returns.2'
                 ], axis=1, inplace=True)
        self.df.rename(columns= {
            'P' : 'sp_comp_p',
            'D' : 'dividend',
            'E' : 'earnings',
            'CPI' : 'cpi'
        }, inplace=True)
        self.df.drop([1831], axis=0, inplace=True)
        self.df['earnings_lag12'] = self.df['earnings'].shift(12)
        self.df['cpi_lag12'] = self.df['cpi'].shift(12)
        self.df['cpi_lag120'] = self.df['cpi'].shift(120)
        self.df['sp_comp_p_lag12'] = self.df['sp_comp_p'].shift(12)
        self.df['yoy_cpi_inflation'] = (self.df['cpi']/self.df['cpi_lag12'] - 1) * 100
        self.df['yoy_sp_return'] = 100* ((self.df['sp_comp_p']/self.df['sp_comp_p_lag12'] - 1) + (self.df['dividend']/self.df['sp_comp_p_lag12']))
        self.df['excess_cape_yield'] = 100 * (1/ self.df['cape'] - ( self.df['long_interest_rate_gs10']/100  - (((self.df['cpi'] / self.df['cpi_lag120'])**(1/10))-1)))

    def columns(self) -> pd.DataFrame:
        return pd.DataFrame(self.df.columns, columns=['colname'])

    def moments(self, year=1930, inflation_threshold = 3):
        return self.df.loc[ (obj.df['year'].astype(int) > year) & (obj.df['yoy_cpi_inflation'] > inflation_threshold)].loc[:, ['yoy_cpi_inflation', 'yoy_sp_return', 'long_interest_rate_gs10']].agg(['count', 'min', 'mean', 'std', 'median', 'max'])

