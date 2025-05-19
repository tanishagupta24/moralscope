class MoralMemory:
    def __init__(self):
        self.past_judgments = []

    def store_judgment(self, dilemma, framework, judgment, justification):
        self.past_judgments.append({
            "dilemma": dilemma,
            "framework": framework,
            "judgment": judgment,
            "justification": justification
        })
