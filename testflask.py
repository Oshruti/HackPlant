# from flask import Flask, render_template
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     # Path to the image you saved
#     plot_path = 'static/sensor_plot.png'
#     return render_template('index.html', plot_path=plot_path)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, Response, jsonify
import matplotlib.pyplot as plt
import io
import pandas as pd

app = Flask(__name__)

# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Function to generate the temperature plot
def generate_temperature_plot():
    data = pd.read_csv('sensor_data.csv', header=None)
    temperature = data.iloc[:, 0]  # First column

    fig, ax = plt.subplots()
    ax.plot(temperature, label='Temperature (°C)', color='red')
    ax.legend()
    ax.set_title("Temperature")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

# Function to generate the humidity plot
def generate_humidity_plot():
    data = pd.read_csv('sensor_data.csv', header=None)
    humidity = data.iloc[:, 1]  # Second column

    fig, ax = plt.subplots()
    ax.plot(humidity, label='Humidity (%)', color='blue')
    ax.legend()
    ax.set_title("Humidity")
    ax.set_xlabel("Time")
    ax.set_ylabel("Humidity (%)")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

# Route to serve the temperature plot dynamically
@app.route('/temperature_plot')
def temperature_plot():
    return Response(generate_temperature_plot(), mimetype='image/png')

# Route to serve the humidity plot dynamically
@app.route('/humidity_plot')
def humidity_plot():
    return Response(generate_humidity_plot(), mimetype='image/png')

# Route to serve the latest sensor data as JSON
@app.route('/latest_data')
def latest_data():
    data = pd.read_csv('sensor_data.csv', header=None)
    latest_temperature = data.iloc[-1, 0]  # Latest temperature value
    latest_humidity = data.iloc[-1, 1]  # Latest humidity value
    return jsonify({
        'temperature': latest_temperature,
        'humidity': latest_humidity
    })

if __name__ == '__main__':
    app.run(debug=True)

