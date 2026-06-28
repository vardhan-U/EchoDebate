# EchoDebate

AI-powered debate practice and rhetoric coach.

Record yourself making an argument. EchoDebate transcribes it, scores your logic, and sends an AI opponent to rebut you with real retrieved evidence — not hallucinated counterpoints. After 2-3 rounds, you get a full breakdown of where your reasoning held and where it didn't.

---

## Features

- **Voice capture** — record your argument in-browser, transcribed automatically via Whisper
- **Logic scoring** — rated across structure, evidence strength, fallacy count, and rebuttal responsiveness, each with a plain-English explanation
- **Adversarial opponent** — searches for a real counter-fact before rebutting you, never fabricates a source
- **Cue card check** — upload a photo of your prep notes and see which points you actually covered

---

## Stack

- **Frontend:** Gradio
- **Transcription:** Whisper
- **LLMs:** phi3:latest,openai/whisper-large-v3 
- **Fact retrieval:** Serper or Tavily search API

## License

MIT
