# chain example A prompts
# TRIAGE_PROCESS_A1 = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

# ### Instruction:
# Provide a list of names of fictitious companies that make {input}.

# ### Response:
# """

TRIAGE_PROCESS_A1 = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
You need to categorize the following question:
{input}

Pick one category only

### Input:
- Facilities: cleaning or broken things, or deal with security issues.
- Planning: services, bus delays, train delays, cannot get on bus or train.
- Customer Information: general information about translink including policies on fare or services available in the region.
- Compass Card: paying for transit fare on buses and skytrains, inquiry about card balances, cost of taking transit.

### Response:
The category would fall under: """

TRIAGE_PROCESS_A2 = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
You need to categorize the following question:
{input}

Pick one category only

### Input:
- Urgent: time sensitive and require immediate response
- Informational: not time sensitive and is a general inquiry

### Response:
The category would fall under: """

TRIAGE_PROCESS_A3 = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Please provide an answer for this question.

### Input:
{input}

### Response:"""

# chain example B prompts
TRIAGE_PROCESS_B1 = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
You will be provided with some of your memories. Given the memories provided, please answer this question: {input}?

### Input:
Here are some of my memories from my notes ... {task1_summaries}

### Response:
"""

TRIAGE_PROCESS_B2 = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
What is a follow up question that you can ask to learn more about from following fact?

### Input:
{task1_output}

### Response:
To learn more about this fact, this is the question I would ask: """

TRIAGE_PROCESS_B3 = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Given the facts provided, please answer this question: {input}?
In response to this question, you asked the following follow-up question, and obtained information from Google Search below: {task2_output}

### Input:
Information obtained from Google Search ... {task3_summaries}

### Response:
"""
