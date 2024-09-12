import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Inicializa o app Dash
app = dash.Dash(__name__)

# Dados iniciais das estacas e bairros..
estacas = {
    'Salvador Imbuí': ['Itapuã', 'Mussurunga', 'Lauro de Freitas', 'Brotas', 'Imbuí'],
    'Salvador': ['Cabula', 'Sete de Abril', 'Cajazeiras', 'Vale dos Lagos', 'Tancredo Neves'],
    'Salvador Norte': ['Barra', 'Rio Vermelho', 'Graça', 'Horto Florestal', 'Candeal', 'Alphaville'],
    'Salvador Sul': ['Boca do Rio', 'Amaralina', 'Cidade Baixa', 'Ogunjá', 'Vale das Pedrinhas']
}

categorias = [
    'Jovens casados',
    'Com idade de ser missionários',
    'Dificuldade de socialização',
    'Problemas familiares',
    'Recém chegados de ser missionários',
    'Problemas psicológicos'
]

# Armazena dados das estacas
dados_estacas = {estaca: {bairro: [0] * len(categorias) for bairro in bairros} for estaca, bairros in estacas.items()}

# Layout do app
app.layout = html.Div([
    html.Div([
        html.H1("Dashboard de Jovens", style={'color': '#333', 'textAlign': 'center'}),
        
        # Dropdown para selecionar Estaca
        html.Label("Estaca:", style={'color': '#555'}),
        dcc.Dropdown(
            id='estaca-dropdown',
            options=[{'label': estaca, 'value': estaca} for estaca in estacas.keys()],
            value='Salvador Imbuí',
            style={'width': '50%', 'margin': '10px auto'}
        ),
        
        # Dropdown para selecionar Bairro
        html.Label("Bairro:", style={'color': '#555'}),
        dcc.Dropdown(id='bairro-dropdown', style={'width': '50%', 'margin': '10px auto'}),
        
        # Inputs para categorias
        html.Div([
            html.Div([
                html.Label(categoria, style={'color': '#555'}),
                dcc.Input(id=f'input-{i}', type='number', value=0, min=0, style={
                    'width': '100px', 
                    'padding': '10px', 
                    'borderRadius': '5px', 
                    'border': '1px solid #ddd', 
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                    'marginRight': '10px'
                })
            ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'})
            for i, categoria in enumerate(categorias)
        ], style={'marginTop': '20px', 'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
        
        # Botão para atualizar os gráficos
        html.Button('Atualizar Gráficos', id='update-button', n_clicks=0, style={
            'backgroundColor': '#007bff', 
            'color': 'white', 
            'border': 'none', 
            'padding': '10px 20px', 
            'borderRadius': '5px', 
            'cursor': 'pointer',
            'fontSize': '16px',
            'marginTop': '20px'
        }),
        
        # Gráficos
        html.Div([
            html.Div(id='graphs-container', style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-start', 'marginTop': '20px'}),
            html.Div(id='bairro-graphs-container', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'marginTop': '40px'})
        ])
    ], style={'backgroundColor': '#f4f4f4', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'})
])

# Callback para atualizar a lista de bairros com base na estaca selecionada
@app.callback(
    Output('bairro-dropdown', 'options'),
    Input('estaca-dropdown', 'value')
)
def update_bairro_dropdown(selected_estaca):
    return [{'label': bairro, 'value': bairro} for bairro in estacas[selected_estaca]]

# Callback para criar os gráficos de pizza
@app.callback(
    [Output('graphs-container', 'children'),
     Output('bairro-graphs-container', 'children')],
    [Input('update-button', 'n_clicks')] +
    [Input(f'input-{i}', 'value') for i in range(len(categorias))] +
    [Input('estaca-dropdown', 'value'), Input('bairro-dropdown', 'value')]
)
def update_graphs(n_clicks, *args):
    valores = args[:-2]
    estaca_selecionada = args[-2]
    bairro_selecionado = args[-1]
    
    # Atualiza os dados da estaca selecionada
    dados_estacas[estaca_selecionada][bairro_selecionado] = valores
    
    # Cria o gráfico para a estaca selecionada
    fig_estaca = px.pie(
        values=[sum(dados_estacas[estaca_selecionada][bairro]) for bairro in estacas[estaca_selecionada]],
        names=estacas[estaca_selecionada],
        title=f'Distribuição de Categorias na Estaca {estaca_selecionada}',
        hole=0.3
    )
    
    # Cria gráficos para cada bairro da estaca selecionada
    fig_bairros = [
        dcc.Graph(
            figure=px.pie(
                values=dados_estacas[estaca_selecionada][bairro],
                names=categorias,
                title=f'{bairro} - {estaca_selecionada}',
                hole=0.3
            ),
            style={'flex': '1 1 40%', 'margin': '10px'}
        )
        for bairro in estacas[estaca_selecionada]
    ]
    
    return [dcc.Graph(figure=fig_estaca, style={'width': '100%', 'marginBottom': '20px'})], fig_bairros

# Executa o servidor no navegador
if __name__ == '__main__':
    app.run_server(debug=True)
