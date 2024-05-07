from flask import Flask, request, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

filename = "C://Users//Prakhar Singh//Desktop//Prakhar//Sample Docs//DataDictionaryKPIMod.xlsx"

# Load BERT model for semantic encoding
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Can change the threshold value here to see expected results
def search_excel_for_columns(search_term, threshold=0.3):
    try:
        df = pd.read_excel(filename)
    except FileNotFoundError:
        return None, 'File not found'
    except pd.errors.EmptyDataError:
        return None, 'No data found in the file'

    combined_text = df['Dashboard'] + ' ' + df['KPI'] + ' ' + df['Description']
    
    # Semantic encoding of search term
    search_embedding = model.encode(search_term, convert_to_tensor=True)
    text_embeddings = model.encode(combined_text.tolist(), convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(search_embedding, text_embeddings)[0]
    print("Cosine Similarity Scores:", cos_scores)
    matching_indices = (cos_scores >= threshold).nonzero().flatten().tolist()
    
    # Collect all matching rows
    matching_results = []
    for index in matching_indices:
        row = df.iloc[index]
        matching_results.append({
            'ID': int(row['ID']),
            'Dashboard': str(row['Dashboard']),
            'KPI': str(row['KPI']),
            'Description': str(row['Description'])
        })
    
    return matching_results, None

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search_term')
    
    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400
    
    try:
        results, error = search_excel_for_columns(search_term)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'result': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
