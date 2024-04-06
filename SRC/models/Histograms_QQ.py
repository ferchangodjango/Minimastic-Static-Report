import statsmodels.api as sm
from scipy import stats
import numpy as np
import random
import pandas as pd
from bokeh.io import output_notebook,show
from bokeh.plotting import figure
from bokeh.layouts import layout
import math
from bokeh.io import curdoc 

#Q_Q_Graphs(Data,column,distribution,s,n,p)
#You need to pass the Data, column
#You can change the kind of distribution ['normal','lognormal','binomial']
#Scale for distribution lognormal
#n y p for distribution binomial

def Q_Q_Graphs(Data,column,distribution,s=0.9,n=500,p=0.1,ancho=400,alto=400):
    curdoc().theme='dark_minimal'
    figure_Q_Q=figure(title='Q-Q of '+str(column),plot_width=ancho,plot_height=alto)
    figure_Q_Q.xgrid.grid_line_color=None
    figure_Q_Q.ygrid.grid_line_alpha=0.7
    figure_Q_Q.xaxis.axis_label='Size'
    figure_Q_Q.yaxis.axis_label='Probability desity'
    figure_Q_Q.toolbar.autohide=True
    
    if distribution=='normal':
        
        Datos_Q_Q=Data[[column]].sort_values(by=column)
        Datos_Q_Q=Datos_Q_Q.reset_index(drop=True)
        Datos_Q_Q=Datos_Q_Q.reset_index()
        Datos_Q_Q['i']=Datos_Q_Q['index']+1
        Datos_Q_Q['j']=(Datos_Q_Q['i']-(1/2))/Datos_Q_Q['index'].count()
        Datos_Q_Q['Z']=stats.norm().ppf(Datos_Q_Q['j'])
        figure_Q_Q.y_range.start = Datos_Q_Q[column].min()
        figure_Q_Q.x_range.start = Datos_Q_Q['Z'].min()
        figure_Q_Q.scatter(Datos_Q_Q.Z,Datos_Q_Q[column])
        return figure_Q_Q

    elif distribution=='lognormal':
        Datos_Q_Q=Data[[column]].sort_values(by=column)
        Datos_Q_Q=Datos_Q_Q.reset_index(drop=True)
        Datos_Q_Q=Datos_Q_Q.reset_index()
        Datos_Q_Q['i']=Datos_Q_Q['index']+1
        Datos_Q_Q['j']=(Datos_Q_Q['i']-(1/2))/Datos_Q_Q['index'].count()
        Datos_Q_Q['Z']=stats.lognorm.ppf(Datos_Q_Q['j'],s)
        
        figure_Q_Q.y_range.start = Datos_Q_Q[column].min()
        figure_Q_Q.x_range.start = Datos_Q_Q['Z'].min()
        figure_Q_Q.scatter(Datos_Q_Q.Z,Datos_Q_Q[column])
        return figure_Q_Q
    
    elif distribution=='binomial':
        Datos_Q_Q=Data[[column]].sort_values(by=column)
        Datos_Q_Q=Datos_Q_Q.reset_index(drop=True)
        Datos_Q_Q=Datos_Q_Q.reset_index()
        Datos_Q_Q['i']=Datos_Q_Q['index']+1
        Datos_Q_Q['j']=(Datos_Q_Q['i']-(1/2))/Datos_Q_Q['index'].count()
        Datos_Q_Q['Z']=stats.binom.ppf(Datos_Q_Q['j'],n,p)
        figure_Q_Q.y_range.start = Datos_Q_Q[column].min()
        figure_Q_Q.x_range.start = Datos_Q_Q['Z'].min()
        figure_Q_Q.scatter(Datos_Q_Q.Z,Datos_Q_Q[column])
        return figure_Q_Q
        
#histogram_plot(Data,column,distribution,m=0,std=1)
#You need to pass the Data, column
#You can change the kind of distribution ['normal','lognormal','binomial']
#Scale for distribution lognormal
#n y p for distribution binomial



def histogram_plot(Data,column,distribution,m=0,std=1,s=0.9,n=500,p=0.1,ancho=400,alto=400):
    curdoc().theme='dark_minimal'
    N=Data[column].count()
    figure_h=figure(title='NORMAL_DISTRIBUTION',plot_width=ancho,plot_height=alto,
               toolbar_location="below")
    figure_h.xgrid.grid_line_color=None
    figure_h.ygrid.grid_line_alpha=0.7
    figure_h.xaxis.axis_label='STD_DESV'
    figure_h.yaxis.axis_label='Probability'
    figure_h.toolbar.autohide=True
    Number_intervals=int(round(1+3.322*math.log10(N),0))
    
    if distribution=='normal':
        hist,edges=np.histogram(Data[column],density=True,bins=Number_intervals)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.norm.pdf(x,m,std)
        # Histograma distribución normal
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Normal_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h 
        
    elif distribution=='lognormal':
        hist,edges=np.histogram(Data[column],density=True,bins=100)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.lognorm.pdf(x,s)
        #Histograma distribucion logonormal
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Logormal_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h
        
    elif distribution=='binomial':
        hist,edges=np.histogram(Data[column],density=True,bins=Number_intervals)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.binom.pmf(x,n,p)
        #Histograma distribucion binomial
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Binomial_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h
    
#histogram_plot_limit(Data,column,distribution,m=0,std=1,s=0.9,n=500,p=0.1,limit1,limit2)
#You need to pass the Data, column
#You can change the kind of distribution ['normal','lognormal','binomial']
#Scale for distribution lognormal
#n y p for distribution binomial
#limit 1 is the min value for you want to calculated the probability
#limit 2 is the max value for you want to calculated the probability

def histogram_plot_limit(Data,column,distribution,limit1,limit2,m=0,std=1,s=0.9,n=500,p=0.1):
    N=Data[column].count()
    Number_intervals=int(round(1+3.322*math.log10(N),0))
    if distribution=='normal':
        hist,edges=np.histogram(Data[column],density=True,bins=100)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.norm.pdf(x,m,std)
        posiciones=np.where((edges>=limit1)&(edges<limit2))
        index_Incial=posiciones[0][0]
        index_final=posiciones[0][-1]
        edges_marcado=edges[index_Incial:index_final+1]
        hist_marcado=hist[index_Incial:index_final+1]
        # Histograma distribución normal
        figure_h=figure(title='NORMAL_DISTRIBUTION',plot_width=600,plot_height=400)
        figure_h.xgrid.grid_line_color=None
        figure_h.ygrid.grid_line_alpha=0.7
        figure_h.xaxis.axis_label='STD_DESV'
        figure_h.yaxis.axis_label='Probability'
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Normal_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        figure_h.quad(top=hist_marcado,bottom=0,left=edges_marcado[:-1],right=edges_marcado[1:],
                      fill_color='#512E5F',line_color='black',legend_label='Normal_distribution')
        return figure_h 
        
    elif distribution=='lognormal':
        hist,edges=np.histogram(Data[column],density=True,bins=100)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.lognorm.pdf(x,s)
        figure_h=figure(title='LOGNORMAL_DISTRIBUTION',plot_width=600,plot_height=400)
        figure_h.xgrid.grid_line_color=None
        figure_h.ygrid.grid_line_alpha=0.7
        figure_h.xaxis.axis_label='STD_DESV'
        figure_h.yaxis.axis_label='Probability'
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Logormal_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h
        
    elif distribution=='binomial':
        hist,edges=np.histogram(Data[column],density=True,bins=Number_intervals)
        x = np.linspace(min(Data[column]), max(Data[column]), num=N)
        y = stats.binom.pmf(x,n,p)
        figure_h=figure(title='BINOMIAL_DISTRIBUTION',plot_width=600,plot_height=400)
        figure_h.xgrid.grid_line_color=None
        figure_h.ygrid.grid_line_alpha=0.7
        figure_h.xaxis.axis_label='STD_DESV'
        figure_h.yaxis.axis_label='Probability'
        figure_h.quad(top=hist,bottom=0,left=edges[:-1],right=edges[1:],
              fill_color='#008080',line_color='black',legend_label='Binomial_distribution')
        figure_h.line(x,y,color='#181515',line_width=2)
        return figure_h