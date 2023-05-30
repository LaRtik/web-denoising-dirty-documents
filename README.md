# Denoising dirty documents with web interface (OCR ML model)

Optical Character Recognition (OCR) is the process of getting type or handwritten documents into a digitized format.

This OCR-model uses denoising autoencoder. Model training time: +-50 minutes.

## How to run?
(it's recommended to use virtual environment)
```bash
git clone https://github.com/LaRtik/web-denoising-dirty-documents/
cd /web-denoising-dirty-documents

# optional venv creating and activating

pip install -r requirements.txt
python3 manage.py runserver
```

### The Django-app uses standart sqlite database, so there is no need to deal with such things as psycorpg and etc.
