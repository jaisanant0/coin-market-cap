import requests
import json
import pandas as pd

global_data=requests.get('https://api.coinmarketcap.com/v2/global')

gdjson_to_pyobj=json.loads(global_data.content.decode('utf-8'))

gd_df_data=pd.DataFrame(gdjson_to_pyobj,columns=['data'])

active_currencies=gd_df_data.loc['active_cryptocurrencies'].loc['data']
print(active_currencies)
active_markets=gd_df_data.loc['active_markets'].loc['data']
bitcoin_percentage_mcap=gd_df_data.loc['bitcoin_percentage_of_market_cap'].loc['data']
last_updated=pd.to_datetime(gd_df_data.loc['last_updated'].loc['data'],unit='s')

quotes_df=pd.DataFrame(gd_df_data.loc['quotes'].loc['data'])

total_market_cap=quotes_df.loc['total_market_cap'].loc['USD']
total_volume_24h=quotes_df.loc['total_volume_24h'].loc['USD']


print('''Active Currencies {0:>15s}\nActive Market {1:>20s}\nBTC Market Dominance {2:>14s}\nTotal Market Cap {3:>27s}
Total Volume 24h {4:>26s}\nLast Updated {5:>35s} \n'''.format((str(active_currencies)),(str(active_markets)),(str(bitcoin_percentage_mcap) +'%')
                                                              ,('$'+str(total_market_cap)),('$'+str(total_volume_24h)),(str(last_updated))))

t10_coin_whole=pd.DataFrame()
ticker=requests.get('https://api.coinmarketcap.com/v2/ticker/?start=1&limit=10')
tjson_to_pyobj=json.loads(ticker.content.decode('utf-8'))
t10_df=pd.DataFrame(tjson_to_pyobj)
t10_df.to_json('/home/JAIS/Desktop/top10',orient='records')

t10_file_df=pd.DataFrame((pd.DataFrame(pd.read_json('/home/JAIS/Desktop/top10')))['data'])
t10_file_data_df=pd.DataFrame(t10_file_df['data'])
for i in range(10) :
    t10_coin=pd.DataFrame(t10_file_data_df.loc[i]['data'])
    t10_coin_whole=t10_coin_whole.append(t10_coin)
    if i == 9 :
        break
    
sort_by_rank=(t10_coin_whole.sort_values('rank')).reset_index(drop=True)
print(sort_by_rank)
coin_name_df=(pd.DataFrame(sort_by_rank['name'],columns=['name']).rename({'name' : 'Coin Name'},axis=1))
#print(coin_name_df['Name'])
rank_df=(pd.DataFrame(sort_by_rank['rank'],columns=['rank']).rename({'rank' : 'Coin Rank'},axis=1))
#print(rank_df)
c_supply_df=(pd.DataFrame(sort_by_rank['circulating_supply']).rename({'circulating_supply' : 'Circulating Supply'},axis=1))
#a=c_supply_df.rename({'circulating_supply' : 'Circulating Supply'},axis=1)
#print(c_supply_df)
m_supply=(pd.DataFrame(sort_by_rank['max_supply']).rename({'max_supply' : 'Max Supply'},axis=1))
t_supply=(pd.DataFrame(sort_by_rank['total_supply']).rename({'total_supply' : 'Total Supply'},axis=1))

t10_quotes_df=(pd.DataFrame(sort_by_rank['quotes']))
t10_quotes_whole=pd.DataFrame()
for i in range(10) :
    quotes=pd.DataFrame(t10_quotes_df.loc[i].loc['quotes'],index=[i])
    t10_quotes_whole=t10_quotes_whole.append(quotes)
#print(t10_quotes_whole)

price=(pd.DataFrame(t10_quotes_whole['price']).rename({'price' : 'Price'},axis=1))
volume_24h=(pd.DataFrame(t10_quotes_whole['volume_24h']).rename({'volume_24h' : 'Volume 24h'},axis=1))
m_cap=(pd.DataFrame(t10_quotes_whole['market_cap']).rename({'market_cap' : 'Market Cap'},axis=1))
#print(m_cap)
p_chane_1h=(pd.DataFrame(t10_quotes_whole['percent_change_1h']).rename({'percent_change_1h' : 'Price Change 1h'},axis=1))
p_chane_24h=(pd.DataFrame(t10_quotes_whole['percent_change_24h']).rename({'percent_change_24h' : 'Price Change 24h'},axis=1))
p_chane_7d=(pd.DataFrame(t10_quotes_whole['percent_change_7d']).rename({'percent_change_7d' : 'Price Change 7d'},axis=1))
#t10_itoc=pd.DataFrame(t10_df['data'],index=t10_df['data'].columns )
#print(t10_itoc)


whole_detail_df=pd.concat([rank_df.reset_index(drop=True),coin_name_df.reset_index(drop=True),price.reset_index(drop=True)
                           ,m_cap.reset_index(drop=True),m_supply.reset_index(drop=True),t_supply.reset_index(drop=True),
                           volume_24h.reset_index(drop=True),p_chane_1h.reset_index(drop=True),p_chane_24h.reset_index(drop=True)
                           ,p_chane_7d.reset_index(drop=True)],axis=1)
whole_detail_df.to_csv('/home/JAIS/Desktop/coinmarketcap.csv',na_rep='Not Fixed',index=False)
#print(whole_detail_df)
