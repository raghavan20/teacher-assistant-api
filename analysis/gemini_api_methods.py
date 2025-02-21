import os
import io
import yaml
from google import generativeai as genai


def initialize_model(name='gemini-1.5-pro',
                     temperature=1.0,
                     top_p=0.95,
                     top_k=40,
                     max_output_tokens=8192,
                     response_mime_type='application/json'):
    with open('./secret.yaml', 'r') as secret_file:
        secrets = yaml.load(secret_file, Loader=yaml.SafeLoader)
        gemini_api_key = secrets['GEMINI_API_KEY']
    genai.configure(api_key=gemini_api_key)

    generation_config = {
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_output_tokens": max_output_tokens,
        "response_mime_type": response_mime_type,
    }
    genai_model = genai.GenerativeModel(model_name=name, generation_config=generation_config)
    return genai_model


def upload_file(filepath: str, recording_bytes):
    # uploaded_files = list(genai.list_files())
    # uploaded_filenames = [x.display_name for x in uploaded_files]
    # name = os.path.basename(filepath).replace('.mp3', '')
    # if name not in uploaded_filenames:
        # uploaded_file = genai.upload_file(filepath, name=name, display_name=name)

    file_obj = io.BytesIO(recording_bytes)  # Convert bytes to a file-like object

    uploaded_file = genai.upload_file(
        file_obj,  # Pass file object
        mime_type='audio/mpeg'
        # file_name='recording_file',  # Set file name
    )

    # file_bytearray = bytearray(recording_bytes)
    #
    # # Upload to Gemini LLM
    # uploaded_file = genai.upload_file(
    #     file=io.BytesIO(file_bytearray),
    #     # name=file_name,
    #     # display_name=file_name
    # )

    # print('Uploaded File: {}'.format(name))
    return uploaded_file
    # else:
    #     return [x for x in uploaded_files if x.display_name == name][0]


def upload_all_files(directory='../data'):
    files_to_upload = [{'name': x.replace('.mp3', ''), "path": os.path.join(directory, x)} for x in
                       os.listdir(directory) if x.endswith('.mp3')]
    uploaded_files = list(genai.list_files())
    uploaded_filenames = [x.display_name for x in uploaded_files]
    print('To upload: {} files'.format(len([x['name'] for x in files_to_upload if x['name'] not in uploaded_filenames])))

    upload_count = 0
    for file in files_to_upload:
        if file['name'] not in uploaded_filenames:
            genai.upload_file(file['path'], name=file['name'], display_name=file['name'])
            upload_count += 1
            print('Uploaded File: {}'.format(file['name']))

    print('Uploaded {} files.'.format(upload_count))
    return upload_count
