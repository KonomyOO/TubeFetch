## TubeFetch

A simple, cross-platform YouTube video downloader with a graphical user interface (GUI) built using **Flet** and **yt-dlp**. This application allows users to fetch available video qualities and download YouTube videos directly to their local machine.

-----

## Features

  - **Get Qualities:** Fetch all available video qualities, including audio-only and video-only options.
  - **Download:** Download videos in your selected quality.
  - **Save Locally:** Videos are saved automatically to a `Downloads` folder.
  - **User-Friendly:** Simple and intuitive graphical interface.

-----

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed on your system:

  - **Python 3.8+**:

      - [Download Python](https://www.python.org/downloads/)
      - On most Linux distributions, you can install it via your package manager:
        ```bash
        sudo apt install python3 python3-pip  # For Ubuntu/Debian
        ```

  - **pip** (Python package installer): Usually comes with Python.

  - **git**:

      - On Linux:
        ```bash
        sudo apt install git  # For Ubuntu/Debian
        sudo dnf install git  # For Fedora
        ```
      - [Download Git](https://git-scm.com/downloads)

  - **FFmpeg**: This is a **crucial dependency** as `yt-dlp` relies on it for merging audio and video streams.

      - On Linux:
        ```bash
        sudo apt install ffmpeg  # For Ubuntu/Debian
        sudo dnf install ffmpeg  # For Fedora
        ```
      - [Download FFmpeg](https://ffmpeg.org/download.html) (Make sure to add it to your system's PATH).

-----

## Setup and Running the Application

Follow these steps to set up and run the application from the source code:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/KonomyOO/TubeFetch.git
    cd TubeFetch/Project/TubeFetch
    ```

2.  **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    python3 main.py
    ```

-----

## 📦 Building a Standalone Executable

You can package the application into a standalone executable using **PyInstaller**. This allows it to run on machines without a Python environment installed (though `ffmpeg` is still required).

> **Note:** PyInstaller creates executables specific to the operating system it runs on.

1.  **Install PyInstaller:** If you haven't already, install it in your virtual environment:

    ```bash
    pip install pyinstaller
    ```

2.  **Navigate to the application directory:** Make sure you are in the `TubeFetch` directory (inside `Project`) where `main.py` is located.

3.  **Build the executable:** Use the prepared `.spec` file.

    ```bash
    pyinstaller youtube_downloader.spec
    ```

    *(If the `.spec` file is not present, you can use a simpler command like: `pyinstaller --noconfirm --onedir --windowed --name "TubeFetch" main.py`)*

4.  **Find the executable:** It will be in the `dist` directory.

      - On Linux, for example: `dist/TubeFetch/TubeFetch`

5.  **Distribution:** When distributing, provide the **entire contents** of the `dist/TubeFetch` folder, not just the executable file.

-----

## Usage

1.  Run the application.
2.  Enter a YouTube video URL into the input field.
3.  Click "**Fetch Available Qualities**".
4.  Select your desired quality from the dropdown menu.
5.  Click "**Download Video**".
6.  The video will be saved in a `Downloads` folder relative to where the application is running.
