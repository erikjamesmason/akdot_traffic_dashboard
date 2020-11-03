import pandas as pd
import plotly.graph_objs as go

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def read_data(dataset):
    """
    simple function to read in data to Pandas Dataframe
    """
    
    df = pd.read_csv(dataset)
    
    return df

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    graph_one = []
    df = read_data('data/AADT_TrafficLink_Dataframe2_TableToExcel.csv')
    
   # df_sterling = df.loc[df['Route_Name']=='Sterling Highway']
    df_list = df.iloc[:, 12:25]
    df_melt = df.melt(id_vars='Traffic_Link_ID', value_vars=df_list)
    df_melt = df_melt.sort_values(['Traffic_Link_ID', 'variable'])
    # df_pivot = df_melt.pivot(index="variable", columns="Traffic_Link_ID", values="value")
    df_melt = df_melt.head(65)
    
    link_list = df_melt.Traffic_Link_ID.unique().tolist()
    for link in link_list:
        x_val = df_melt[df_melt['Traffic_Link_ID']==link].variable.tolist()
        y_val = df_melt[df_melt['Traffic_Link_ID']==link].value.tolist()
        graph_one.append(
              go.Scatter(
              x = x_val,
              y = y_val,
              mode = 'lines',
              name = link,
                  connectgaps=True,
                  hoverinfo="all", hovertext=["variable", "value"]
              )
          )
    
    layout_one = dict(title = 'Sample AADT',
                xaxis = dict(title = '',
                  autotick=False, tick0=2012, dtick=1),
                yaxis = dict(title = 'aadt'),
                      hovermode= "closest",
                      autorange="reversed"
                )
    df_region = df.groupby('REGION').mean().reset_index()
    df_region = df_region.drop('AADT_2006', axis=1)
    df_regions = df_region.iloc[:, 7:18]
    
    df_regions['Region'] = df_region["REGION"]
    region_cols = df_region.iloc[:, 7:18]
    df_region_melt = df_regions.melt(id_vars='Region', value_vars=region_cols)
    
    df_region_melt = df_region_melt.loc[df_region_melt['Region'] != "CENTRAL,NORTHERN"]
    df_region_melt

#     second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    
    x_val = df_region_melt.Region
    y_2019_val = y_val = df_region_melt.loc[df_region_melt['variable']=='AADT_2019'].value
    y_2018_val = y_val = df_region_melt.loc[df_region_melt['variable']=='AADT_2018'].value
    y_2017_val = y_val = df_region_melt.loc[df_region_melt['variable']=='AADT_2017'].value
    graph_two.append(
         go.Bar(
         x = x_val,
         y = y_2019_val,
             hovertext = ['2019','2019','2019'],
            name='2019'
         )
    )
    graph_two.append(
        go.Bar(
         x = x_val,
         y = y_2018_val.tolist(),
             hovertext = ['2018','2018','2018'],
            name='2018'
         )
    )
    graph_two.append(
        go.Bar(
         x = x_val,
         y = y_2017_val.tolist(),
             hovertext = ['2017','2017','2017'],
            name='2017'
         )
    )
   
    layout_two = dict(title = 'Average AADT by Region by Year', 
                      xaxis = dict(title = 'Region'),
                      yaxis = dict(title = 'Culmative Average AADT'),
                      hovermode= "closest",
                    )


# third chart plots percent of population that is rural from 1990 to 2015
    
    graph_three = []
    graph_three.append(
      go.Scatter(
      x = df.Functional_Class,
      y = df.AADT_2019.tolist(),
      mode = 'markers',
          text=df['Traffic_Link_ID'],
          marker=dict(color=df.AADT_2019.tolist(),
                      colorscale='Viridis')
      )
    )
    
    layout_three = dict(title = '2019 AADT by Functional Class',
                xaxis = dict(title = 'Functional Class'),
                yaxis = dict(title = '2019 AADT'),
                        hovermode= "closest",
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    df_fc = df.groupby('Functional_Class')['Traffic_Link_ID'].nunique()
    graph_four.append(
      go.Bar(
      x = df_fc,
      y = df.Functional_Class.unique(),
          orientation='h',
      )
    )

    layout_four = dict(title = 'Count of Traffic Links by Functional Class',
                xaxis = dict(title = 'Traffic Link Count'),
                yaxis = dict(title = 'Functional Class'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures