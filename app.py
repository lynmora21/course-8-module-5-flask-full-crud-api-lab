from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Get JSON data from the request body
    data = request.get_json()

    # Check that JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Check that a title was provided
    if "title" not in data:
        return jsonify({"error": "Event title is required"}), 400

    # Generate a new ID
    new_id = max([event.id for event in events], default=0) + 1

    # Create the new event and add it to the list
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    # Return the new event with a 201 Created status
    return jsonify(new_event.to_dict()), 201


# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Get JSON data from the request body
    data = request.get_json()

    # Check that JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Find the event with the requested ID
    event = next((event for event in events if event.id == event_id), None)

    # Return an error if the event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Check that a title was provided
    if "title" not in data:
        return jsonify({"error": "Event title is required"}), 400

    # Update the event title
    event.title = data["title"]

    # Return the updated event
    return jsonify(event.to_dict()), 200


# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event with the requested ID
    event = next((event for event in events if event.id == event_id), None)

    # Return an error if the event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the in-memory list
    events.remove(event)

    # Return a success message
    return jsonify({
        "message": "Event deleted successfully",
        "event": event.to_dict()
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
