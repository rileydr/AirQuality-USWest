import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.neighbors import KNeighborsClassifier

import knockknock
kk_url = "https://hooks.slack.com/services/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"
kk_channel_name = 'jupyter-notebook'
kk_users = ['@rileyrobertsond']

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def sum_stats(dataframe, filename_string, y_variable):
        
    import sys
    with open(f'{filename_string}', 'w') as f:

        ## COLUMN HEADERS 
        print('index'     ,',',     # 0
              'feature'   ,',',     #
              'dtype'     ,',',     #   
              'non-nulls' ,',',     # 'alias: col_count'
              'nulls'     ,',',     #
              'pct_nulls' ,',',     # 5
              'unique'    ,',',     #
              'mode'      ,',',     #
              'mode_count',',',     #
              'min'       ,',',     #
              'q1'        ,',',     # 10
              'median'    ,',',     #
              'q3'        ,',',     #
              'max'       ,',',     #     
              'mean'      ,',',     #
              'stdev'     ,',',     # 15
              'var'       ,',',     #
              'skew'      ,',',     #
              'kurtosis'  ,',',     #
              'y_corr',             #
              file=f
             )
        col_index = -1  # for index column, starting the numbering at -1 so first row is 0
        
        ## VARIABLE ASSIGNMENTS (DETERMINED BY DATATYPE) 
        for (columnName, columnData) in dataframe.iteritems():
                ## OBJECTS
            if columnData.dtype == object or columnData.dtype == str:                                   
                col_index += 1                                                        # 0
                col_name = columnName                                                 #
                col_dtype = columnData.dtype                                          #
                col_count = columnData.count()   #non-nulls                           #
                col_nulls = columnData.isnull().sum()                                 #
                col_pct_nulls = round((columnData.isnull().sum())/len(columnData),2)  # 5
                col_unique = columnData.nunique()                                     # 
                col_mode = list(columnData.value_counts().items())[0][0]              #
                col_mode_count = columnData.value_counts().max()                      #
                
                col_min = ''                                                          #
                col_q1 = ''                                                           # 10
                col_median = ''                                                       #
                col_q3 = ''                                                           #
                col_max = ''                                                          #
                
                col_mean = ''                                                         #
                col_stdev = ''                                                        # 15
                col_var = ''                                                          #
                col_skew = ''                                                         # 
                col_kurt = ''                                                         #
                col_y_corr = ''                                                       #
                  
                ## NUMERICS
            else:     
                col_index += 1                                                        # 0
                col_name = columnName                                                 #                
                col_dtype = columnData.dtype                                          #
                col_count = columnData.count()   #non-nulls                           #  
                col_nulls = columnData.isnull().sum()                                 #
                col_pct_nulls = round((columnData.isnull().sum())/len(columnData),2)  # 5
                col_unique = columnData.nunique()                                     # 
                col_mode = columnData.mode()[0]                                       #
                col_mode_count = columnData.value_counts().max()                      #          
                
                col_min = columnData.min()                                            #
                col_q1 = columnData.quantile(.25)                                     # 10
                col_median = columnData.median()                                      #
                col_q3 = columnData.quantile(.75)                                     #           
                col_max = columnData.max()                                            #
                
                col_mean = columnData.mean()                                          #
                col_stdev = columnData.std()                                          # 15
                col_var = columnData.var()                                            #
                col_skew = columnData.skew()                                          #
                col_kurt = columnData.kurtosis()                                      #
                try:
                    col_y_corr = columnData.corr(dataframe[y_variable])               #
                except:
                    col_y_corr = ''

                ## PRINT VARIABLES
            print(col_index       ,',',     # 0
                  col_name        ,',',     #
                  col_dtype       ,',',     #
                  col_count       ,',',     #
                  col_nulls       ,',',     #
                  col_pct_nulls   ,',',     # 5
                  col_unique      ,',',     #
                  col_mode        ,',',     #
                  col_mode_count  ,',',     #
                  col_min         ,',',     #
                  col_q1          ,',',     # 10                
                  col_median      ,',',     #
                  col_q3          ,',',     #                  
                  col_max         ,',',     #          
                  col_mean        ,',',     #
                  col_stdev       ,',',     # 15
                  col_var         ,',',     #
                  col_skew        ,',',     #
                  col_kurt        ,',',     #
                  col_y_corr,               #
                  file=f
                  )

### VALUE COUNT DISPLAYS

def val_counts(dataframe):

    for (columnName, columnData) in dataframe.iteritems():

        print(f'Column Name: {columnName}')
        print(f'Unique Values: {dataframe[columnName].nunique()}')
        print('')
        print(dataframe[columnName].value_counts())
        print('')
        print('_________________________')
        print('')
        print('')


def all_uniques(dataframe):

    for (columnName, columnData) in dataframe.iteritems():

        print(f'Column Name: {columnName}')
        print(f'Unique Values: {dataframe[columnName].nunique()}')
        print(f'Unique Values: {np.sort(columnData.unique())}')
        print('')
        print(dataframe[columnName].value_counts())
        print('_________________________')
        print('')
        print('')

### PLOTS

def rapid_plots(dataframe, y_var,min_corr):
    plt.style.use('seaborn-darkgrid')             # removable or customizable

    plot_list = [] 

    for (columnName, columnData) in dataframe.iteritems():
        if columnData.dtype != object:
            if (abs(columnData.corr(dataframe[y_var])) > min_corr) and columnData.corr(dataframe[y_var]) != 1:
                plt.figure()
                viz = sns.regplot(x=dataframe[columnName], y=dataframe[y_var], color='steelblue')
                plt.title(f'{columnName}: {round(columnData.corr(dataframe[y_var]), 5)}')
                plot_list.append(viz)
            else:
                pass
        else:
            pass
                
    return plot_list


### QUICK MODELS

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def quickmod_knns(X, y, klist,random_state=74):
    for k in klist:
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)
        sc = StandardScaler()
        Z_train = sc.fit_transform(X_train)
        Z_test = sc.transform(X_test)
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(Z_train, y_train)
        print(f'𝑘 = {k}')
        print(f'Train Accuracy: {knn.score(Z_train, y_train)}')
        print(f' Test Accuracy: {knn.score(Z_test, y_test)}')
        print('')

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def quickmod_logregsa_nlp(X_train, y_train, X_test, y_test, alist, penalty, solver='liblinear', random_state=74):
    for a in alist:
        sc = StandardScaler(with_mean=False)
        Z_train = sc.fit_transform(X_train)
        Z_test = sc.transform(X_test)
        logreg = LogisticRegression(penalty=penalty, C=(1/a), solver=solver, random_state=random_state)
        logreg.fit(Z_train, y_train)
        print(f'𝛼 = {a}')
        print(f'𝐶 = {1/a}')
        print(f'Train Accuracy: {logreg.score(Z_train, y_train)}')
        print(f' Test Accuracy: {logreg.score(Z_test, y_test)}')
        print('')

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def quickmod_logregsa(X, y, alist, penalty, solver='liblinear', random_state=74):
    for a in alist:
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)
        sc = StandardScaler()
        Z_train = sc.fit_transform(X_train)
        Z_test = sc.transform(X_test)
        logreg = LogisticRegression(penalty=penalty, C=(1/a), solver=solver, random_state=random_state)
        logreg.fit(Z_train, y_train)
        print(f'𝛼 = {a}')
        print(f'𝐶 = {1/a}')
        print(f'Train Accuracy: {logreg.score(Z_train, y_train)}')
        print(f' Test Accuracy: {logreg.score(Z_test, y_test)}')
        print('')

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def quickmod_logregsa_coefs(X, y, alist, penalty, solver='liblinear', random_state=74):
    for a in alist:
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)
        sc = StandardScaler()
        Z_train = sc.fit_transform(X_train)
        Z_test = sc.transform(X_test)
        logreg = LogisticRegression(penalty=penalty, C=(1/a), solver=solver, random_state=random_state)
        logreg.fit(Z_train, y_train)
        coefs = list(zip(X.columns, (list(np.exp(logreg.coef_)[0]))))
        print(f'𝛼 = {a}')
        print(f'𝐶 = {1/a}')
        print(f'Intercept: {logreg.intercept_[0]}')
        print(f'Coefficients:')
        for coef in coefs:
            print(coef)
        print('')

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def quickmod_logregsc(X, y, clist, penalty, solver='liblinear', random_state=74):
    for c in clist:
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)
        sc = StandardScaler()
        Z_train = sc.fit_transform(X_train)
        Z_test = sc.transform(X_test)
        logreg = LogisticRegression(penalty=penalty, C=c, solver=solver, random_state=random_state)
        logreg.fit(Z_train, y_train)
        print(f'𝐶 = {c}')
        print(f'Train Accuracy: {logreg.score(Z_train, y_train)}')
        print(f' Test Accuracy: {logreg.score(Z_test, y_test)}')  
        print('')

@knockknock.slack_sender(webhook_url=kk_url, channel=kk_channel_name, user_mentions=kk_users)
def quickmod_logregsc_coefs(X, y, clist, penalty, solver='liblinear', random_state=74):
    for c in clist:
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)
        sc = StandardScaler()
        Z_train = sc.fit_transform(X_train)
        Z_test = sc.transform(X_test)
        logreg = LogisticRegression(penalty=penalty, C=c, solver=solver, random_state=random_state)
        logreg.fit(Z_train, y_train)
        print(f'𝐶 = {c}')
        print(f'Intercept: {logreg.intercept_[0]}')
        print(f'Coefficients:')
        for coef in coefs:
            print(coef)
        print('')


# print(f'     Intercept: {logreg.intercept_[0]}')
# print(f'  Coefficients: {logreg.coef_[0]}')
# print(f'   Predictions: {logreg.predict(X_test)[:10]}')        
# print(f' Probabilities: {logreg.predict_proba(X_test)[:10]}')      



def make_colormap(colors_list): 
    from colour import Color
    from matplotlib.colors import LinearSegmentedColormap

    color_map = LinearSegmentedColormap.from_list( 'my_list', [ Color( c ).rgb for c in colors_list ] )
    plt.figure( figsize = (15,3))
    plt.imshow( [list(np.arange(0, len( ramp_colors ) , 0.1)) ] , interpolation='nearest', origin='lower', cmap= color_map )
    plt.xticks([])
    plt.yticks([])
    return color_map

# custom_cmap = make_colormap( ['#ACD701','#69B636','#32A318'] ) 