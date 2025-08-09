from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)
CONTACTS_FILE = "contacts.txt"

# Read contacts from file
def read_contacts():
    contacts = []
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    contacts.append({"name": parts[0], "phone": parts[1], "email": parts[2]})
    return contacts

# Write contacts to file
def write_contacts(contacts):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as file:
        for c in contacts:
            file.write(f"{c['name']}|{c['phone']}|{c['email']}\n")

@app.route("/", methods=["GET", "POST"])
def home():
    contacts = read_contacts()

    if request.method == "POST":
        action = request.form.get("action")
        if action == "Add":
            name = request.form.get("name", "").strip()
            phone = request.form.get("phone", "").strip()
            email = request.form.get("email", "").strip()
            if name and phone:
                contacts.append({"name": name, "phone": phone, "email": email})
                write_contacts(contacts)
        elif action == "Delete":
            name = request.form.get("name", "").strip()
            contacts = [c for c in contacts if c["name"].lower() != name.lower()]
            write_contacts(contacts)
        elif action == "Search":
            query = request.form.get("search_query", "").lower()
            contacts = [c for c in contacts if query in c["name"].lower() or query in c["phone"]]

    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return render_template_string(html_content, contacts=contacts)

@app.route("/style.css")
def css():
    return send_from_directory(".", "style.css")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
