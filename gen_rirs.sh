"""Automatically generate 'room impulse responses' based on the parameters given in config/config.py or a custom config file 
"""

# RIR files
python ./RIR_parameter.py | parallel --colsep ' ' python ./RIR_write_quaternion.py
