import io
import os
import tempfile

import streamlit as st
from PIL import Image

from int.i3 import i2i_style


def main():
    st.title("Image Style Converter")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    style_options = ["analog_film", "film_noir", "line_art", "spring_festival"]
    selected_style = st.selectbox("Choose a style", style_options)

    if uploaded_file is not None:
        if st.button("Run"):
            image_bytes = uploaded_file.getvalue()

            image = Image.open(io.BytesIO(image_bytes))

            st.image(image, caption="Uploaded Image", use_column_width=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                image.save(temp_file.name, format="JPEG")
                temp_file_path = temp_file.name

            try:
                result_image_url = i2i_style(temp_file_path, selected_style)

                st.image(result_image_url, caption="Processed Image", use_column_width=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                os.unlink(temp_file_path)


if __name__ == "__main__":
    main()
