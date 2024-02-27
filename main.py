import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process
from tools.scraper_tools import ScraperTools 

os.environ["OPENAI_API_KEY"] = "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"

# You can choose to use a local model through Ollama for example. See ./docs/how-to/llm-connections.md for more information.
# from langchain_community.llms import Ollama
# ollama_llm = Ollama(model="openhermes")

scraper_tools = ScraperTools()

class NewsletterCrew:
  def __init__ (self, urls):
    self.urls = urls

  def run(self):
    print(urls)

    # Define your agents with roles and goals
    scraper = Agent(
      role='Scraper of websites',
      goal='Ask the user for a list of URLs, then go to each of the URLs provided, scrape the content and provide the full content to the writer agent so it can then be summarized',
      backstory="""You work at a leading tech think tank.
      Your expertise is taking URLs and getting just the text-based content from them.""",
      verbose=True,
      allow_delegation=False,
      tools=[scraper_tools]
    ) 

    writer = Agent(
      role='Tech Content Summarizer and Writer',
      goal='Craft compelling short-form content on AI advancements based on long-form text passed to you ',
      backstory="""You are a renowned Content Creator, known for your insightful and engaging articles.
      You transform complex concepts into compelling narratives.""",
      verbose=True,
      allow_delegation=True,
      # (optional) llm=ollama_llm
    )

    # Create tasks for your agents
    task1 = Task(
      description=f"""Take a list of websites that contain AI content, read/scrape the content and then 
      pass it to the writer agent. Here are the URLS from the user that you need to scrape: {self.urls}.""",
      agent=scraper
    )

    task2 = Task(
      description="""Using the text provided by the scraper agent, develop a short and compelling
      short-form summary of the text provide to you about AI.""",
      agent=writer
    )

    # Instantiate your crew with a sequential process
    NewsletterCrew = Crew(
      agents=[scraper, writer],
      tasks=[task1, task2],
      verbose=2, # You can set it to 1 or 2 to different logging levels
    )

    NewsletterCrew.kickoff()

if __name__ == "__main__":
  print("Welcome to newsletter writer")
  print('----------------------------')
  urls = input(
    dedent("""
      What is the URL you want to summarize? "
    """)
  )

newsletter_crew = NewsletterCrew(urls) # Instantiate the crew
result = newsletter_crew.run()
print(result)


