import base64
import os
import random

import anthropic
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

load_dotenv()


def get_caption(image_path):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    media_type = "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You will be given an image to describe in natural language. Your task is to provide a detailed and accurate description of the contents of the image.\n\nHere is the image:\n\n<image>",
                    },
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": media_type, "data": image_data},
                    },
                    {
                        "type": "text",
                        "text": "</image>\n\nGuidelines for describing the image:\n1. Start with a general overview of what you see in the image.\n2. Describe the main subjects or focal points of the image.\n3. Note any important details about the setting, background, or environment.\n4. Mention colors, textures, and lighting if they are significant to the image.\n5. Describe any actions or interactions taking place in the image.\n6. If there are people in the image, describe their appearance, clothing, and expressions.\n7. For objects, describe their size, shape, and position relative to other elements in the image.\n8. If you can identify any specific landmarks, brands, or well-known figures, mention them.\n9. Avoid making assumptions or interpretations beyond what you can directly observe in the image.\n\nPlease provide your description in a clear, concise manner, using proper grammar and punctuation. Aim for a description that would allow someone who cannot see the image to form an accurate mental picture of its contents.\n\nWrite your description inside <description> tags. Your response should look like this:\n\n<description>\n[Your detailed description of the image goes here]\n</description>\n\nRemember to focus on what you can actually see in the image, and avoid speculating about things that are not visible or making subjective judgments about the quality or purpose of the image.",
                    },
                ],
            }
        ],
    )

    description = message.content[0].text  # type: ignore
    start_tag = "<description>"
    end_tag = "</description>"
    start_index = description.find(start_tag) + len(start_tag)
    end_index = description.find(end_tag)
    caption = description[start_index:end_index].strip()

    return caption


def main():
    st.title("Image Gallery")

    image_folder = "exps/2c166503-a49f-4422-913b-1a6348ca3dab"

    if not os.path.exists(image_folder):
        st.error(f"Image folder not found: {image_folder}")
        return

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    if not image_files:
        st.warning("No image files found in the specified folder.")
        return

    if "selected_images" not in st.session_state:
        st.session_state.selected_images = random.sample(image_files, min(10, len(image_files)))

    cols = st.columns(5)
    for i, image_file in enumerate(st.session_state.selected_images):
        image_path = os.path.join(image_folder, image_file)
        try:
            with Image.open(image_path) as image:
                selected = cols[i % 5].checkbox("Select", key=f"select_{i}")  # noqa: F841
                cols[i % 5].image(image, use_column_width=True)
                if cols[i % 5].button("Get Caption", key=f"caption_{i}"):
                    caption = get_caption(image_path)
                    cols[i % 5].write(caption)
        except Exception as e:
            st.error(f"Error loading image {image_file}: {str(e)}")

    if st.button("Align"):
        st.write("Selected Images and Preferences:")

        table_data = [
            {
                "Image": image_file,
                "Preference": "Preferred" if st.session_state.get(f"select_{i}", False) else "Not preferred",
            }
            for i, image_file in enumerate(st.session_state.selected_images)
        ]

        st.table(table_data)


if __name__ == "__main__":
    main()
