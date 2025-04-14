from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .course_generator import take_user_input_and_create_course, generate_mindmap_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CourseRequest(BaseModel):
    topic: str
    difficulty: str

@app.post("/generate-course/")
async def generate_course(request: CourseRequest):
    try:
        course_content = take_user_input_and_create_course(request.topic, request.difficulty)
        if isinstance(course_content, str):
            import json
            # This will raise an error if the JSON is invalid
            course_content = json.loads(course_content)
        
        return course_content
    
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON generated: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-mindmap/")
async def generate_mindmap(course_content: dict):
    try:
        mindmap_data = generate_mindmap_data(course_content)
        if not mindmap_data:
            raise HTTPException(status_code=500, detail="Failed to generate mindmap data")
        return mindmap_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



