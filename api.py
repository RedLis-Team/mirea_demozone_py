import base64
import io
from deepl import DeepLCLI
from fastapi import FastAPI, Response, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status


from controller import Controller

from sdxl import generate_image

files = Controller()

app = FastAPI(
	debug=True,
)

origins = [
	"http://localhost",
	"http://localhost:8000",
	"http://localhost:3000",
	"http://localhost:8080",
	"http://0.0.0.0:8080",
	"http://77.37.239.19:8080",
	"91.227.189.14:5173"
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

@app.get("/", status_code=status.HTTP_421_MISDIRECTED_REQUEST)
def read_root():
	return Response(status_code=status.HTTP_421_MISDIRECTED_REQUEST)

# @app.post("/loadsound")
# def load_sound(file: UploadFile):
# 	#TODO add validate file
# 	files.write(file, "input.wav", no_check=True)
	
@app.post("/run")
async def processing(text: str):
	deepl = DeepLCLI("ru", "en")
	text = await deepl.translate_async(text)
	image = generate_image(text)
	f = open(f'{files.files_path}/answer.jpeg', 'wb')
	f.write(image)
	f.close()
	# print(image)
	
	# buff = io.BytesIO()
	# return status.HTTP_200_OK
	# return Response(
	# 	# base64.b64encode(buff.getvalue()).decode("utf-8"),
	# 	image,
	# 	media_type="image/jpeg",
	# 	headers={"Cache-Control": "no-cache", "name": "answer.wav", "file-type": "image/jpeg", "type": "image/jpeg"},
	# 	status_code=status.HTTP_200_OK
	# )
	return "answer.jpeg"

@app.get("/answer")
async def get_image() -> Response:  # As long as we don't use the file server, don't touch it!!!
    return Response(  # As long as we don't use the file server, don't touch it!!!
        files.read("answer.jpeg"),
        media_type="image/jpeg",
        headers={"Cache-Control": "no-cache", "name": "answer.jpeg", "file-type": "image/jpeg", "type": "image/jpeg"},
        status_code=status.HTTP_200_OK
    ) 

# @app.get("/answer")
# def get_ans():
#     return Response(
# 		files.read("answer.wav"),
# 		media_type="audio/wav",
# 		headers={"Cache-Control": "no-cache", "name": "answer.wav", "file-type": "audio/wav", "type": "audio/wav"},
# 		status_code=status.HTTP_200_OK
# 	)
