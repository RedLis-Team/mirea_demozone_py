from fastapi import FastAPI, Response, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette import status


from controller import Controller

from ttso import ttss

files = Controller()

app = FastAPI(
	debug=True,
)

origins = [
	"http://localhost",
	"http://localhost:8000",
	"http://localhost:3000",
	"http://localhost:8080"
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

@app.post("/loadsound")
def load_sound(file: UploadFile):
	#TODO add validate file
	files.write(file, "input.wav", no_check=True)
	
@app.post("/run")
def processing(text: str):
    ttss(text, files.files_path+"input.wav")
    return status.HTTP_200_OK

@app.get("/answer")
def get_ans():
    return Response(
		files.read("answer.wav"),
		media_type="audio/wav",
		headers={"Cache-Control": "no-cache", "name": "answer.wav", "file-type": "audio/wav", "type": "audio/wav"},
		status_code=status.HTTP_200_OK
	)
