from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary storage for student records
students = {}

# Home route
@app.route('/')
def home():
	return jsonify({
		"message": "Welcome to Student Management REST API"
	})

# GET - Retrieve all students
@app.route('/students', methods=['GET'])
def get_students():
	return jsonify(list(students.values())), 200

# POST - Add a new student
@app.route('/students', methods=['POST'])
def add_student():
	data = request.get_json()

	if not data or 'name' not in data or 'course' not in data:
		return jsonify({"error": "Name and course are required"}), 400

	student_id = max(students.keys(), default=0) + 1

	student = {
		"id": student_id,
		"name": data['name'],
		"course": data['course']
	}

	students[student_id] = student

	return jsonify(student), 201

# GET - Retrieve a particular student
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
	student = students.get(student_id)

	if student is None:
		return jsonify({"error": "Student not found"}), 404

	return jsonify(student), 200

# PUT - Update student details
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
	student = students.get(student_id)

	if student is None:
		return jsonify({"error": "Student not found"}), 404

	data = request.get_json()

	if not data:
		return jsonify({"error": "Request data is required"}), 400

	student['name'] = data.get('name', student['name'])
	student['course'] = data.get('course', student['course'])

	return jsonify(student), 200

# DELETE - Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
	if student_id not in students:
		return jsonify({"error": "Student not found"}), 404

	del students[student_id]

	return jsonify({"message": "Student deleted successfully"}), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
