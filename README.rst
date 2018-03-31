pyspreadsheet
=====

A python package to easily send data to Google Sheets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


1) Installation
'''''''''''''''

Open a terminal and install pyspreadsheet package

::

    pip install pyspreadsheet


2) Use
''''''

1) Find a client_secrets.json file

Log into the Google Developers Console with the Google account whose spreadsheets you want to access. Create (or select) a project and enable the Drive API and Sheets API (under Google Apps APIs).
Go to the Credentials for your project and create New credentials > OAuth client ID > of type Other. In the list of your OAuth 2.0 client IDs click Download JSON for the Client ID you just created. Save the file as client_secrets.json.


2) Be sure that you have set environment variables with path to client_secrets.json file (by default ./)  and a path where pyspreadsheet will store Google Credentials (by default ./)


::

    export GOOGLE_CLIENT_SECRET_PATH="./"
    export GOOGLE_CREDENTIALS_PATH="./"

3) Prepare your data like that:


.. code:: python

    data = {
            "worksheet_name"    : 'name_of_the_worsheet_you_want_to_send_data'
            "columns_name"  : [first_column_name,second_column_name,...,last_column_name],
            "rows"      : [[first_raw_value,second_raw_value,...,last_raw_value],...]
        }

4) Send your data to the right with the sheet_id paramater:


.. code:: python

    import pyspreadsheet
    pyspreadsheet.send_to_sheet(sheet_id, data)

- pyspreadsheet will warn you if it has to overwrite some data, except if first row (column_name) are the same than column_name you want to send

2) Import from Redshift to Google Sheets
''''''''''''''''''''''''''''''''''''''''
pyspreadsheet has a function to export result of a Amazon Redshift query to a Google Sheet. This use `pyred <https://github.com/dacker-team/pyred/>`_.
Simply write:


.. code:: python

    import pyspreadsheet
    pyspreadsheet.redshift.query_to_sheet(sheet_id, worksheet_name, instance, query)

