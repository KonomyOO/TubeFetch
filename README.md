    1 # TubeFetch
    2 
    3 A simple, cross-platform YouTube video downloader with a graphical user interface (GUI) built using Flet and yt-dlp. This application allows
      users to fetch available video qualities and download YouTube videos directly to their local machine.
    4 
    5 ## Features
    6 
    7 *   Fetch available video qualities (including audio-only and video-only options).
    8 *   Download videos in selected quality.
    9 *   Save downloaded videos to a `Downloads` folder.
   10 *   User-friendly graphical interface.
   11 
   12 ## Prerequisites
   13 
   14 Before you begin, ensure you have the following installed on your system:
   15 
   16 *   **Python 3.8+**:
   17     *   [Download Python](https://www.python.org/downloads/)
   18     *   On most Linux distributions, you can install it via your package manager (e.g., `sudo apt install python3 python3-pip` on
      Ubuntu/Debian).
   19 
   20 *   **pip** (Python package installer): Usually comes with Python.
   21 
   22 *   **git** (for cloning the repository):
   23     *   On Linux: `sudo apt install git` (Ubuntu/Debian) or `sudo dnf install git` (Fedora).
   24     *   [Download Git](https://git-scm.com/downloads)
   25 
   26 *   **FFmpeg**: `yt-dlp` (which this application uses) relies on `ffmpeg` for merging video and audio streams, and for converting formats.
      **This is a crucial dependency.**
   27     *   On Linux: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora).
   28     *   [Download FFmpeg](https://ffmpeg.org/download.html) (ensure it's added to your system's PATH).
   29 
   30 ## Setup and Running the Application
   31 
   32 Follow these steps to set up and run the application from source:
   33 
   34 *   **Clone the repository:**
      git clone https://github.com/KonomyOO/TubeFetch.git
      cd TubeFetch/Project # Navigate into the 'Project' directory
   1 
   2 *   **Create a virtual environment (recommended):**
      python3 -m venv venv
      source venv/bin/activate  # On Windows: .\venv\Scripts\activate

   1 
   2 *   **Install Python dependencies:**
      pip install -r requirements.txt
   1 
   2 *   **Run the application:**
      python3 main.py
   1 
   2 ## Building a Standalone Executable (Optional)
   3 
   4 You can package the application into a standalone executable using `PyInstaller`. This allows the application to run on machines without a 
     Python environment installed (though `ffmpeg` is still required).
   5 
   6 **Note:** `PyInstaller` creates executables specific to the operating system it runs on. If you build on Linux, the executable will only work
     on Linux.
   7 
   8 *   **Install PyInstaller:**
   9     If you haven't already, install `PyInstaller` in your virtual environment:
      pip install pyinstaller

   1 
   2 *   **Navigate to the application directory:**
   3     Ensure you are in the `Project` directory where `main.py` and `youtube_downloader.spec` are located.
   4 
   5 *   **Build the executable:**
   6     We've prepared a `.spec` file for Flet applications. Use it to build:
      pyinstaller youtube_downloader.spec

    1     *(If `youtube_downloader.spec` is not present, you can create it with the content provided in our previous conversation, or use a
      simpler command like `pyinstaller --noconfirm --onedir --windowed --name "TubeFetch" main.py`)*
    2 
    3 *   **Find the executable:**
    4     The executable will be located in the `dist` directory. For example, on Linux, you'll find it at `dist/TubeFetch/TubeFetch`.
    5 
    6 *   **Distribution:**
    7     When distributing, you must provide the **entire contents** of the `dist/TubeFetch` folder, not just the executable file itself.
    8 
    9 ## Usage
   10 
   11 *   Run the application.
   12 *   Enter a YouTube video URL into the input field.
   13 *   Click "Fetch Available Qualities".
   14 *   Select your desired quality from the dropdown.
   15 *   Click "Download Video".
   16 *   The video will be saved in a `Downloads` folder relative to where the application is run.
