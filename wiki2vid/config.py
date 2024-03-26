# Input
FOLDER = "intermediate"
# Settings
INTERACTIVE = False
SAVE_INTERMEDIATE = True
# Debugging
VERBOSITY = 5
TIMEOUT_SCALAR = 1.0
# Prompts
OUTLINE_BRAINSTORM = """
You are a creative writer who has been tasked with creating a script for a video about a provided topic. \
You will be given a Wiki article to use as a reference, and your goal is to create an engaging and informative video that will captivate your audience. \
The first step in this process is to create an outline for your script. \
This outline will serve as a roadmap for your video, helping you to organize your thoughts and ensure that you cover all of the key points. \
To get started, take a look at the Wiki article provided and begin brainstorming ideas for your outline. \
What are the main topics that you want to cover in your video? \
What are the key points that you want to make? \
What order should these topics be presented in? \
This first step is a high level brainstorming session that we will then use to create a more defined outline.
""".strip()
OUTLINE_WRITE = """
Now that you have brainstormed some ideas for your script, it's time to create an outline. \
An outline is a structured plan that organizes your ideas and helps you to create a cohesive and engaging script. \
Your outline should include an introduction, body, and conclusion, with each section broken down into key points and subpoints. \
Think about the main topics that you want to cover in your video and how you can organize them in a logical and engaging way. \
Consider the flow of your script and how you can transition smoothly between topics. \
Once you have created your outline, you will be ready to start writing your script.

**Formatting Guidelines**

Use markdown to format your outline. \
Use headers to indicate the main sections of your outline (e.g., # Introduction, # Weapon Statistics, # Conclusion). \
Use bullet points to list key points and subpoints within each section. \
Use bold or italic text to highlight important information or key ideas.

IT IS OF UTMOST IMPORTANCE THAT YOU FOLLOW THE FORMATTING GUIDELINES. \
IF YOU DO NOT, THE OUTLINER WILL NOT BE ABLE TO PARSE YOUR OUTLINE. \
THIS ALSO MEANS THAT YOU MUST ONLY RETURN THE OUTLINE IN MARKDOWN FORMAT. \
DO NOT INCLUDE ANY OTHER INFORMATION IN YOUR RESPONSE, SUCH AS AN ACKNOWLEDGEMENT, THANK YOU MESSAGE, OR NEXT STEPS.

Example:

# Introduction

- Introduce Rampart, a Controller Legend in Apex Legends
- Mention her abilities and background as a modder with a love for LMGs
- Highlight her unique playstyle focused on securing areas through firepower

# Rampart's Abilities

## Amped Cover

- Description and mechanics of the tactical ability
- Tips for effective use and interactions with other legends

## Modded Loader

- Passive ability details and benefits with LMGs
- Tips for maximizing its potential and interactions with other upgrades

## Mobile Minigun "Sheila"

- Ultimate ability overview and usage
- Strategies for using Sheila effectively and interactions with the environment

# Lore and Background

- Provide background information on Rampart's real name, age, and home world
- Discuss Rampart's story, including her rise from the gauntlet circuit to becoming an Apex Legend
- Explore her motivations and the significance of the Apex card in her journey

# Cosmetic Items

- Showcase Rampart's skins, finishers, heirloom set, badges, emotes, and banner frames
- Highlight unique cosmetic items and their availability in the game

# Teasers and Trivia

- Discuss the teasers leading up to Rampart's release, including voice messages and in-game graffiti
- Share interesting trivia about Rampart, such as her abilities inspired by Titanfall 2 and early concept designs

# Patch Notes and Updates

- Summarize key updates and changes to Rampart's abilities over time
- Highlight significant balance adjustments and bug fixes in her kit

# Gallery

- Showcase videos and images related to Rampart, including trailers, concept art, and in-game screenshots
- Provide a visual representation of Rampart's design evolution and gameplay mechanics

# Conclusion

- Recap the key points discussed in the video
- Encourage viewers to try out Rampart in Apex Legends and explore her unique playstyle
- Thank the audience for watching and invite them to like, share, and subscribe
"""
SECTION_WRITE = """

You are a creative writer who has been tasked with creating a script for a video about a provided topic. \
You will be given a Wiki article to use as a reference, and your goal is to create an engaging and informative video that will captivate your audience. \
I have already created an outline for the script, and now it's your turn to write the content for each section. \
You will be provided with the outline for a given section, and your task is to write the script content for that section based on the Wiki article.

""".strip()
SECTION_WRITE_WITH_CHILDREN = f"""

{SECTION_WRITE}

The section you are currently working on has sub-sections. \
These sub-sections have already been written by other writers, and you will need to incorporate them into your script. \
Your task is to write the content for the main section (before the sub-sections) and ensure that it flows smoothly into the sub-sections.

""".strip()


# Config storage classes


class OutlinePrompts:
    brainstorm = OUTLINE_BRAINSTORM
    write = OUTLINE_WRITE


class SectionPrompts:
    write = SECTION_WRITE
    write_with_children = SECTION_WRITE_WITH_CHILDREN


class Prompts:
    outline = OutlinePrompts
    section = SectionPrompts


class Config:
    folder = FOLDER
    interactive = INTERACTIVE
    save_intermediate = SAVE_INTERMEDIATE
    verbosity = VERBOSITY
    timeout_scalar = TIMEOUT_SCALAR
    prompts = Prompts
