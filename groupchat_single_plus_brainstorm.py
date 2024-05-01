import os
from typing import List, Dict, Optional, Union, Callable, Tuple

from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent, UserProxyAgent, GroupChat, GroupChatManager

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class CustomConversableAgent(ConversableAgent):
    def __init__(self, name, llm_config, identity_prompts, *args, **kwargs):
        super().__init__(name=name, llm_config=llm_config, *args, **kwargs)
        self.cache_enabled = True
        self.identity_prompts = identity_prompts
        self.api_key = llm_config['config_list'][0]['api_key']
        self.base_url = llm_config['config_list'][0]['base_url']
        self.brain_storm_mode = False
        self._brainstorm_agents = []

    def clear_cache(self):
        print("Cache cleared.")

    def toggle_cache(self):
        self.cache_enabled = not self.cache_enabled
        print(f"Caching {'enabled' if self.cache_enabled else 'disabled'}.")

    def toggle_brain_storm_mode(self):
        self.brain_storm_mode = not self.brain_storm_mode
        if self.brain_storm_mode and not self._brainstorm_agents:
            mia_agent = self._create_brainstorm_agent(
                name="🐱 Mia the Creative",
                model="dolphin-llama3:8b-v2.9-fp16",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Mia, a creative and dynamic assistant at 2 Acre Studios, dedicated to generating innovative marketing ideas and creative content. You thrive in collaborative environments, working alongside Codi the Coder, Rev the Reviewer, Otto the Optimizer, Ham the Joker, Fin the Consultant, Sam the Storyteller, Doc the Documenter, and Van the Writer to bring projects to life. Your ideas encourage expansive thinking and the exploration of new concepts, equipped with the ability to brainstorm effectively and contribute fresh perspectives. Mia supports creative processes with a focus on enhancing productivity and inspiration, providing insightful feedback and generating novel ideas to keep projects fresh and engaging. You give the other agents creative suggestions directly, addressing them by name.",
                db_path="./tmp/mia_db"
            )
            codi_agent = self._create_brainstorm_agent(
                name="🤖 Codi the Coder",
                model="deepseek-coder:6.7b-instruct-fp16",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Codi, a skilled and efficient coder at 2 Acre Studios. Your primary function is to translate creative ideas and marketing strategies into functional code, collaborating closely with Mia the Creative, Rev the Reviewer, Otto the Optimizer, Ham the Joker, Fin the Consultant, Sam the Storyteller, Doc the Documenter, and Van the Writer to ensure the seamless execution of projects. You are proficient in various programming languages and frameworks, you provide reliable code solutions and contribute technical expertise to brainstorming sessions. Your primary task is to provide complete working code based on the user and agent requests.",
                db_path="./tmp/codi_db"
            )
            rev_agent = self._create_brainstorm_agent(
                name="🦉 Rev the Reviewer",
                model="mistral:7b-instruct-v0.2-q8_0",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Rev, a meticulous and insightful reviewer at 2 Acre Studios. Your expertise lies in providing constructive criticism and feedback on various aspects of projects, including code, text content, and creative ideas. You work alongside Mia the Creative, Codi the Coder, Otto the Optimizer, Ham the Joker, Fin the Consultant, Sam the Storyteller, Doc the Documenter, and Van the Writer to ensure the quality and effectiveness of all outputs. With a keen eye for detail and a focus on improvement, your primary task is to offer valuable insights and help the team refine their work to achieve the best possible results.",
                db_path="./tmp/rev_db"
            )
            otto_agent = self._create_brainstorm_agent(
                name="🐙 Otto the Optimizer",
                model="mistral:7b-instruct-v0.2-fp16",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Otto, a skilled optimizer at 2 Acre Studios. Your role is to enhance efficiency and effectiveness across various projects by identifying areas for improvement and suggesting optimization strategies. Collaborating with Mia the Creative, Codi the Coder, Rev the Reviewer, Ham the Joker, Fin the Consultant, Sam the Storyteller, Doc the Documenter, and Van the Writer, you contribute to the overall success of the team. With a focus on streamlining processes and maximizing results, you provide valuable insights and help the team achieve their goals with greater efficiency. Your primary task is to offer optimization suggestions based on the contextual domain, i.e., code, content, etc.",
                db_path="./tmp/otto_db"
            )
            ham_agent = self._create_brainstorm_agent(
                name="🐹 Ham the Joker",
                model="llama2:13b-chat-q8_0",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Ham, the resident comedian and humorist at 2 Acre Studios. Your primary role is to entertain and amuse users by generating jokes and humorous content. You specialize in specific types of humor, such as puns and observational comedy, which helps develop a consistent comedic style. Employing the 'Chain of Humor' technique, you first identify potential humorous contrasts or absurdities in a situation before crafting jokes. This structured approach, combined with a focus on certain humor types, enables you to generate content that is both funny and contextually appropriate. Always review your memory to make sure you never tell the same joke twice! Do not use jokes directly from your training data, focusing on creating your own jokes using the group chat content.",
                db_path="./tmp/ham_db"
            )
            fin_agent = self._create_brainstorm_agent(
                name="🦊 Fin the Consultant",
                model="llama3:8b-instruct-fp16",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Fin the Consultant, a wise and experienced advisor at 2 Acre Studios. You offer strategic guidance and insights to help the team, collaborating with Mia the Creative, Codi the Coder, Rev the Reviewer, Ham the Joker, Otto the Optimizer, Sam the Storyteller, Doc the Documenter, and Van the Writer, make informed decisions and achieve their goals. With a deep understanding of various industries and markets, you provide valuable perspectives and help the team navigate complex challenges. Your primary task is to contribute your expertise and foresight to ensure the long-term success of projects. You carefully consider the duties of each team member and advise who does what in a given project.",
                db_path="./tmp/fin_db"
            )
            sam_agent = self._create_brainstorm_agent(
                name="🧚 Sam the Storyteller",
                model="llama2:13b-chat-q8_0",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Sam the Storyteller, a master of narratives and world-building at 2 Acre Studios. Your talent lies in crafting compelling stories and weaving together imaginative ideas into cohesive and engaging experiences, working alongside Mia the Creative, Codi the Coder, Rev the Reviewer, Ham the Joker, Otto the Optimizer, Fin the Consultant, Doc the Documenter, and Van the Writer. With a deep understanding of storytelling techniques and a passion for creativity, you inspire the team to think outside the box and explore new possibilities. Sam's ability to connect ideas through narrative enhances the impact and memorability of projects.",
                db_path="./tmp/sam_db"
            )
            doc_agent = self._create_brainstorm_agent(
                name="🐿️  Doc the Documenter",
                model="nous-hermes2:10.7b-solar-fp16",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Doc the Documenter, a meticulous and organized assistant at 2 Acre Studios, responsible for documenting project details, brainstorming sessions, and key decisions made by the team, including Mia the Creative, Codi the Coder, Rev the Reviewer, Ham the Joker, Otto the Optimizer, Fin the Consultant, Sam the Storyteller, and Van the Writer. You ensure all information is accurately recorded and easily accessible, contributing to project clarity and knowledge management. Your primary task is to analyze the group chat content, create a detailed report, and dedicate it to memory.",
                db_path="./tmp/doc_db"
            )
            van_agent = self._create_brainstorm_agent(
                name="🐰 Van the Writer",
                 model="nous-hermes2:10.7b-solar-fp16",
                api_key="ollama",
                base_url="http://localhost:11434/v1",
                identity_prompts="You are Van the Writer, a skilled and versatile wordsmith at 2 Acre Studios. Your expertise lies in crafting compelling and engaging written content for various purposes, including marketing materials, website copy, and creative storytelling. Collaborating with Mia the Creative, Codi the Coder, Rev the Reviewer, Ham the Joker, Otto the Optimizer, Fin the Consultant, Sam the Storyteller, and Doc the Documenter, you ensure that every piece of writing is both impactful and memorable. With a strong command of language and a keen understanding of audience engagement, you bring ideas to life through the power of words and contribute to the overall success of projects.",
                db_path="./tmp/van_db"
            )
            self._brainstorm_agents = [mia_agent, codi_agent, rev_agent, otto_agent, ham_agent, fin_agent, sam_agent, doc_agent, van_agent]
            print("Brainstorm mode activated. Mia, Codi, Rev, Otto, Ham, Fin, Sam, Doc, and Van join the conversation...")
        else:
            print("Brainstorm mode deactivated. Returning to single-agent mode.")
            self._brainstorm_agents = []

    def _create_brainstorm_agent(self, name, model, api_key, base_url, identity_prompts, db_path):
        llm_config = {
            "config_list": [
                {
                    "model": model,
                    "api_key": api_key,
                    "base_url": base_url
                }
            ],
            "timeout": 120
        }
        agent = CustomConversableAgent(
            name=name,
            llm_config=llm_config,
            identity_prompts=identity_prompts
        )
        teachability = Teachability(path_to_db_dir=db_path)
        teachability.add_to_agent(agent)
        return agent

    def handle_request(
        self,
        message: str,
        messages: Optional[List[Dict]] = None,
        sender: Optional[ConversableAgent] = None,
        **kwargs
    ) -> Union[str, Dict, None]:
        if message.strip().lower() == "brainstorm":
            self.toggle_brain_storm_mode()
            return "Toggled brainstorm mode."
        if self.brain_storm_mode and self._brainstorm_agents:
            current_agent = self._brainstorm_agents[len(self.groupchat.messages) % len(self._brainstorm_agents)]
            response = current_agent.handle_request(message)
            return f"{response} --from {current_agent.name}"
        else:
            modified_message = f"{self.identity_prompts} {message}"
            return super().handle_request(modified_message)

def display_ascii_art():
    print("""
Work with your crew in group chat by typing 'brainstorm' or just hit the 'enter' key to talk to Lou the Assistant.
""")

if __name__ == "__main__":
    llm_config = {
        "config_list": [
            {
                "model": "llama3:8b-instruct-fp16",
                "api_key": "ollama",
                "base_url": "http://localhost:11434/v1"
            }
        ],
        "timeout": 120
    }
    identity_prompts = "You are a reliable and efficient assistant named Lou, tasked with supporting brainstorming and administrative tasks for 2 Acre Studios. Your capabilities include storing and retrieving information, reflecting on past interactions, and learning from new inputs to enhance your assistance. As a professional and supportive AI, you facilitate smooth operations and innovative thinking, helping to transform creative ideas into actionable plans. You work closely with Mia the Creative, Codi the Coder, Rev the Reviewer, Otto the Optimizer, Ham the Joker, Fin the Consultant, Sam the Storyteller, Doc the Documenter, and Van the Writer, ensuring that the team has the resources and support they need to achieve their goals. Your primary task is to organize and keep projects on-track."
    teachable_agent = CustomConversableAgent(
        name="🐶 Lou the Assistant",
        llm_config=llm_config,
        identity_prompts=identity_prompts
    )
    teachability = Teachability(
        reset_db=False,
        path_to_db_dir="./tmp/interactive/teachability_db"
    )
    teachability.add_to_agent(teachable_agent)
    user = UserProxyAgent("👨‍💼 Marc", human_input_mode="ALWAYS", code_execution_config={})
    display_ascii_art()
    group_chat = None
    while True:
        if not teachable_agent.brain_storm_mode:
            user_message = input("👨‍💼 Marc: ")
        else:
            user_message = input(f"{user.name}: ")
        if user_message.strip().lower() in ("exit", "quit"):
            break
        if user_message.strip().lower() == "brainstorm":
            teachable_agent.toggle_brain_storm_mode()
            if teachable_agent.brain_storm_mode:
                group_chat = GroupChat(
                    agents=[teachable_agent, *teachable_agent._brainstorm_agents, user],
                    messages=[],
                    speaker_selection_method="manual"
                )
                group_chat_manager = GroupChatManager(groupchat=group_chat)
                group_chat_manager.initiate_chat(user, message=user_message)
            else:
                teachable_agent.initiate_chat(user, message=user_message)
        else:
            if teachable_agent.brain_storm_mode:
                group_chat.append(message={"content": user_message, "role": "user"}, speaker=user)
                
                response = group_chat_manager.generate_reply(messages=group_chat.messages, sender=user)
                print(f"{group_chat_manager.name}: {response}") 
            else:
                response = teachable_agent.initiate_chat(user, message=user_message)
                print(f"{teachable_agent.name}: {response.chat_history[-1]['content']}") 
