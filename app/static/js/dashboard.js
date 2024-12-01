// app/static/js/dashboard.js

const parameterInfo = {
  dimensions: {
      label: "Dimensions",
      description: "Think of this as the number of directions strings can move in. While we see 4 dimensions (up/down, left/right, forward/back, and time), strings need more! The extra dimensions are curled up super tiny. 10D is special for superstrings.",
      min: 4,
      max: 26
  },
  tension: {
      label: "String Tension (T)",
      description: "Just like a guitar string, this is how 'tight' our strings are! Higher tension means they vibrate with more energy, like tightening a guitar string makes higher notes. This scales all excited states by √T.",
      min: 0.000001,
      max: 1000000
  },
  coupling: {
      label: "Coupling Constant (g)",
      description: "How strongly strings interact with each other, like the strength of magnets. A smaller number means weaker interactions. We keep this small because it makes our calculations work better!",
      min: 0.000001,
      max: 1
  },
  alpha_prime: {
      label: "α' (Alpha Prime)",
      description: "This sets how big our strings are! It's like a conversion between energy and length. Smaller α' means shorter strings and higher energies. The mass formula uses this as M² = n/α'.",
      min: 0.000001,
      max: 100
  }
};

function createParameterControls() {
  const container = document.createElement('div');
  container.className = 'bg-white rounded-lg shadow p-6 mb-8';
  container.innerHTML = `
      <h2 class="text-2xl font-bold mb-4">String Theory Parameters</h2>
      <p class="text-gray-600 mb-6">Adjust these values to explore how they affect the string spectrum!</p>
  `;

  for (const [key, info] of Object.entries(parameterInfo)) {
      const controlGroup = document.createElement('div');
      controlGroup.className = 'mb-6';
      controlGroup.innerHTML = `
          <div class="flex justify-between items-center mb-2">
              <label for="${key}" class="font-medium text-gray-700">${info.label}</label>
              <input type="number" 
                     id="${key}" 
                     min="${info.min}" 
                     max="${info.max}" 
                     step="${key === 'dimensions' ? '1' : 'any'}"
                     class="border rounded px-3 py-2 w-32 text-right">
          </div>
          <div class="bg-blue-50 p-4 rounded-lg">
              <p class="text-sm text-blue-800">${info.description}</p>
              <p class="text-xs text-blue-600 mt-2">Valid range: ${info.min} to ${info.max}</p>
          </div>
      `;
      container.appendChild(controlGroup);
  }

  // Insert before the mass spectrum div
  const massSpectrumDiv = document.getElementById('massSpectrum');
  massSpectrumDiv.parentElement.insertBefore(container, massSpectrumDiv);
}

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

function updateMassSpectrum(spectrum) {
  // Main spectrum trace
  const mainTrace = {
      x: Array.from({length: spectrum.length}, (_, i) => i),
      y: spectrum,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'Mass Levels',
      line: {
          color: '#4299e1',
          width: 2
      },
      marker: {
          size: 8,
          color: '#2a4365'
      }
  };
  
  // Calculate degeneracy (number of states) at each level
  const degeneracy = spectrum.map((_, i) => {
      if (i === 0) return 1;  // Ground state
      // Higher states have more possible configurations
      return i * Math.pow(2, Math.min(i, 3));  // Simplified degeneracy
  });

  // Degeneracy trace
  const degTrace = {
      x: Array.from({length: spectrum.length}, (_, i) => i),
      y: degeneracy,
      yaxis: 'y2',
      type: 'bar',
      name: 'States per Level',
      marker: {
          color: 'rgba(66, 153, 225, 0.2)'
      },
      hovertemplate: '%{y} possible states<extra></extra>'
  };

  const layout = {
      title: 'String Mass Spectrum with State Counting',
      xaxis: {
          title: 'Energy Level (n)',
          gridcolor: 'rgba(0,0,0,0.1)'
      },
      yaxis: {
          title: 'Mass (M)',
          titlefont: {color: '#2a4365'},
          tickfont: {color: '#2a4365'},
          gridcolor: 'rgba(0,0,0,0.1)'
      },
      yaxis2: {
          title: 'Number of States',
          titlefont: {color: '#4299e1'},
          tickfont: {color: '#4299e1'},
          overlaying: 'y',
          side: 'right',
          showgrid: false
      },
      paper_bgcolor: 'rgba(0,0,0,0)',
      plot_bgcolor: 'rgba(0,0,0,0)',
      font: {
          family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
      },
      showlegend: true,
      legend: {
          x: 0,
          y: 1.2
      }
  };

  Plotly.newPlot('massSpectrum', [mainTrace, degTrace], layout);
}

function updateInputs(data) {
  Object.keys(parameterInfo).forEach(key => {
      const input = document.getElementById(key);
      if (input && data[key] !== undefined) {
          input.value = data[key];
      }
  });
}

function updateStateDisplay(data) {
  const display = document.getElementById('stateDisplay');
  display.textContent = JSON.stringify(data, null, 2);
}

async function updateSystem() {
  const params = {};
  Object.keys(parameterInfo).forEach(key => {
      const input = document.getElementById(key);
      if (input) {
          const value = input.type === 'number' ? parseFloat(input.value) : input.value;
          params[key] = value;
      }
  });

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

function addEventListeners() {
  Object.keys(parameterInfo).forEach(key => {
      const input = document.getElementById(key);
      if (input) {
          input.addEventListener('change', updateSystem);
      }
  });
}

function initDashboard() {
  createParameterControls();
  updateDisplay();
  addEventListeners();
  setInterval(updateDisplay, 5000);
}

document.addEventListener('DOMContentLoaded', initDashboard);