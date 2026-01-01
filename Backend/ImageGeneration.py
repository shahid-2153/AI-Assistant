import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
import io
from time import sleep

def open_image(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

API_URL = "https://router.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(
        requests.post,
        API_URL,
        headers=headers,
        json=payload
    )

    content_type = response.headers.get("content-type", "")

    # ✅ Only return bytes if it's an image
    if "image" in content_type:
        return response.content

    # ❌ Otherwise print error and return None
    try:
        print("HF Error:", response.json())
    except Exception:
        print("HF Error (raw):", response.text)

    return None


async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4k, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        await asyncio.sleep(1)
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        image_path = fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg"

        try:
            if image_bytes is None:
                print(f"Skipping image {i+1} (no valid image data)")
                continue

            img = Image.open(io.BytesIO(image_bytes))
            img.save(image_path, "JPEG")
            print(f"Saved image: {image_path}")
        except Exception as e:
            print(f"Error saving image {i+1}: {e}")

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_image(prompt)

print("Waiting for input in ImageGeneration.data...")

while True:
    try:
        if not os.path.exists(r"Frontend/Files/ImageGeneration.data"):
            print("Waiting for ImageGeneration.data file to be created...")
            sleep(1)
            continue  

        with open(r"Frontend/Files/ImageGeneration.data", "r") as f:
            Data = f.read().strip()

        if not Data:  
            sleep(1)
            continue

        if "," in Data:
            Prompt, Status = Data.split(",", 1)
            Prompt, Status = Prompt.strip(), Status.strip()
        else:
            print("Invalid data format in ImageGeneration.data. Waiting for valid input...")
            sleep(1)
            continue  

        if Status.lower() == "true":
            print(f"Generating Images for prompt: {Prompt}")
            GenerateImages(prompt=Prompt)

            with open(r"Frontend/Files/ImageGeneration.data", "w") as f:
                f.write("False,False")  

        else:
            sleep(1)  

    except Exception as e:
        print(f"Unexpected Error: {e}")
        sleep(1)
