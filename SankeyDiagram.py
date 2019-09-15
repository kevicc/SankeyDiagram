# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 10:25:58 2019

@author: kpericak
"""

import pandas as pd 
import numpy as np
from plotly.offline import iplot
from tabulate import tabulate

listInput = [
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS NOTHING','N/A','N/A', 80],  
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','MAKEUP','SPENDS >= $20', 15],
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','MAKEUP','SPENDS < $20', 5],
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','CLOTHES','SPENDS >= $20', 2],
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','CLOTHES','SPENDS < $20', 8],
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','FACE CARE','SPENDS >= $20',1],
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','FACE CARE','SPENDS < $20',9],
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','FOOD', 'SPENDS >= $20', 0],
             ['ENTERS MALL', 'ENTERS STORE', 'BUYS SOMETHING','FOOD', 'SPENDS < $20', 10],
             ['ENTERS MALL', 'N/A', 'N/A','N/A','N/A', 150]        
            ]    

headers = ['MALL', 'STORE', 'ACTION', 'ITEM', 'SPEND', 'COUNTS']

df = pd.DataFrame(list(listInput))     #create dataframe
df.columns = headers
df = df.replace('N/A', np.NaN)

#https://medium.com/kenlok/how-to-create-sankey-diagrams-from-dataframes-in-python-e221c1b4d6b0

def genSankey(df,cat_cols=[],value_cols='', title=''):
    
    labelList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))        
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList)) 
            
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    
    #make sankey now
    data_trace = dict(
    type = 'sankey',
    domain = dict(
                  x =  [0,1],
                  y =  [0,1]
                 ),
    orientation = "h",
    #valueformat = "00.0f",
    node = dict(
                pad = 5,
                thickness = 30,
                line = dict(
                            color = "black",
                            width = 0.5
                            ),
    label =  labelList 
    ),
    link = dict(
              source = sourceTargetDf['sourceID'],
              target = sourceTargetDf['targetID'],
              value = sourceTargetDf['count']      
               )
    )

    layout = dict(
                    title = title,
                    #height = 500,
                    #width = 1000,
                    font = dict(
                                size = 10
                                )
                 )


    fig = dict(data=[data_trace], layout=layout)
    return fig

fig = genSankey(df,
                cat_cols = ['STORE', 'ACTION', 'ITEM','SPEND'],
                value_cols = 'COUNTS', title = 'Purchase Journey at a Store in the Mall'
                )
iplot(fig)

headers = list(df)
print(tabulate(df,headers=headers))

