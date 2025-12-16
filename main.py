import json
import csv
import os



# DECORATOR FOR ERROR HANDLING
def safe_run(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"[ERROR] {e}")
    return wrapper



# CONTACT CLASS (OOP)
class Contact:
    def __init__(self, name, phone, email=""):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {"name": self.name, "phone": self.phone, "email": self.email}



# CONTACT BOOK MANAGER (OOP)
class ContactBook:
    def __init__(self, json_file="contacts.json"):
        self.json_file = json_file
        self.contacts = self.load_contacts()

    
    # Load contacts from JSON
    @safe_run
    def load_contacts(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                return json.load(file)
        return []

   
    # Save contacts to JSON
    @safe_run
    def save_contacts(self):
        with open(self.json_file, "w") as file:
            json.dump(self.contacts, file, indent=4)

    
    # Add contact
    @safe_run
    def add_contact(self, contact: Contact):
        self.contacts.append(contact.to_dict())
        self.save_contacts()
        print("\nContact Added Successfully")

   
    # Update contact
    @safe_run
    def update_contact(self, name):
        for c in self.contacts:
            if c["name"].lower() == name.lower():
                print("Enter new details (leave blank to keep current):")
                new_phone = input(f"Phone ({c['phone']}): ") or c["phone"]
                new_email = input(f"Email ({c['email']}): ") or c["email"]

                c["phone"] = new_phone
                c["email"] = new_email
                self.save_contacts()
                print("\nContact Updated Successfully")
                return

        print("Contact Not Found")

    
    # Delete contact
    @safe_run
    def delete_contact(self, name):
        for c in self.contacts:
            if c["name"].lower() == name.lower():
                self.contacts.remove(c)
                self.save_contacts()
                print("\nContact Deleted Successfully")
                return

        print("Contact Not Found")


    # Search contact
    @safe_run
    def search_contact(self, name):
    
        def match(c):
            return c["name"].lower() == name.lower()

        for c in self.contacts:
            if match(c):
                print("\n--- Contact Found ---")
                print(f"Name : {c['name']}")
                print(f"Phone: {c['phone']}")
                print(f"Email: {c['email']}")
                return

        print("Contact Not Found")

    
    # Export contacts to CSV
    @safe_run
    def export_to_csv(self, csv_file="contacts.csv"):
        with open(csv_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "phone", "email"])
            writer.writeheader()
            writer.writerows(self.contacts)
        print("\nContacts Exported to CSV")



# MENU DRIVEN PROGRAM
def main():
    book = ContactBook()

    while True:
        print("\n===== CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. Update Contact")
        print("3. Delete Contact")
        print("4. Search Contact")
        print("5. Export to CSV")
        print("6. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            book.add_contact(Contact(name, phone, email))

        elif ch == "2":
            name = input("Enter contact name to update: ")
            book.update_contact(name)

        elif ch == "3":
            name = input("Enter contact name to delete: ")
            book.delete_contact(name)

        elif ch == "4":
            name = input("Enter name to search: ")
            book.search_contact(name)

        elif ch == "5":
            book.export_to_csv()

        elif ch == "6":
            print("Exiting...")
            break

        else:
            print("Invalid Choice, try again!")


if __name__ == "__main__":
    main()
