import pandas as pd
import numpy as np
from models.Histograms_QQ import histogram_plot,Q_Q_Graphs


from bokeh.plotting import figure
from bokeh.embed import file_html,components
from bokeh.io import curdoc
from bokeh.themes import Theme

from bokeh.resources import CDN,INLINE
from bokeh.layouts import layout
import math
import statsmodels.api as sm
from scipy import stats
import random

class DataGraphs():

    @classmethod
    def HistogramWeight(self,db):
        try:
            connect_db=db.connect
            QUERY_CONSULTA="""SELECT  animals_feature.idFeature,animals_feature.idAnimals,animals_feature.Weitgh,animals_feature.time_life,animals.NAME
                        FROM animals_feature
                        INNER JOIN animals ON animals_feature.idAnimals=animals.idAnimals"""
            Data_frame=pd.read_sql_query(QUERY_CONSULTA,connect_db)

            #Clasificando los datos.
            Uniques_values=list(Data_frame.idAnimals.unique())
            Data_frame_separado=[Data_frame.loc[Data_frame.idAnimals==Uniques_values[i]] for i in range(len(Uniques_values))]
            mu_lista=[Data_frame_separado[i]['Weitgh'].mean() for i in range(len(Uniques_values))]
            sigma_lista=[Data_frame_separado[i]['Weitgh'].std() for i in range(len(Uniques_values))]    

            
            
            Histograma_Weitgh=[histogram_plot(Data_frame_separado[i],'Weitgh','Cats' , m=mu_lista[i],std=sigma_lista[i],distribution='normal') for i in range(len(Uniques_values))]
            
            Graficas_Q_Q=[Q_Q_Graphs(Data_frame_separado[i],'Weitgh','Cats',distribution='normal') for i in range(len(Uniques_values))]

            lay_out_total=layout(Histograma_Weitgh,Graficas_Q_Q)
            html=file_html(lay_out_total,CDN,'histograma')
            return html
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def HistogramJson(self,db,name):
        try:
            connect_db=db.connect
            QUERY_CONSULTA="""SELECT  animals_feature.idFeature,animals_feature.idAnimals,animals_feature.Weitgh,animals_feature.time_life,animals.NAME
                        FROM animals_feature
                        INNER JOIN animals ON animals_feature.idAnimals=animals.idAnimals
                        WHERE animals.NAME='{}'""".format(name)
            Data_frame=pd.read_sql_query(QUERY_CONSULTA,connect_db)

            #Clasificando los datos.
            Uniques_values=list(Data_frame.idAnimals.unique())
            Data_frame_separado=[Data_frame.loc[Data_frame.idAnimals==Uniques_values[i]] for i in range(len(Uniques_values))]
            mu_lista=[Data_frame_separado[i]['Weitgh'].mean() for i in range(len(Uniques_values))]
            sigma_lista=[Data_frame_separado[i]['Weitgh'].std() for i in range(len(Uniques_values))]    

            Histograma_Weitgh=[histogram_plot(Data_frame_separado[i],'Weitgh',name,m=mu_lista[i],std=sigma_lista[i],distribution='normal',ancho=500,alto=300) for i in range(len(Uniques_values))]
            Graficas_Q_Q=[Q_Q_Graphs(Data_frame_separado[i],'Weitgh',name,distribution='normal',ancho=500,alto=300) for i in range(len(Uniques_values))]

            #Get the first block of code about the histogram
            lay_out_total=layout(Histograma_Weitgh)
            script,div=components(lay_out_total)
            js_resources = INLINE.render_js()
            css_resources = INLINE.render_css()
            
            #Get the second block of code about the Q_Q_Graphs
            lay_out_total_QQ=layout(Graficas_Q_Q)
            script2,div2=components(lay_out_total_QQ)
            js_resources2 = INLINE.render_js()
            css_resources2 = INLINE.render_css()

            #Normaltest
            k2,p_value=stats.normaltest(Data_frame_separado[0]['Weitgh'])       

            data={
                "plot_script":script,
                "plot_div":div,
                "js_resources":js_resources,
                "css_resources":css_resources,
                "plot_script2":script2,
                "plot_div2":div2,
                "js_resources2":js_resources2,
                "css_resources2":css_resources2,
                "k2":round(k2),
                "p_value":round(p_value)}

            return data
        
        except Exception as ex:
            raise Exception(ex)
        
        


        