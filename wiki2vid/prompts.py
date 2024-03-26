from langchain_core.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    StringPromptTemplate,
    SystemMessagePromptTemplate,
)

# Outlining

OUTLINE_BRAINSTORM = """
As a creative scriptwriter for educational videos, your task is to brainstorm engaging and informative topics from a Wiki article. \
Focus on identifying captivating elements and key information that will appeal to the audience, while maintaining brevity. \
Consider unique angles or lesser-known facts that could enhance viewer interest. \
Avoid detailed technicalities or exhaustive lists to keep the video concise. \
Begin brainstorming potential topics and a general structure, avoiding a detailed outline at this stage.

Specifically for Apex Characters, consider the following information. Other information, such as cosmetics, are irrelevant for this task:
- Abilities
    - Ultimate Ability
    - Tactical Ability
    - Passive Ability
- Any other perks or unique features if applicable
""".strip()


OUTLINE_WRITE = """
As a scriptwriter, using the ideas from your brainstorm, create a structured outline for the video script. \
Your outline should include a clear introduction, body, and conclusion, focusing only on the most interesting and relevant aspects of the topic. \
Use markdown formatting with headers for main sections and bullet points for key topics. \
Remember to keep the content concise and avoid including extraneous details like exhaustive technical data or comprehensive lists.

Specifically for Apex Characters, consider the following structure. Other information, such as cosmetics, are irrelevant for this task:
- Intro
- Abilities
    - Ultimate Ability
    - Tactical Ability
    - Passive Ability
- Any other perks or unique features if applicable
- Conclusion


**Formatting Guidelines:**
- Markdown headers for each section.
- Bullet points for key points and subpoints.
- Bold or italic for emphasis.
- Keep it concise and engaging, adhering strictly to markdown format.
- Your response should be only the outline, and should not include any acknowledgements of the task, instructions, or next steps.
    - The first line of your response should be `## Introduction`, and the last line should be the last bullet point of the conclusion.
""".strip()


# Section Rough Draft Writing

SECTION_WRITE = """
As a video scriptwriter, your job is to write engaging content for a specific section, based on the provided outline. \
Craft the script in a way that is informative yet concise, ensuring it captures the essence of the topic. \
Avoid lengthy expositions, focusing instead on clear and concise delivery. \
The script should be in plain text and formatted as engaging prose. \
Remember, the length of each section should correspond to its importance, with key sections given more detail. 

**Instructions:**
- Write in plain text, avoiding markdown formatting.
- Focus on brevity and clarity.
- Ensure the content is engaging and flows well.
- Your response should be only the plaintext content for the specific section, without any additional instructions, acknowledgements, editing notes, visual guides, titles, or markdown. Your response is only the text that is read.
""".strip()

SECTION_WRITE_WITH_CHILDREN = """
As a scriptwriter, your task is to write content for the main section of a script that includes pre-written sub-sections. \
Focus on creating an introductory part that smoothly leads into these sub-sections. \
Ensure this main section is concise, setting the stage for the sub-sections without duplicating their content. \
Your goal is to ensure a seamless and logical transition that ties the section together cohesively.

**Instructions:**
- Write content only for the main section.
- Avoid repeating content from the sub-sections.
- Ensure a smooth flow into the sub-sections.
""".strip()

# Feedback and Revision

SECTION_FEEDBACK = """
As a script reviewer, your role is to provide constructive feedback on a specific section of the script. \
Evaluate the section's clarity, accuracy, engagement, and length. \
Identify areas where the content could be trimmed or expanded for greater impact. \
Offer specific recommendations to make the section more engaging while ensuring it remains concise. \
Balance your feedback with positive points and targeted improvement areas.

**Feedback Focus:**
- Assess clarity and accuracy.
- Judge engagement and pacing.
- Suggest specific improvements.
- Comment on the section's length.
""".strip()

SECTION_REVISE = """
As a scriptwriter tasked with revisions, your objective is to refine a script section based on received feedback. \
Enhance the clarity, accuracy, and engagement of the content, focusing on brevity. \
Work towards streamlining the section, eliminating unnecessary details, and enhancing its focus. \
Incorporate feedback thoughtfully to produce a more concise, focused, and engaging narrative.

**Revision Goals:**
- Effectively incorporate feedback.
- Reduce length and cut out superfluous details.
- Improve clarity and engagement.
- Aim for a concise, compelling narrative.
""".strip()

# Prompt Templates
OUTLINE_BRAINSTORM_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            OUTLINE_BRAINSTORM, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{wiki_content}", additional_kwargs={"name": "wiki_content"}
        ),
    ]
)
OUTLINE_WRITE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            OUTLINE_WRITE, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{wiki_content}", additional_kwargs={"name": "wiki_content"}
        ),
        AIMessagePromptTemplate.from_template(
            "{brainstorm}",
            additional_kwargs={"name": "brainstorming_results"},
        ),
    ]
)
SECTION_WRITE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            SECTION_WRITE, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{wiki_content}", additional_kwargs={"name": "wiki_content"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_outline}",
            additional_kwargs={"name": "section_outline"},
        ),
    ]
)
SECTION_WRITE_WITH_CHILDREN_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            SECTION_WRITE_WITH_CHILDREN,
            additional_kwargs={"name": "instructions"},
        ),
        HumanMessagePromptTemplate.from_template(
            "{wiki_content}", additional_kwargs={"name": "wiki_content"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{children}",
            additional_kwargs={"name": "children"},
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_outline}",
            additional_kwargs={"name": "section_outline"},
        ),
    ]
)
SECTION_REVISE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            SECTION_REVISE, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_content}", additional_kwargs={"name": "section_content"}
        ),
    ]
)
SECTION_FEEDBACK_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            SECTION_FEEDBACK, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_content}", additional_kwargs={"name": "section_content"}
        ),
    ]
)


# Access classes
class OutlinePrompts:
    brainstorm = OUTLINE_BRAINSTORM_TEMPLATE
    write = OUTLINE_WRITE_TEMPLATE


class SectionPrompts:
    write = SECTION_WRITE_TEMPLATE
    write_with_children = SECTION_WRITE_WITH_CHILDREN_TEMPLATE
    feedback = SECTION_FEEDBACK_TEMPLATE
    revise = SECTION_REVISE_TEMPLATE


class Prompts:
    outline = OutlinePrompts
    section = SectionPrompts
