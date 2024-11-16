import sqlite3
import subprocess
from predict import final
import pdfkit

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
# Connect to the SQLite database
conn = sqlite3.connect('datasets/messages.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()
import subprocess

#def call_predict_script(posts):
#    try:
#        # Call the predict.py script with posts as an argument
#        result = subprocess.run(["python", "predict.py", posts], capture_output=True, text=True, check=True)
#        print("Prediction script executed successfully.")
#        print(result)
#        # Capture the output of the predict.py script
#        prediction = result.stdout.strip()
#        return prediction
#    except subprocess.CalledProcessError as e:
#        print("Error:", e)



def merge_user_posts(user_name):
    # Fetch all message content associated with the specified user name
    cursor.execute("SELECT message_content FROM messages WHERE user_name = ?", (user_name,))
    user_posts = cursor.fetchall()

    # Merge all user posts into one string
    merged_posts = ' ||| '.join([post[0] for post in user_posts])

    return merged_posts

def generate_html_report(result,user):
    # Decode the result into personality traits
    IE = "Introversion (I)" if result[0] == 'I' else "Extroversion (E)"
    NS = "Intuition (N)" if result[1] == 'N' else "Sensing (S)"
    FT = "Feeling (F)" if result[2] == 'F' else "Thinking (T)"
    JP = "Judging (J)" if result[3] == 'J' else "Perceiving (P)"
    
    introversion_extroversion = "You tend to be more introspective and reserved, preferring solitary activities and quiet environments." if result[0] == 'I' else "You thrive in social settings, enjoying interactions with others and seeking out new experiences."
    intuition_sensing = "You often focus on abstract ideas and future possibilities, trusting your instincts and imagination." if result[1] == 'N' else "You rely on concrete facts and details, preferring practical solutions and focusing on the present moment."
    feeling_thinking = "You make decisions based on empathy and personal values, prioritizing harmony and emotional considerations." if result[2] == 'F' else "You approach decisions logically and analytically, weighing pros and cons to find the most rational solution."
    judging_perceiving = "You prefer structure and organization, seeking closure and making plans to achieve your goals." if result[3] == 'J' else "You are flexible and adaptable, embracing spontaneity and keeping your options open."
    specified_user=user
    
    # Generate HTML report
    html_content = """
    <html>
    <head>
        <title>Personality Analysis Report for {} </title>
    </head>
    <body>
        <h1>Personality Analysis Report for {} </h1>
        <p>IE: {}</p>
        <p>NS: {}</p>
        <p>FT: {}</p>
        <p>JP: {}</p>
        <h2>Detailed Analysis:</h2>
        <ul>
            <li><b>{}:</b> {}</li>
            <li><b>{}:</b> {}</li>
            <li><b>{}:</b> {}</li>
            <li><b>{}:</b> {}</li>
        </ul>
    </body>
    </html>
    """.format(specified_user, specified_user, IE, NS, FT, JP, IE, introversion_extroversion, NS,intuition_sensing, FT, feeling_thinking, JP, judging_perceiving)

    return html_content

def save_pdf(html_content, output_path):
    # Convert HTML to PDF and save to output path
    pdfkit.from_string(html_content, output_path, configuration =config)

# Example usage: Specify the user name
specified_user = 'Margaret'

# Get merged posts for the specified user
merged_posts = merge_user_posts(specified_user)

#merged_posts = """ They act like they care They tell me to share But when I carve the stories on my arm The doctor just calls it self harm I’m not asking for attention There’s a reason I have apprehensions I just need you to see What has become of me||| I know I’m going crazy But they think my thoughts are just hazy When in that chaos, in that confusion I’m crying out for help, to escape my delusions||| Mental health is a state of mind How does one keep that up when assistance is denied All my failed attempts to fight the blaze You treat it like its a passing phase||| Well stop, its not, because mental illness is real Understand that we’re all not made of steel Because when you brush these issues under the carpet You make it seem like its our mistake we’re not guarded||| Don’t you realise that its a problem that needs to be addressed Starting at home, in our nest Why do you keep your mouths shut about such things Instead of caring for those with broken wings||| What use is this social stigma When mental illness is not even such an enigma Look around and you’ll see the numbers of the affected hiding under the covers ||| This is an issue that needs to be discussed Not looked down upon with disgust Mental illness needs to be accepted So that people can be protected ||| Let me give you some direction People need affection The darkness must be escaped Only then the lost can be saved||| Bring in a change Something not very strange The new year is here Its time to eradicate fear||| Recognise the wrists under the knives To stop mental illness from taking more lives Let’s break the convention Start ‘suicide prevention’.||| Hoping the festival of lights drives the darkness of mental illness away"""

# Print the merged posts
#print("Merged posts for", specified_user, ":", merged_posts)

# Close the database connection
conn.close()

results=final(merged_posts)

# Sample result (replace with actual result)
#result = "IFTP"

# Generate HTML report
html_content = generate_html_report(results,specified_user)

# Save HTML report as PDF
output_path = f'personality_analysis_report_{specified_user}.pdf'
save_pdf(html_content, output_path)

print("PDF report generated successfully.")
