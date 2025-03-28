import os
import re
import torch
import time
from llama_cpp import Llama

# Check if CUDA is available and print device info
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Expand model path and load the LLM (Mistral-7B GGUF model)
model_path = os.path.expanduser("models/mistral-7b-instruct-v0.1.Q4_K_M.gguf")
try:
    llm = Llama(model_path=model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

### **Game Parameters**
MAX_ROUNDS = 10
MAX_RETRIES = 3  # Maximum retries for a move

class SemanticGame:
    def __init__(self, relation_set, forbidden_patterns):
        self.RS = relation_set
        self.FPR = forbidden_patterns
        self.tau_history = []
        self.current_tau = None
        self.current_formula = None
        self.current_role = "Author"  # Start with Author

    def generate_author_move(self, retry_count=0):
        prompt = f"""
You are Alice, the Author in a structured debate to approximate τ(RS, FPR) as described in our document.
Relation Set (RS): {self.RS}
Forbidden Pattern Rule (FPR): {self.FPR}
Hint: For triangle‑free formulas, note that a minimal odd cycle (a pentagon) yields a satisfaction fraction of approximately 0.80000.

Your task:
1. Propose a valid CNF formula F using variables (x1, x2, …, xn) that adheres to these conditions.
2. Provide a numerical claim for τ (a value between 0 and 1) based on your formula.
3. Include a Guarantor Algorithm in pseudocode that explains how this τ is achieved.
4. Provide a brief explanation.

Format exactly as:
Formula F = [your CNF formula]
Claimed τ = [a number, e.g., 0.80000]
Guarantor Algorithm (pseudo-code):
[Your pseudocode here]
Explanation: [Your reasoning here]

Now, please provide your response.
        """
        try:
            response = llm(prompt, max_tokens=500)
            text = response["choices"][0]["text"].strip()
            return text
        except Exception as e:
            print(f"Error in generate_author_move: {e}")
            return "Error: No valid response generated by Author."

    def generate_reviewer_move(self, formula, claimed_tau):
        prompt = f"""
You are Bob, the Reviewer in a structured debate about τ(RS, FPR).
The Author (Alice) has proposed the following:
Formula F = {formula}
Claimed τ = {claimed_tau}

Your task:
1. Critically evaluate this proposal. If flawed, provide a counterexample assignment and propose a revised formula with a revised τ.
2. Also, provide a Challenger Algorithm in pseudocode that constructs a worst-case instance.
3. Explain your reasoning.

Format exactly as:
Reviewer Response: [Your detailed critique, including counterexample]
Revised τ = [new value, if applicable]
New Formula F' = [your revised formula, if applicable]
Challenger Algorithm (pseudo-code):
[Your pseudocode here]
Explanation: [Your detailed explanation]

Now, please provide your response.
        """
        try:
            response = llm(prompt, max_tokens=500)
            text = response["choices"][0]["text"].strip()
            return text
        except Exception as e:
            print(f"Error in generate_reviewer_move: {e}")
            return "Reviewer Response: Error encountered; no valid response generated."

    def extract_tau(self, text):
        match = re.search(r"(?:Claimed τ|Revised τ) = ([0-9]*\.?[0-9]+)", text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def extract_formula(self, text):
        match = re.search(r"(?:Formula F|New Formula F') = (.+)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def play_round(self, round_num):
        print(f"\n🔹 **Round {round_num}: {self.current_role}'s Move** 🔹")
        if self.current_role == "Author":
            # Retry Author move up to MAX_RETRIES if valid output is not produced
            for attempt in range(MAX_RETRIES):
                response = self.generate_author_move()
                print(f"📜 **Author's Move (Alice), attempt {attempt+1}:**\n{response}")
                formula = self.extract_formula(response)
                tau = self.extract_tau(response)
                if tau is not None and formula is not None:
                    self.current_tau = tau
                    self.current_formula = formula
                    self.current_role = "Reviewer"
                    break
                else:
                    print("⚠️  Invalid τ and/or formula. Retrying Author's move...")
                    time.sleep(1)
            else:
                print("❌ Author failed to provide a valid move after multiple attempts.")
                return  # Abort round if no valid move is produced
        else:
            response = self.generate_reviewer_move(self.current_formula, self.current_tau)
            print(f"🔍 **Reviewer's Response (Bob):**\n{response}")
            revised_tau = self.extract_tau(response)
            new_formula = self.extract_formula(response)
            if revised_tau is not None:
                self.current_tau = revised_tau
            if new_formula is not None:
                self.current_formula = new_formula
            self.current_role = "Author"
        self.tau_history.append(self.current_tau)
        print(f"📊 **Current τ Estimate:** {self.current_tau}")

    def run_game(self):
        print("🎮 **Starting the Semantic Game!** 🎮")
        for round_num in range(1, MAX_ROUNDS + 1):
            self.play_round(round_num)
        final_tau = self.current_tau if self.current_tau is not None else "Unknown"
        print(f"\n🏁 **Game Over! Final τ(RS, FPR) estimate: {final_tau}**")
        print(f"📈 Evolution of τ: {self.tau_history}")

if __name__ == "__main__":
    relation_set = "R(a, b) = a + b = 1"
    forbidden_patterns = "Any triple of constraints must be satisfiable"
    game = SemanticGame(relation_set, forbidden_patterns)
    game.run_game()

    # Explicit cleanup to prevent destructor errors
    try:
        del llm
    except Exception as e:
        print(f"Error during model cleanup: {e}")
