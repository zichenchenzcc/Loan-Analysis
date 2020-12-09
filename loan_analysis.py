import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from Loan import *
from functions import *
import dash_table
from dash.exceptions import PreventUpdate
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

# input loan amount, payment per month, interest per year and extra payment for the first loan
controls = dbc.Card(
    [
        dcc.Store(id='memory-output'),
        dcc.Store(id='memory-outputa'),
        dcc.Store(id='memory-outputb'),
        dcc.Store(id='memory-outputc'),
        dcc.Store(id='memory-outputfig'),
        html.H4(dbc.Label("First Loan")),
        dbc.FormGroup([
                html.H5(dbc.Label("Loan amount")),
                dcc.Input(type="number", 
                          id="loan-amount")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("Payment per month")),
                dcc.Input(type="number", 
                          id="payment-per-month")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("Interest rate per year")),
                dcc.Input(type="number", 
                          id="interest-rate")
        ]),
        html.Div(id="error1"),
        dbc.FormGroup([
                html.H5(dbc.Label("extra1")),
                dcc.Input(type="number", 
                          id="extra1")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("extra2")),
                dcc.Input(type="number", 
                          id="extra2")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("extra3")),
                dcc.Input(type="number", 
                          id="extra3")
        ]),
        
    ],
    body=True,
)

# output total payment, total interest, and terminate time
control_output = dbc.Card(
                        [dbc.CardBody([
                                        html.H4("Total Payment:", className="card-title"),
                                        html.H5(html.Div(id="total-payment"))
                                        ]),
                        dbc.CardBody([
                                        html.H4("Total Interest:", className="card-title"),
                                        html.H5(html.Div(id="total-interest"))
                                        ]),
                        dbc.CardBody([
                                        html.H4("Terminate Time:", className="card-title"),
                                        html.H5(html.Div(id="total-time"))
                                        ])
                        ])

# input loan amount, payment per month, interest per year and extra payment for the second loan
controls2 = dbc.Card(
    [
        dcc.Store(id='memory-output2'),  
        dcc.Store(id='memory-outputa2'),
        dcc.Store(id='memory-outputb2'),
        dcc.Store(id='memory-outputc2'),
        dcc.Store(id='memory-outputfig2'),
        html.H4(dbc.Label("Second Loan")),
        dbc.FormGroup([
                html.H5(dbc.Label("Loan amount")),
                dcc.Input(type="number", 
                          id="loan-amount2")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("Payment per month")),
                dcc.Input(type="number", 
                          id="payment-per-month2")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("Interest rate per year")),
                dcc.Input(type="number", 
                          id="interest-rate2")
        ]),
        html.Div(id="error2"),
        dbc.FormGroup([
                html.H5(dbc.Label("extra1")),
                dcc.Input(type="number", 
                          id="extra12")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("extra2")),
                dcc.Input(type="number", 
                          id="extra22")
        ]),
        dbc.FormGroup([
                html.H5(dbc.Label("extra3")),
                dcc.Input(type="number", 
                          id="extra32")
        ])
    ],
    body=True,
)

# button to show or hide payment schedule
collapse = html.Div(
    [
        dbc.Button(
            "Show payment schedule",
            id="collapse-button",
            className="mb-3",
            color="primary",
        )])

# payment schedule shown after clicking 'show payment schedule'
collapse1 = dbc.Collapse(dash_table.DataTable(
                                            id='memory-table',
                                            columns=[{'name': i, 'id': i} for i in column_name],
                                            style_table={'height': '300px', 'minWidth': '100%'},
                                            style_cell={'fontSize':15, 'font-family':'sans-serif',
                                                        'height': 'auto',
                                                        'minWidth': '130px', 'width': '130px', 'maxWidth': '130px',
                                                        'whiteSpace': 'normal'
                                                    }
                                            ),
            id="collapse",
        )

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.P("Loan Calculator",style={'text-align':'center','font-size':'200%','background-color':'powderblue'}))),
        dbc.Row([dbc.Col(controls, md=2),
                 dbc.Col(controls2, md=2),
                 dbc.Col(dcc.Graph(id='memory-graph'),style={'width': '170vh', 'height': '70vh',
                                 'margin-bottom': '10px',
                                 'verticalAlign': 'middle'}),
                 dbc.Col([html.Br(),
                          dbc.Row(control_output,style={'width': '50vh', 'height': '70vh',
                                 'margin-top': '10px',
                                 'margin-bottome': '60px',
                                 'horizontalAlign': 'middle'})], md=2)
                          ]),
        dbc.Row([dbc.Col(dbc.CardBody([
                                        html.H5(dbc.Label("Start Date"),className="card-title"),
                                        dcc.DatePickerSingle(
        id='start-date',
        month_format='MMM Do, YY',
        placeholder='MMM Do, YY',
        date=date.today())
                                        ],style={'margin-top': '10px','margin-bottome': '100px'})),
        dbc.Col(collapse,style={'margin-left': '20px',
                                 'margin-top': '10px',
                                 'verticalAlign': 'middle'})]),
        dbc.Row(collapse1,style={'margin-left': '250px',
                                 'margin-bottom': '10px',
                                 'verticalAlign': 'middle'})
        ],
        id="main-container",
        style={"display": "flex", "flex-direction": "column"},
        fluid=True
    )

# make collapse button available
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# store data for the first loan
@app.callback([Output('memory-output', 'data'),
               Output('memory-outputa', 'data'),
               Output('memory-outputb', 'data'),
               Output('memory-outputc', 'data'),
               Output('memory-outputfig', 'data')],
              [Input('loan-amount','value'),
               Input('interest-rate','value'),
               Input('payment-per-month','value'),
               Input('extra1','value'),
               Input('extra2','value'),
               Input('extra3','value'),
               Input('start-date', 'date')])
def table_figure2(loan_amount,interest_rate,payment,extra1,extra2,extra3,start_date1):
    y = int(list(start_date1)[0]+list(start_date1)[1]+list(start_date1)[2]+list(start_date1)[3])
    m = int(list(start_date1)[5]+list(start_date1)[6])
    d = min(int(list(start_date1)[8]+list(start_date1)[9]),28)
    start_date = date(y,m,d)
    if loan_amount !=None and payment != None and interest_rate!= None:
        ex1 = disting(extra1)
        ex2 = disting(extra2)
        ex3 = disting(extra3) 
        loan = Loan(loan_amount,interest_rate,payment,ex1+ex2+ex3)
        a,b,c = compute_schedule_loan(loan_amount, interest_rate, payment, ex1+ex2+ex3)
        loan_noextra = Loan(loan_amount,interest_rate,payment,0)  
        df = date_trans(to_df(loan),start_date)
        df_noextra = date_trans(to_df(loan_noextra),start_date)
        new_df = pd.concat([df_noextra['Month'],df_noextra['End Principal'],df['End Principal']],axis =1)
        new_df.columns = ['Month','No extra','Extra all']
        new_df = new_df.append({'Month':start_date,'No extra':loan_amount,'Extra all':loan_amount},ignore_index = True).sort_values(by = 'Month')
        return df.to_dict('record'),a,b,c,new_df.to_dict('record')
       
    else:    
        df = pd.DataFrame(columns = ['Month', 'Begin Principal', 'Payment', 'Extra Payment','Applied Principal', 'Applied Interest', 'End Principal'])
        return df.to_dict('record'),0,0,0,[]

# store data for the second loan
@app.callback([Output('memory-output2', 'data'),
               Output('memory-outputa2', 'data'),
               Output('memory-outputb2', 'data'),
               Output('memory-outputc2', 'data'),
               Output('memory-outputfig2', 'data')],
              [Input('loan-amount2','value'),
               Input('interest-rate2','value'),
               Input('payment-per-month2','value'),
               Input('extra12','value'),
               Input('extra22','value'),
               Input('extra32','value'),
               Input('start-date', 'date')])
def table_figure2(loan_amount,interest_rate,payment,extra1,extra2,extra3,start_date1):
    y = int(list(start_date1)[0]+list(start_date1)[1]+list(start_date1)[2]+list(start_date1)[3])
    m = int(list(start_date1)[5]+list(start_date1)[6])
    d = min(int(list(start_date1)[8]+list(start_date1)[9]),28)
    start_date = date(y,m,d)
    if loan_amount !=None and payment != None and interest_rate!= None:
        ex1 = disting(extra1)
        ex2 = disting(extra2)
        ex3 = disting(extra3) 
        loan = Loan(loan_amount,interest_rate,payment,ex1+ex2+ex3)
        a,b,c = compute_schedule_loan(loan_amount, interest_rate, payment, ex1+ex2+ex3)
        loan_noextra = Loan(loan_amount,interest_rate,payment,0)  
        df = date_trans(to_df(loan),start_date)
        df_noextra = date_trans(to_df(loan_noextra),start_date)
        new_df = pd.concat([df_noextra['Month'],df_noextra['End Principal'],df['End Principal']],axis =1)
        new_df.columns = ['Month','No extra','Extra all']
        new_df = new_df.append({'Month':start_date,'No extra':loan_amount,'Extra all':loan_amount},ignore_index = True).sort_values(by = 'Month')
        return df.to_dict('record'),a,b,c,new_df.to_dict('record')
       
    else:    
        df = pd.DataFrame(columns = ['Month', 'Begin Principal', 'Payment', 'Extra Payment','Applied Principal', 'Applied Interest', 'End Principal'])
        return df.to_dict('record'),0,0,0,[]

# update figure
@app.callback(Output('memory-graph', 'figure'),
              [Input('memory-outputfig', 'data'),
              Input('memory-outputfig2', 'data')])
def figure(df1,df2):
    if df1 == []:
        if df2 == []:
            raise PreventUpdate
        else:
            df2 = pd.DataFrame(df2).set_index('Month')
            fig = px.line(df2,title='End Principal by date')
            fig.update_yaxes(title_text="End Principal")
    elif df2 == []:
        df1 = pd.DataFrame(df1).set_index('Month')
        fig = px.line(df1,title='End Principal by date')
        fig.update_yaxes(title_text="End Principal")
    else:
        df1 = pd.DataFrame(df1).set_index('Month')
        df2 = pd.DataFrame(df2).set_index('Month')
        dft = pd.concat([df1,df2],join='outer',axis =1).reset_index()
        dft.columns = ['Month','Loan 1 No Extra','Loan 1 Extra All','Loan 2 No Extra','Loan 2 Extra All']
        dft = dft.set_index('Month')
        fig = px.line(dft,title='End Principal by date')
        fig.update_yaxes(title_text="End Principal")
    return fig

# return data of memory table     
@app.callback(Output('memory-table', 'data'),
              [Input('memory-output', 'data'),
              Input('memory-output2', 'data')])
def on_data_set_table(df1,df2):
    if df1 == []:
        if df2 == []:
            raise PreventUpdate
        else:
            dft = pd.DataFrame(df2)
    elif df2 == []:
        dft = pd.DataFrame(df1)
    else:
        df1 = pd.DataFrame(df1)
        df2 = pd.DataFrame(df2)
        df1 = df1.set_index('Month')
        df2 = df2.set_index('Month')
        dft = df1.add(df2,fill_value=0)
        dft = dft.reset_index()
    return dft.to_dict('record')

# return total payment
@app.callback(Output('total-payment', 'children'),
              [Input('memory-outputa', 'data'),
              Input('memory-outputa2', 'data')])
def total_payment(a1,a2):
    if a1 == 0 and a2 == 0:
        return None
    else:
        return (str(round(a1+a2,2))+' dollar(s).')

# return total interest
@app.callback(Output('total-interest', 'children'),
              [Input('memory-outputb', 'data'),
              Input('memory-outputb2', 'data')])
def total_interest(b1,b2):
    if b1 == 0 and b2 == 0:
        return None
    else:
        return (str(round(b1+b2,2))+' dollar(s).')

# return terminate time    
@app.callback(Output('total-time', 'children'),
              [Input('memory-outputc', 'data'),
              Input('memory-outputc2', 'data')])
def total_time(c1,c2):
    if c1 == 0 and c2 == 0:
        return None
    else:
        return (str(max(c1,c2))+' month(s).')
                
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
