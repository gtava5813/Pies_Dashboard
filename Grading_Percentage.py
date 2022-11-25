#!/usr/bin/env python
# coding: utf-8

# ### Energy Grades
# Local Law 33 of 2018 amended the Administrative Code of the City of New York in relation to energy efficiency scores and grades for buildings required to benchmark their energy and water consumption. These energy efficiency scores and grades for these buildings are assigned and disclosed in accordance with the new section §28-309.12 annually, based on benchmarking reporting consistent with Federal energy efficiency standards.
#
# An energy efficiency score is the Energy Star Rating that a building earns using the United States Environmental Protection Agency online benchmarking tool, Energy Star Portfolio Manager, to compare building energy performance to similar buildings in similar climates. As per Local Law 95 of 2019 grades based on Energy Star energy efficiency scores will be assigned as follows:
#
# A – score is equal to or greater than 85
#
# B – score is equal to or greater than 70 but less than 85
#
# C – score is equal to or greater than 55 but less than 70
#
# D – score is less than 55
#
# F – for buildings that didn’t submit required benchmarking information
#
# N – for buildings exempted from benchmarking or not covered by the Energy Star program.
#
# The energy label includes both a letter grade and the energy efficiency score of the building. Please reference the following document for more information Local Law 33 as amended by LL95 of 2019 Steps to Compliance.
#
# Additional Information
# For more details and to start the benchmarking process, please reference the Local Law 33 as amended by LL95 of 2019 Steps to Compliance, LL33 - Frequently Asked Questions, and visit the Compliance Instructions page.
#
# The status of a violation can be found online by using the Department’s Building Information System (BIS) at any time. To follow up by email, please send inquiries to sustainability@buildings.nyc.gov with the BBL, BIN, address and violation number for the building.
#
# If you believe a violation was issued in error, you may submit a Benchmarking Violation Challenge Form. This form must be sent to the Department within 30 days of the violation postmark. Email the form to sustainability@buildings.nyc.gov.
#
# To follow up on a challenge, please call the (212) 393-2574 or email sustainability@buildings.nyc.gov.
#
# Additional Resources
# NYC Mayor's Office of Sustainability
#
# Energy Star Portfolio Manager
#
# DOF Benchmarking Website

from bokeh.palettes import Category20c, Category20, Category10
import requests
import json
from bokeh.models.widgets.tables import NumberFormatter, BooleanFormatter
from panel.template import DefaultTheme
from bokeh.transform import cumsum
from bokeh.plotting import figure
from bokeh.plotting import figure, output_file, show
from bokeh.resources import INLINE
from bokeh.io import output_notebook
from math import pi
import holoviews as hv
import panel as pn
import pandas as pd
import numpy as np
import hvplot.pandas
import os
import hvplot.pandas  # noqa
import matplotlib
pn.extension()
pn.extension('tabulator')
hv.extension("bokeh")
DefaultTheme.find_theme(pn.template.MaterialTemplate)


# Making a get request
Success = False
response = requests.get(
    'https://data.cityofnewyork.us/resource/355w-xvp2.json')
# print response
if response.ok:
    print('The request succeeded')
    Success = True
else:
    print('Bad Request')


# print('https://data.cityofnewyork.us/resource/355w-xvp2.json?boroughname=BROOKLYN')

def Borough_Names(Place):
    global only
    Len_A = len(only.query("letterscore == 'A'"))
    Len_B = len(only.query("letterscore == 'B'"))
    Len_C = len(only.query("letterscore == 'C'"))
    Len_D = len(only.query("letterscore == 'D'"))
    Len_F = len(only.query("letterscore == 'F'"))
    Len_N = len(only.query("letterscore == 'N'"))

    Grading = {
        'A': int(Len_A),
        'B': int(Len_B),
        'C': int(Len_C),
        'D': int(Len_D),
        'F': int(Len_F),
        'N': int(Len_N)}

    # making a percent
    data = pd.Series(Grading).reset_index(
        name='Total').rename(columns={'index': 'Grades'})
    data['angle'] = data['Total']/data['Total'].sum() * 2*pi
    data['color'] = Category10[len(Grading)]
    data['percent'] = data['Total'] / sum(Grading.values()) * 100

    p = figure(height=350, title=str(Place) + " Grades Total Percent", toolbar_location=None,
               tools="hover", tooltips="@Grades: @percent{0.2f} %", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='Grades', source=data)
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    pie_place = p
    return pie_place


def Grading_pipe():
    global only
    Len_A = len(only.query("letterscore == 'A'"))
    Len_B = len(only.query("letterscore == 'B'"))
    Len_C = len(only.query("letterscore == 'C'"))
    Len_D = len(only.query("letterscore == 'D'"))
    Len_F = len(only.query("letterscore == 'F'"))
    Len_N = len(only.query("letterscore == 'N'"))

    Grading = {
        'A': int(Len_A),
        'B': int(Len_B),
        'C': int(Len_C),
        'D': int(Len_D),
        'F': int(Len_F),
        'N': int(Len_N)}

    # making a percent
    data = pd.Series(Grading).reset_index(
        name='Total').rename(columns={'index': 'Grades'})
    data['percent'] = data['Total'] / sum(Grading.values()) * 100
    Table_Data = data
    return Table_Data

#Total = pd.read_json(r'https://data.cityofnewyork.us/resource/355w-xvp2.json?$limit=21681')


bokeh_formatters = {'percent': NumberFormatter(format='0.00')}

# Manhattan
only = pd.read_json(
    r'https://data.cityofnewyork.us/resource/355w-xvp2.json?boroughname=MANHATTAN&$limit=10000')
#Only = (df[df['BoroughName'] == 'MANHATTAN'])
Manhattan = (Borough_Names('Manhattan'))
Manhattan_Table = Grading_pipe()
MN_widget = pn.widgets.Tabulator(Manhattan_Table, pagination='remote',
                                 page_size=10, sizing_mode='stretch_width', formatters=bokeh_formatters)

# BROOKLYN
only = pd.read_json(
    r'https://data.cityofnewyork.us/resource/355w-xvp2.json?boroughname=BROOKLYN&$limit=100000')
#Only = (df[df['BoroughName'] == 'BROOKLYN'])
Brooklyn = (Borough_Names('Brooklyn'))
Brooklyn_Table = Grading_pipe()
BK_widget = pn.widgets.Tabulator(Brooklyn_Table, pagination='remote',
                                 page_size=10, sizing_mode='stretch_width', formatters=bokeh_formatters)


# Queens
only = pd.read_json(
    r'https://data.cityofnewyork.us/resource/355w-xvp2.json?boroughname=QUEENS&$limit=10000')
#Only = (df[df['BoroughName'] == 'QUEENS'])
Queens = (Borough_Names('Queens'))
Queens_Table = Grading_pipe()
QN_widget = pn.widgets.Tabulator(Queens_Table, pagination='remote',
                                 page_size=10, sizing_mode='stretch_width', formatters=bokeh_formatters)

# BRONX
only = pd.read_json(
    r'https://data.cityofnewyork.us/resource/355w-xvp2.json?boroughname=BRONX&$limit=10000')
#Only = (df[df['BoroughName'] == 'BRONX'])
Bronx = (Borough_Names('Bronx'))
Bronx_Table = Grading_pipe()
BX_widget = pn.widgets.Tabulator(Bronx_Table, pagination='remote',
                                 page_size=10, sizing_mode='stretch_width', formatters=bokeh_formatters)

# STATEN ISLAND

only = pd.read_json(
    r'https://data.cityofnewyork.us/resource/355w-xvp2.json?boroughname=STATEN%20ISLAND&$limit=10000')
#Only = (df[df['BoroughName'] == 'STATEN ISLAND'])
Staten_Island = (Borough_Names('Staten Island'))
Staten_Island_Table = Grading_pipe()
IS_widget = pn.widgets.Tabulator(
    Staten_Island_Table, pagination='remote', page_size=10, sizing_mode='stretch_width')

# Layout using Template
template = pn.template.FastListTemplate(
    title='Building Energy Grading dashboard', sidebar=[pn.pane.Markdown("# Energy Grades"),
                                                        pn.pane.Markdown("#### Local Law 33 of 2018 amended the Administrative Code of the City of New York in relation to energy efficiency scores and grades for buildings required to benchmark their energy and water consumption. These energy efficiency scores and grades for these buildings are assigned and disclosed in accordance with the new section §28-309.12 annually, based on benchmarking reporting consistent with Federal energy efficiency standards. An energy efficiency score is the Energy Star Rating that a building earns using the United States Environmental Protection Agency online benchmarking tool, Energy Star Portfolio Manager, to compare building energy performance to similar buildings in similar climates. As per Local Law 95 of 2019 grades based on Energy Star energy efficiency scores will be assigned as follows: A – score is equal to or greater than 85 B – score is equal to or greater than 70 but less than 85 C – score is equal to or greater than 55 but less than 70 D – score is less than 55 F – for buildings that didn’t submit required benchmarking information N – for buildings exempted from benchmarking or not covered by the Energy Star program. The energy label includes both a letter grade and the energy efficiency score of the building. Please reference the following document for more information Local Law 33 as amended by LL95 of 2019 Steps to Compliance. Additional Information For more details and to start the benchmarking process, please reference the Local Law 33 as amended by LL95 of 2019 Steps to Compliance, LL33 - Frequently Asked Questions, and visit the Compliance Instructions page. The status of a violation can be found online by using the Department’s Building Information System (BIS) at any time. To follow up by email, please send inquiries to sustainability@buildings.nyc.gov with the BBL, BIN, address and violation number for the building. If you believe a violation was issued in error, you may submit a Benchmarking Violation Challenge Form. This form must be sent to the Department within 30 days of the violation postmark. Email the form to sustainability@buildings.nyc.gov. To follow up on a challenge, please call the (212) 393-2574 or email sustainability@buildings.nyc.gov. Additional Resources NYC Mayor's Office of Sustainability Energy Star Portfolio Manager DOF Benchmarking Website.")
                                                        ],
    main=[
        pn.Row(pn.Column(Manhattan), pn.Column(MN_widget)),
        pn.Row(pn.Column(Brooklyn), pn.Column(BK_widget)),
        pn.Row(pn.Column(Queens), pn.Column(QN_widget)),
        pn.Row(pn.Column(Bronx), pn.Column(BX_widget)),
        pn.Row(pn.Column(Staten_Island), pn.Column(IS_widget))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)

template.show()
template.servable()
