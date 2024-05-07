from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

filename = "C://Users//Prakhar Singh//Desktop//Prakhar//Sample Docs//DataDictionaryKPIMod.xlsx"

def search_excel_for_id_and_matching_column(search_term):
    df = pd.read_excel(filename)
    matching_rows = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]
    id_column = matching_rows['ID']
    matching_column_name = matching_rows.columns[matching_rows.apply(lambda col: search_term.lower() in str(col).lower(), axis=0)][0]
    matching_column_data = matching_rows[matching_column_name]
    result = pd.DataFrame({'ID': id_column, matching_column_name: matching_column_data})
    result_json = result.to_json(orient='records')
    return result_json

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search_term')
    
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400
    
    try:
        result = search_excel_for_id_and_matching_column(search_term)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
