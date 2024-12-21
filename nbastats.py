from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def show_table():
    # Load the CSV file
    df = pd.read_csv('nbastats.csv')
    
    # Group by personId and personName to calculate total points
    top_scorers = df.groupby(['personId', 'personName'])['points'].sum().reset_index()
    top_scorers = top_scorers.nlargest(10, 'points')

    # Create bar graph
    plt.figure(figsize=(10, 6))
    plt.barh(top_scorers['personName'], top_scorers['points'], color='skyblue')
    plt.xlabel('Points')
    plt.title('Top 10 NBA Scorers of All Time')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest scorer on top

    # Save the plot to a bytes object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode()
    plt.close()

    # Convert DataFrame to HTML
    table_html = df.to_html(classes='table table-striped', index=False)

    # HTML template
    template = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <title>NBA Stats</title>
      </head>
      <body>
        <div class="container">
          <h1 class="mt-5">NBA Stats</h1>
          <h2 class="mt-3">Top 10 NBA Scorers of All Time</h2>
          <img src="data:image/png;base64,{{ graph_url }}" class="img-fluid" alt="Bar graph of top 10 NBA scorers">
          <div class="mt-5">
            {{ table | safe }}
          </div>
        </div>
      </body>
    </html>
    '''

    return render_template_string(template, table=table_html, graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)
