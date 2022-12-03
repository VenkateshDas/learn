import streamlit as st
import markdown
import requests
import os


def create_markdown_editor():
    # Create a text input field where the user can enter their markdown text
    markdown_text = st.text_area("Enter your markdown text here:")

    # Convert the markdown text to HTML
    html = markdown.markdown(markdown_text)

    # Display the markdown text and the rendered HTML in the app
    st.write(markdown_text, unsafe_allow_html=True)
    st.write(html, unsafe_allow_html=True)

    return markdown_text


def save_markdown_file(markdown_text):
    # Set the name and location of the markdown file
    file_name = ".md"
    file_path = "contents/"

    # Save the markdown text to the file
    with open(file_path, "w") as f:
        f.write(markdown_text)
    st.success("Markdown file saved successfully!")
    return file_path, file_name


def push_to_repository(markdown_text, file_path, file_name):
    # Set the URL of your Github repository
    repository_url = "https://api.github.com/repos/{username}/{repository}"

    # Read the contents of the markdown file
    with open(file_path, "r") as f:
        file_contents = f.read()

    # Set the branch where the file should be added (usually "main" or "master")
    branch = "main"

    # Set the commit message for the new file
    commit_message = "Add new blog post"

    # Set username and token for authentication
    username = "VenkateshDas"
    token = os.environ.get("GIT_TOKEN")

    # Create a new file in the repository using the Github API
    response = requests.put(
        f"{repository_url}/contents/{file_name}",
        json={
            "message": commit_message,
            "branch": branch,
            "content": file_contents,
        },
        auth=(username, token),
    )

    # Check the response status code to see if the file was created successfully
    if response.status_code == 200:
        st.success("Blog post added successfully!")
    else:
        st.error("Failed to add blog post. Check the error message for more details.")
        st.error(response.json()["message"])


def main():
    markdown_text = create_markdown_editor()
    file_name = st.text_input("Enter the name of the markdown file:")
    if st.button("Save Markdown File"):
        file_path, file_name = save_markdown_file(markdown_text)
        if st.button("Push to Github Repository"):
            push_to_repository(markdown_text, file_path, file_name)


if __name__ == "__main__":
    main()
