import anthropic
import streamlit as st


def run_claude(api_key: str, source_file_contents: str, template_file):
    client = anthropic.Anthropic(api_key = api_key)
    filename = f"{template_file.name.split(".")[0]}_out.txt"
    template_file_contents = template_file.read()

    try:
        st.spinner("Running Claude API calls...")

        with st.spinner():
            client = anthropic.Anthropic(api_key = api_key)
            print("Starting Claude API calls...")

            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.0,
                
                messages=[
                    {"role": "user", "content": f"Can you please analyse this in very close detail - {source_file_contents}. Please exclude your preamble message."}
                ]
            )
            prompt1_answer = message.content[0].text
            # st.write("Prompt 1 done. Starting Prompt 2...")

            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.0,

                messages = [
                    {"role": "user", "content": f"Okay from this script: {prompt1_answer} - Can you get the following answers please only from what the script says What are the pain points? \nWhat is their core problem? \nWhat are the symptoms? \nWhat do they feel emotionally about the problem? \nGive me a situation of how they experience their problem & how people react to them. \nPlease exclude your preamble message."}
                ]
            )
            prompt2_answer = message.content[0].text

            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.0,

                messages = [
                    {"role": "user", "content": f"Based from this script specifically: {prompt2_answer} - What is the unique mechanism problem?\n What is the unique mechanism solution? \nPlease exclude your preamble message."}
                ]
            )
            prompt3_answer = message.content[0].text

            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0.0,

                messages = [
                    {"role": "user", "content": f"Im going to give you a complete different script its about pain but the reason why im giving you this is because the structure of this script is amazing i want to follow the structure line by line but i want to change the words to meet for neuropathy the first document i told you to analyse so now you know the core problems symptoms and how they feel emotionally about the problem even the unique mechanism solution and problem about the first script can you take that information and paste it into this new script whilst following the new scripts structure. For example if the first sentence of the new script says [75% of the population are slowly destroying their neck every single day. ] we want to change that to something like [75% of the population are slowly destroying their feet every single day.] you see how i kept the structure the same we want to do that as much as possible but change the information to foot neuropathy and we will take the information out the first document i asked you to analyse here is the script to follow the structure. Key things to note: our brand is called Kyrona Clinic and the product is called Kyrona NMES Foot Massager Sandals. Please be sure to finish the whole script. Here is the script - {template_file_contents}. \nPlease exclude your preamble message."}
                ]
            )
            prompt4_answer = message.content[0].text
            st.write("Output generated successfully!")

        st.download_button(
            label=f"Download {filename}",
            data=prompt4_answer.encode(),
            file_name=f"{filename}_output.txt",
            mime="text/plain"
        )

    
    except Exception as e:
        st.error(f"Error: {e}")
        return


def main():
    st.title("VSL Generator")

    # Text input
    api_key = st.text_input("Claude API Key", "Enter API Key here...")

    # Single file upload
    source_file = st.file_uploader("Source File")

    # Multiple files upload
    template_file = st.file_uploader("Template File", accept_multiple_files=True)

    if st.button("Generate Output"):
        if not api_key or not source_file or not template_file:
            st.error("Please provide all inputs.")
            return
        
        source_file_contents = source_file.read()
        for file in template_file:
            run_claude(api_key, source_file_contents, file)

if __name__ == "__main__":
    main()
