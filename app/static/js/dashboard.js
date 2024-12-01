// app/static/js/dashboard.js

const parameterInfo = {
    dimensions: {
        label: "Dimensions",
        description: "Think of this as the number of directions strings can move in. While we see 4 dimensions (up/down, left/right, forward/back, and time), strings need more! The extra dimensions are curled up super tiny. 10D is special for superstrings.",
        min: 4,
        max: 26,
        type: "number"
    },
    tension: {
        label: "String Tension (T)",
        description: "Just like a guitar string, this is how 'tight' our strings are! Higher tension means they vibrate with more energy, like tightening a guitar string makes higher notes. This scales all excited states by √T.",
        min: 0.000001,
        max: 1000000,
        type: "number"
    },
    coupling: {
        label: "Coupling Constant (g)",
        description: "How strongly strings interact with each other, like the strength of magnets. A smaller number means weaker interactions. We keep this small because it makes our calculations work better!",
        min: 0.000001,
        max: 1,
        type: "number"
    },
    alpha_prime: {
        label: "α' (Alpha Prime)",
        description: "This sets how big our strings are! It's like a conversion between energy and length. Smaller α' means shorter strings and higher energies. The mass formula uses this as M² = n/α'.",
        min: 0.000001,
        max: 100,
        type: "number"
    },
    topology: {
        label: "Topology",
        description: "The shape of the curled-up extra dimensions. Different topologies affect how strings can vibrate and interact:",
        type: "select",
        options: {
            "Calabi-Yau": "The standard choice for superstring theory - preserves supersymmetry",
            "Torus": "Simple 'donut-like' shape - easier to understand but less realistic",
            "Orbifold": "Like a folded space - introduces interesting symmetries",
            "K3": "A special 4D space important for string dualities"
        }
    }
};

function createControlElement(key, info) {
    const controlGroup = document.createElement('div');
    controlGroup.className = 'mb-6';

    const labelDiv = document.createElement('div');
    labelDiv.className = 'flex justify-between items-center mb-2';

    const label = document.createElement('label');
    label.htmlFor = key;
    label.className = 'font-medium text-gray-700';
    label.textContent = info.label;

    labelDiv.appendChild(label);

    let input;
    if (info.type === 'select') {
        input = document.createElement('select');
        input.id = key;
        input.className = 'border rounded px-3 py-2 w-48';
        Object.keys(info.options).forEach(optionKey => {
            const option = document.createElement('option');
            option.value = optionKey;
            option.textContent = optionKey;
            input.appendChild(option);
        });
    } else {
        input = document.createElement('input');
        input.type = 'number';
        input.id = key;
        input.min = info.min;
        input.max = info.max;
        input.step = key === 'dimensions' ? '1' : 'any';
        input.className = 'border rounded px-3 py-2 w-32 text-right';
    }

    labelDiv.appendChild(input);
    controlGroup.appendChild(labelDiv);

    const description = document.createElement('div');
    description.className = 'bg-blue-50 p-4 rounded-lg';

    if (info.type === 'select') {
        const topologyDesc = document.createElement('p');
        topologyDesc.id = `${key}-description`;
        topologyDesc.className = 'text-sm text-blue-800 mb-2';
        description.appendChild(topologyDesc);

        input.addEventListener('change', () => {
            topologyDesc.textContent = info.options[input.value];
        });
        setTimeout(() => {
            topologyDesc.textContent = info.options[input.value];
        }, 0);
    }

    const descText = document.createElement('p');
    descText.className = 'text-sm text-blue-800';
    descText.textContent = info.description;
    description.appendChild(descText);

    if (info.type === 'number') {
        const range = document.createElement('p');
        range.className = 'text-xs text-blue-600 mt-2';
        range.textContent = `Valid range: ${info.min} to ${info.max}`;
        description.appendChild(range);
    }

    controlGroup.appendChild(description);
    return controlGroup;
}

function createParameterControls() {
    const container = document.createElement('div');
    container.className = 'bg-white rounded-lg shadow p-6 mb-8';
    container.innerHTML = `
        <h2 class="text-2xl font-bold mb-4">String Theory Parameters</h2>
        <p class="text-gray-600 mb-6">Adjust these values to explore how they affect the string spectrum!</p>
    `;

    for (const [key, info] of Object.entries(parameterInfo)) {
        const controlElement = createControlElement(key, info);
        container.appendChild(controlElement);
    }

    const massSpectrumDiv = document.getElementById('massSpectrum');
    massSpectrumDiv.parentElement.insertBefore(container, massSpectrumDiv);
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

    // Calculate fixed y-axis ranges based on the current spectrum
    const maxMass = Math.max(...spectrum) * 1.1; // Add 10% padding
    const maxDegeneracy = Math.max(...degeneracy) * 1.1;

    const layout = {
        title: 'String Mass Spectrum with State Counting',
        height: 600, // Set a larger height
        width: window.innerWidth * 0.9, // Make it responsive but not full width
        xaxis: {
            title: 'Energy Level (n)',
            gridcolor: 'rgba(0,0,0,0.1)',
            range: [-0.5, spectrum.length - 0.5] // Fix x-axis range
        },
        yaxis: {
            title: 'Mass (M)',
            titlefont: {color: '#2a4365'},
            tickfont: {color: '#2a4365'},
            gridcolor: 'rgba(0,0,0,0.1)',
            range: [0, maxMass], // Fix primary y-axis range
            fixedrange: true // Prevent zooming/panning
        },
        yaxis2: {
            title: 'Number of States',
            titlefont: {color: '#4299e1'},
            tickfont: {color: '#4299e1'},
            overlaying: 'y',
            side: 'right',
            showgrid: false,
            range: [0, maxDegeneracy], // Fix secondary y-axis range
            fixedrange: true // Prevent zooming/panning
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
        },
        // Add margin to prevent cutting off
        margin: {
            l: 80,  // Increased left margin for axis labels
            r: 80,  // Increased right margin for secondary axis
            t: 100, // More space for title
            b: 80   // More space for x-axis labels
        }
    };

    Plotly.newPlot('massSpectrum', [mainTrace, degTrace], layout, {
        displayModeBar: false, // Hide the modebar
        responsive: true // Make the plot responsive
    });
}

function updateDisplay() {
    return new Promise(async (resolve, reject) => {
        try {
            const response = await fetch('/api/v1/string-theory/');
            const data = await response.json();
            
            if (data.status === 'success') {
                // Update numeric inputs and state display
                Object.keys(parameterInfo).forEach(key => {
                    const input = document.getElementById(key);
                    if (input && parameterInfo[key].type === 'number' && data[key] !== undefined) {
                        input.value = data[key];
                    }
                });
                
                // Update topology only if it's shown in the UI
                const topologyInput = document.getElementById('topology');
                if (topologyInput && data.compactification && 
                    topologyInput.value !== data.compactification.topology) {
                    topologyInput.value = data.compactification.topology;
                    const desc = document.getElementById('topology-description');
                    if (desc) {
                        desc.textContent = parameterInfo.topology.options[data.compactification.topology];
                    }
                }

                updateMassSpectrum(data.data.mass_spectrum);
                updateStateDisplay(data.data);
            }
            resolve();
        } catch (error) {
            console.error('Error fetching system state:', error);
            reject(error);
        }
    });
}

function updateInputs(data) {
    Object.keys(parameterInfo).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            if (key === 'topology' && data.compactification) {
                input.value = data.compactification.topology;
                const desc = document.getElementById(`${key}-description`);
                if (desc) {
                    desc.textContent = parameterInfo[key].options[data.compactification.topology];
                }
            } else if (data[key] !== undefined) {
                input.value = data[key];
            }
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
        if (input && input.value) {
            if (input.type === 'number') {
                params[key] = parseFloat(input.value);
            } else if (parameterInfo[key].type === 'select') {
                params[key] = input.value;
            }
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

let lastUpdateTime = 0;
const UPDATE_INTERVAL = 2000;  // 2 seconds

function addEventListeners() {
    Object.keys(parameterInfo).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            if (parameterInfo[key].type === 'select') {
                input.addEventListener('change', async () => {
                    lastUpdateTime = Date.now();
                    await updateSystem();
                });
            } else {
                input.addEventListener('change', updateSystem);
            }
        }
    });
}

function initDashboard() {
    createParameterControls();
    updateDisplay();
    addEventListeners();
    
    // Periodic updates that respect manual changes
    setInterval(async () => {
        const timeSinceLastUpdate = Date.now() - lastUpdateTime;
        if (timeSinceLastUpdate >= UPDATE_INTERVAL) {
            await updateDisplay();
        }
    }, UPDATE_INTERVAL);
}

document.addEventListener('DOMContentLoaded', initDashboard);