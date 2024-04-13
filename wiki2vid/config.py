from wiki2vid.prompts import Prompts

# Input
FOLDER = "output"
# AI Models
LLM_MODEL = "gpt-3.5-turbo"  # gpt-4-0125-preview, gpt-3.5-turbo
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
    llm_model = LLM_MODEL
    interactive = INTERACTIVE
    save_intermediate = SAVE_INTERMEDIATE
    num_feedbacks = NUM_FEEDBACKS
    verbosity = VERBOSITY
    timeout_scalar = TIMEOUT_SCALAR
    prompts = Prompts
