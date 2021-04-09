import pandas as pd
import argparse
import matplotlib.pyplot as plt

covid_data = pd.read_csv('owid-covid-data (1).csv',encoding = 'ISO-8859-1')
df = covid_data.loc[:,['location','date','total_cases','new_cases','total_deaths','new_deaths']]
df.insert(1,'month',pd.DatetimeIndex(df['date']).month)
df = df[pd.DatetimeIndex(df['date']).year == 2020].drop(['date'],axis = 1)
final = df.pivot_table(values=['new_cases', 'new_deaths'],index=['location','month'],aggfunc=sum)
final.insert(0,'total_cases',df.groupby(['location','month'])['total_cases'].max())
final.insert(2,'total_deaths',df.groupby(['location','month'])['total_deaths'].max())
final.insert(0,'case_fatality_rate',final['new_deaths']/final['new_cases'])
final.head()

plot_data = pd.DataFrame()
plot_data.insert(0,'confirmed_new_cases',df.groupby('location')['total_cases'].max())
plot_data.insert(1,'case_fatality_rate',df.groupby('location')['total_deaths'].max()/plot_data['confirmed_new_cases'])
plot_data = plot_data[((plot_data.case_fatality_rate - plot_data.case_fatality_rate.mean()) / plot_data.case_fatality_rate.std()).abs() < 3]
plot_data.plot.scatter(x='confirmed_new_cases',y='case_fatality_rate')
plot_data.plot.scatter(x='confirmed_new_cases',y='case_fatality_rate', logx = True)
