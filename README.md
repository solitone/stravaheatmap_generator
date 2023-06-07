# StravaHeatmap Generator

## Introduction

StravaHeatmap Generator is a web application that creates map definition files or URLs to visualize Strava Heatmaps in cartographic applications. 

Currently, StravaHeatmap Generator primarily supports the creation of map definition files for Cartograph Maps. However, we aim to expand our support to more platforms and services in the future.

## Features

- Generation of map definition files for Cartograph Maps application
- Interactive interface to choose preferences for Heatmap generation

## Getting Started

### Prerequisites

To run StravaHeatmap Generator locally, you need the following:

- Python 3
- Flask
- Flask-Babel

### Installation

1. Clone the repository:

```shell
git clone https://github.com/<your_username>/stravaheatmap_generator.git
```

2. Install the required Python packages:
```shell
pip install -r requirements.txt
```

3. Create a `stravalogin.py` file in the app root directory with the following variables defined:
```python
STRAVA_USR = "<YOUR_STRAVA_USERNAME>"
STRAVA_PWD = "<YOUR_STRAVA_PASSWORD>"
```
4. Run the application:
```shell
python app.py
```
The application will start running on `localhost:5555`.

## Usage

Once the application is running, you can use it to generate Strava Heatmaps for the Cartograph Maps application. Select your preferences, submit the form, and a map definition file will be created and made available for download.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details.
