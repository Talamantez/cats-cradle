// app/static/js/dashboard.js

// Initialize the dashboard
async function initDashboard() {
    await updateDisplay();
    setInterval(updateDisplay, 5000); // Update every 5 seconds
}

// Fetch and display current system state
async function updateDisplay() {
    try {
        const response = await fetch('/api/v1/string-theory/');
        const data = await response.json();
        
        if (data.status === 'success') {
            updateInputs(data.data);
            updateMassSpectrum(data.data.mass_spectrum);
            updateStateDisplay(data.data);
        }
    } catch (error) {
        console.error('Error fetching system state:', error);
    }
}

// Update the mass spectrum visualization
function updateMassSpectrum(spectrum) {
    const trace = {
        x: Array.from({length: spectrum.length}, (_, i) => i),
        y: spectrum,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Mass Spectrum',
        line: {
            color: '#4299e1',
            width: 2
        },
        marker: {
            size: 8,
            color: '#2a4365'
        }
    };

    const layout = {
        title: 'String Mass Spectrum',
        xaxis: {
            title: 'Energy Level'
        },
        yaxis: {
            title: 'Mass (M)'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: {
            family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
        }
    };

    Plotly.newPlot('massSpectrum', [trace], layout);
}

// Update input fields with current values
function updateInputs(data) {
    document.getElementById('dimensions').value = data.dimensions;
    document.getElementById('tension').value = data.tension;
    document.getElementById('coupling').value = data.coupling;
    document.getElementById('alpha_prime').value = data.alpha_prime;
}

// Update the state display
function updateStateDisplay(data) {
    const display = document.getElementById('stateDisplay');
    display.textContent = JSON.stringify(data, null, 2);
}

// Send updated parameters to the server
async function updateSystem() {
    const params = {
        dimensions: parseInt(document.getElementById('dimensions').value),
        tension: parseFloat(document.getElementById('tension').value),
        coupling: parseFloat(document.getElementById('coupling').value),
        alpha_prime: parseFloat(document.getElementById('alpha_prime').value)
    };

    try {
        const response = await fetch('/api/v1/string-theory/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            updateMassSpectrum(data.data.mass_spectrum);
            updateStateDisplay(data.data);
        }
    } catch (error) {
        console.error('Error updating system:', error);
    }
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', initDashboard);