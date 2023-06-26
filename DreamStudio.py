import streamlit as st
from PIL import Image
import requests
import io
import os
import warnings
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from io import BytesIO

stability_api = client.StabilityInference(
    key='sk-pfDu0gbnTExXFPJQ30Zp4FGBTVhm4gLMHRc6vFKdBjF3JPCA', 
    verbose=True, 
    engine="stable-diffusion-xl-beta-v2-2-2", 
)


st.title("What do you want to see?")
prompt = st.text_area("Prompt")
button = st.button("Generate")
if button and prompt:
    
    with st.spinner("Loading..."):
        try:
            answers = stability_api.generate(
                prompt=prompt,
                seed=892226758, 
                steps=30, 
                cfg_scale=8.0, 
                width=512,
                height=512, 
                sampler=generation.SAMPLER_K_DPMPP_2M 
            )
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        warnings.warn(
                            "Your request activated the API's safety filters and could not be processed."
                            "Please modify the prompt and try again.")
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        global img
                        img = Image.open(io.BytesIO(artifact.binary))
                        img.save(str(artifact.seed)+ ".png")
                        st.image(img, caption="Image")
        except:
            st.error("Error")
    
