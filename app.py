import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://use.fontawesome.com/releases/v5.8.1/css/all.css', dbc.themes.FLATLY]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                title='North Carolina Utility Data')
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2283556934497259"
                crossorigin="anonymous"></script>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
server = app.server
app.config.suppress_callback_exceptions = True