import yaml

with open(r'/Users/adam/src/cardfinder/config.yaml') as yaml_file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)


TWILIO_SID = config_data.get('twilio_sid')
TWILIO_TOKEN = config_data.get('twilio_token')
TWILIO_NUMBER = config_data.get('twilio_number')

TARGET_NUMBERS = config_data.get('target_numbers')