import re
from .llm import client

habits_of_mind = """
1. Persisting – Stick to it; remain focused and follow through.
2. Managing Impulsivity – Think before acting; remain calm and thoughtful.
3. Listening with Understanding and Empathy – Understand others’ perspectives and emotions.
4. Thinking Flexibly – Consider alternative viewpoints and adapt strategies.
5. Thinking about Thinking (Metacognition) – Be aware of your own thinking process.
6. Striving for Accuracy and Precision – Seek clarity, exactness, and craftsmanship.
7. Questioning and Problem Posing – Ask good questions and identify problems to solve.
8. Applying Past Knowledge to New Situations – Transfer learning to new contexts.
9. Thinking and Communicating with Clarity and Precision – Express ideas clearly and accurately.
10. Gathering Data Through All Senses – Use all sensory inputs to inform thinking.
11. Creating, Imagining, and Innovating – Generate new and original ideas.
12. Responding with Wonderment and Awe – Show curiosity and fascination with learning.
13. Taking Responsible Risks – Venture beyond comfort zones thoughtfully.
14. Finding Humor – Appreciate the humorous and be able to laugh at oneself.
15. Thinking Interdependently – Work effectively with others and value collaboration.
16. Remaining Open to Continuous Learning – Show humility and a willingness to grow.
""".strip()


# remove the number via regex
habits = [re.sub(r'^\d+\.\s*', '', line) for line in habits_of_mind.split("\n")]


habit_meta_examples = {
    "Persisting – Stick to it; remain focused and follow through.": [
        "This seems complicated, but I’ll keep breaking it down until it makes sense.",
        "Even though I'm frustrated, I know I need to stay with it and not give up yet.",
        "I've come this far—I just need to push through the last few steps."
    ],
    "Managing Impulsivity – Think before acting; remain calm and thoughtful.": [
        "Let me think about how a careful detective would methodically tackle such a situation.",
        "Let me start by breaking down what a crisis management plan typically includes.",
        "Hmm, first, I need to figure out the product. Since it's not specified, maybe I should make some assumptions.",
        "I should also consider the project's current phase before jumping to a conclusion."
    ],
    "Listening with Understanding and Empathy – Understand others’ perspectives and emotions.": [
        "Also, maybe anticipate Taylor's possible reactions. If they become defensive, stay calm and redirect to the positive intent of the feedback.",
        "I need to make sure the approach is supportive and doesn't make Riley feel like they're being pitied or singled out.",
        "Check-ins are important to ensure both feel heard and their contributions are valued.",
        "I should actively listen and reflect their concerns before offering any suggestions."
    ],
    "Thinking Flexibly – Consider alternative viewpoints and adapt strategies.": [
        "Also, consider potential issues like burnout, so the policy should include guidelines on taking vacations and time off.",
        "Another thought: maybe there's a way to reallocate existing resources rather than bringing in new ones.",
        "Wait, what about alternative water sources?",
        "Maybe there's a totally different way to frame this problem."
    ],
    "Thinking about Thinking (Metacognition) – Be aware of your own thinking process.": [
        "I need to make sure that my own biases are acknowledged.",
        "I might be missing something here. Maybe I should consider the venue and logistics more carefully.",
        "Let me double-check whether my reasoning aligns with the evidence.",
        "I noticed I was jumping to conclusions—let me slow down and reassess my assumptions.",
        "Wait, is that right? Hmm, maybe I'm getting confused. Let me think again."
    ],
    "Striving for Accuracy and Precision – Seek clarity, exactness, and craftsmanship.": [
        "I should verify that all the figures add up correctly before finalizing.",
        "Let me go back and reword this to be more precise and avoid any misinterpretation.",
        "I might be missing something here. Maybe I should consider the venue and logistics more carefully.",
        "I should define each term I use to avoid ambiguity."
    ],
    "Questioning and Problem Posing – Ask good questions and identify problems to solve.": [
        "Wait, should I also consider environmental factors?",
        "What are the key areas to focus on?",
        "What about questions related to privacy?",
        "How does this impact the stakeholders long term?"
    ],
    "Applying Past Knowledge to New Situations – Transfer learning to new contexts.": [
        "From what I remember, sustainable cities focus on reducing environmental impact, promoting green spaces, using renewable energy, efficient transportation, and maybe community involvement.",
        "Let me start by recalling what I know about animal migration.",
        "Okay, so I need to create a communication guide for astronauts interacting with a non-human intelligent species, using my knowledge of English dialects.",
        "Let me apply what I learned in my last presentation to improve this one."
    ],
    "Thinking and Communicating with Clarity and Precision – Express ideas clearly and accurately.": [
        "I should structure the analysis by first introducing the technology, then discussing its environmental benefits, followed by the economic impacts, and finally addressing the challenges.",
        "Each of these steps needs to be detailed. Let me go through each one and think about the specifics.",
        "Now I'll craft a comprehensive marketing strategy that addresses these elements while being specific enough to be useful and actionable.",
        "I should avoid vague words and be as clear as possible."
    ],
    "Gathering Data Through All Senses – Use all sensory inputs to inform thinking.": [
        "Let me start by recalling the different senses: sight, sound, touch, smell, taste.",
        "Next, the sounds may matter too.",
        "To evaluate the quality of a smartphone, I should examine its design, screen clarity, speaker output, and tactile feedback.",
        "What can I learn by additionally observing body language and facial expressions?"
    ],
    "Creating, Imagining, and Innovating – Generate new and original ideas.": [
        "I wonder if combining both would allow for a rich vocabulary.",
        "Alternatively, using acoustic methods. Maybe a network of drums with different tones and rhythms?",
        "Something else: Is there a way to use game mechanics to improve this experience?"
    ],
    "Responding with Wonderment and Awe – Show curiosity and fascination with learning.": [
        "Wait, here's an idea. Let's think about the interplay between continuous and discrete mathematics.",
        "Wow, I never realized how elegant this solution is.",
        "It's amazing how complex systems emerge from such simple rules.",
        "I’m genuinely curious about how that mechanism works under the hood."
    ],
    "Taking Responsible Risks – Venture beyond comfort zones thoughtfully.": [
        "Public safety: AI-powered surveillance. But need to address privacy by having clear policies on data retention and oversight.",
        "Wait, although beneficial, what about the risks of data being sold or shared without consent?",
        "I should also consider regulatory changes—acting now might prepare us better for future compliance demands."
    ],
    "Finding Humor – Appreciate the humorous and be able to laugh at oneself.": [
        "Maybe throw in some funny thoughts about the coffee's temperature or the color of the liquid.",
        "Well, at least if this fails, I’ll have a great story to tell!",
        "Let me add a light-hearted comment to ease the tension in the meeting."
    ],
    "Thinking Interdependently – Work effectively with others and value collaboration.": [
        "Next, understanding each member's expertise.",
        "If everyone knows what they're supposed to do, there's less confusion. Maybe assigning specific tasks based on each agency's strengths.",
        "Another thought is about integrating diverse perspectives.",
        "Let’s combine our ideas to develop something even stronger."
    ],
    "Remaining Open to Continuous Learning – Show humility and a willingness to grow.": [
        "The tech sector is always changing, so staying current is crucial.",
        "So keeping up with funding opportunities and what's considered innovative or important in the field.",
        "I’m realizing that my initial assumption may have been too narrow—I need to expand my understanding.",
        "Let me seek feedback and improve my approach for next time."
    ]
}


habit_example_mapping = {
    "persisting": "Persisting – Stick to it; remain focused and follow through.",
    "managing_impulsivity": "Managing Impulsivity – Think before acting; remain calm and thoughtful.",
    "listening_with_understanding_and_empathy": "Listening with Understanding and Empathy – Understand others’ perspectives and emotions.",
    "thinking_flexibly": "Thinking Flexibly – Consider alternative viewpoints and adapt strategies.",
    "thinking_about_thinking_metacognition": "Thinking about Thinking (Metacognition) – Be aware of your own thinking process.",
    "striving_for_accuracy_and_precision": "Striving for Accuracy and Precision – Seek clarity, exactness, and craftsmanship.",
    "questioning_and_problem_posing": "Questioning and Problem Posing – Ask good questions and identify problems to solve.",
    "applying_past_knowledge_to_new_situations": "Applying Past Knowledge to New Situations – Transfer learning to new contexts.",
    "thinking_and_communicating_with_clarity_and_precision": "Thinking and Communicating with Clarity and Precision – Express ideas clearly and accurately.",
    "gathering_data_through_all_senses": "Gathering Data Through All Senses – Use all sensory inputs to inform thinking.",
    "creating_imagining_and_innovating": "Creating, Imagining, and Innovating – Generate new and original ideas.",
    "responding_with_wonderment_and_awe": "Responding with Wonderment and Awe – Show curiosity and fascination with learning.",
    "taking_responsible_risks": "Taking Responsible Risks – Venture beyond comfort zones thoughtfully.",
    "finding_humor": "Finding Humor – Appreciate the humorous and be able to laugh at oneself.",
    "thinking_interdependently": "Thinking Interdependently – Work effectively with others and value collaboration.",
    "remaining_open_to_continuous_learning": "Remaining Open to Continuous Learning – Show humility and a willingness to grow."
}


habit_extraction_prompt_with_evidence_provided_with_format_enforcement_v5_system = """
You will be given a THINKING PASSAGE that describes a person's internal thinking while solving a problem. Your task is to determine whether a specific cognitive habit is **explicitly** demonstrated in the thought process.

To make this judgment, you must first identify and extract a **verbatim statement** from the THINKING PASSAGE that **clearly and directly** supports the presence of the specified habit.

---

### Habit to evaluate:
{habit}

### Examples of statements that would support this habit:
{example_meta_thinking_statements}

---

Your response must strictly follow this JSON format:
```
{{
    "evidence": "Exact sentence from the THINKING PASSAGE that directly demonstrates the habit, or an empty string if no such sentence exists",
    "is_reflected": true/false (true if the evidence sentence directly demonstrates the habit, false otherwise)
}}
```

---

### Instructions (read carefully):
- Your answer must be based **only on explicit statements** from the THINKING PASSAGE. Do not infer, interpret, or assume anything beyond what is written.
- Do **not** paraphrase, summarize, or reword the evidence. Use **exact text only** in the "evidence" field except empty string.
- If multiple statements support the habit, extract **only the first full sentence (in order of appearance)** that clearly and directly demonstrates it — even if only part of that sentence reflects the habit.
- If **no statement clearly demonstrates** the habit, leave the `"evidence"` field **empty** and set `"is_reflected"` to `false`.
- The presence of other habits in the same sentence is acceptable — your task is to judge **only whether the specified habit is present**.
- Responses that rely on vague or implicit reasoning will be considered invalid.
"""

from pydantic import BaseModel

class HabitOccurrence(BaseModel):
    evidence: str
    is_reflected: bool



def judge_habit_occurrence_by_showing_evidence_with_format_enforcement_system(thinking: str, habit: str) -> tuple[str, str] | dict:
    habit_name = habit_example_mapping[habit]
    example_meta_thinking_statements = habit_meta_examples[habit_name]

    formated_example_meta_thinking_statements = "\n\n".join([f'Example: "{example_meta_thinking_statement}"' for example_meta_thinking_statement in example_meta_thinking_statements])

    habit_extraction_query = habit_extraction_prompt_with_evidence_provided_with_format_enforcement_v5_system.format(habit=f"**{habit_name}**", example_meta_thinking_statements=formated_example_meta_thinking_statements)
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-mini",
        messages = [
            {"role": "system", "content": habit_extraction_query},
            {"role": "user", "content": f"Please analyze the following THINKING PASSAGE to determine whether the habit is reflected:\n{thinking}"}
        ],
        temperature=0.0,
        top_p=0.95,
        max_tokens=1024,
        frequency_penalty=1.0,
        response_format=HabitOccurrence,
    )
    response_content = response.choices[0].message.parsed
    return response_content.dict()