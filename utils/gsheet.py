import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
from datetime import datetime
import json

# Cache the gspread client to avoid re-authenticating on every rerun
@st.cache_resource(ttl=3600) # Cache for 1 hour
def get_gsheet_client(creds_json: dict):
    """
    Authenticates with Google Sheets using service account credentials.
    Returns a gspread client.
    """
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Google Sheets authentication failed: {e}")
        return None

def test_gsheet_connection(creds_data=None):
    """Test Google Sheets connection by authorizing client without quota-heavy API calls"""
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        if creds_data:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
        else:
            if 'global_gsheets_creds' not in st.session_state:
                return False
            creds = ServiceAccountCredentials.from_json_keyfile_dict(st.session_state.global_gsheets_creds, scope)

        # Authorize client
        client = gspread.authorize(creds)

        # Minimal test: get an access token (no quota cost)
        token = creds.get_access_token()

        if token.access_token:
            return True
        else:
            return False

    except Exception as e:
        st.error(f"Connection test failed: {str(e)}")
        return False

def extract_sheet_id(url_or_id):
    """Extract sheet ID from URL or return ID if already provided"""
    if not url_or_id:
        return ""
    
    if '/' not in url_or_id:
        return url_or_id
    
    if '/d/' in url_or_id:
        return url_or_id.split('/d/')[1].split('/')[0]
    
    return url_or_id

@st.cache_data(ttl=600) # Cache sheet data for 10 minutes
def get_sheet_data(sheet_id, worksheet_name=None, use_cache=True):
    """Get data from Google Sheet with caching"""
    try:
        sheet_id = extract_sheet_id(sheet_id)
        cache_key = f"{sheet_id}_{worksheet_name or 'default'}"
        
        if use_cache and 'sheets_cache' in st.session_state:
            cache = st.session_state.sheets_cache
            if cache_key in cache:
                cache_entry = cache[cache_key]
                if time.time() - cache_entry.get('timestamp', 0) < 300:
                    return cache_entry['data'], "Success (cached)"
        
        client = get_gsheet_client(st.session_state.global_gsheets_creds)
        if not client:
            return None, "Google Sheets credentials not configured"
        
        spreadsheet_name = sheet_id  # Assuming sheet_id is the spreadsheet name for simplicity
        spreadsheet = client.open(spreadsheet_name)
        
        if worksheet_name:
            worksheet = spreadsheet.worksheet(worksheet_name)
        else:
            worksheet = spreadsheet.get_worksheet(0)
        
        records = worksheet.get_all_records()
        
        if not records:
            return pd.DataFrame(), "Success (empty sheet)"
        
        df = pd.DataFrame(records)
        df = df.dropna(how='all')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        if 'sheets_cache' not in st.session_state:
            st.session_state.sheets_cache = {}
        
        st.session_state.sheets_cache[cache_key] = {
            'data': df,
            'timestamp': time.time(),
            'sheet_title': spreadsheet.title,
            'worksheet_title': worksheet.title
        }
        
        return df, "Success"
        
    except gspread.exceptions.SpreadsheetNotFound:
        return None, "Spreadsheet not found. Check the sheet ID and sharing permissions."
    except gspread.exceptions.WorksheetNotFound:
        return None, f"Worksheet '{worksheet_name}' not found."
    except Exception as e:
        return None, f"Error loading sheet data: {str(e)}"

def append_row_to_sheet(sheet_id, row_data, worksheet_name=None):
    """Append a row to Google Sheet"""
    try:
        sheet_id = extract_sheet_id(sheet_id)
        client = get_gsheet_client(st.session_state.global_gsheets_creds)
        if not client:
            return False, "Google Sheets credentials not configured"
        
        spreadsheet_name = sheet_id  # Assuming sheet_id is the spreadsheet name for simplicity
        spreadsheet = client.open(spreadsheet_name)
        
        if worksheet_name:
            worksheet = spreadsheet.worksheet(worksheet_name)
        else:
            worksheet = spreadsheet.get_worksheet(0)
        
        worksheet.append_row(row_data)
        
        cache_key = f"{sheet_id}_{worksheet_name or 'default'}"
        if 'sheets_cache' in st.session_state and cache_key in st.session_state.sheets_cache:
            del st.session_state.sheets_cache[cache_key]
        
        return True, "Row appended successfully"
        
    except Exception as e:
        return False, f"Error appending row: {str(e)}"

def update_sheet_data(sheet_id, df, worksheet_name=None):
    """Update entire sheet with DataFrame"""
    try:
        sheet_id = extract_sheet_id(sheet_id)
        client = get_gsheet_client(st.session_state.global_gsheets_creds)
        if not client:
            return False, "Google Sheets credentials not configured"
        
        spreadsheet_name = sheet_id  # Assuming sheet_id is the spreadsheet name for simplicity
        if worksheet_name:
            success = update_sheet_data(client, spreadsheet_name, worksheet_name, df)
        else:
            worksheet = spreadsheet.get_worksheet(0)
            worksheet.clear()
            data_to_update = [df.columns.values.tolist()] + df.values.tolist()
            worksheet.update(data_to_update)
            success = True
        
        cache_key = f"{sheet_id}_{worksheet_name or 'default'}"
        if 'sheets_cache' in st.session_state and cache_key in st.session_state.sheets_cache:
            del st.session_state.sheets_cache[cache_key]
        
        return success, "Sheet updated successfully"
        
    except Exception as e:
        return False, f"Error updating sheet: {str(e)}"

def get_sheet_info(sheet_id):
    """Get information about a Google Sheet"""
    try:
        sheet_id = extract_sheet_id(sheet_id)
        client = get_gsheet_client(st.session_state.global_gsheets_creds)
        if not client:
            return None, "Google Sheets credentials not configured"
        
        spreadsheet_name = sheet_id  # Assuming sheet_id is the spreadsheet name for simplicity
        spreadsheet = client.open(spreadsheet_name)
        worksheets = spreadsheet.worksheets()
        
        info = {
            'title': spreadsheet.title,
            'id': spreadsheet.id,
            'url': spreadsheet.url,
            'worksheet_count': len(worksheets),
            'worksheets': [
                {
                    'title': ws.title,
                    'id': ws.id,
                    'row_count': ws.row_count,
                    'col_count': ws.col_count
                }
                for ws in worksheets
            ]
        }
        
        return info, "Success"
        
    except Exception as e:
        return None, f"Error getting sheet info: {str(e)}"

def create_new_worksheet(sheet_id, worksheet_name, rows=1000, cols=26):
    """Create a new worksheet in existing spreadsheet"""
    try:
        sheet_id = extract_sheet_id(sheet_id)
        client = get_gsheet_client(st.session_state.global_gsheets_creds)
        if not client:
            return False, "Google Sheets credentials not configured"
        
        spreadsheet_name = sheet_id  # Assuming sheet_id is the spreadsheet name for simplicity
        spreadsheet = client.open(spreadsheet_name)
        worksheet = spreadsheet.add_worksheet(
            title=worksheet_name,
            rows=rows,
            cols=cols
        )
        
        return True, f"Worksheet '{worksheet_name}' created successfully"
        
    except Exception as e:
        return False, f"Error creating worksheet: {str(e)}"

def delete_worksheet(sheet_id, worksheet_name):
    """Delete a worksheet from spreadsheet"""
    try:
        sheet_id = extract_sheet_id(sheet_id)
        client = get_gsheet_client(st.session_state.global_gsheets_creds)
        if not client:
            return False, "Google Sheets credentials not configured"
        
        spreadsheet_name = sheet_id  # Assuming sheet_id is the spreadsheet name for simplicity
        spreadsheet = client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        spreadsheet.del_worksheet(worksheet)
        
        cache_key = f"{sheet_id}_{worksheet_name}"
        if 'sheets_cache' in st.session_state and cache_key in st.session_state.sheets_cache:
            del st.session_state.sheets_cache[cache_key]
        
        return True, f"Worksheet '{worksheet_name}' deleted successfully"
        
    except Exception as e:
        return False, f"Error deleting worksheet: {str(e)}"

def clear_cache(sheet_id=None):
    """Clear cache for specific sheet or all sheets"""
    if 'sheets_cache' not in st.session_state:
        return
    
    if sheet_id:
        sheet_id = extract_sheet_id(sheet_id)
        keys_to_remove = [k for k in st.session_state.sheets_cache.keys() if k.startswith(sheet_id)]
        for key in keys_to_remove:
            del st.session_state.sheets_cache[key]
    else:
        st.session_state.sheets_cache = {}

def batch_get_sheets_data(sheet_configs):
    """Get data from multiple sheets efficiently"""
    results = {}
    
    for config in sheet_configs:
        sheet_id = config.get('sheet_id', '')
        worksheet_name = config.get('worksheet_name')
        key = config.get('key', sheet_id)
        
        if sheet_id:
            df, error = get_sheet_data(sheet_id, worksheet_name)
            if df is not None:
                results[key] = df
            else:
                st.warning(f"Failed to load {key}: {error}")
    
    return results

def export_sheet_data(df, format='csv'):
    """Export DataFrame to various formats"""
    try:
        if format.lower() == 'csv':
            return df.to_csv(index=False), 'text/csv'
        elif format.lower() == 'excel':
            return df.to_excel(index=False), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif format.lower() == 'json':
            return df.to_json(orient='records', indent=2), 'application/json'
        else:
            return None, None
    except Exception as e:
        st.error(f"Export error: {e}")
        return None, None

@st.cache_data(ttl=3600) # Cache list of sheets for 1 hour
def list_all_spreadsheets(client) -> list:
    """
    Lists all spreadsheets accessible by the service account.
    """
    try:
        spreadsheets = client.list_spreadsheets()
        return [s.title for s in spreadsheets]
    except Exception as e:
        st.error(f"Error listing spreadsheets: {e}")
        return []
