from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class BelgeAnalizProjesi():
	"""Belge Analiz Projesi ekibi"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def ozetleyici(self) -> Agent:
		return Agent(
			config=self.agents_config['ozetleyici'],
			verbose=True
		)

	@agent
	def hukuk_analisti(self) -> Agent:
		return Agent(
			config=self.agents_config['hukuk_analisti'],
			verbose=True
		)

	@task
	def ozetleme_gorevi(self) -> Task:
		return Task(
			config=self.tasks_config['ozetleme_gorevi'],
		)

	@task
	def hukuki_analiz_gorevi(self) -> Task:
		return Task(
			config=self.tasks_config['hukuki_analiz_gorevi'],
			output_file='hukuki_rapor.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Belge Analiz Ekibi oluşturma"""

		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True
		)
