import sys
from pathlib import Path


# Backend Settings
host = '0.0.0.0'
port = '5000'

# Root Path
root_path = Path(__file__).parents[0].resolve()
sys.path.append(str(root_path))

# Demo Images Path
demo_path = root_path.joinpath('demo')

# Trained Weights Path
weights_path = root_path.joinpath('weights')

# Model Devices
crowd_counter_device = 0
fire_detector_device = 0
vad_detector_device = 0
