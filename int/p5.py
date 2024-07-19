messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "You are tasked with summarizing a document into a maximum of 10 bullet points. Here is the document to be summarized:\n\n<document>\n{{DOCUMENT}}\n</document>\n\nTo create an effective summary, follow these steps:\n\n1. Carefully read through the entire document to understand its main ideas and key points.\n\n2. Identify the most important information, focusing on main concepts, crucial details, and significant conclusions.\n\n3. Condense this information into clear, concise bullet points.\n\n4. Limit your summary to a maximum of 10 bullet points. If the document is short or simple, you may use fewer bullet points, but never exceed 10.\n\n5. Ensure that each bullet point captures a distinct and important idea from the document.\n\n6. Present the bullet points in a logical order that reflects the structure and flow of the original document.\n\nWhen creating your bullet points, adhere to these guidelines:\n\n- Keep each bullet point brief and to the point, ideally no more than one or two sentences.\n- Use clear, straightforward language.\n- Avoid redundancy between bullet points.\n- Do not include minor details or examples unless they are crucial to understanding the main point.\n- Ensure that the bullet points, when read together, provide a comprehensive overview of the document's key content.\n\nPresent your summary within <summary> tags, with each bullet point on a new line, preceded by a dash (-). For example:\n\n<summary>\n- First key point\n- Second key point\n- Third key point\n</summary>\n\nBegin your summary now.",
            }
        ],
    }
]
