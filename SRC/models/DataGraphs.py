import pandas as pd
import numpy as np
from models.Histograms_QQ import histogram_plot,Q_Q_Graphs


from bokeh.plotting import figure
from bokeh.embed import file_html,components
from bokeh.io import curdoc
from bokeh.themes import Theme

from bokeh.resources import CDN,INLINE
from bokeh.layouts import layout
from scipy import stats


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
            #Confidence interval
            #Data
            mu=Data_frame_separado[0]['Weitgh'].mean()
            sigma=Data_frame_separado[0]['Weitgh'].std()
            N=Data_frame_separado[0]['Weitgh'].count()
            alpha=0.05
            alpha_medios=alpha/2
            DF=N-1
            #Define z value
            Z_tabla=stats.norm.ppf(alpha_medios)
            #Inferior confidence limit
            LIC=mu-abs(Z_tabla)*(sigma/(N**0.5))
            #Superior  confidence limit
            LSC=mu+abs(Z_tabla)*(sigma/(N**0.5))
            #Inferior prediction limit.
            LIP=mu-abs(Z_tabla)*(sigma)*((1+1/N)**0.5)
            #Suoerior prediction limit.
            LSP=mu+abs(Z_tabla)*(sigma)*((1+1/N)**0.5)   

            #Inferior tolerance limit.
            LIT=mu-abs(1.96)*(sigma)
            #Superior tolerance limit.
            LST=mu+abs(1.96)*(sigma)
            #Graph about statistic intervals.
            x=[LIT,LST]
            y=[1.3,1.3]
            x2=[LIC,LSC]
            y2=[1.1,1.1]
            x3=[LIP,LSP]
            y3=[1.2,1.2]

            TOOL_TIPS=[("LS","$x")]
            figureStasticsIntervals=figure(title='Statistics_limits',plot_width=600,plot_height=200,tooltips=TOOL_TIPS)
            figureStasticsIntervals.line(x,y,line_width=6,color='#D7BDE2')
            figureStasticsIntervals.dash(x,y,size=100,angle=1.57)
            figureStasticsIntervals.line(x2,y2,line_width=6,color='#48C9B0')
            figureStasticsIntervals.dash(x2,y2,size=100,angle=1.57)
            figureStasticsIntervals.line(x3,y3,line_width=6,color='#3498DB')
            figureStasticsIntervals.dash(x3,y3,size=100,angle=1.57)
            #Get the second block of code about the Statistic graphs
            
            script3,div3=components(figureStasticsIntervals)
            js_resources3 = INLINE.render_js()
            css_resources3 = INLINE.render_css()

            data={
                "plot_script":script,
                "plot_div":div,
                "js_resources":js_resources,
                "css_resources":css_resources,
                "plot_script2":script2,
                "plot_div2":div2,
                "js_resources2":js_resources2,
                "css_resources2":css_resources2,
                "plot_script3":script3,
                "plot_div3":div3,
                "js_resources3":js_resources3,
                "css_resources3":css_resources3,
                "k2":round(k2),
                "p_value":round(p_value),
                "LIC":round(LIC,3),
                "LSC":round(LSC,3),
                "LIP":round(LIP,3),
                "LSP":round(LSP,3),
                "LIT":round(LIT,3),
                "LST":round(LST,3),
                }

            return data
        
        except Exception as ex:
            raise Exception(ex)
        
        


        