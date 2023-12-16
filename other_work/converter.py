import json

def transform_entry(entry):
    try:
        # Extract the numeric ID from the resourceId
        resource_id_parts = entry["resourceId"].split('/')
        numeric_id = int(resource_id_parts[-2]) if len(resource_id_parts) > 1 else None
        
        # Normalize the event names
        event_normalized = entry["event"].replace("keydown", "keyDown").replace("keyup", "keyUp")

        # Create the transformed entry dictionary
        transformed_entry = {
            "resourceId": numeric_id,
            "key": entry["key"],
            "keyCode": entry["keyCode"],
            "event": event_normalized,
            "courseId": None if entry["courseId"] == "##placeholder" else entry["courseId"],
            "unixTimestamp": entry["unixTimestamp"],
            "clientId": entry["clientId"],
            "personId": entry["personId"]  # Keeping the email as an ID
        }
        
        # Remove keys with None values or placeholders
        transformed_entry = {k: v for k, v in transformed_entry.items() if v is not None and "##placeholder" not in str(v)}
        
        return transformed_entry
    except Exception as e:
        # Return a message with the error detail
        return f"Error processing entry: {e}"

def transform_data(data):
    return [transform_entry(entry) for entry in data]

def main():
    input_file_path = 'path_to_your_input_file.json'
    output_file_path = 'path_to_your_output_file.json'

    # Read the input JSON file
    with open(input_file_path, 'r') as file:
        data = json.load(file)["data"]

    # Transform the data
    transformed_data = transform_data(data)

    # Write the transformed data to an output file
    with open(output_file_path, 'w') as file:
        json.dump(transformed_data, file, indent=4)

    print(f"Data transformed successfully. Output written to {output_file_path}")

if __name__ == "__main__":
    main()
