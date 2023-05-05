import sys
import gradio as gr
import random
import time
import hashlib
from datetime import datetime

sys.path.append("./")
from src.util import agent_logs, get_epoch_time


class WebUI:
    """a simple and awesome ui to display agent actions and thought processes"""

    gradio_app = None
    shared_chat_history = None

    def __init__(self, func, ui_type="garage_day_idea"):
        # clear old logs
        agent_logs.clear_log()
        # initialize app layouts
        if ui_type == "garage_day_idea":
            self.gradio_app = self._init_garage_day_idea(
                self._clear_log_before_func(func)
            )
        # initialize chat history
        self.customer_chat_history = []
        self.agent_chat_history = []
        # last message sent
        self.last_customer_query_msg = ""
        self.last_agent_response_msg = ""

    @staticmethod
    def _clear_log_before_func(func):
        def inner1(prompt):
            # clear old logs
            agent_logs.clear_log()
            return func(prompt)

        return inner1

    def generate_response(self, input_text):
        bot_message = random.choice(
            [
                "How are you?",
                "I am well, thank you for asking",
                "It's a great day.",
            ]
        )

        return bot_message

    def respond(self, message, chat_history):
        self.customer_chat_history = chat_history
        self.last_customer_query_msg = message
        self.agent_chat_history.append(
            (self.last_agent_response_msg, self.last_customer_query_msg)
        )
        # insert chatbot interruption
        return "", self.agent_chat_history

    def agent_respond(self, message, chat_history):
        self.agent_chat_history = chat_history
        self.last_agent_response_msg = message
        self.customer_chat_history.append(
            (self.last_customer_query_msg, self.last_agent_response_msg)
        )
        # # revise agent chat
        # self.agent_chat_history = self.agent_chat_history[:-1]
        # self.agent_chat_history.append(
        #     (self.last_agent_response_msg, self.last_customer_query_msg)
        # )
        return "", self.customer_chat_history

    def _init_garage_day_idea(self, func):
        # resource:
        # - https://gradio.app/theming-guide/#discovering-themes
        # - https://gradio.app/quickstart/#more-complexity
        # - https://gradio.app/reactive-interfaces/
        # - https://gradio.app/blocks-and-event-listeners/
        # - https://gradio.app/docs/#highlightedtext

        with gr.Blocks(theme="sudeepshouche/minimalist") as demo:
            gr.Markdown("# TextTransit Instant Messenging System")
            thought_out = None
            # with gr.Tab("Demo"):
            with gr.Row():
                with gr.Column(scale=1, min_width=600):
                    with gr.Tab("Customer"):
                        customer_chat = gr.Chatbot(
                            label="Customer Feedback",
                            interactive=True,
                            lines=6,
                            # value="Buses constantly late, missed important meetings.",
                        )
                        customer_msg = gr.Textbox()
                        customer_send = gr.Button("Send to TransLink")
                        clear = gr.Button("Clear")
                        # text_input = gr.Textbox(
                        #     info="Your thoughts are important to us, please tell us about your transit experience.",
                        #     placeholder="Enter here",
                        #     lines=3,
                        #     value="Buses constantly late, missed important meetings.",
                        # )
                        # text_button.click(func, inputs=text_input, outputs=text_output)
                        # text_button = gr.Button("Send Feedback")
                        # text_output = gr.Textbox(lines=5, label="Automated response")

                    with gr.Tab("TransLink Staff"):
                        server_status = gr.Radio(
                            ["online", "offline"],
                            label="Status",
                            value="online",
                            interactive=True,
                            info="Set offline to delegate automated response to Bot.",
                        )
                        agent_chat = gr.Chatbot(
                            label="Current Chat with Customer",
                            interactive=True,
                            lines=6,
                        )
                        agent_msg = gr.Textbox()
                        # revise_chat = gr.Button("Request Revision")
                        agent_send = gr.Button("Send to Customer")
                        # clear = gr.Button("Clear")
                        # revise_chat.click(respond, [msg, chatbot], [msg, chatbot])
                        # server_status.change(filter, server_status, [rowA, rowB, rowC])
                        # clear.click(lambda: None, None, chatbot, queue=False)

                    with gr.Tab("Virtual Assistant"):
                        with gr.Column(scale=1, min_width=600):
                            thought_out = gr.HTML(
                                label="Thought Process", scroll_to_output=True
                            )
                            customer_chat.change(
                                self.get_thought_process_log,
                                inputs=[],
                                outputs=thought_out,
                                queue=True,
                                every=1,
                            )

            #         with gr.Tab("Administrator"):
            #             shutdown_server = gr.Button("Shutdown Server")
            # shutdown_server.click(demo.close)

            customer_msg.submit(
                self.respond, [customer_msg, customer_chat], [agent_msg, agent_chat]
            )
            customer_send.click(
                self.respond, [customer_msg, customer_chat], [agent_msg, agent_chat]
            )
            agent_msg.submit(
                self.agent_respond,
                [agent_msg, agent_chat],
                [customer_msg, customer_chat],
            )
            agent_send.click(
                self.agent_respond,
                [agent_msg, agent_chat],
                [customer_msg, customer_chat],
            )
            clear.click(lambda: None, None, customer_chat, queue=False)
        return demo

    def get_thought_process_log(self):
        langchain_log = agent_logs.read_log()
        process_html = langchain_log
        # clean up new lines
        process_html = (
            process_html.replace(" \n", "\n")
            .replace("\n\n\n", "\n")
            .replace("\n\n", "\n")
            .replace(": \n", ": ")
            .replace(":\n", ": ")
        )
        # convert new lines to html
        process_html = process_html.replace("\n", "<br>")
        # add colors to different content
        # https://htmlcolors.com/color-names
        # color Tools Available Black
        process_html = process_html.replace(
            "Tools available:", """<p style="color:Black;">Tools available:"""
        )
        # color Question Black
        process_html = process_html.replace(
            "Question:", """</p><p style="color:Black;">Question:"""
        )
        process_html = process_html.replace(
            "Query:", """</p><p style="color:#348017;">Query:"""
        )
        # color Thought Medium Forest Green
        process_html = process_html.replace(
            "Thought:", """</p><p style="color:#348017;">Thought:"""
        )
        # color Action Bee Yellow
        process_html = process_html.replace(
            "Action:", """</p><p style="color:#E9AB17;">Action:"""
        )
        # color Action Bee Yellow
        process_html = process_html.replace(
            "Action Input:", """</p><p style="color:#E9AB17;">Action Input:"""
        )
        # color Observation Denim Dark Blue
        process_html = process_html.replace(
            "Observation:", """</p><p style="color:#151B8D;">Observation:"""
        )
        # color Observation Black
        process_html = process_html.replace(
            "Final Answer:", """</p><p style="color:Black;"><b>Final Answer</b>:"""
        )
        # color Answer Denim Dark Blue
        process_html = process_html.replace(
            "Answer:", """</p><p style="color:#151B8D;">Answer:"""
        )
        # add closing p
        process_html = f"""{process_html}</p>"""
        return process_html

    @staticmethod
    def generate_auth():
        temp_user = "test"
        temp_password = hashlib.md5(str(get_epoch_time()).strip().encode()).hexdigest()
        auth = (temp_user, temp_password)
        print(f"A temporary auth value as been generated: {auth}")
        return auth

    def launch(
        self,
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=False,
        prevent_thread_lock=False,
        auth=None,
        share=False,
    ):
        if share == True and auth is None:
            auth = self.generate_auth()
        self.gradio_app.queue().launch(
            server_name=server_name,
            server_port=server_port,
            inbrowser=inbrowser,
            prevent_thread_lock=prevent_thread_lock,
            auth=auth,
            share=share,
        )


if __name__ == "__main__":

    def test_func(prompt):
        answer = f"Question: {prompt}\nThis is a test output."
        import time

        time.sleep(5)
        return answer

    # test this class
    ui_test = WebUI(test_func)
    ui_test.launch(server_name="0.0.0.0", server_port=7860)
