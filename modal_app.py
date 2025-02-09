# modal_app.py
import modal

# Define a Modal stub
stub = modal.Stub(name="devfest-25")

# Define the base image and mount the local directory
image = (
    modal.Image.debian_slim()
    .pip_install("streamlit")
    .pip_install_from_requirements("/Users/takshikajambhule/Documents/Hackathon/new/devfest-25/requirements.txt")  # If requirements.txt exists
    .add_local_dir(
        local_path="/Users/takshikajambhule/Documents/Hackathon/new/devfest-25",  # Your local repository
        remote_path="/app"  # Path inside the Modal container
    )
)

# Define the Streamlit function
@stub.function(image=image)
def run_streamlit():
    import os
    import subprocess

    # Change directory to the mounted repository
    os.chdir("/app")
    
    # Run the Streamlit app (update the file name if it's not `app.py`)
    subprocess.run(["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"])

# Serve the app as a local entry point
if __name__ == "__main__":
    with stub.run():
        run_streamlit.call()
