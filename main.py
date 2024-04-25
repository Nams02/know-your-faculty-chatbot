from flask import Flask, render_template, request
import pandas as pd
from langchain.llms import OpenAI
import os

os.environ['OPENAI_API_KEY'] = 'your_api_key'
model = OpenAI(temperature=0.6)


df = pd.read_csv("fdata.csv", encoding="ISO-8859-1", sep=';')

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():

    user_input = request.form['inp']
    user_input1 = request.form['inp1']

    data = df[df['Name'] == user_input][['Phone Number', 'Description']]

    if data.empty:
        return f'''ERROR: We regret to inform that requested faculty member's details are currently unavailable.\nKindly request you to attempt an alternative name.\nRest assured, we are actively working to enhance and expand our system capabilities.'''
    data = data.to_html(index=False)

    prompt = model(
        "Information: " + data + "Answer the following: " + user_input1)

    return f'{prompt}'


if __name__ == '__main__':
    app.run(debug=True)
