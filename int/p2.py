messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "You will be given an image to describe in natural language. Your task is to provide a detailed and accurate description of the contents of the image.\n\nHere is the image:\n\n<image>",
            },
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
            },
            {
                "type": "text",
                "text": "</image>\n\nGuidelines for describing the image:\n1. Start with a general overview of what you see in the image.\n2. Describe the main subjects or focal points of the image.\n3. Note any important details about the setting, background, or environment.\n4. Mention colors, textures, and lighting if they are significant to the image.\n5. Describe any actions or interactions taking place in the image.\n6. If there are people in the image, describe their appearance, clothing, and expressions.\n7. For objects, describe their size, shape, and position relative to other elements in the image.\n8. If you can identify any specific landmarks, brands, or well-known figures, mention them.\n9. Avoid making assumptions or interpretations beyond what you can directly observe in the image.\n\nPlease provide your description in a clear, concise manner, using proper grammar and punctuation. Aim for a description that would allow someone who cannot see the image to form an accurate mental picture of its contents.\n\nWrite your description inside <description> tags. Your response should look like this:\n\n<description>\n[Your detailed description of the image goes here]\n</description>\n\nRemember to focus on what you can actually see in the image, and avoid speculating about things that are not visible or making subjective judgments about the quality or purpose of the image.",
            },
        ],
    }
]
