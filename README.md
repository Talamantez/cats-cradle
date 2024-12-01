# Cats Cradle - String Theory Dashboard

Cats Cradle is a web application that provides a dashboard for visualizing and interacting with a string theory simulation. Users can view the current state of the system, update various parameters, and observe the changes in the mass spectrum.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [License](#license)

## Installation

To set up the Cats Cradle app, follow these steps:

1. Clone the repository:
git clone https://github.com/talamantez/cats-cradle.git

2. Navigate to the project directory:
cd cats-cradle

3. Create a virtual environment and activate it:
python -m venv venv

4. Install the required dependencies:
pip install -r requirements.txt

5. Start the development server:
uvicorn app.main:app --reload

6. Open your web browser and navigate to `http://localhost:8000`.

## Usage

The Cats Cradle app provides a user interface for interacting with the string theory simulation. Users can:

1. View the current state of the system, including the dimensions, tension, coupling, alpha prime, and compactification parameters.
2. Observe the mass spectrum visualization, which updates in real-time as the system parameters change.
3. Modify the system parameters by updating the input fields and clicking the "Update" button.
4. Monitor the state changes and mass spectrum updates in the state display.

## API Endpoints

The app exposes the following API endpoints:

- `GET /api/v1/string-theory/`: Retrieves the current state of the string theory system.
- `POST /api/v1/string-theory/update`: Updates the parameters of the string theory system.

## Development

If you want to contribute to the development of the Cats Cradle app, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
git checkout -b feature/my-feature

3. Make your changes and ensure that the tests pass:
pytest

4. Commit your changes and push to your forked repository.
5. Create a pull request against the main repository.

## Contributing

We welcome contributions to the Cats Cradle project. If you find any issues or have ideas for improvements, please open an issue on the [GitHub repository](https://github.com/talamantez/cats-cradle/issues).

## Changelog

### Version 1.0.0 (2024-11-30)
- Initial release of the Cats Cradle app
- Implemented the string theory simulation and dashboard
- Added API endpoints for retrieving and updating system parameters
- Included a mass spectrum visualization
- Set up the development and testing environment

## License

This project is licensed under the [MIT License](LICENSE).
