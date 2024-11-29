# star_war_rag

## Instructions:
1. git clone the code locally
2. Copy the .env file under common folder (As the api_key under openAI_Datacom.env doesn't work)
- make sure put openAI.env under common folder
- make sure model="gpt-4o" in def generate_response in main.py for OpenAI account 
3. setup an visual environment by
```bash
python3 -m venv rag
source rag/bin/activate  (Mac)
myenv\Scripts\activate (Windows)
```
4. install dependencies by
```bash
pip install -r requirements.txt
```
5. Run main.py to lanch the project
6. Enter the question in command line:Who is Luke Skywalker’ s father?
7. The expected message should be:
```json
{
  "user_prompt": "Who is Luke Skywalker's father ?",
  "retrieved_context": "Luke Skywalker is a Jedi Knight and the son of Anakin Skywalker, who became Darth Vader",
  "system_response": "Anakin Skywalker, Luke's father is, hmmm. Yes, yes, Darth Vader became he did."
}
```
where the system_response can be slightly different, as the LLMs generate response randomly each time.

# Notes:
1. Answer can be silight different each time, as the LLMs generate answers randomly
2. When run it first time, it takes a little bit long to download the sentence-transformers model
3. In function generate_response, the model="Gpt4o" if use API from Datacom, model="gpt-4o", if use API from OpenAI account