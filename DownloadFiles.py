from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

api.dataset_download_files('sahityasetu/ufo-sightings', path='./', unzip=True)