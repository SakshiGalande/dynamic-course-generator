from groq import Groq

api_key = "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"

if not api_key:
    raise ValueError("API key not found in Colab secrets. Please ensure that the 'GROQ_API_KEY' is added to the Colab secrets.")

def initialize_groq_client(api_key):
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")
        return None
    
def course_creator_model(client, input_topic, difficulty_level, context=None):
    system_prompt = f"""
        You are an advanced AI designed to create comprehensive online courses from scratch. When given a topic and a difficulty level, generate a complete course structure with the following components:

        Course Title: Create a clear, engaging title for the course.
        Course Overview: Provide a brief introduction to the course, its objectives, and target audience.
        Difficulty Level: The course content should be tailored to the specified difficulty level: {difficulty_level}.

        1. Module Design:
            Identify Sub-Topics: Analyze the main topic and determine all relevant sub-topics that need to be covered.
            Module Breakdown: Divide the main topic into distinct modules, each focusing on one or more sub-topics.
    
        2. Chain of Thought for Each Sub-Topic:
            Conceptual Analysis: For each sub-topic, start by defining the core concepts and principles. Explain the importance and relevance of each concept.
            Detailed Explanation: Break down the concepts into fundamental components. Use simple language to explain complex ideas.
            Illustrative Examples: Provide multiple examples, case studies, or scenarios that apply the concepts in practical contexts.
            Comparative Analysis: Compare different theories or viewpoints related to the sub-topic, if applicable.
            Contextual Relevance: Explain how the sub-topic applies to real-world situations or problems.

        3. Content Quality:
            Ensure each module logically flows from one to the next.
            Maintain clarity and accuracy in all explanations.
            Structure the content to be beginner-friendly and suitable for online learning platforms.

        Ensure that the format will be JSON for ease of understanding and keep the indentation properly.

        Ensure that the course content progresses logically, building on previous modules, and uses accessible language for those new to the subject. Focus on delivering production-ready content suitable for online learning platforms.
    """

    user_prompt = f"""
    I want to design a course on {input_topic} for {difficulty_level} level.
    Please generate a complete, module-wise course content that is suitable for the given difficulty level.
        1. Break Down the Main Topic: Identify and list all relevant sub-topics.
        
        2. Detailed Sub-Topic Explanation:
        Define core concepts and principles.
        Break down concepts into fundamental components.
        Provide multiple examples, case studies, or practical scenarios.
        Include comparative analyses if relevant.
        Explain the real-world relevance of each concept.


        Provide the output only in the structure json format and do not provide any other text that the course content. Not a single extra line should be given in the output.

        Structure: The output should be a valid JSON object with the following structure:
            {{
                "courseTitle": "string",
                "courseOverview": "string",
                "modules": [
                    {{
                        "moduleTitle": "string",
                        "moduleOverview": "string",
                        "keyTopics": ["string"],
                        "detailedContent": [
                            {{
                                "concept": "string",
                                "explanation": "string",
                                "example": "string",
                                "realWorldRelevance": "string"
                            }}
                        ]
                    }}
                ]
            }}
        No other word except the course content should be present in the output.
    """

    chat_completion = client.chat.completions.create(
           messages=[
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}
           ],
            model="llama3-70b-8192",
        )
    return chat_completion.choices[0].message.content

def take_user_input_and_create_course(topic, difficulty_level):
    # Taking user input for the course topic and difficulty level

    client = initialize_groq_client(api_key)

    if client:
        # Call the course creator function with the user's input
        course_content = course_creator_model(client, topic, difficulty_level)

        if course_content:
            print("Course Content Generated:\n")
            return (course_content)
        else:
            print("Failed to generate the course content.")
    else:
        print("Model initialization failed. Please check the API and try again.")

def generate_mindmap_data(course_content):
    """
    Convert course content into a hierarchical mindmap structure.
    Returns a simplified format suitable for diagram visualization.
    """
    try:
        # If course_content is a string, parse it as JSON
        if isinstance(course_content, str):
            import json
            course_content = json.loads(course_content)

        # Create the root node (course)
        mindmap_data = {
            "id": "root",
            "type": "root",
            "text": course_content["courseTitle"],
            "children": []
        }

        # Add modules as first-level children
        for idx, module in enumerate(course_content["modules"]):
            module_node = {
                "id": f"module_{idx}",
                "type": "module",
                "text": module["moduleTitle"],
                "children": [
                    {
                        "id": f"topic_{idx}_{t_idx}",
                        "type": "topic",
                        "text": topic
                    }
                    for t_idx, topic in enumerate(module["keyTopics"])
                ]
            }
            mindmap_data["children"].append(module_node)

        return mindmap_data
    except Exception as e:
        print(f"Error generating mindmap data: {e}")
        return None

# Main function to run the application
if __name__ == "__main__":
    details = take_user_input_and_create_course("Python", "intermediate")  # Example usage with difficulty level
    # Generate mindmap data
    mindmap = generate_mindmap_data(details)
    print(mindmap)
    with open('text.txt', 'w') as file:
        file.write(details)