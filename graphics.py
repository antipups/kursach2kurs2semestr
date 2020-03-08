import plotly
import plotly.graph_objs as go


def third_graphic(**kwargs):
    fig1 = go.Scatter3d(x=kwargs.get('x'),
                        y=kwargs.get('y'),
                        z=kwargs.get('z'),
                        marker=dict(opacity=0.9,
                                    reversescale=True,
                                    colorscale='Blues',
                                    size=5),
                        mode='lines+markers')

    # Создаём layout
    mylayout = go.Layout(xaxis=dict(title="curb-weight"),
                         yaxis=dict(title="price"),
                         height=400,
                         title='3Д График',
                         )

    # Строим диаграмму и сохраняем HTML
    return plotly.io.to_html({"data": [fig1],
                              "layout": mylayout},
                             full_html=False, )


def second_graphic(**kwargs):
    fig1 = go.Scatter(x=kwargs.get('x'),
                      y=kwargs.get('y'),
                      mode='lines+markers')     # как именно представить

    # Создаём layout
    mylayout = go.Layout(xaxis=dict(title=kwargs.get('name_x')),
                         yaxis=dict(title=kwargs.get('name_y')),
                         height=400,
                         title='2Д График',
                         )

    # Строим диаграмму и сохраняем HTML
    return plotly.io.to_html({"data": [fig1],
                              "layout": mylayout},
                             full_html=False, )


def first_graphic(**kwargs):
    fig = go.Pie(labels=kwargs.get('labels'),
                 values=kwargs.get('values'))
    mylayout = go.Layout(
                         height=400,
                         title='1Д График',
                         )
    return plotly.io.to_html({"data": [fig],
                              "layout": mylayout},
                             full_html=False, )
