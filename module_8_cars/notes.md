Attempts to run on local GPU

pip install plaidml-keras plaidbench
plaidml-setup
plaidbench keras mobilenet
import os; os.environ['KERAS_BACKEND'] = 'plaidml.keras.backend'