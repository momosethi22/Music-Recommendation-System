# Music Recommendation System 

## Overview

This Music Recommendation System leverages a large dataset of 30-second Spotify MP3 tracks, combining audio feature extraction and machine learning to provide personalized music recommendations. This system was built with a Flask backend and a dynamic frontend, allowing users to interactively discover music based on their preferences.

## Dataset

The dataset includes a vast collection of Spotify tracks, each clip lasting 30 seconds. We preprocessed this dataset to extract key audio features essential for music analysis:

- **MFCC (Mel Frequency Cepstral Coefficients):** Captures the timbral aspects of the audio.
- **ZCR (Zero Crossing Rate):** Measures the rate at which the signal changes from positive to negative or back.
- **Spectral Centroid:** Indicates where the center of mass of the spectrum is located.

File names were simplified by removing leading zeros. All data, including extracted features and track details, were stored in MongoDB using track IDs for efficient retrieval.

## Metadata Integration

We utilized `fma_metadata` to enrich our dataset with additional information such as track names and artist details. This metadata was extracted from various CSV files and integrated into MongoDB, aligning with the corresponding track IDs. This enrichment facilitates a richer user experience by allowing users to view detailed track and artist information alongside recommendations.

## Model Training

Initial attempts to train the recommendation model using Apache Spark were hindered by issues with the MongoDB Spark connector. Consequently, we adapted our approach to employ K-means clustering based on genre ID and MFCC features. This method proved effective for segmenting the dataset into distinct musical genres, which serve as the basis for our recommendation logic.

## System Architecture

### Backend

The backend of the system is built using Flask. It handles:
- Serving the frontend
- Managing database operations
- Processing play events to generate and update music recommendations

### Frontend

The frontend is an interactive web interface where users can:
- Play music tracks
- View current playing tracks
- Receive recommendations dynamically based on their listening history

Whenever a user plays a track, the system automatically updates to show recommended tracks based on the clustering model's output.

## Usage

To use the Music Recommendation System, follow these steps:

1. **Start the Backend Server:**
   - Navigate to the system directory.
   - Run `python app.py` to start the Flask server.

2. **Access the Frontend:**
   - Open a web browser.
   - Visit localhost to access the music streaming interface.

3. **Play and Explore:**
   - Click on any track to start playing.
   - Explore the dynamically updated recommendations based on your choices.

## Future Enhancements

Future improvements might include:
- Enhancing the recommendation algorithm by incorporating more complex machine learning models.
- Increasing the dataset size and variety for broader music coverage.
- Optimizing the system's performance and scalability by resolving integration issues with Apache Spark.

## Conclusion

This Music Recommendation System offers a user-friendly platform for music discovery based on sophisticated audio analysis and machine learning techniques. It provides a personalized listening experience by recommending tracks that align with users' musical preferences.
