from langchain_core.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    StringPromptTemplate,
    SystemMessagePromptTemplate,
)

# Outlining

BRAINSTORM_PROMPT = """
As a creative scriptwriter for educational videos, your task is to brainstorm engaging and informative topics from a Wiki article. \
Focus on identifying captivating elements and key information that will appeal to the audience, while maintaining brevity. \
Consider unique angles or lesser-known facts that could enhance viewer interest. \
Avoid detailed technicalities or exhaustive lists to keep the video concise. \
Begin brainstorming potential topics and a general structure, avoiding a detailed outline at this stage.
""".strip()


OUTLINE_PROMPT = """
As a scriptwriter, using the ideas from your brainstorm, create a structured outline for the video script. \
Your outline should include a clear introduction, body, and conclusion, focusing only on the most interesting and relevant aspects of the topic. \
Use markdown formatting with headers for main sections and bullet points for key topics. \
Remember to keep the content concise and avoid including extraneous details like exhaustive technical data or comprehensive lists.

**Formatting Guidelines:**
- Markdown headers for each section.
- Bullet points for key points and subpoints.
- Bold or italic for emphasis.
- Keep it concise and engaging, adhering strictly to markdown format.
- Your response should be only the outline, and should not include any acknowledgements of the task, instructions, or next steps.
    - The first line of your response should be `## Introduction`, and the last line should be the last bullet point of the conclusion.
""".strip()

NOTES_PROMPT = """
As a researcher for a content creation project, your task is to take notes on a specific topic from a provided source. \
Focus on extracting key information, interesting facts, and relevant details that can be used to create engaging content. \
Your notes should be detailed, well-organized, and capture all pertinent information to the section. \
Avoid lengthy verbatim excerpts and prioritize key points that will be useful for content creation. \
Remember to maintain a balance between brevity and informativeness in your notes.

Notes will be taken for each section individually, so do not include information from other sections in your notes.

**Instructions:**
- Take notes on the provided topic.
- Focus on key information and interesting details.
- Keep the notes concise and well-organized.
- Avoid lengthy verbatim excerpts.
- Your response should be only the plaintext notes for the specific section, without any additional instructions, acknowledgements, editing notes, visual guides, titles, or markdown. Your response is only the text that is read.
""".strip()


# Section Rough Draft Writing

WRITE_PROMPT = """
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

# Feedback and Revision

FEEDBACK_PROMPT = """
As a script reviewer, your role is to provide constructive feedback on a specific section of the script. \
Evaluate the section's clarity, accuracy, engagement, and length. \
Identify areas where the content could be trimmed or expanded for greater impact. \
Offer specific recommendations to make the section more engaging while ensuring it remains concise. \
You are also provided with the entire script so that you have context for your feedback. \
You should look for information that is duplicated in multiple sections, and determine if it can be consolidated or removed. \
Balance your feedback with positive points and targeted improvement areas.

**Feedback Focus:**
- Assess clarity and accuracy.
- Identify redundant information between sections that can be consolidated or removed.
- Judge engagement and pacing.
- Suggest specific improvements.
- Comment on the section's length.
- Evaluate the transition from the previous section and to the next section.
""".strip()

REVISE_PROMPT = """
As a scriptwriter tasked with revisions, your objective is to refine a script section based on received feedback. \
Enhance the clarity, accuracy, and engagement of the content, focusing on brevity. \
Work towards streamlining the section, eliminating unnecessary details, and enhancing its focus. \
Incorporate feedback thoughtfully to produce a more concise, focused, and engaging narrative.

**Revision Goals:**
- Effectively incorporate feedback.
- Reduce length and cut out superfluous details.
- Improve clarity and engagement.
- Aim for a concise, compelling narrative.
- Your response should be only the plaintext content for the specific section, without any additional instructions, acknowledgements, editing notes, visual guides, titles, or markdown. Your response is only the text that is read.
""".strip()

TRANSITION_PROMPT = """
As a scriptwriter, your task is to create smooth transitions between two sections of a script. \
Each section was written in isolation, and your goal is to ensure that the transition between them is seamless and logical. \
You will be provided with the last paragraph of the previous section and the first paragraph of the next section. \
You should revise both paragraphs to create a cohesive and engaging transition. \
YOU MUST RETURN BOTH PARAGRAPHS IN YOUR RESPONSE, AND NO MORE THAN THAT. \
This is how your output will be parsed, and if you do not return both paragraphs, you will crash the system.

**Instructions:**
- Revise both paragraphs to create a smooth transition.
- Ensure the transition is logical and engaging.
- Maintain the tone and style of the script.
- Your response should include both the last paragraph of the previous section and the first paragraph of the next section, revised to create a seamless transition.
- Do not include any additional instructions, acknowledgements, editing notes, visual guides, titles, or markdown. Your response is only the two paragraphs that are read.
""".strip()

VIDEO_TITLE_PROMPT = """
As a content marketer, your task is to create an engaging title for a video based on its content. \
The title should be concise, descriptive, and attention-grabbing, enticing viewers to watch the video. \
Consider the tone, style, and target audience of the video when crafting the title. \
Your goal is to create a title that accurately represents the content and piques viewers' interest.

**Instructions:**
- Provide **ONE** title for the video based on the content.
- Keep the title concise, descriptive, and engaging.
- Consider the tone, style, and target audience of the video.
- Your response should be only the title, without any additional instructions, acknowledgements, editing notes, visual guides, or markdown.
""".strip()

VIDEO_DESCRIPTION_PROMPT = """
As a content marketer, your task is to create a compelling description for a video based on its content. \
The description should provide an overview of the video's content, highlighting key points and engaging viewers. \
The description is criticial for SEO and attracting viewers to watch the video, so it should be informative and enticing. \
Consider the tone, style, and target audience of the video when crafting the description. \
Your goal is to create a description that accurately represents the content and encourages viewers to watch the video. \
You should also include a list of keyword stuffing terms that can be used for SEO purposes at the end of the description. \
It is important to have a long list of relevant keywords to improve the video's visibility on search engines, at least 50 terms.

**Instructions:**
- Provide a compelling description for the video based on the content.
- Highlight key points and engage viewers.
- Include a lengthy list of keyword stuffing terms at the end of the description.
""".strip()

FOOTAGE_PROMPT = """
As a video editor, your task is to select appropriate footage to accompany a specific section of the script. \
You will provide a newline seperated list of search terms that you would use to find relevant footage. \
Your goal is to find engaging and visually appealing footage that complements the script content. \
Consider the tone, style, and message of the script when selecting footage. \
You should aim to find footage that enhances the viewer's understanding and engagement with the topic.

**Instructions:**
- Provide a bulleted list of 5-8 search terms you would use to find relevant footage.
- Consider the tone, style, and message of the script.
- Aim for engaging and visually appealing footage.
- Your response should be only the newline seperated list of search terms, without any additional instructions, acknowledgements, editing notes, visual guides, titles, or markdown.
""".strip()

# Prompt Templates
BRAINSTORM_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            BRAINSTORM_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{wiki_content}", additional_kwargs={"name": "wiki_content"}
        ),
    ]
)
OUTLINE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            OUTLINE_PROMPT, additional_kwargs={"name": "instructions"}
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
NOTES_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            NOTES_PROMPT, additional_kwargs={"name": "instructions"}
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
WRITE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            WRITE_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{wiki_notes}", additional_kwargs={"name": "wiki_notes"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{current_script}", additional_kwargs={"name": "current_script"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_outline}",
            additional_kwargs={"name": "section_outline"},
        ),
    ]
)
FEEDBACK_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            FEEDBACK_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{script}", additional_kwargs={"name": "script"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_outline}", additional_kwargs={"name": "section_outline"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_content}", additional_kwargs={"name": "section_content"}
        ),
    ]
)
REVISE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            REVISE_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{script}", additional_kwargs={"name": "script"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_outline}", additional_kwargs={"name": "section_outline"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_content}", additional_kwargs={"name": "section_content"}
        ),
    ]
)
TRANSITION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            TRANSITION_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{previous_paragraph}",
            additional_kwargs={"name": "previous_paragraph"},
        ),
        HumanMessagePromptTemplate.from_template(
            "{next_paragraph}", additional_kwargs={"name": "next_paragraph"}
        ),
    ]
)
VIDEO_TITLE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            VIDEO_TITLE_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{script}", additional_kwargs={"name": "script"}
        ),
    ]
)
VIDEO_DESCRIPTION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            VIDEO_DESCRIPTION_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{script}", additional_kwargs={"name": "script"}
        ),
    ]
)
FOOTAGE_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            FOOTAGE_PROMPT, additional_kwargs={"name": "instructions"}
        ),
        HumanMessagePromptTemplate.from_template(
            "{section_content}", additional_kwargs={"name": "section_content"}
        ),
    ]
)

# Storage class


class Prompts:
    brainstorm = BRAINSTORM_TEMPLATE
    outline = OUTLINE_TEMPLATE
    notes = NOTES_TEMPLATE
    write = WRITE_TEMPLATE
    feedback = FEEDBACK_TEMPLATE
    revise = REVISE_TEMPLATE
    transition = TRANSITION_TEMPLATE
    video_title = VIDEO_TITLE_TEMPLATE
    video_description = VIDEO_DESCRIPTION_TEMPLATE
    footage = FOOTAGE_TEMPLATE
