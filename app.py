from flask import Flask, request, render_template_string
from jinja2 import Template

app = Flask(__name__)

# --- Simplified LCA Data Model ---
# All values are per kg
# Scores are mock data for demonstration
data = {
    'aluminum_virgin': {'carbon': 15.0, 'water': 1.5, 'energy': 15.0, 'waste': 2.5, 'score': 45},
    'aluminum_recycled': {'carbon': 1.5, 'water': 0.1, 'energy': 1.0, 'waste': 0.2, 'score': 92},
    'copper_virgin': {'carbon': 3.5, 'water': 2.0, 'energy': 4.0, 'waste': 0.8, 'score': 60},
    'copper_recycled': {'carbon': 0.8, 'water': 0.3, 'energy': 0.8, 'waste': 0.15, 'score': 85},
    'steel_virgin': {'carbon': 2.5, 'water': 0.5, 'energy': 0.5, 'waste': 1.2, 'score': 75},
    'steel_recycled': {'carbon': 0.5, 'water': 0.1, 'energy': 0.2, 'waste': 0.1, 'score': 90},
    'zinc_virgin': {'carbon': 3.0, 'water': 1.0, 'energy': 1.5, 'waste': 0.6, 'score': 68},
    'zinc_recycled': {'carbon': 0.7, 'water': 0.2, 'energy': 0.5, 'waste': 0.1, 'score': 88},
    'nickel_virgin': {'carbon': 5.0, 'water': 2.5, 'energy': 5.5, 'waste': 1.0, 'score': 55},
    'nickel_recycled': {'carbon': 1.2, 'water': 0.4, 'energy': 1.5, 'waste': 0.2, 'score': 83},
    'tin_virgin': {'carbon': 4.0, 'water': 1.8, 'energy': 3.5, 'waste': 0.7, 'score': 62},
    'tin_recycled': {'carbon': 1.0, 'water': 0.3, 'energy': 0.9, 'waste': 0.1, 'score': 87},
    'lead_virgin': {'carbon': 4.5, 'water': 0.8, 'energy': 0.9, 'waste': 1.5, 'score': 58},
    'lead_recycled': {'carbon': 0.9, 'water': 0.15, 'energy': 0.2, 'waste': 0.1, 'score': 89},
    'gold_virgin': {'carbon': 25000.0, 'water': 3000.0, 'energy': 5000.0, 'waste': 1000.0, 'score': 20},
    'gold_recycled': {'carbon': 150.0, 'water': 50.0, 'energy': 200.0, 'waste': 10.0, 'score': 95},
    'silver_virgin': {'carbon': 12000.0, 'water': 1500.0, 'energy': 2500.0, 'waste': 500.0, 'score': 30},
    'silver_recycled': {'carbon': 70.0, 'water': 20.0, 'energy': 100.0, 'waste': 5.0, 'score': 93},
}

# --- Simplified Lifecycle Stage Data (Mock) ---
# Represents the percentage of impact from each stage
lifecycle_impacts = {
    'virgin': {
        'Raw Material Extraction': 60,
        'Manufacturing & Processing': 30,
        'Transportation': 5,
        'End-of-Life': 5,
    },
    'recycled': {
        'Raw Material Extraction': 10,
        'Manufacturing & Processing': 60,
        'Transportation': 10,
        'End-of-Life': 20,
    }
}

# --- History storage (in-memory for the prototype) ---
history = []

# --- HTML Templates (as strings) ---
input_form_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Driven LCA Prototype</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .score-good { background-color: #d1fae5; color: #065f46; }
        .score-medium { background-color: #fffbe6; color: #b45309; }
        .score-bad { background-color: #fee2e2; color: #991b1b; }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full mb-8">
        <h1 class="text-4xl font-extrabold text-gray-800 text-center mb-2">AI-Powered LCA Tool</h1>
        <p class="text-xl text-gray-600 text-center mb-8">Analyze the environmental footprint of metals.</p>
        <form action="/" method="post" class="space-y-6">
            <div>
                <label for="material" class="block text-gray-700 font-semibold mb-2">Select a Metal:</label>
                <select id="material" name="material" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                    {% for mat in materials %}
                        <option value="{{ mat['id'] }}">{{ mat['name'] }}</option>
                    {% endfor %}
                </select>
            </div>
            <div>
                <label for="quantity" class="block text-gray-700 font-semibold mb-2">Quantity (in kg):</label>
                <input type="number" id="quantity" name="quantity" step="0.01" required class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
            </div>
            <button type="submit" class="w-full bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 shadow-lg">
                Analyze
            </button>
        </form>
    </div>
    {% if history %}
    <div class="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
        <h2 class="text-2xl font-bold text-gray-800 mb-4 text-center">Previous Analyses</h2>
        <ul class="space-y-4">
            {% for entry in history %}
            <li class="p-4 bg-gray-50 rounded-lg shadow-inner flex justify-between items-center">
                <div>
                    <p class="font-bold text-lg">{{ entry.material_name }} ({{ entry.quantity }} kg)</p>
                    <p class="text-sm text-gray-600">Score: <span class="font-semibold">{{ entry.overall_score }}</span></p>
                </div>
                <div class="rounded-full h-8 w-8 text-white font-bold flex items-center justify-center 
                            {% if entry.overall_score > 80 %} bg-green-600
                            {% elif entry.overall_score > 60 %} bg-yellow-600
                            {% else %} bg-red-600 {% endif %}">
                    {{ entry.overall_score }}
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
</body>
</html>
"""

results_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LCA Results</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .score-good { background-color: #d1fae5; color: #065f46; }
        .score-medium { background-color: #fffbe6; color: #b45309; }
        .score-bad { background-color: #fee2e2; color: #991b1b; }
    </style>
</head>
<body class="bg-gray-100 min-h-screen p-4 flex flex-col items-center">
    <div class="bg-white rounded-2xl shadow-xl p-8 mt-8 max-w-4xl w-full">
        <div class="text-center mb-8">
            <h1 class="text-4xl font-extrabold text-gray-800 mb-2">LCA Results for {{ material_name }}</h1>
            <p class="text-xl text-gray-600">Analyzing <strong>{{ quantity }} kg</strong> of material</p>
        </div>

        <!-- High-Level Sustainability Scorecard -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-4 text-center">Sustainability Scorecard</h2>
            <div class="p-6 rounded-lg text-center shadow-md {{ overall_score_class }}">
                <p class="text-7xl font-bold">{{ overall_score }}</p>
                <p class="text-xl font-semibold mt-2">Overall LCA Score</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4 text-center">
                <div class="p-4 rounded-lg score-medium shadow-md">
                    <p class="font-bold text-2xl">{{ carbon }}</p>
                    <p class="text-sm">Carbon Footprint (kg CO2e)</p>
                </div>
                <div class="p-4 rounded-lg score-medium shadow-md">
                    <p class="font-bold text-2xl">{{ water }}</p>
                    <p class="text-sm">Water Usage (m³)</p>
                </div>
                <div class="p-4 rounded-lg score-medium shadow-md">
                    <p class="font-bold text-2xl">{{ energy }}</p>
                    <p class="text-sm">Energy (kWh)</p>
                </div>
            </div>
        </div>

        <!-- Life Cycle Stage Breakdown -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-4 text-center">Life Cycle Stage Breakdown</h2>
            <canvas id="lifecycleChart"></canvas>
            <p class="text-center text-sm text-gray-500 mt-2">
                <strong>Hotspot Identified:</strong> {{ hotspot_stage }} has the highest impact.
            </p>
        </div>

        <!-- Comparison and Scenario Analysis -->
        <div class="mb-8">
            <h2 class="text-2xl font-bold text-gray-800 mb-4 text-center">Comparison & What-If Scenario</h2>
            <div class="bg-blue-50 border-l-4 border-blue-500 rounded-lg p-6 shadow-md">
                <p class="text-lg text-blue-800 font-semibold">
                    <strong>Insight:</strong> Your choice of material significantly impacts sustainability. Switching to a recycled material would improve the LCA score from
                    <span class="font-bold">~{{ virgin_score }}</span> to <span class="font-bold">~{{ recycled_score }}</span>, representing a huge step towards a circular economy.
                </p>
            </div>
        </div>
        
        <div class="text-center mt-8">
            <a href="/" class="inline-block bg-gray-300 text-gray-800 font-bold py-3 px-6 rounded-full hover:bg-gray-400">
                Run a New Analysis
            </a>
        </div>
    </div>
    
    <script>
        const ctx = document.getElementById('lifecycleChart').getContext('2d');
        const lifecycleChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Raw Material Extraction', 'Manufacturing & Processing', 'Transportation', 'End-of-Life'],
                datasets: [{
                    label: 'Impact by Stage (%)',
                    data: [{{ lifecycle_data['Raw Material Extraction'] }}, {{ lifecycle_data['Manufacturing & Processing'] }}, {{ lifecycle_data['Transportation'] }}, {{ lifecycle_data['End-of-Life'] }}],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)', 
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            material = request.form['material']
            quantity = float(request.form['quantity'])

            material_data = data.get(material)
            if material_data is None:
                return "Error: Material not found.", 404

            # --- Simplified Logic for Scorecard ---
            carbon_footprint = material_data['carbon'] * quantity
            water_usage = material_data['water'] * quantity
            energy_consumption = material_data['energy'] * quantity
            overall_score = material_data['score']

            if overall_score > 80:
                overall_score_class = "score-good"
            elif overall_score > 60:
                overall_score_class = "score-medium"
            else:
                overall_score_class = "score-bad"

            # --- Simplified Logic for Lifecycle and Scenario ---
            material_type = 'recycled' if 'recycled' in material else 'virgin'
            lifecycle_data = lifecycle_impacts[material_type]

            # Find the hotspot stage
            hotspot_stage = max(lifecycle_data, key=lifecycle_data.get)

            # Simplified scenario for comparison
            opposite_material = material.replace(
                'virgin', 'recycled') if 'virgin' in material else material.replace('recycled', 'virgin')
            virgin_score = data[opposite_material.replace(
                'recycled', 'virgin')]['score']
            recycled_score = data[opposite_material.replace(
                'virgin', 'recycled')]['score']

            # Save the current analysis to history
            history.append({
                'material_name': material.replace('_', ' ').title(),
                'quantity': quantity,
                'overall_score': overall_score,
            })

            return render_template_string(
                results_page_html,
                material_name=material.replace('_', ' ').title(),
                quantity=quantity,
                carbon=f"{carbon_footprint:.2f}",
                water=f"{water_usage:.2f}",
                energy=f"{energy_consumption:.2f}",
                overall_score=overall_score,
                overall_score_class=overall_score_class,
                lifecycle_data=lifecycle_data,
                hotspot_stage=hotspot_stage,
                virgin_score=virgin_score,
                recycled_score=recycled_score,
            )
        except Exception as e:
            return f"An error occurred: {e}", 500

    materials_for_dropdown = [
        {'id': k, 'name': k.replace('_', ' ').title()} for k in data.keys()]
    return render_template_string(input_form_html, materials=materials_for_dropdown, history=history)


if __name__ == '__main__':
    app.run(debug=True)
