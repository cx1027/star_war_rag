# star_war_rag
Instructions:
1. setup an visual environment by
python3 -m venv rag
source rag/bin/activate  (Mac)
myenv\Scripts\activate (Windows)
2. install dependencies by
pip install -r requirements.txt
3. Run main.py to lanch the project
4. Enter the question in command line:Who is Luke Skywalker’ s father?
5. The expected message should be
{
  "user_prompt": "Who is Luke Skywalker \u2019 s father ?",
  "retrieved_context": "Luke Skywalker is a Jedi Knight and the son of Anakin Skywalker, who became Darth Vader",
  "system_response": "Anakin Skywalker, Luke's father is, hmmm. Yes, yes, Darth Vader became he did."
}
where the system_response can be slightly different, as the LLMs generate response randomly each time.

Notice:
1. Answer can be silight different each time, as the LLMs generate answers randomly
2. When run it first time, it takes a little bit long to download the sentence-transformers model
3. In function generate_response, the model="Gpt4o" if use API from Datacom, model="gpt-4o", if use API from OpenAI account