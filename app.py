import concurrent.futures
import os
import uuid
from urllib.parse import quote

import replicate
import requests
from dotenv import load_dotenv
from requests.exceptions import ProxyError, RequestException, SSLError

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
SM_MS_API_TOKEN = os.getenv("SM_MS_TOKEN")
SERP_API_TOKEN = os.getenv("SERP_API_TOKEN")


def upload_image(image_path):
    url = "https://sm.ms/api/v2/upload"
    headers = {
        "Authorization": SM_MS_API_TOKEN,
    }
    files = {
        "smfile": open(image_path, "rb"),
    }

    response = requests.post(url, headers=headers, files=files)  # type: ignore

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print("Image uploaded successfully!")
            return result["data"]["url"]
        elif "Image upload repeated limit" in result.get("message", ""):
            print("Image already exists, reusing the URL.")
            return result["images"]
        else:
            print("Failed to upload image:", result.get("message"))
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None


def run_instant_id(config):
    output = replicate.run(
        "zsxkib/instant-id:f1ca369da43885a347690a98f6b710afbf5f167cb9bf13bd5af512ba4a9f7b63", input=config
    )
    return output


def get_style_config(style_name):
    styles = {
        "analog_film": {
            "prompt": "analog film photo of a man. faded film, desaturated, 35mm photo, grainy, vignette, vintage, Kodachrome, Lomography, stained, highly detailed, found footage, masterpiece, best quality",
            "negative_prompt": "(lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured (lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch,deformed, mutated, cross-eyed, ugly, disfigured",
            "sdxl_weights": "protovision-xl-high-fidel",
            "guidance_scale": 5,
        },
        "film_noir": {
            "prompt": "Film noir style. Monochrome, high contrast, dramatic shadows, 1940s style, mysterious, cinematic",
            "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, vibrant, colorful",
            "guidance_scale": 5,
            "num_inference_steps": 50,
            "width": 400,
            "height": 400,
        },
        "line_art": {
            "prompt": "line art drawing. professional, sleek, modern, minimalist, graphic, line art, vector graphics",
            "negative_prompt": "anime, photorealistic, 35mm film, deformed, glitch, blurry, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, mutated, realism, realistic, impressionism, expressionism, oil, acrylic",
            "guidance_scale": 3,
            "sdxl_weights": "animagine-xl-30",
            "num_inference_steps": 50,
            "width": 400,
            "height": 400,
        },
        "spring_festival": {
            "prompt": "minimalist, very intricate colours, simplified continuous line colour drawing in the style of ink pen drawing by Michelangelo, white background, colours, heavy use of palette knives, only inky real colours on paper (colours)",
            "negative_prompt": "(lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured (lowres, low quality, worst quality:1.2), (text:1.2), watermark, painting, drawing, illustration, glitch,deformed, mutated, cross-eyed, ugly, disfigured, plain",
            "guidance_scale": 5,
            "ip_adapter_scale": 0.8,
            "num_inference_steps": 30,
            "controlnet_conditioning_scale": 0.8,
            "width": 640,
            "height": 640,
        },
    }
    return styles.get(style_name, styles)


def search_images(query, num_images=100):
    params = {
        "engine": "google_images",
        "q": query,
        "ijn": 0,
        "api_key": SERP_API_TOKEN,
        "num": num_images,
    }

    response = requests.get("https://serpapi.com/search", params=params)

    if response.status_code == 200:
        results = response.json()
        images = results["images_results"][:num_images]
        image_urls = [image["original"] for image in images]
        return image_urls
    else:
        print(f"Error: {response.status_code}")
        return []


def i2i_style(image_path, style_name):
    uploaded_image_url = upload_image(image_path)

    if uploaded_image_url:
        config = get_style_config(style_name)
        config["image"] = uploaded_image_url

        result = run_instant_id(config)
        if result and isinstance(result, list) and len(result) > 0:
            return result[0]
        else:
            raise ValueError("No valid result returned from run_instant_id")
    else:
        raise ValueError("Failed to upload image")


def download_image(url, folder_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        filename = f"{uuid.uuid4()}.jpg"
        with open(os.path.join(folder_path, filename), "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    except SSLError:
        print(f"SSL error encountered with url: {url}. Skipping...")
    except ProxyError:
        print(f"Proxy error encountered with url: {url}. Skipping...")
    except RequestException as e:
        print(f"Error downloading {url}: {str(e)}. Skipping...")
    except Exception as e:
        print(f"Unexpected error downloading {url}: {str(e)}. Skipping...")


def crawl_images_by_query(query, num_images=200):
    image_urls = search_images(query, num_images)

    unique_id = str(uuid.uuid4())
    folder_name = quote(unique_id)
    folder_path = os.path.join("images", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    if image_urls:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(download_image, url, folder_path) for url in image_urls]
            concurrent.futures.wait(futures)
    else:
        print("No images found.")

    return folder_path


if __name__ == "__main__":
    print(i2i_style("prompt/1.jpg", "line_art"))
    # print(crawl_images_by_query("新海诚"))
