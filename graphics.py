import plotly
import plotly.graph_objs as go


def third_graphic():
    fig1 = go.Scatter3d(x=tuple(x for x in range(10000)),
                        y=tuple(x for x in range(10000)),
                        z=tuple(x for x in range(10000)),
                        marker=dict(opacity=0.9,
                                    reversescale=True,
                                    colorscale='Blues',
                                    size=5),
                        line=dict(width=0.02),
                        mode='markers')

    # Создаём layout
    mylayout = go.Layout(xaxis=dict(title="curb-weight"),
                         yaxis=dict(title="price"),
                         height=400,
                         width=350,
                         title='3Д График',
                         )

    # Строим диаграмму и сохраняем HTML
    return plotly.io.to_html({"data": [fig1],
                              "layout": mylayout},
                             full_html=False, )


def second_graphic():
    fig1 = go.Scatter(x=tuple(x for x in range(10000)),
                      y=tuple(x for x in range(10000)),
                      mode='markers')

    # Создаём layout
    mylayout = go.Layout(xaxis=dict(title="curb-weight"),
                         yaxis=dict(title="price"),
                         height=400,
                         width=350,
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
                         width=350,
                         title='1Д График',
                         )
    return plotly.io.to_html({"data": [fig],
                              "layout": mylayout},
                             full_html=False, )
