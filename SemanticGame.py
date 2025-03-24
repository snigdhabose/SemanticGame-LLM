import os
from llama_cpp import Llama

# Load the LLM (Mistral-7B GGUF model)
llm = Llama(model_path="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")

### **Game Parameters**
MAX_ROUNDS = 5  # Set max number of game rounds

class SemanticGame:
    def __init__(self, relation_set, forbidden_patterns):
        self.RS = relation_set  # Set of allowed logical relations
        self.FPR = forbidden_patterns  # Forbidden pattern rules
        self.tau_history = []  # Tracks values of τ(RS, FPR)
        self.current_tau = None  # Current estimated τ

    def generate_author_move(self):
        """Generates an (RS, FPR)-formula F using LLM."""
        prompt = f"""
            You are the Author in a structured debate about τ(RS, FPR).
            RS = ClausalR(2,2), FPR = TRUE.
            Propose a complete (RS, FPR)-formula F in CNF notation.
            Explicitly state a numerical claim for τ.
            Your output should be:
            1. "Formula F = ..."
            2. "Claimed τ = ..."
            """
        response = llm(prompt, max_tokens=100)  # Fix applied here
        return response["choices"][0]["text"].strip()

    def generate_reviewer_move(self, formula):
        """Reviewer challenges the formula F and finds an assignment J to maximize FractionSat(F, J)."""
        reviewer_prompt = f"""
            You are the Reviewer in a structured debate about τ(RS, FPR).
            The Author's formula is:
            {formula}

            1. If the formula is correct, confirm τ.
            2. If incorrect, provide a counterexample assignment that achieves a higher/lower τ.
            3. If the formula is invalid, explain the logical flaw.
            Your output should be:
            1. "Reviewer Response: ..."
            2. "Revised τ = ..." (if applicable)
            """
        response = llm(reviewer_prompt, max_tokens=100)  # Fix applied here
        return response["choices"][0]["text"].strip()

    def evaluate_tau_change(self, old_tau, new_tau):
        """Tracks how τ evolves over time."""
        if old_tau is None:
            return f"Initial τ estimate: {new_tau}"
        elif new_tau is None:
            return f"New τ value was not found. Assuming it remains at {old_tau}."
        elif new_tau > old_tau:
            return f"Reviewer found a better assignment! τ increased from {old_tau} to {new_tau}."
        elif new_tau < old_tau:
            return f"Author overestimated! τ reduced from {old_tau} to {new_tau}."
        else:
            return f"τ remains stable at {new_tau}."

    def play_round(self, round_num):
        """Plays one round of the Author-Reviewer game."""
        print(f"\n🔹 **Round {round_num}** 🔹")

        # **Author Move**
        author_claim = self.generate_author_move()
        print(f"📜 **Author's formula & τ claim:**\n{author_claim}")

        # **Reviewer Move**
        reviewer_response = self.generate_reviewer_move(author_claim)
        print(f"🔎 **Reviewer finds issues or better assignment:**\n{reviewer_response}")

        # Extract τ from the responses (Basic Parsing Logic)
        new_tau = self.extract_tau_from_text(author_claim)
        if not new_tau:
            new_tau = self.extract_tau_from_text(reviewer_response)
        
        # Compare with previous τ
        evaluation = self.evaluate_tau_change(self.current_tau, new_tau)
        self.current_tau = new_tau
        self.tau_history.append(new_tau)

        print(f"📊 **Result of Round {round_num}:** {evaluation}")

    def extract_tau_from_text(self, text):
        """Extracts numerical τ value from LLM response."""
        import re
        matches = re.findall(r'\b0\.\d+\b|\b1(?:\.0*)?\b', text)  # Extracts decimal numbers between 0 and 1
        if matches:
            return float(matches[0])
        else:
            return 1.0  # Default value if no valid τ is found




    def run_game(self):
        """Runs multiple rounds of the game."""
        print("🎮 **Starting the Semantic Game!** 🎮")
        for round_num in range(1, MAX_ROUNDS + 1):
            self.play_round(round_num)

        # Final Conclusion
        final_tau = self.current_tau if self.current_tau is not None else "Unknown"
        print(f"\n🏁 **Game Over! Final τ(RS, FPR) estimate: {final_tau}**")
        print(f"📈 Evolution of τ: {self.tau_history}")

# **Run the Game**
if __name__ == "__main__":
    # Example values (modify as needed)
    relation_set = "ClausalR(2,2)"
    forbidden_patterns = "TRUE"  # No additional constraints

    game = SemanticGame(relation_set, forbidden_patterns)
    game.run_game()

