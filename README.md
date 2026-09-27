# Cloud-Native YouTube Video Generation Pipeline

This project automates the creation of YouTube Shorts or videos using a 100% cloud-based approach. It is structured to be easily hosted on GitHub and orchestrated by GitHub Actions, meaning **zero local execution is required** on your machine.

## Architecture Structure
```text
.
├── .github/workflows/
│   └── youtube_worker.yml      # The cloud orchestrator (runs daily)
├── src/
│   ├── script_generator.py     # AI logic for scripting (Groq/OpenAI)
│   └── Colab_Video_Generator.ipynb # Colab GPU Notebook (for manual execution)
├── kaggle/
│   ├── kernel-metadata.json    # Kaggle API config
│   └── kaggle_renderer.ipynb   # Kaggle GPU Notebook (automated)
├── outputs/                    # Scripts get saved here automatically
├── requirements.txt
└── README.md
```

## How to Set Up

### 1. GitHub Setup
1. Push this folder to a new GitHub repository.
2. In your repository on GitHub, go to **Settings > Secrets and variables > Actions**.
3. Add your text-generation API key as a Secret:
   - Name: `GROQ_API_KEY` (Paste your Groq API key)
   - Name: `OPENAI_API_KEY` (Paste your OpenAI key, if using it)
4. Go to **Settings > Actions > General > Workflow permissions** and select **Read and write permissions** so the bot can save daily scripts to the `outputs/` folder.

### 2. Choose Your GPU Rendering Approach

#### Option A: Fully Automated using Kaggle (API)
Kaggle allows you to trigger GPU jobs purely through code, making it fully automatable:
1. Get your Kaggle API key (`kaggle.json` from your Kaggle account settings).
2. Edit `kaggle/kernel-metadata.json` and replace `YOUR_KAGGLE_USERNAME` with your real Kaggle username.
3. In GitHub, add two more Repository Secrets:
   - `KAGGLE_USERNAME` (Your Kaggle username)
   - `KAGGLE_KEY` (The token from `kaggle.json`)
4. **How it works:** Every day, GitHub Actions will generate the script, commit it to GitHub, and automatically push the `kaggle_renderer.ipynb` to Kaggle via their API. Kaggle will then run it on a GPU in the background! You just log into Kaggle later to download the `final_video.mp4` from the notebook's output.

#### Option B: Manual Trigger using Google Colab
Colab doesn't have an official API, but you can manually run it anytime:
1. Open Google Colab in your browser.
2. Upload `src/Colab_Video_Generator.ipynb` (or link it directly from your GitHub).
3. Update the `url` string in the Notebook code with your raw GitHub URL for `outputs/latest_script.txt` (e.g., `https://raw.githubusercontent.com/YourUsername/YourRepo/main/outputs/latest_script.txt`).
4. Set the runtime to **GPU** and run all cells when you want the video.

## Customization
* **Scheduling**: Edit the `cron` schedule in `.github/workflows/youtube_worker.yml`.
