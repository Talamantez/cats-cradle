# Cat's Cradle - String Theory Explorer

Cat's Cradle is a Mass Spectrum Equation simulator for various topologies in the form of a web application that provides a dashboard for visualizing and interacting with the string theory simulation. Users can view the current state of the system, update various parameters, and observe the changes in the mass spectrum.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/talamantez/cats-cradle.git
cd cats-cradle
```

2. Start the application:
```bash
docker compose up -d
```

3. Open your web browser and navigate to `http://localhost:8000`

To stop the application:
```bash
docker compose down
```

## Features

The Cat's Cradle dashboard provides:

- Interactive parameter controls for string theory simulation
  - Dimensions (4-26)
  - String Tension
  - Coupling Constant
  - α' (Alpha Prime)
  - Compare Topologies:
      TOPOLOGY_FACTORS = {
        "Calabi-Yau": 1.0,  # Standard case
        "Torus": 0.8,       # Simpler topology
        "Orbifold": 1.2,    # More complex spectrum
        "K3": 1.5           # Rich structure with supersymmetry
    }
- Real-time mass spectrum visualization
- Live system state monitoring
- Automatic parameter validation
- Beautiful, responsive interface

## API Endpoints

The app exposes the following API endpoints:

- `GET /api/v1/string-theory/`: Retrieves the current state of the string theory system
- `POST /api/v1/string-theory/update`: Updates the parameters of the string theory system
- Swagger UI documentation available at `/docs`
- ReDoc documentation available at `/redoc`

## Development

### Local Development with Docker

1. Make changes to the code
2. Rebuild and restart the containers:
```bash
docker compose down
docker compose up -d --build
```

### Running Tests
```bash
docker compose run --rm api pytest
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Physics Background

This simulation implements basic string theory concepts:

- The dimensions parameter (default: 10) matches superstring theory's required spacetime dimensions
- String tension and coupling parameters control string interactions
- Alpha prime (α') determines the characteristic string length scale
- Mass spectrum follows the relationship M² = n/α'
- Topology:  The study of the fundamental shape and connectivity of spacetime
