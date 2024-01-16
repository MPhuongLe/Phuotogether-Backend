import os
from flask import Flask, render_template, jsonify, request, Blueprint
import json
from database_connector import DatabaseConnector

item_blueprint = Blueprint('item', __name__)

supabase = DatabaseConnector().connection

## Get items by trip id
@item_blueprint.route('/get_items', methods=['GET'])
def get_items():
    try: 
        tripid = request.args.get('tripid')

        if not tripid:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("item").select("itemno", "name").eq("tripid", tripid).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    
# Update items by trip id
@item_blueprint.route('/update_items', methods=['POST'])
def update_items():
    try:
        data = request.get_json()

        tripid = data.get('tripid')
        items = data.get('items')

        if not tripid or not items or not isinstance(items, list):
            return jsonify({"error": "Invalid JSON format or missing required parameters"}), 400

        # Delete existing items for the specified trip
        delete_response = supabase.table("item").delete().eq("tripid", tripid).execute()

        if 'error' in delete_response.data:
            return jsonify({"error": f"Supabase error: {delete_response.data['error']}"}), 500

        # Insert new items
        new_items_data = [{"tripid": tripid, "itemno": i + 1, "name": item} for i, item in enumerate(items)]
        insert_response = supabase.table("item").upsert(new_items_data).execute()

        if 'error' in insert_response.data:
            return jsonify({"error": f"Supabase error: {insert_response.data['error']}"}), 500

        # Return a success response
        return json.dumps(insert_response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
## Delete item by ID
@item_blueprint.route('/delete_items', methods=['DELETE'])
def delete_items():
    try:
        tripid = request.args.get('tripid')

        if not tripid:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("item").delete().eq("tripid", tripid).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
