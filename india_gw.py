# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 16:33:58 2024

@author: Deep_
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

for dirname, _, filenames in os.walk(r"C:\Users\Deep_\Downloads\Kaggle\India_GW\Data"):
    for filename in filenames:
        print(os.path.join(dirname,filename))
        
#Read the data
df = pd.read_csv(r"C:\Users\Deep_\Downloads\Kaggle\India_GW\Data\Dynamic_2017_2_0.csv", index_col=0)

print(df.isna().sum())

df = df.dropna()

print(df.isna().sum())

print(df.shape)
print(df.info)
print(df.dtypes)

f, ax = plt.subplots(figsize=(10,7))
sns.heatmap(df.drop(df.columns[:2], axis=1).corr(), annot=True)
plt.show()


# =============================================================================
# Net Ground Water Availability for future use
# =============================================================================
def calculate_annual_reserve(df_local):
    state_list_local = []
    total_gw_water_recharge_local = []
    curr_gw_extr_list_local = []
    future_available_gw_list_local = []

    for state_local, subset in df_local.groupby('Name of State'):
        state_list_local.append(state_local)
        total_gw_water_recharge_local.append(sum(subset['Total Annual Ground Water Recharge']))
        curr_gw_extr_list_local.append(sum(subset['Total Current Annual Ground Water Extraction']))
        future_available_gw_list_local.append(sum(subset['Net Ground Water Availability for future use']))

    df_1 = pd.DataFrame({"State": state_list_local,
                          "GW_Recharge": total_gw_water_recharge_local,
                          "GW_Extraction": curr_gw_extr_list_local, 
                          "Future_GW_Available": future_available_gw_list_local})

    df_1.sort_values(['GW_Recharge', 'GW_Extraction'], inplace=True)
    df_1['Annual_Reserve'] = df_1['GW_Recharge'] - df_1['GW_Extraction']

    return df_1

df_1 = calculate_annual_reserve(df)

f,ax = plt.subplots(figsize=(12,8))
plt.barh(df_1['State'],df_1['Annual_Reserve'], color=(df_1['Annual_Reserve']>0).map({True: 'g',False: 'r'}))
plt.show()


f,ax = plt.subplots(figsize=(12,8))
sns.set_color_codes("muted")
sns.barplot(x="GW_Recharge", y="State", data = df_1, label="Available GW",color="b")
sns.barplot(x="GW_Extraction", y="State", data = df_1, label="GW Extraction", color="r")
ax.legend(ncol=2,loc="upper right", frameon="True")
plt.show()

f,ax = plt.subplots(figsize=(12,8))
df_1.sort_values("Future_GW_Available",inplace=True)
sns.barplot(x="Future_GW_Available", y="State", data=df_1)
plt.show()


df_raj = df[df["Name of State"] == "RAJASTHAN"]



for state in list(df["Name of State"].unique()):
    print(state)


f,ax = plt.subplots(figsize=(12,8))
sns.barplot(x="Annual GW Allocation for Domestic Use as on 2025", y="Name of District", data=df_raj)
plt.show()

df_raj.sort_values("Stage of Ground Water Extraction (%)", ascending=True,inplace=True)
print(df_raj[["Name of State","Name of District", "Stage of Ground Water Extraction (%)"]])



plt.figure(figsize=(12,9))
sns.barplot(x="Recharge from rainfall During Monsoon Season",y="Name of State", data=df)
plt.show()


fig,axs = plt.subplots(6,6,figsize=(12,8))

for idx,state in enumerate(df['Name of State'].value_counts().sort_values(ascending=False)[0:36].index):
    print(idx,state)
    axs[idx//6,idx%6].hist(x = df[df['Name of State']==state]['Stage of Ground Water Extraction (%)'], color='b')
    axs[idx//6,idx%6].set_title(state)
plt.suptitle("State wise GW Extraction distribution")
plt.tight_layout()
fig.subplots_adjust(top=0.88)
plt.show()









































