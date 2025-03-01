<template>
  <div class="container">
    <h2>Adaptive Learning: Solve Coding Challenges</h2>

    <div>
      <h3>Select a Programming Language</h3>
      <select v-model="selectedLanguage">
        <option disabled value="">Select a language</option>
        <option v-for="lang in languages" :key="lang" :value="lang">{{ lang }}</option>
      </select>
      <button @click="generateChallenge">Generate Challenge</button>
    </div>

    <div v-if="currentQuestion" class="challenge-section">
      <h3>Coding Challenge</h3>
      <p>{{ currentQuestion }}</p>
      <textarea v-model="userSolution" placeholder="Write your solution here..."></textarea>
      <button @click="submitSolution">Submit Solution</button>
    </div>

    <div v-if="feedback">
      <h3>Feedback</h3>
      <p>{{ feedback }}</p>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";

export default {
  setup() {
    const languages = ["Python", "JavaScript", "Java", "C++"];
    const selectedLanguage = ref("");
    const currentQuestion = ref("");
    const userSolution = ref("");
    const feedback = ref("");

    const generateChallenge = async () => {
      if (!selectedLanguage.value) {
        alert("Please select a language first.");
        return;
      }

      try {
        // ✅ Corrected API endpoint to /questions/generate/
        const response = await axios.post("http://127.0.0.1:8000/questions/generate/", {
          language: selectedLanguage.value,
        });

        currentQuestion.value = response.data.question;
        userSolution.value = "";
        feedback.value = "";
      } catch (error) {
        console.error("Error generating question:", error);
        alert("Failed to generate question.");
      }
    };

    const submitSolution = async () => {
      if (!currentQuestion.value || !userSolution.value.trim()) {
        alert("Please enter a solution first.");
        return;
      }

      try {
        const response = await axios.post("http://127.0.0.1:8000/submissions/evaluate/", {
          question: currentQuestion.value,
          user_solution: userSolution.value,
        });

        feedback.value = response.data.feedback;
      } catch (error) {
        console.error("Error evaluating solution:", error);
        alert("Failed to evaluate solution.");
      }
    };

    return { languages, selectedLanguage, currentQuestion, userSolution, feedback, generateChallenge, submitSolution };
  },
};
</script>

<style>
.container {
  padding: 20px;
  max-width: 600px;
  margin: auto;
}
select, textarea {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}
button {
  padding: 8px 12px;
  background: #42b983;
  border: none;
  color: white;
  cursor: pointer;
}
.challenge-section {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  background: #f9f9f9;
  border-radius: 5px;
}
</style>
