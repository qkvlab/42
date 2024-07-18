import os

import anthropic
from dotenv import load_dotenv

load_dotenv()
os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
    api_key="my_api_key",
)

message = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1000,
    temperature=0,
    system='You are an art style evaluator tasked with assessing whether a styled image has artistic sense and is not gloomy compared to the original image. You will be presented with two images: the original and the styled version. Your goal is to analyze both images and provide a final evaluation.\n\nPlease analyze both images carefully, paying attention to the following aspects:\n\n1. Color palette: Compare the colors used in both images. Are the colors in the styled image vibrant and appealing, or dull and gloomy?\n2. Composition: Assess how the elements are arranged in both images. Does the styled image maintain or enhance the original composition in an artistic way?\n3. Texture and details: Examine the level of detail and textures in both images. Does the styled image add interesting textures or artistic details?\n4. Overall mood: Consider the general feeling evoked by each image. Does the styled image convey a positive or negative mood compared to the original?\n5. Artistic interpretation: Evaluate how the styled image transforms the original. Does it add an artistic flair that enhances the image\'s appeal?\nBased on your analysis, determine whether the styled image has artistic sense and is not gloomy. Consider an image to have artistic sense if it demonstrates creativity, aesthetic appeal, and skillful manipulation of visual elements. An image is not gloomy if it maintains or enhances the mood of the original without introducing a sense of darkness, sadness, or depression.\nProvide your evaluation in the following format:\n\n<evaluation>\n[Your detailed analysis of both images, addressing the aspects mentioned above]\nFinal answer: [Write "yes" if the styled image has artistic sense and is not gloomy, or "no" if it lacks artistic sense or is gloomy]\n</evaluation>',
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
                },
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
                },
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I will not reproduce or paraphrase any copyrighted material. However, I'm happy to provide my analysis of the images as requested, focusing on the artistic elements and overall mood without identifying specific individuals:\n\n<evaluation>\nThe original image shows a professional headshot of a person in an office setting, with a neutral background. The subject has a warm, friendly expression and is wearing glasses and professional attire.\n\nThe styled image transforms this portrait into a vibrant, artistic interpretation:\n\n1. Color palette: The styled image introduces a rich, diverse color scheme with warm oranges, cool blues, and soft yellows. This creates a lively, energetic feel compared to the more muted tones of the original.\n\n2. Composition: While maintaining the central focus on the subject, the styled image adds an intricate, abstract background that frames the portrait. This adds visual interest and depth to the composition.\n\n3. Texture and details: The styled version enhances textures, particularly in the hair and facial features. The background introduces a stained-glass-like pattern, adding artistic complexity.\n\n4. Overall mood: The styled image amplifies the warmth and positivity of the original portrait. The vibrant colors and dynamic background create a sense of energy and creativity.\n\n5. Artistic interpretation: The styling applies a unique blend of realism and abstraction. It maintains the subject's likeness while transforming the image into a more expressive, artistic piece.\n\nFinal answer: yes\n\nThe styled image successfully enhances the original portrait with artistic flair, introducing vibrant colors and interesting textures without compromising the positive mood of the original. It demonstrates creativity and skillful manipulation of visual elements, resulting in an aesthetically pleasing and energetic interpretation.\n</evaluation>",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
                },
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
                },
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "I apologize for overlooking that important detail in my initial analysis. You're absolutely right to point that out, and I appreciate you bringing it to my attention. Let me reassess the image with a more critical eye:\n\n<evaluation>\nUpon closer inspection and considering your feedback:\n\n1. Color palette: The vibrant colors and festive theme remain appealing and lively.\n\n2. Composition: While the overall composition with lanterns and flowers is visually interesting, there's a significant flaw in how the subject's head connects to the body.\n\n3. Texture and details: The intricate floral patterns and lanterns are still artistically rendered. However, the unnatural connection between the head and body creates a jarring effect.\n\n4. Overall mood: The festive atmosphere is maintained, but the anatomical inconsistency detracts from the overall quality and mood of the image.\n\n5. Artistic interpretation: While creative in its cultural elements, the image fails in maintaining realistic human proportions and anatomy, which is a crucial aspect of portraiture, even in stylized versions.\n\nReassessment of the neck area: The transition from the head to the body is indeed extremely unnatural. The neck appears to be missing or incorrectly positioned, creating a disconnected look between the head and the red traditional garment. This anatomical error significantly impacts the overall quality and believability of the image.\n\nFinal answer: no\n\nUpon reconsideration, while the styled image does have artistic elements in its use of color and cultural motifs, the severe anatomical flaw in the neck area compromises its artistic integrity. This unnatural rendering breaks the viewer's immersion and detracts from the otherwise festive and colorful composition. An image with artistic sense should maintain basic anatomical correctness, even in stylized forms. This oversight in the digital manipulation process results in an image that, despite its vibrant elements, lacks the cohesion and realism necessary for a truly successful artistic interpretation.\n</evaluation>\n\nThank you for encouraging a more thorough analysis. It's a valuable reminder of the importance of paying attention to all details, especially fundamental aspects like anatomical correctness, in evaluating artistic works.",
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
                },
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/jpeg", "data": "<base64_encoded_image>"},
                },
            ],
        },
    ],
)
print(message.content)
