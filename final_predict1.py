import sqlite3
import subprocess
import pdfkit
import tkinter as tk
from tkinter import filedialog
from predict import final

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# Function to merge user posts from the database
def merge_user_posts(cursor, user_name):
    cursor.execute("SELECT message_content FROM messages WHERE user_name = ?", (user_name,))
    user_posts = cursor.fetchall()
    merged_posts = ' ||| '.join([post[0] for post in user_posts])
    return merged_posts

# Function to generate HTML report
def generate_html_report(result, user):
    # Decode the result into personality traits
    IE = "Introversion (I)" if result[0] == 'I' else "Extroversion (E)"
    NS = "Intuition (N)" if result[1] == 'N' else "Sensing (S)"
    FT = "Feeling (F)" if result[2] == 'F' else "Thinking (T)"
    JP = "Judging (J)" if result[3] == 'J' else "Perceiving (P)"
    
    introversion_extroversion = "You tend to be more introspective and reserved, preferring solitary activities and quiet environments." if result[0] == 'I' else "You thrive in social settings, enjoying interactions with others and seeking out new experiences."
    intuition_sensing = "You often focus on abstract ideas and future possibilities, trusting your instincts and imagination." if result[1] == 'N' else "You rely on concrete facts and details, preferring practical solutions and focusing on the present moment."
    feeling_thinking = "You make decisions based on empathy and personal values, prioritizing harmony and emotional considerations." if result[2] == 'F' else "You approach decisions logically and analytically, weighing pros and cons to find the most rational solution."
    judging_perceiving = "You prefer structure and organization, seeking closure and making plans to achieve your goals." if result[3] == 'J' else "You are flexible and adaptable, embracing spontaneity and keeping your options open."
    
    specified_user = user
    
    # Generate HTML report
    html_content = f"""
    <html>
    <head>
        <title>Personality Analysis Report for {specified_user} </title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 16px;
                color: #333;
                margin: 20px;
            }}
            h1 {{
                color: #0066cc;
                font-size: 24px;
            }}
            p {{
                color: #009933;
                font-size: 18px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            b {{
                font-weight: bold;
            }}
            .button {{
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <h1>Personality Analysis Report</h1>
        <p>IE: {IE}</p>
        <p>NS: {NS}</p>
        <p>FT: {FT}</p>
        <p>JP: {JP}</p>
        <h2>Detailed Analysis:</h2>
        <ul>
            <li><b>{IE}:</b> {introversion_extroversion}</li>
            <li><b>{NS}:</b> {intuition_sensing}</li>
            <li><b>{FT}:</b> {feeling_thinking}</li>
            <li><b>{JP}:</b> {judging_perceiving}</li>
        </ul>
    </body>
    </html>
    """
    return html_content

# Function to save HTML report as PDF
def save_pdf(html_content, output_path):
    pdfkit.from_string(html_content, output_path, configuration=config)

# Function to handle button click event
import shutil

def generate_report_and_download():
    specified_user = entry.get()  # Get user input from the entry widget

    # Connect to the SQLite database
    conn = sqlite3.connect('datasets/messages2.db')
    cursor = conn.cursor()

    # Merge user posts from the database
    merged_posts = merge_user_posts(cursor, specified_user)

    # Close the database connection
    conn.close()

    # Generate personality analysis result (replace with actual result)
    # results = final(merged_posts)
    # Sample result
    results=final(merged_posts)

    # Generate HTML report
    html_content = generate_html_report(results, specified_user)

    # Save HTML report as PDF
    output_path = f'personality_analysis_report_{specified_user}.pdf'
    save_pdf(html_content, output_path)

    # Specify download location
    download_location = filedialog.askdirectory()

    # Move the PDF file to the download location
    shutil.move(output_path, download_location)

    print("PDF report generated and downloaded successfully.")

# Create a Tkinter window
window = tk.Tk()
window.title("Personality Analysis Report Generator")

# Set window size and position
window.geometry("600x400+400+200")  # Width x Height + X_offset + Y_offset

# Create and pack widgets
label = tk.Label(window, text="Enter the specified user name:", font=("Arial", 18))
label.pack(pady=10)

entry = tk.Entry(window, font=("Arial", 16), width=40)
entry.pack(pady=10)

button = tk.Button(window, text="Generate Report and Download PDF", font=("Arial", 16), command=generate_report_and_download, bg="#4CAF50")
button.pack(pady=20)

# Run the main event loop
window.mainloop()
