import requests
from bs4 import BeautifulSoup
import csv
import json
import tkinter as tk
import sqlite3

# Function to scrape data
def scrape_data():
    url = input("Enter the website URL to scrape: ")
    output_format = input("Enter output format (csv/json): ").lower()

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Scrape headlines and links
        headlines = soup.find_all('h2')
        links = soup.find_all('a')

        data = []
        for i, headline in enumerate(headlines):
            data.append({
                'headline': headline.get_text(strip=True),
                'link': links[i].get('href') if i < len(links) else None
            })

        if output_format == 'csv':
            with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['headline', 'link'])
                writer.writeheader()
                writer.writerows(data)
            print("Data saved to scraped_data.csv")
        elif output_format == 'json':
            with open('scraped_data.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print("Data saved to scraped_data.json")
        else:
            print("Invalid output format. Choose 'csv' or 'json'.")
    except Exception as e:
        print(f"Error occurred while scraping: {e}")

# Function to perform arithmetic operations
def perform_operation(operation):
    try:
        result = eval(operation)
        print(f"Result: {result}")
        save_to_history(operation, result)
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
    except Exception as e:
        print(f"Invalid input: {e}")

# Function to save history to SQLite
def save_to_history(operation, result):
    conn = sqlite3.connect('calculator_history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS history (operation TEXT, result REAL)''')
    cursor.execute("INSERT INTO history (operation, result) VALUES (?, ?)", (operation, result))
    conn.commit()
    conn.close()

# Function to view history
def view_history():
    conn = sqlite3.connect('calculator_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history")
    rows = cursor.fetchall()
    conn.close()
    print("Calculation History:")
    for row in rows:
        print(f"Operation: {row[0]}, Result: {row[1]}")

# GUI for calculator
def calculator_gui():
    def calculate():
        operation = operation_entry.get()
        try:
            result = eval(operation)
            result_label.config(text=f"Result: {result}")
            save_to_history(operation, result)
        except ZeroDivisionError:
            result_label.config(text="Error: Division by zero is not allowed.")
        except Exception as e:
            result_label.config(text=f"Error: {e}")

    root = tk.Tk()
    root.title("Calculator")

    tk.Label(root, text="Enter Operation:").pack()
    operation_entry = tk.Entry(root, width=20)
    operation_entry.pack()

    tk.Button(root, text="Calculate", command=calculate).pack()

    result_label = tk.Label(root, text="Result: ")
    result_label.pack()

    root.mainloop()

# Main menu
def main():
    while True:
        print("\nChoose an option:")
        print("1. Web Scraper")
        print("2. Calculator (Console)")
        print("3. Calculator (GUI)")
        print("4. View Calculation History")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            scrape_data()
        elif choice == '2':
            operation = input("Enter operation (e.g., 2 + 2): ")
            perform_operation(operation)
        elif choice == '3':
            calculator_gui()
        elif choice == '4':
            view_history()
        elif choice == '5':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
