from transformers import pipeline
import gradio as gr
phi3=pipeline("text-generation",model="microsoft/Phi-3-mini-4k-instruct")
voice_recog = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3",chunk_length_s=30)

def debateanalyser(data):
    messages = [{
            "role": "system",
            "content": ("You are an expert in debating. Analyze the given debate from an opponent. "
                "Provide exactly up to 5 concise points for flaws, up to 4 concise points for "
                "counter-debates, and a final logic level out of 10. Use this exact text structure:\n"
                "**Flaws:**\n[Points here]\n\n"
                "**Counter Debates:**\n[Points here]\n\n"
                "**Logic Level:** [Score]/10")},
        {"role": "user", "content": data}
    ]
    result = phi3(messages, max_new_tokens=1024,return_full_text=False)
    return result[0]["generated_text"] if isinstance(result, list) else result

def cardanalysis(data):
    messages = [{"role":"system","content":"You are good analyser based on the data given write the drawbacks and logics that are actually missing it in maximum of 4 points."},
    {"role":"user","content":data}]
    return phi3(messages)
def speech_output(useraudio):
    extracted_data = voice_recog(useraudio,return_timestamps=True)
    return extracted_data["text"]

def card_coverage(usercuecard_path, extracted_text):
    card_extract = pipeline("image-text-to-text",
        model="prithivMLmods/Qwen3-VL-4B-Instruct-Unredacted-MAX-GGUF",)
    card_extracted_data = card_extract(usercuecard_path + " output should only be the extracted data as it is.")
    card_text = card_extracted_data[0]["generated_text"] if isinstance(card_extracted_data, list) else card_extracted_data
    prompt = ("You are given two sets of information.\n"
        "Info 1 - What the user argued: " + extracted_text + "\n"
        "Info 2 - What the user prepared: " + card_text + "\n"
        "Identify what is present in Info 2 but missing in Info 1. "
        "List maximum 2-4 missing points only.")
    result = phi3(prompt, max_new_tokens=256)
    return result[0]["generated_text"] if isinstance(result, list) else result

def run_pipeline(audio_input, cuecard_image):
    if audio_input is None:
        return "Upload an audio clip.", "", ""
    
    transcript = speech_output(audio_input)
    debate_analysis = debateanalyser(transcript) 
        
    if cuecard_image is not None:
        coverage_result = card_coverage(cuecard_image, transcript)
    else:
        coverage_result = "No cue card uploaded."
        return transcript, debate_analysis, coverage_result


demo = gr.Interface(
    fn=run_pipeline,
    inputs=[
        gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Debate Audio (record or upload)"
        ),
        gr.Image(
            type="filepath",
            label="Cue Card (optional-upload a photo of your preparation notes)"
        ),
    ],
    outputs=[
        gr.Textbox(label="Transcript", lines=4),
        gr.Textbox(label="Debate Analysis (flaws, counter-debates, logic score)", lines=10),
        gr.Textbox(label="Coverage Gaps (what you prepared but didn't argue)", lines=6),
    ],
    title="Debate Analyser",
    description="Record or upload your debate audio, optionally add your cue card, then click Submit to get AI feedback.",
    flagging_mode="never",
)

demo.launch(share=True)