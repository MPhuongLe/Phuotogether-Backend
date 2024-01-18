import os
from flask import Flask, render_template, jsonify, request, Blueprint, send_file
import json
from database_connector import DatabaseConnector

user_blueprint = Blueprint('user', __name__)

supabase = DatabaseConnector().connection

## Get user by ID
@user_blueprint.route('/get_user', methods=['GET'])
def get_user_by_id():
    try: 
        user_id = request.args.get('id')

        if not user_id:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("user").select("*").eq("id", user_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
def find_user_file(user_id):
    # Assuming the files are stored in a directory named 'images/AVATAR'
    user_files_dir = '../images/AVATAR'

    # Iterate over common image formats (you can extend this list based on your needs)
    image_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp']

    for format in image_formats:
        file_path = os.path.join(user_files_dir, f'{user_id}.{format}')
        if os.path.exists(file_path):
            return file_path

    return None

@user_blueprint.route('/get_avatar', methods=['GET'])
def get_user_file():
    try:
        user_id = request.args.get('id')
        # Ensure the user ID is a valid filename
        user_id = ''.join(c for c in user_id if c.isalnum() or c in ('_', '-'))

        if not user_id:
            return jsonify({"error": "Missing required parameter"}), 400
        file_path = find_user_file(user_id)

        if file_path:
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Get user by ID
@user_blueprint.route('/get_user_by_account', methods=['POST'])
def get_user_by_account():
    try: 
        data = request.get_json()
        emailortel = data.get('emailortel')
        password = data.get('password')

        if not emailortel or not password:
            return jsonify({"error": "Missing required parameter"}), 400

        response = supabase.table("user").select("*").eq("emailortel", emailortel).execute()

        user_data = response.data[0]
        if 'password' in user_data and user_data['password'] == password:
            return json.dumps(response.data, ensure_ascii=False)
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": "Invalid credentials"}), 500
    
@user_blueprint.route('/update_avatar', methods=['POST'])
def update_avatar():
    try:
        user_id = request.form.get('id')

        if not user_id:
            return jsonify({"error": "Missing required parameter 'id'"}), 400

        # Check if the request contains a file
        if 'avatar' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        avatar_file = request.files['avatar']
        _, file_extension = os.path.splitext(avatar_file.filename)

        # Ensure the user ID is a valid filename
        user_id = ''.join(c for c in user_id if c.isalnum() or c in ('_', '-'))

        # Assuming the files are stored in a directory named 'images/AVATAR'
        user_files_dir = '../images/AVATAR'

        # Save the new avatar file
        avatar_path = os.path.join(user_files_dir, f'{user_id}{file_extension}')
        avatar_file.save(avatar_path)

        return jsonify({"success": "Avatar updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Insert user 
@user_blueprint.route('/insert_user', methods=['POST'])
def insert_user():
    try:
        data = request.get_json()
        emailortel = data.get('emailortel')
        logintype = data.get('logintype', True) # Default value = True
        password = data.get('password')
        fullname = data.get('fullname')
        print(data, emailortel, logintype, password, fullname)

        if not emailortel or not password:
            return jsonify({"error": "Missing required parameters"}), 400

        user_data = {
            "emailortel": emailortel,
            "logintype": logintype,
            "password": password,
            "fullname": fullname,
        }

        response = supabase.table("user").upsert([user_data]).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Delete user by ID
@user_blueprint.route('/delete_user', methods=['DELETE'])
def delete_user_by_id():
    try:
        data = request.get_json()
        user_id = data.get('id')
        
        if not user_id:
            return jsonify({"error": "User ID is missing"}), 400
        
        response = supabase.table("user").delete().eq("id", user_id).execute()
        
        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
## Update user by ID
@user_blueprint.route('/update_user', methods=['PUT'])
def update_user_by_id():
    try:
        data = request.get_json()
        user_id = data.get('id', 0)
        password = data.get('password')
        fullname = data.get('fullname')

        if not user_id or (not password and not fullname):
            return jsonify({"error": "Missing required parameters"}), 400

        update_data = {}
        if password:
            update_data['password'] = password
        if fullname:
            update_data['fullname'] = fullname

        response = supabase.table("user").update(update_data).eq('id', user_id).execute()

        if 'error' in response.data:
            return jsonify({"error": f"Supabase error: {response.data['error']}"}), 500
        else:
            return json.dumps(response.data, ensure_ascii=False)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
