# coding: utf-8
import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask, send_from_directory

import numpy as np
import plotly.graph_objs as go

import os
import sys
import subprocess
import shutil

import uuid
import base64

import time


#GLOBAL VARIABLE
UPLOAD_DIRECTORY = 'uploads'

#SERVER
# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server)

@server.route('/download/<path:path>')
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

#Dash will not protect against ID exceptions : 
app.config['suppress_callback_exceptions']=True
################################################################################################

############################## /DISPLAYS X-Rays/ ##############################
########### 1. X-Ray dysplay

XRay_display=html.Div([
    html.Hr(),
    html.H1('X-Ray Scattering'),
    html.Button('Advanced options', id='adv_opt_III',n_clicks=0,style={'margin-top':'10px'}),
        html.Div(id='adv_opt_III_display'),
        html.Hr(),
        html.Div([
            html.Div([
                html.H5(
                    'What do you want to do?')
                ], className="twelve columns padded"
                )
            ],
            style={'margin-top':'10px','margin-bottom':'10px'},
            className="row gs-header gs-text-header"
            ),
        dcc.Dropdown(
            id='Choice_X',
            options=[
                {'label':'Prediction','value':'prediction'},
                {'label':'Fit','value':'fit'}
                ],
            placeholder="Select between a prediction or fit",
            ),

        html.Div(id='upload_display_X'),
        html.Button('Calculation', id='calculation_button_X',n_clicks=0,style={'margin-top':'10px'}),
        html.P(id='placeholder_X'),
        html.Div(id='final_display_X')
],
className="page",
)

########### 2. ADVANCED OPTIONS DYSPLAYS

Advanced_parameters_III=html.Div([
    html.Strong(['Keep this window open if you want these options to be taken into account']),
    ####First Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Expansion order'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.Input(
                id='n_X',
                type='text',
                size=3,
            ),     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Hydration shell contrast (in %)'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.Input(
                id='dro_X',
                type='text',
                value='5',
                placeholder='5',
                min=1,
                max=4,
                size=3,
                style={
                    'background-color':'#ffe6e6'
                }                
            ),                   
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),

    ####Second Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Explicit hydrogens'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.RadioItems(
                id='hyd_X',
                options=[
                    {'value': 'exp_hyd'}
                ],               
            )     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Coarser representation of Hydration shell'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.RadioItems(
                id='fast_X',
                options=[
                    {'value': 'hyd_shell'}
                ],              
            )                  
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),
    html.Strong(["Remark : you can let the Expansion order and Explicit bulk SLD empty"]),

])

Advanced_parameters_IIIa=html.Div([
    html.Strong(['Keep this window open if you want these options to be taken into account']),
    ####A Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Number of  points'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.Input(
                id='ns_X',
                type='text',
                value='101',
                placeholder='101',
                min=1,
                max=5000,
                size=3,
                style={
                    'background-color':'#ffe6e6',
                }
            ),     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Max angle (1/A)'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.Input(
                id='ms_X',
                type='text',
                value='0.5',
                placeholder='0.5',
                max=1,
                size=3,
                style={
                    'background-color':'#ffe6e6',
                }                
            ),                   
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),

])

Advanced_parameters_IIIb=html.Div([
    html.Strong(['Keep this window open if you want these options to be taken into account']),
    ####First Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Fitting of absolute intensity (in %)'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.Input(
                id='absFit_X',
                type='text',
                size=3,
            ),     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('No Smearing'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.RadioItems(
                id='noSmearing_X',
                options=[
                    {'value': 'no_smear'}
                ],              
            )                              
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),

    ####Second Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Negative contrast'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.RadioItems(
                id='neg_X',
                options=[
                    {'value': 'neg_cont'}
                ],              
            )                 
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Constant factor'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.RadioItems(
                id='cst_X',
                options=[
                    {'value': 'cst_fact'}
                ],              
            )                             
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),
    html.Strong(["Remark : you can let the Fitting of absolute intensity (in %) empty"]),
])

########### 3. FIT OR PREDICTION DYSPLAYS

fit_display_X=html.Div([
    html.Div([
        html.Div([
            html.H5(
                    'Upload your data file')
            ], className="twelve columns padded")
        ],
        style={'margin-top':'10px','margin-bottom':'10px'},
        className="row gs-header gs-text-header"),  
    dcc.Upload(
            id='upload-data_X',
            children=html.Div([
                'Drag and drop or click to select a file to upload.'
            ]),
            style={
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'display':'block',
                'margin-left': 'auto',
                'margin-rigth':'auto',
                'background-color':'#ffe6e6'
            },
            multiple=True
    ),
    html.Div(id='Data_uploaded_X'),
    html.Button('Advanced options', id='adv_opt_IIIb',n_clicks=0,style={'margin-top':'10px'}),
    html.Div(id='adv_opt_IIIb_display'),
])

prediction_display_X=html.Div([
    html.Button('Advanced options', id='adv_opt_IIIa',n_clicks=0,style={'margin-top':'10px'}),
    html.Div(id='adv_opt_IIIa_display'),
])

########### 4. RESULTS DYSPLAYS

def Result_prediction_adv_opt_III_IIIa():
    return html.Div([
    html.P(id='placeholder_prediction_adv_opt_III_IIIa'),
    results_display_prediction()
    ])

def Result_prediction_adv_opt_III():
    return html.Div([
    html.P(id='placeholder_prediction_adv_opt_III'),
    results_display_prediction()
    ])

def Result_prediction_adv_opt_IIIa():
    return html.Div([
    html.P(id='placeholder_prediction_adv_opt_IIIa'),
    results_display_prediction()
    ])

def Result_prediction_X():
    return html.Div([
    html.P(id='placeholder_prediction_X'),
    results_display_prediction()
    ])

def Result_fit_adv_opt_III_IIIb():
    return html.Div([
    html.P(id='placeholder_fit_adv_opt_III_IIIb'),
    results_display_fit()
    ])

def Result_fit_adv_opt_III():
    return html.Div([
    html.P(id='placeholder_fit_adv_opt_III'),
    results_display_fit()
    ])

def Result_fit_adv_opt_IIIb():
    return html.Div([
    html.P(id='placeholder_fit_adv_opt_IIIb'),
    results_display_fit()
    ])

def Result_fit_X():
    return html.Div([
    html.P(id='placeholder_fit_X'),
    results_display_fit()
    ])

############################## \END DISPLAYS X-Rays\ ##############################

############################## /DISPLAYS NEUTRONS/ ##############################
########### 1. NEUTRON DYSPLAYS

neutron_display=html.Div([
    html.Hr(),
    html.H1('Neutron Scattering'),
    html.Div([
        html.Div([
            html.H5(
                    'Enter your parameters')
            ], className="twelve columns padded")
    ],
    style={'margin-top':'10px','margin-bottom':'10px'},
    className="row gs-header gs-text-header"),
    ####First line
    html.Div([
            ####Text1
        html.Div([
                html.P('Buffer deuteration (0-1)'),
                ],
                style=dict(
                    width='30%',
                    display='table-cell'
                ),
                ),
        ####Input1
        html.Div([
                dcc.Input(
                    id='d2o',
                    placeholder='0',
                    type='text',
                    value='0',
                    min=0,
                    max=1,
                    size=3,
                    style={
                        'background-color':'#ffe6e6'
                    }
                    ),        
                ],
                style=dict(
                    width='25%',
                    display='table-cell'                
                )
                ),
        ####Text2
        html.Div([
                html.P('Molecule deuteration (0-1)'),
                ],
                style=dict(
                    width='30%',
                    display='table-cell'
                ),
                ),
        ####Input2
        html.Div([
                dcc.Input(
                    id='deut',
                    placeholder='0',
                    type='text',
                    value='0',
                    min=0,
                    max=1,
                    size=3,
                    style={
                        'background-color':'#ffe6e6'
                    }                    
                ),                    
                ],
                style=dict(
                    width='25%',
                    display='table-cell'
                ),
                ),

            ],
            style=dict(
                width='100%',
                display='table',
            ),
            ),

        ####Second line
        html.Div([
                ####Text1
        html.Div([
                html.P('Concentration (mg/mL)'),
                ],
                style=dict(
                    width='30%',
                    display='table-cell'
                ),
                ),
        ####Input1
        html.Div([
                    dcc.Input(
                        id='conc',
                        placeholder='1',
                        type='text',
                        value='1',
                        size=3,
                        style={
                            'background-color':'#ffe6e6'
                        }                    
                    ),     
                ],
                style=dict(
                    width='25%',
                    display='table-cell'                
                )
                ),
        ####Text2
        html.Div([
                    html.P('Exchange'),
                ],
                style=dict(
                    width='30%',
                    display='table-cell'
                ),
                ),
        ####Input2
        html.Div([
                    dcc.Input(
                        id='exchange',
                        placeholder='0.9',
                        type='text',
                        value='0.9',
                        min=0,
                        max=1,
                        size=3,
                        style={
                            'background-color':'#ffe6e6'
                        }                    
                    ),                   
                ],
                style=dict(
                    width='25%',
                    display='table-cell'
                ),
                ),

            ],
            style=dict(
                width='100%',
                display='table',
            ),
            ),
        html.Button('Advanced options', id='adv_opt_II',n_clicks=0,style={'margin-top':'10px'}),
        html.Div(id='adv_opt_II_display'),
        html.Hr(),
        html.Div([
        html.Div([
            html.H5(
                    'What do you want to do?')
            ], className="twelve columns padded")
        ],
        style={'margin-top':'10px','margin-bottom':'10px'},
        className="row gs-header gs-text-header"),
        dcc.Dropdown(
            id='Choice',
            options=[
                {'label':'Prediction','value':'prediction'},
                {'label':'Fit','value':'fit'}
                ],
            placeholder="Select between a prediction or fit",
            ),

        html.Div(id='upload_display'),
        html.Button('Calculation', id='calculation_button',n_clicks=0,style={'margin-top':'10px'}),
        html.P(id='placeholder'),
        html.Div(id='final_display')
],
className="page",
)

########### 2. ADVANCED OPTIONS DYSPLAYS

Advanced_parameters_IIb=html.Div([
    html.Strong(['Keep this window open if you want these options to be taken into account']),
    ####First Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Fitting of absolute intensity (in %)'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.Input(
                id='absFit',
                type='text',
                size=3,
            ),     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('No Smearing'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.RadioItems(
                id='noSmearing',
                options=[
                    {'value': 'no_smear'}
                ],              
            )                              
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),

    ####Second Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Negative contrast'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.RadioItems(
                id='neg',
                options=[
                    {'value': 'neg_cont'}
                ],              
            )                 
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Constant factor'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.RadioItems(
                id='cst',
                options=[
                    {'value': 'cst_fact'}
                ],              
            )                             
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),
    html.Strong(["Remark : you can let the Fitting of absolute intensity (in %) empty"]),
])

Advanced_parameters_IIa=html.Div([
    html.Strong(['Keep this window open if you want these options to be taken into account']),
    ####A Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Number of  points'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.Input(
                id='ns',
                type='text',
                value='101',
                placeholder='101',
                min=1,
                max=5000,
                size=3,
                style={
                    'background-color':'#ffe6e6',
                }
            ),     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Max angle (1/A)'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.Input(
                id='ms',
                type='text',
                value='0.5',
                placeholder='0.5',
                max=1,
                size=3,
                style={
                    'background-color':'#ffe6e6',
                }                
            ),                   
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),
])

Advanced_parameters_II=html.Div([
    html.Strong(['Keep this window open if you want these options to be taken into account']),
    ####First Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Expansion order'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.Input(
                id='n',
                type='text',
                size=3,
            ),     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Hydration shell contrast (in %)'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.Input(
                id='dro',
                type='text',
                value='5',
                placeholder='5',
                min=1,
                max=4,
                size=3,
                style={
                    'background-color':'#ffe6e6'
                }                
            ),                   
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),

    ####Second Line
    html.Div([
        ####Text1
        html.Div([
            html.P('Explicit bulk SLD'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input1
        html.Div([
            dcc.Input(
                id='bulkSLD',
                type='text',
                value=None,
                size=3,
            ),     
        ],
        style=dict(
            width='25%',
            display='table-cell'                
        )
        ),
        ####Text2
        html.Div([
            html.P('Coarser representation of Hydration shell'),
        ],
        style=dict(
            width='30%',
            display='table-cell'
        ),
        ),
        ####Input2
        html.Div([
            dcc.RadioItems(
                id='fast',
                options=[
                    {'value': 'hyd_shell'}
                ],
                #values=''               
            )                  
        ],
        style=dict(
            width='25%',
            display='table-cell'
        ),
        ),
    ],
    style=dict(
        width='100%',
        display='table',
    ),
    ),
    html.P("Angular units"),
    dcc.Dropdown(
        id='au',
        options=[
            {'label':'1/A, q = 4pi sin(theta)/lambda','value':'1'},
            {'label':'1/nm, q = 4pi sin(theta)/lambda','value':'2'},
            {'label':'1/A, s = 2sin(theta)/lambda','value':'3'},
            {'label':'1/nm, s = 2sin(theta)/lambda','value':'4'},
            
        ],
        value='1',
        placeholder="Select an angular unit",
    ),
    html.Strong(["Remark : you can let the Expansion order and Explicit bulk SLD empty"]),
])

########### 3. FIT OR PREDICTION DYSPLAYS

fit_display=html.Div([
    html.Div([
        html.Div([
            html.H5(
                    'Upload your data file')
            ], className="twelve columns padded")
        ],
        style={'margin-top':'10px','margin-bottom':'10px'},
        className="row gs-header gs-text-header"),  
    dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and drop or click to select a file to upload.'
            ]),
            style={
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'display':'block',
                'margin-left': 'auto',
                'margin-rigth':'auto',
                'background-color':'#ffe6e6'
            },
            multiple=True
    ),
    html.Div(id='Data_uploaded'),
    html.Button('Advanced options', id='adv_opt_IIb',n_clicks=0,style={'margin-top':'10px'}),
    html.Div(id='adv_opt_IIb_display'),
])

prediction_display=html.Div([
    html.Button('Advanced options', id='adv_opt_IIa',n_clicks=0,style={'margin-top':'10px'}),
    html.Div(id='adv_opt_IIa_display'),
])

########### 4. RESULTS DYSPLAYS

def results_display_prediction():
    Results=html.Div([
        html.Hr(),
        html.Div([
            html.Div([
                html.H5(
                        'Results')
                ], className="twelve columns padded")
        ],
        style={'margin-top':'10px','margin-bottom':'10px'},
        className="row gs-header gs-text-header"),
        html.H2('Graph'),
        dcc.Graph(id='graph_prediction'),
        dcc.Interval(
            id='update_graph',
            interval=1*1000,
            n_intervals=0
        ),
        html.Hr(),
        html.H2('Download links'),
        html.Ul(
            id='file-list',
            style={
                'margin-left':'20px'
            })
        ], )
    return Results

def results_display_fit():
    Results=html.Div([
        html.Hr(),
        html.Div([
            html.Div([
                html.H5(
                        'Results')
                ], className="twelve columns padded")
        ],
        style={'margin-top':'10px','margin-bottom':'10px'},
        className="row gs-header gs-text-header"),
        html.H2('Graph'),
        dcc.Graph(id='graph_fit'),
        dcc.Interval(
            id='update_graph',
            interval=1*1000,
            n_intervals=0
        ),
        html.Hr(),
        html.H2('Download links'),
        html.Ul(
            id='file-list',
            style={
                'margin-left':'20px'
            })
        ], )
    return Results

def Result_prediction_adv_opt_II_IIa():
    return html.Div([
    html.P(id='placeholder_prediction_adv_opt_II_IIa'),
    results_display_prediction()
    ])

def Result_prediction_adv_opt_II():
    return html.Div([
    html.P(id='placeholder_prediction_adv_opt_II'),
    results_display_prediction()
    ])

def Result_prediction_adv_opt_IIa():
    return html.Div([
    html.P(id='placeholder_prediction_adv_opt_IIa'),
    results_display_prediction()
    ])
def Result_prediction():
    return html.Div([
    html.P(id='placeholder_prediction'),
    results_display_prediction()
    ])

def Result_fit_adv_opt_II_IIb():
    return html.Div([
    html.P(id='placeholder_fit_adv_opt_II_IIb'),
    results_display_fit()
    ])

def Result_fit_adv_opt_II ():
    return html.Div([
    html.P(id='placeholder_fit_adv_opt_II'),
    results_display_fit()
    ])

def Result_fit():
    return html.Div([
    html.P(id='placeholder_fit'),
    results_display_fit()
    ])

def Result_fit_adv_opt_IIb():
    return html.Div([
    html.P(id='placeholder_fit_adv_opt_IIb'),
    results_display_fit()
    ])

############################## \END DISPLAYS\ ##############################


############################## \END DISPLAYS NEUTRONS\ ##############################

############################## /LAYOUT/ ##############################

def get_header():
    header = html.Div([
        html.Div([
            html.Img(src='https://www.eso.org/public/archives/logos/screen/ill.jpg', height='102', width='95')
        ],className="three columns  ",
        ),
        html.Div([
            html.H1(
                'SAXS & SANS',
                style={'textAlign': 'center','margin-bottom':'2px'}),
            html.Hr(style={'margin-bottom':'2px','margin-top':'2px'}),
            html.H5(
                '-Profile Computation-',
                style={'textAlign': 'center','margin-top':'2px'}),
        ],className="six columns "),
    ],className="row "
    )
    return header

app.layout = html.Div([
    dcc.Interval(
                id='folder-update',
                interval=1*10000 #in miliseconds
            ),
    get_header(),
    html.Div([
        html.Div([
            html.H5(
                    'Upload your pdb file')
            ], className="twelve columns padded")
    ],
    style={'margin-top':'10px'},
    className="row gs-header gs-text-header"),
    #html.H2(''),
    dcc.Upload(
        id='upload-prot',
        children=html.Div([
            'Drag and drop or click to select a file to upload.'
            ]),
        style={
            #'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'display':'block',
            'margin-top':'10px',
            'margin-left': 'auto',
            'margin-rigth':'auto',
            'background-color':'#ffe6e6'
    },
    multiple=True
    ),
    html.Div(id='Prot_uploaded'),
    html.P(id='id_folder', style={'display':'none'}),
    html.P(id='placeholder_folder_update'),
    html.Div([
        html.Div([
            html.H5(
                    'What is your method ?')
            ], className="twelve columns padded")
    ],
    style={'margin-top':'10px','margin-bottom':'10px'},
    className="row gs-header gs-text-header"),
    dcc.Dropdown(
        id='Scattering_selection',
        options=[
            {'label':'Neutron Scattering','value':'neutron_scattering'},
            {'label':'X-Ray scattering','value':'XRay_scattering'},
        ],
        placeholder="Select a method",
    ),
    html.P(id='id_folder', style={'display':'none'}),
    html.Div(id='scattering_display'),        
],
className="page",
)
############################## \END LAYOUT\ ##############################


############################## /FUNCTIONS/ ##############################

##Decode and store a file uploaded with Plotly Dash
def save_file(name, content,id):
    data = content.encode('utf8').split(b';base64,')[1]
    upload_path = os.path.join(UPLOAD_DIRECTORY, id)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    with open(os.path.join(upload_path, name), 'wb') as fp:
        fp.write(base64.decodebytes(data))

##List the files in the upload directory
def uploaded_files(id_folder):
    files = []
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    files=os.listdir(file_path)
    return files

##Create a Plotly Dash 'A' element that downloads a file from the app
def file_download_link(filename,id_folder):
    loc = os.path.join('/download/',id_folder)
    location=os.path.join(loc,filename)
    return html.A(filename, href=location)

############################## \FUNCTIONS\ ##############################


############################## /CALLBACKS/ ##############################

########### 1. Cleaning uploads folder

@app.callback(
    Output('placeholder_folder_update','children'),
    events=[Event('folder-update','interval')]
    )
def update_uploads_folder():
    for somefolder in os.listdir(UPLOAD_DIRECTORY):
        folder_path=os.path.join(UPLOAD_DIRECTORY,somefolder)
        st=os.stat(folder_path)
        mtime=st.st_mtime # time of most recent somefolder modification
        elapsed_time=time.time()-mtime #elapsed time since mtime in seconds
        print(elapsed_time, file=sys.stderr)
        if elapsed_time>60:
            print('remove %s'%somefolder, file=sys.stderr)
            shutil.rmtree(folder_path)#remove the folder if it is more than 1 minute old

########### 2. UPLOADS

##Upload and Save protein file and return the id of the unique folder
@app.callback(
    Output('id_folder','children'),
    [Input('upload-prot', 'filename'), Input('upload-prot', 'contents')])

def upload_prot(uploaded_filenames, uploaded_file_contents):
    id = str(uuid.uuid4())
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data, id)
        return id

##Upload and Save data file (remove .txt file if it already exist in the unique folder)
@app.callback(
    Output('placeholder','children'),
    [Input('upload-data', 'filename'), Input('upload-data', 'contents'), Input('id_folder','children')]
)
def update_folder_and_upload_data(uploaded_filenames, uploaded_file_contents,id_folder):
        
        #update folder
        files=uploaded_files(id_folder)
        index=[]
        for i in range (len(files)):
            filename=files[i]
            if filename[-4:]=='.txt':
                index.append(filename)
        for i in index:
            file_path=os.path.join(UPLOAD_DIRECTORY,id_folder)
            removed_file_path=os.path.join(file_path,i)
            os.remove(removed_file_path)
        
        #upload data file
        if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, data in zip(uploaded_filenames, uploaded_file_contents):
                save_file(name, data, id_folder)

@app.callback(
    Output('placeholder_X','children'),
    [Input('upload-data_X', 'filename'), Input('upload-data_X', 'contents'), Input('id_folder','children')]
)
def update_folder_and_upload_data(uploaded_filenames, uploaded_file_contents,id_folder):
        
        #update folder
        files=uploaded_files(id_folder)
        index=[]
        for i in range (len(files)):
            filename=files[i]
            if filename[-4:]=='.txt':
                index.append(filename)
        for i in index:
            file_path=os.path.join(UPLOAD_DIRECTORY,id_folder)
            removed_file_path=os.path.join(file_path,i)
            os.remove(removed_file_path)
        
        #upload data file
        if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, data in zip(uploaded_filenames, uploaded_file_contents):
                save_file(name, data, id_folder)

########### 3. SELECTION (BUTTON or DROPDOWN) DYSPLAYS CALLBACKS
@app.callback(
    Output('Data_uploaded_X', 'children'),
    [Input('upload-data_X', 'filename'), Input('upload-data_X', 'contents'), Input('id_folder','children')])
def update_file_update(filename,contents,id_folder):
    if filename is not None and contents is not None:
        if filename[0][-4:]=='.pdb':
            return html.H5('This type of file is not taken into account. Please reload the page.')
        else :
            return html.P(filename)

@app.callback(
    Output('Data_uploaded', 'children'),
    [Input('upload-data', 'filename'), Input('upload-data', 'contents'), Input('id_folder','children')])
def update_file_update(filename,contents,id_folder):
    if filename is not None and contents is not None:
        if filename[0][-4:]=='.pdb':
            return html.H5('This type of file is not taken into account. Please reload the page.')
        else :
            return html.P(filename)

            
@app.callback(
    Output('Prot_uploaded', 'children'),
    [Input('upload-prot', 'filename'), Input('upload-prot', 'contents'), Input('id_folder','children')])
def update_file_update(filename,contents,id_folder):
    if filename is not None and contents is not None:
        if filename[0][-4:]=='.pdb':
            return html.P(filename)
        else :
            return html.H5('This type of file is not taken into account. Please reload the page.')

@app.callback(
    Output('scattering_display', 'children'),
    [Input('Scattering_selection','value')])
def display_x_or_n(choice):
    if choice=='neutron_scattering':
        return neutron_display
    elif choice=='XRay_scattering' :
        return XRay_display

@app.callback(
    Output('upload_display', 'children'),
    [Input('Choice','value')])
def display_f_or_p(choice):
    if choice=='fit':
        return fit_display
    elif choice=='prediction' :
        return prediction_display

@app.callback(
    Output('upload_display_X', 'children'),
    [Input('Choice_X','value')])
def display_f_or_p_X(choice):
    if choice=='fit':
        return fit_display_X
    elif choice=='prediction' :
        return prediction_display_X

@app.callback(
    Output('adv_opt_II_display', 'children'),
    [Input('adv_opt_II','n_clicks')])
def adv_opt_II_display(n_clicks):
    if n_clicks%2 !=0:
        return Advanced_parameters_II

@app.callback(
    Output('adv_opt_IIa_display', 'children'),
    [Input('adv_opt_IIa','n_clicks')])
def adv_opt_IIa_display(n_clicks):
    if n_clicks%2 !=0:
        return Advanced_parameters_IIa

@app.callback(
    Output('adv_opt_IIb_display', 'children'),
    [Input('adv_opt_IIb','n_clicks')])
def adv_opt_IIb_display(n_clicks):
    if n_clicks%2 !=0:
        return Advanced_parameters_IIb
    
@app.callback(
    Output('adv_opt_III_display', 'children'),
    [Input('adv_opt_III','n_clicks')])
def adv_opt_III_display(n_clicks):
    if n_clicks%2 !=0:
        return Advanced_parameters_III

@app.callback(
    Output('adv_opt_IIIa_display', 'children'),
    [Input('adv_opt_IIIa','n_clicks')])
def adv_opt_IIIa_display(n_clicks):
    if n_clicks%2 !=0:
        return Advanced_parameters_IIIa

@app.callback(
    Output('adv_opt_IIIb_display', 'children'),
    [Input('adv_opt_IIIb','n_clicks')])
def adv_opt_IIIb_display(n_clicks):
    if n_clicks%2 !=0:
        return Advanced_parameters_IIIb

########### 4. CHOICE OF WHICH METHOD OF CALCULATION TO TAKE
## >Neutrons
@app.callback(
    Output('final_display', 'children'),
    [Input('calculation_button','n_clicks'),Input('Choice','value'),Input('adv_opt_II','n_clicks')])
def which_pepsi_sans_calculation(click_calculation,choice,click_adv_optII):
    if click_calculation >0 : 
        if click_adv_optII %2 !=0:
            if choice=='prediction':
                return html.Div(id='calculation_prediction_adv_optII')
            elif choice=='fit':
                return html.Div(id='calculation_fit_adv_optII')
        else:
            if choice=='prediction':
                return html.Div(id='calculation_prediction')
            elif choice=='fit':
                return html.Div(id='calculation_fit')

@app.callback(
    Output('calculation_prediction_adv_optII', 'children'),
    [Input('adv_opt_IIa','n_clicks')]
)
def calculation_prediction_adv_optII_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_prediction_adv_opt_II_IIa()
    else:
        return Result_prediction_adv_opt_II()

@app.callback(
    Output('calculation_prediction', 'children'),
    [Input('adv_opt_IIa','n_clicks')]
)
def calculation_prediction_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_prediction_adv_opt_IIa()
    else:
        return Result_prediction()

@app.callback(
    Output('calculation_fit_adv_optII', 'children'),
    [Input('adv_opt_IIb','n_clicks')]
)
def calculation_fit_adv_optII_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_fit_adv_opt_II_IIb()
    else:
        return Result_fit_adv_opt_II()

@app.callback(
    Output('calculation_fit', 'children'),
    [Input('adv_opt_IIb','n_clicks')]
)
def calculation_fit_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_fit_adv_opt_IIb()
    else:
        return Result_fit()

## >X-Rays

@app.callback(
    Output('final_display_X', 'children'),
    [Input('calculation_button_X','n_clicks'),Input('Choice_X','value'),Input('adv_opt_III','n_clicks')])
def which_pepsi_saxs_calculation(click_calculation,choice,click_adv_optIII):
    if click_calculation >0 : 
        if click_adv_optIII %2 !=0:
            if choice=='prediction':
                return html.Div(id='calculation_prediction_adv_optIII')
            elif choice=='fit':
                return html.Div(id='calculation_fit_adv_optIII')
        else:
            if choice=='prediction':
                return html.Div(id='calculation_prediction_X')
            elif choice=='fit':
                return html.Div(id='calculation_fit_X')

@app.callback(
    Output('calculation_prediction_adv_optIII', 'children'),
    [Input('adv_opt_IIIa','n_clicks')]
)
def calculation_prediction_adv_optIII_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_prediction_adv_opt_III_IIIa()
    else:
        return Result_prediction_adv_opt_III()

@app.callback(
    Output('calculation_prediction_X', 'children'),
    [Input('adv_opt_IIIa','n_clicks')]
)
def calculation_prediction_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_prediction_adv_opt_IIIa()
    else:
        return Result_prediction_X()

@app.callback(
    Output('calculation_fit_adv_optIII', 'children'),
    [Input('adv_opt_IIIb','n_clicks')]
)
def calculation_fit_adv_optII_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_fit_adv_opt_III_IIIb()
    else:
        return Result_fit_adv_opt_III()

@app.callback(
    Output('calculation_fit_X', 'children'),
    [Input('adv_opt_IIIb','n_clicks')]
)
def calculation_fit_adv_optII_func(n_clicks):
    if n_clicks %2 !=0:
        return Result_fit_adv_opt_IIIb()
    else:
        return Result_fit_X()

########### 5. PEPSI-SANS CALCULATION 
##>Neutrons

## CHOICE : PREDICTION + ADV OPT II
@app.callback(
    Output('placeholder_prediction_adv_opt_II', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ##Advanced Options II
    Input('n','value'),Input('au','value'),Input('fast','value'),Input('dro','value'),Input('bulkSLD','value'),
    ]) 

def pepsi_calculation_prediction_adv_opt_II(id_folder,d2o,deut,conc,exchange,n,au,fast,dro,bulkSLD):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SANS", os.path.join(file_path, name[0]),'-o', output_path,'-au',au,'--dro',dro,'--conc', conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if bulkSLD != None:
            command_line.extend(['--bulkSLD',bulkSLD])
        subprocess.check_output(command_line)
        shutil.move("result.log", file_path)

## CHOICE : PREDICTION +ADV OPT II + ADV OPT IIa
@app.callback(
    Output('placeholder_prediction_adv_opt_II_IIa', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ##Advanced Options II
    Input('n','value'),Input('au','value'),Input('fast','value'),Input('dro','value'),Input('bulkSLD','value'),
    ##Advanced Options IIa
    Input('ns','value'),Input('ms','value')
    ]) 

def pepsi_calculation_prediction_adv_opt_II_IIa(id_folder,d2o,deut,conc,exchange,n,au,fast,dro,bulkSLD,ns,ms):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SANS", os.path.join(file_path, name[0]),'-o', output_path,'-au',au,'--number_of_points',ns,'--maximum_scattering_vector',ms,'--dro',dro,'--conc', conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if bulkSLD != None:
            command_line.extend(['--bulkSLD',bulkSLD])
        subprocess.check_output(command_line)
        shutil.move("result.log", file_path)

## CHOICE : PREDICTION + ADV OPT IIa
@app.callback(
    Output('placeholder_prediction_adv_opt_IIa', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ##Advanced Options IIa
    Input('ns','value'),Input('ms','value')
    ]) 

def pepsi_calculation_prediction_adv_opt_IIa(id_folder,d2o,deut,conc,exchange,ns,ms):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        subprocess.check_output(["bin/Pepsi-SANS", os.path.join(file_path, name[0]),'-o', output_path,'--number_of_points',ns,'--maximum_scattering_vector',ms,'--conc',conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange])
        shutil.move("result.log", file_path)
    
## CHOICE : PREDICTION
@app.callback(
    Output('placeholder_prediction', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ]) 
def pepsi_calculation_prediction(id_folder,d2o,deut,conc,exchange):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        subprocess.check_output(["bin/Pepsi-SANS", os.path.join(file_path, name[0]),'-o', output_path,'--conc',conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange])
        shutil.move("result.log", file_path)

## CHOICE : FIT + ADV OPT II + ADV OPT IIb
@app.callback(
    Output('placeholder_fit_adv_opt_II_IIb', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ##Advanced Options II
    Input('n','value'),Input('au','value'),Input('fast','value'),Input('dro','value'),Input('bulkSLD','value'),
    ##Advanced Options IIb
    Input('cst','value'),Input('neg','value'),Input('noSmearing','value'),Input('absFit','value')
    ]) 

def pepsi_calculation_fit_adv_opt_II_IIb(id_folder,d2o,deut,conc,exchange,n,au,fast,dro,bulkSLD,cst,neg,noSmearing,absFit):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SANS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path,'-au',au,'--dro',dro,'--conc', conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if bulkSLD != None:
            command_line.extend(['--bulkSLD',bulkSLD])
        if cst == 'cst_fact' :
            command_line.extend(['--cst'])
        if neg == 'neg_cont' :
            command_line.extend(['--neg'])
        if noSmearing == 'no_smear' :
            command_line.extend(['--noSmearing'])
        if absFit !=None :
            command_line.extend(['--absFit',absFit])
        subprocess.check_output(command_line)
        shutil.move("result.log", file_path)

## CHOICE : FIT + ADV OPT II
@app.callback(
    Output('placeholder_fit_adv_opt_II', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ##Advanced Options II
    Input('n','value'),Input('au','value'),Input('fast','value'),Input('dro','value'),Input('bulkSLD','value')
    ]) 

def pepsi_calculation_fit_adv_opt_II(id_folder,d2o,deut,conc,exchange,n,au,fast,dro,bulkSLD):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SANS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path,'-au',au,'--dro',dro,'--conc', conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if bulkSLD != None:
            command_line.extend(['--bulkSLD',bulkSLD])
        subprocess.check_output(command_line)
        shutil.move("result.log", file_path)

## CHOICE : FIT
@app.callback(
    Output('placeholder_fit', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ]) 
def pepsi_calculation_fit(id_folder,d2o,deut,conc,exchange):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        subprocess.check_output(["bin/Pepsi-SANS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path,'--conc',conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange])
        shutil.move("result.log", file_path)


## CHOICE : FIT + ADV OPT IIb
@app.callback(
    Output('placeholder_fit_adv_opt_IIb', 'children'),
    [Input('id_folder','children'),
    ##Parameters
    Input('d2o','value'),Input('deut','value'),Input('conc','value'),Input('exchange','value'),
    ##Advanced Options IIb
    Input('cst','value'),Input('neg','value'),Input('noSmearing','value'),Input('absFit','value')
    ]) 

def pepsi_calculation_fit_adv_opt_IIb(id_folder,d2o,deut,conc,exchange,cst,neg,noSmearing,absFit):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SANS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path,'--conc', conc,'--deut',deut,'--d2o',d2o,'--exchange',exchange]
        if cst == 'cst_fact' :
            command_line.extend(['--cst'])
        if neg == 'neg_cont' :
            command_line.extend(['--neg'])
        if noSmearing == 'no_smear' :
            command_line.extend(['--noSmearing'])
        if absFit !=None :
            command_line.extend(['--absFit',absFit])
        subprocess.check_output(command_line)
        shutil.move("result.log", file_path)

##>X-Rays

## CHOICE : PREDICTION +ADV OPT III + ADV OPT IIIa
@app.callback(
    Output('placeholder_prediction_adv_opt_III_IIIa', 'children'),
    [Input('id_folder','children'),
    ##Advanced Options III
    Input('n_X','value'),Input('fast_X','value'),Input('dro_X','value'),Input('hyd_X','value'),
    ##Advanced Options IIIa
    Input('ns_X','value'),Input('ms_X','value')
    ]) 

def pepsi_calculation_prediction_adv_opt_III_IIIa(id_folder,n,fast,dro,hyd,ns,ms):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SAXS", os.path.join(file_path, name[0]),'-o', output_path,'--number_of_points',ns,'--maximum_scattering_vector',ms,'--dro',dro]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if hyd=='exp_hyd':
            command_line.extend(['--hyd'])
        subprocess.check_output(command_line)

## CHOICE : FIT + ADV OPT III
@app.callback(
    Output('placeholder_fit_adv_opt_III', 'children'),
    [Input('id_folder','children'),
    ##Advanced Options III
    Input('n_X','value'),Input('fast_X','value'),Input('dro_X','value'),Input('hyd_X','value'),
    ]) 

def pepsi_calculation_fit_adv_opt_III(id_folder,n,fast,dro,hyd):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SAXS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path,'--dro',dro]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if hyd=='exp_hyd':
            command_line.extend(['--hyd'])
        subprocess.check_output(command_line)

## CHOICE : PREDICTION + ADV OPT IIIa
@app.callback(
    Output('placeholder_prediction_adv_opt_IIIa', 'children'),
    [Input('id_folder','children'),
    ##Advanced Options IIIa
    Input('ns_X','value'),Input('ms_X','value')
    ])

def pepsi_calculation_prediction_adv_opt_IIIa(id_folder,ns,ms):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SAXS", os.path.join(file_path, name[0]),'-o', output_path,'--number_of_points',ns,'--maximum_scattering_vector',ms,]
        subprocess.check_output(command_line)

## CHOICE : PREDICTION
@app.callback(
    Output('placeholder_prediction_X', 'children'),
    [Input('id_folder','children'),
    ]) 
def pepsi_calculation_prediction_X(id_folder):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        subprocess.check_output(["../bin/Pepsi-SAXS", os.path.join(file_path, name[0]),'-o', output_path])

## CHOICE : PREDICTION + ADV OPT III
@app.callback(
    Output('placeholder_prediction_adv_opt_III', 'children'),
    [Input('id_folder','children'),
    ##Advanced Options III
    Input('n_X','value'),Input('fast_X','value'),Input('dro_X','value'),Input('hyd_X','value'),
    ]) 

def pepsi_calculation_prediction_adv_opt_III(id_folder,n,fast,dro,hyd):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SAXS", os.path.join(file_path, name[0]),'-o', output_path,'--dro',dro]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if hyd=='exp_hyd':
            command_line.extend(['--hyd'])
        subprocess.check_output(command_line)

## CHOICE : FIT + ADV OPT III + ADV OPT IIIb
@app.callback(
    Output('placeholder_fit_adv_opt_III_IIIb', 'children'),
    [Input('id_folder','children'),
    ##Advanced Options III
    Input('n_X','value'),Input('fast_X','value'),Input('dro_X','value'),Input('hyd_X','value'),
    ##Advanced Options IIIb
    Input('cst_X','value'),Input('neg_X','value'),Input('noSmearing_X','value'),Input('absFit_X','value')
    ]) 

def pepsi_calculation_fit_adv_opt_III_IIIb(id_folder,n,fast,dro,hyd,cst,neg,noSmearing,absFit):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SAXS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path,'--dro',dro]
        if n !=None:
            command_line.extend(['-n',n])
        if fast=='hyd_shell':
            command_line.extend(['--fast'])
        if hyd=='exp_hyd':
            command_line.extend(['--hyd'])
        if cst == 'cst_fact' :
            command_line.extend(['--cst'])
        if neg == 'neg_cont' :
            command_line.extend(['--neg'])
        if noSmearing == 'no_smear' :
            command_line.extend(['--noSmearing'])
        if absFit !=None :
            command_line.extend(['--absFit',absFit])
        subprocess.check_output(command_line)

## CHOICE : FIT + ADV OPT IIIb
@app.callback(
    Output('placeholder_fit_adv_opt_IIIb', 'children'),
    [Input('id_folder','children'),
    ##Advanced Options IIIb
    Input('cst_X','value'),Input('neg_X','value'),Input('noSmearing_X','value'),Input('absFit_X','value')
    ]) 

def pepsi_calculation_fit_adv_opt_IIIb(id_folder,cst,neg,noSmearing,absFit):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        command_line=["bin/Pepsi-SAXS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path]
        if cst == 'cst_fact' :
            command_line.extend(['--cst'])
        if neg == 'neg_cont' :
            command_line.extend(['--neg'])
        if noSmearing == 'no_smear' :
            command_line.extend(['--noSmearing'])
        if absFit !=None :
            command_line.extend(['--absFit',absFit])
        subprocess.check_output(command_line)

## CHOICE : FIT
@app.callback(
    Output('placeholder_fit_X', 'children'),
    [Input('id_folder','children'),
    ]) 
def pepsi_calculation_fit(id_folder):
    file_path = os.path.join(UPLOAD_DIRECTORY, id_folder) 
    output_path = os.path.join(file_path, 'result.out')
    name=os.listdir(file_path)
    exit=0
    for filename in name:
        if filename[-4:]=='.out' or filename[-4:]=='.log':
            exit+=1
    if exit ==0:
        subprocess.check_output(["bin/Pepsi-SAXS", os.path.join(file_path, name[1]),os.path.join(file_path, name[0]),'-o', output_path])

########### 6. GRAPH

@app.callback(
    Output('graph_prediction','figure'),
    [Input('id_folder','children'),Input('update_graph','n_intervals')],
    events=[Event('update_graph','interval')])  

def graph_prediction(id_folder,n_interval):
    if n_interval==1 or n_interval==2 : 
        file_path=os.path.join(UPLOAD_DIRECTORY,id_folder)
        output_path=os.path.join(file_path,'result.out')
        if os.path.exists(output_path):
            print('graph is under construction',file=sys.stderr)            
            data=np.loadtxt(output_path,skiprows=6)
            q=data[:,0]
            I=data[:,1]
            Iat=data[:,2]
            Iev=data[:,3]
            Ihs=data[:,4]
            trace=[]
            I_value=[I,Iat,Iev,Ihs]
            I_name=['I','Iat','Iev','Ihs']
            for i in range (4):
                trace.append(go.Scatter(
                    x=q,
                    y=I_value[i],
                    name=I_name[i]
                ))
            return {
                'data': trace,
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'q'},
                    yaxis={'type':'log','title': 'I'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                    hovermode='closest'
                    )
                }

@app.callback(
    Output('graph_fit','figure'),
    [Input('id_folder','children'),Input('update_graph','n_intervals')],
    events=[Event('update_graph','interval')])  

def graph_fit(id_folder,n_interval):
    if n_interval==1 or n_interval==2 : 
        file_path=os.path.join(UPLOAD_DIRECTORY,id_folder)
        output_path=os.path.join(file_path,'result.out')
        if os.path.exists(output_path):
            print('graph is under construction',file=sys.stderr)            
            data=np.loadtxt(output_path,skiprows=1)
            q=data[:,0]
            Iexp=data[:,1]
            Ifit=data[:,4]
            trace=[]
            I_value=[Iexp,Ifit]
            I_name=['Iexp','I fit']
            for i in range (2):
                trace.append(go.Scatter(
                    x=q,
                    y=I_value[i],
                    name=I_name[i]
                ))
            return {
                'data': trace,
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'q'},
                    yaxis={'type':'log','title': 'I'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                    hovermode='closest'
                    )
                }

########### 7. FILE DOWNLOAD LINKS

@app.callback(
    Output('file-list','children'),
    [Input('id_folder','children')],
    events=[Event('update_graph','interval')]) 
def update_output(id_folder):  
        files = uploaded_files(id_folder)
        print('files in the unique folder in the uploads folder : ', file=sys.stderr)
        print (files, file=sys.stderr)
        if len(files) == 0:
            return [html.Li('No files yet!')]
        else:
            return [html.Li(file_download_link(filename,id_folder)) for filename in files]


############################## \END CALLBACKS\ ##############################

################################################################################################
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server()
