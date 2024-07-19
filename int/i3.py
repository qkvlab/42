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


def upload_image(image_path, max_retries=3):
    url = "https://sm.ms/api/v2/upload"
    headers = {
        "Authorization": SM_MS_API_TOKEN,
    }
    files = {
        "smfile": open(image_path, "rb"),
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, files=files, timeout=30)  # type: ignore
            response.raise_for_status()

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
        except (SSLError, RequestException) as e:
            print(f"Error during image upload (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                print("Max retries reached. Skipping this image.")
                return None
    return None


def run_instant_id(config, max_retries=3):
    for attempt in range(max_retries):
        try:
            output = replicate.run(
                "zsxkib/instant-id:f1ca369da43885a347690a98f6b710afbf5f167cb9bf13bd5af512ba4a9f7b63", input=config
            )
            return output
        except Exception as e:
            print(f"Error in run_instant_id (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                print("Max retries reached. Skipping this configuration.")
                return None
    return None


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
            "prompt": "line art drawing profile picture, professional, sleek, modern, minimalist, graphic, line art, vector graphics",
            "negative_prompt": "photorealistic, 35mm film, deformed, glitch, blurry, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, mutated, realism, realistic, impressionism, expressionism, oil, acrylic",
            "guidance_scale": 6,
            "sdxl_weights": "animagine-xl-30",
            "num_inference_steps": 50,
            "width": 640,
            "height": 640,
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


def i2i_style_auto(folder_path, style_name):
    output_folder = os.path.join(folder_path, f"{style_name}_output")
    os.makedirs(output_folder, exist_ok=True)

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    def process_image(image_file):
        input_path = os.path.join(folder_path, image_file)
        try:
            result_url = i2i_style(input_path, style_name)
            if result_url:
                output_filename = f"{os.path.splitext(image_file)[0]}_{style_name}.jpg"
                output_path = os.path.join(output_folder, output_filename)
                response = requests.get(result_url)
                if response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"Processed and saved: {output_filename}")
                else:
                    print(f"Failed to download processed image for {image_file}")
            else:
                print(f"Failed to process {image_file}")
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_image, image_files)

    return output_folder


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


def explore_hyperparameters(image_path):
    base_config = get_style_config("line_art")

    image_urls = [
        # upload_image("images/team_pic/alex.jpg"),
        # upload_image("images/team_pic/anonymous.jpg"),
        # upload_image("images/team_pic/barry.jpg"),
        # upload_image("images/team_pic/evan.jpg"),
        # upload_image("images/team_pic/lei.jpg"),
        # upload_image("images/team_pic/poppy.jpg"),
        # upload_image("images/team_pic/xin.jpg"),
        # upload_image("images/team_pic/yiwen.jpg"),
    ]
    prompt_variations = [
        "line art drawing profile picture, minimalist, professional, sleek, modern, graphic, line art",
    ]
    guidance_scale_range = [5, 7, 9]
    num_inference_steps_range = [30, 50, 70]
    width_height_pairs = [(512, 512), (1024, 1024)]

    results = []
    experiment_folder = os.path.join("experiments", f"line_art_{uuid.uuid4().hex[:8]}")
    os.makedirs(experiment_folder, exist_ok=True)

    def run_experiment(image_url, prompt, guidance_scale, num_inference_steps, width, height):
        config = base_config.copy()
        config.update(
            {
                "prompt": prompt,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps,
                "width": width,
                "height": height,
                "image": image_url,
            }
        )

        if config["image"] is None:
            print(f"Skipping experiment due to image upload failure: {config}")
            return None

        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = run_instant_id(config)
                if result and isinstance(result, list) and len(result) > 0:
                    result_url = result[0]
                    image_name = os.path.splitext(os.path.basename(image_url))[0]
                    filename = f"{image_name}_p{prompt_variations.index(prompt)}_g{guidance_scale}_s{num_inference_steps}_w{width}_h{height}.jpg"
                    file_path = os.path.join(experiment_folder, filename)

                    response = requests.get(result_url, timeout=30)
                    if response.status_code == 200:
                        with open(file_path, "wb") as f:
                            f.write(response.content)
                        print(f"Generated and saved image: {filename}")
                        return {"config": config, "result_url": result_url, "file_path": file_path}
                    else:
                        print(f"Failed to download image for config: {config}")
                else:
                    print(f"No valid result for config: {config}")
            except Exception as e:
                print(f"Error with config {config} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt == max_retries - 1:
                    print("Max retries reached. Skipping this configuration.")

        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for image_url in image_urls:
            for prompt in prompt_variations:
                for guidance_scale in guidance_scale_range:
                    for num_inference_steps in num_inference_steps_range:
                        for width, height in width_height_pairs:
                            futures.append(
                                executor.submit(
                                    run_experiment,
                                    image_url,
                                    prompt,
                                    guidance_scale,
                                    num_inference_steps,
                                    width,
                                    height,
                                )
                            )

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    return results, experiment_folder


if __name__ == "__main__":
    image_path = "images/prompt/2.jpg"
    results, experiment_folder = explore_hyperparameters(image_path)
    print(f"Experiment results saved in: {experiment_folder}")
    print(f"Total configurations tested: {len(results)}")
