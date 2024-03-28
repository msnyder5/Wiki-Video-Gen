from wiki2vid.prompts import Prompts

# Input
FOLDER = "output/trainsurfing"
# Settings
INTERACTIVE = False
SAVE_INTERMEDIATE = True
NUM_FEEDBACKS = 1
# Debugging
VERBOSITY = 2
TIMEOUT_SCALAR = 0.0
# Config storage classes


class Config:
    folder = FOLDER
    interactive = INTERACTIVE
    save_intermediate = SAVE_INTERMEDIATE
    num_feedbacks = NUM_FEEDBACKS
    verbosity = VERBOSITY
    timeout_scalar = TIMEOUT_SCALAR
    prompts = Prompts
