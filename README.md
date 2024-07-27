# TraxFish

🐡 Comment "ID?" on DJ mixes no more 😎

The application is deployed on [Streamlit](https://traxfish.streamlit.app/)

## Development

1. Install Python modules:
    ```bash
    pip install -r requirements.txt
    ```
2. Create secrets for Shazam API:
    - Create a directory called `.streamlit`
    - Create a file called `secrets.toml`
    - Enter your `api_key` in the following format in `secrets.toml` file:
    ```bash
    api_key = "<your-api-key>"
    ```
3. Start local Streamlit app:
    ```bash
    make app
    ```

## App structure

```bash
.
├── Makefile
├── README.md
├── app.py
├── components
│   ├── __init__.py
│   ├── intro.py
│   ├── track_form.py
│   └── track_list.py
├── index.py
├── packages.txt
├── requirements.txt
├── tracks_exceptions
│   ├── InvalidUrlException.py
│   ├── NoSourceException.py
│   ├── TooManySourceException.py
│   └── __init.py__
└── utils
    ├── __init__.py
    ├── audio_processing.py
    └── querier.py
```

### `components`
- Streamlit UI components
#### `intro`
Intro text
#### `track_form`
Components to let user upload, paste links and select scan frequency
#### `track_list`
Render tracklist as a table

### `utils`
#### `querier`
- Validates user input files and URLs
- Queries `audio_processing` based on user's track source

#### `audio_processing`
Main worker that processes uploaded files and queries shazam api