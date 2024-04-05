import pandas as pd
import numpy as np
from models.Histograms_QQ import histogram_plot,Q_Q_Graphs

from bokeh.io import output_notebook,show,output_file
from bokeh.plotting import figure
from bokeh.embed import file_html,components

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

            
            
            Histograma_Weitgh=[histogram_plot(Data_frame_separado[i],'Weitgh',m=mu_lista[i],std=sigma_lista[i],distribution='normal') for i in range(len(Uniques_values))]
            
            Graficas_Q_Q=[Q_Q_Graphs(Data_frame_separado[i],'Weitgh',distribution='normal') for i in range(len(Uniques_values))]

            lay_out_total=layout(Histograma_Weitgh,Graficas_Q_Q)
            html=file_html(lay_out_total,CDN,'histograma')
            return html
        
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def HistogramJson(self,db):
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

            
            
            Histograma_Weitgh=[histogram_plot(Data_frame_separado[i],'Weitgh',m=mu_lista[i],std=sigma_lista[i],distribution='normal',ancho=300,alto=300) for i in range(len(Uniques_values))]
            
            Graficas_Q_Q=[Q_Q_Graphs(Data_frame_separado[i],'Weitgh',distribution='normal',ancho=300,alto=300) for i in range(len(Uniques_values))]

            lay_out_total=layout(Histograma_Weitgh,Graficas_Q_Q)
            script,div=components(lay_out_total)
            js_resources = INLINE.render_js()
            css_resources = INLINE.render_css()
            data={
                "plot_script":script,
                "plot_div":div,
                "js_resources":js_resources,
                "css_resources":css_resources}

            return data
        
        except Exception as ex:
            raise Exception(ex)
        
        


        