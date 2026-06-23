def debateanalyser(client,data):
    messages = [{"role":"system","content":"""You are an expert in debating now analyse the given debate from an opponent and give out the flaws maximum of 5 points,counter debates maximum of 4 ponts and the logical level out of 10 in this example format only:[{"debate_flaws":"flaws go here",
    "counter-debate":"counter-debate goes here",
    "logic-level:"logic-level goes here"
    }] and dont think for more than 1 minute"""},
    {"role":"user","content":data}]
    result = client.chat.completions.create(model = "phi3:instruct",messages = messages)
    return result.choices[0].message.content
