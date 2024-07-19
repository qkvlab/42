messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "You will be provided with an image. Your task is to accurately summarize the style of the image.\n\nHere is the image:\n<image>",
            },
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
            },
            {
                "type": "text",
                "text": "</image>\n\nIn this context, \"style\" refers to the visual characteristics, artistic techniques, and key elements that define the overall aesthetic of the image. These are the materials and key information that could be referenced when generating similar images for Stable Diffusion (SD) models in the future.\n\nCarefully analyze the provided image, paying attention to various style elements including but not limited to:\n\n1. Medium (e.g., digital art, oil painting, photograph, sketch)\n2. Color palette and use of color\n3. Lighting and shadows\n4. Composition and layout\n5. Texture and brushwork (if applicable)\n6. Level of detail and realism\n7. Artistic movement or genre (if identifiable)\n8. Mood or atmosphere\n9. Subject matter and how it's portrayed\n10. Any unique or distinctive features\n\nAfter analyzing the image, provide a detailed summary of its style. Your summary should be comprehensive yet concise, capturing the essence of the image's visual style in a way that could guide future image generation.\n\nPresent your analysis in the following format:\n\n<style_summary>\n[Your detailed description of the image's style, addressing the elements mentioned above and any other relevant aspects. Be specific and use descriptive language.]\n</style_summary>\n\nRemember to focus on the visual and artistic elements rather than the content or meaning of the image. Your goal is to provide a clear and accurate representation of the image's style that could be used as a reference for generating similar images.",
            },
        ],
    }
]
