# Song Recommender System

## Project Overview
A sophisticated song recommendation system that leverages machine learning to suggest songs based on user preferences and compatibility analysis.

## Features
- Song recommendation using advanced ML algorithms
- Compatibility checker for music preferences
- Web application interface for easy interaction

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/song-recommeneder-system.git
cd song-recommeneder-system/ML\ Project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
python app.py
```

## Project Structure
- `app.py`: Main web application
- `song_recommender.py`: Core recommendation logic
- `train_model.py`: Model training script
- `evaluate.py`: Model evaluation script
- `spotify_utils.py`: Utility functions for Spotify data
- `models/`: Directory containing trained models
- `Dataset Creation.ipynb`: Notebook for dataset preparation
- `EDA.ipynb`: Exploratory Data Analysis notebook

## Technologies Used
- Python
- Flask
- Scikit-learn
- Pandas
- Spotify API

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.
