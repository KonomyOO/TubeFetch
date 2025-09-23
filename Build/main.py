import flet as ft
import os
import threading
import subprocess
import json
import re
import yt_dlp

# --- Constants ---
DOWNLOADS_DIR = os.path.join(os.path.expanduser('~'), "Downloads")

class YouTubeDownloaderApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "YouTube Downloader"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window_width = 550
        self.page.window_height = 420
        self.page.window_resizable = False

        self.available_streams = {}

        self._create_ui()

    def _create_ui(self):
        self.url_input = ft.TextField(
            label="Video URL",
            hint_text="Enter YouTube video URL here",
            expand=True,
            border_radius=8,
            on_change=self._clear_status_on_input
        )
        self.fetch_button = ft.ElevatedButton(
            text="Fetch Available Qualities",
            icon=ft.Icons.SEARCH,
            on_click=self._start_fetch_thread,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        self.quality_dropdown = ft.Dropdown(
            label="Select Quality",
            options=[ft.dropdown.Option("No qualities fetched", disabled=True)],
            value="No qualities fetched",
            expand=True,
            border_radius=8
        )
        self.download_button = ft.ElevatedButton(
            text="Download Video",
            icon=ft.Icons.DOWNLOAD,
            on_click=self._start_download_thread,
            disabled=True,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE
            )
        )
        self.progress_bar = ft.ProgressBar(value=0, width=self.page.window_width - 40)
        self.progress_percentage_text = ft.Text("0%", text_align=ft.TextAlign.CENTER)
        self.status_text = ft.Text("Welcome! Enter a URL to begin.", size=12, color=ft.Colors.WHITE70)

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                self.url_input,
                                ft.IconButton(
                                    icon=ft.Icons.CLEAR,
                                    tooltip="Clear URL",
                                    on_click=lambda e: [setattr(self.url_input, 'value', ''), self.url_input.update(), setattr(self.status_text, 'value', 'Welcome! Enter a URL to begin.'), self.status_text.update()]
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(height=10),
                        ft.Row(
                            [self.fetch_button],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            [
                                self.quality_dropdown,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(height=20),
                        ft.Row(
                            [self.download_button],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Container(height=15),
                        ft.Column(
                            [
                                self.progress_percentage_text,
                                self.progress_bar,
                                self.status_text,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0
                ),
                padding=20,
                expand=True
            )
        )
        self.page.update()

    def _clear_status_on_input(self, e):
        self.status_text.value = ""
        self.page.update()

    def _show_notification(self, message, is_error=False):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message),
            open=True,
            bgcolor=ft.Colors.RED_700 if is_error else ft.Colors.GREEN_700,
            duration=5000
        )
        self.page.update()

    def _set_ui_state(self, is_active):
        self.url_input.disabled = not is_active
        self.fetch_button.disabled = not is_active
        self.quality_dropdown.disabled = not is_active
        # Download button state is managed separately based on available_streams
        if not is_active:
            self.download_button.disabled = True
        elif self.available_streams:
            self.download_button.disabled = False
        self.page.update()

    def _start_fetch_thread(self, e):
        self.page.run_thread(self._fetch_streams)

    def _fetch_streams(self):
        print("[_fetch_streams] Method called.")
        url = self.url_input.value
        if not url:
            self._show_notification("Please enter a video URL", is_error=True)
            return

        self.status_text.value = "Fetching streams, please wait..."
        self._set_ui_state(False)
        self.progress_bar.value = None # Indeterminate
        self.page.update()

        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'noplaylist': True,
                'quiet': True,
                'simulate': True, # Only extract info, don't download
                'force_generic_extractor': True, # Ensure it works for various URLs
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False) # download=False to only extract info
                video_info = ydl.sanitize_info(info_dict)

            video_streams = [f for f in video_info['formats'] if f.get('vcodec') != 'none' and f.get('ext') == 'mp4']
            
            if not video_streams:
                self._show_notification("No suitable MP4 streams found.", is_error=True)
                self.status_text.value = "No streams found."
                self.page.update()
                return

            # Group streams by height and find the best quality (largest filesize) for each height
            best_streams_by_height = {}
            for stream in video_streams:
                height = stream.get('height')
                if height:
                    current_best = best_streams_by_height.get(height)
                    if current_best is None or \
                       (stream.get('filesize') or stream.get('filesize_approx', 0)) > \
                       (current_best.get('filesize') or current_best.get('filesize_approx', 0)):
                        best_streams_by_height[height] = stream
            
            # Sort by height in descending order
            sorted_best_streams = sorted(best_streams_by_height.values(), key=lambda x: x.get('height', 0), reverse=True)

            quality_options = []
            self.available_streams = {}
            for stream in sorted_best_streams:
                filesize = stream.get('filesize') or stream.get('filesize_approx')
                height = stream.get('height', 'N/A')
                quality_label = f"{height}p"
                if filesize:
                    quality_label += f" - {round(filesize / (1024*1024), 2)} MB"
                
                self.available_streams[quality_label] = f"{stream['format_id']}+bestaudio"
                quality_options.append(ft.dropdown.Option(quality_label))
            
            if quality_options:
                # Add MP3 Audio Only option
                best_audio_stream = next((f for f in video_info['formats'] if f.get('acodec') != 'none' and f.get('ext') == 'm4a'), None)
                if best_audio_stream:
                    audio_filesize = best_audio_stream.get('filesize') or best_audio_stream.get('filesize_approx')
                    audio_label = "MP3 Audio Only"
                    if audio_filesize:
                        audio_label += f" - {round(audio_filesize / (1024*1024), 2)} MB"
                    self.available_streams[audio_label] = "bestaudio[ext=m4a]"
                    quality_options.append(ft.dropdown.Option(audio_label))

                # Add MP4 Video Only options
                # Filter for true video-only streams (acodec is 'none')
                true_video_only_streams = [f for f in video_info['formats'] if f.get('vcodec') != 'none' and f.get('acodec') == 'none' and f.get('ext') == 'mp4']

                best_video_only_streams_by_height = {}
                for stream in true_video_only_streams:
                    height = stream.get('height')
                    if height:
                        current_best = best_video_only_streams_by_height.get(height)
                        # Prioritize stream with larger filesize for the same height
                        if current_best is None or \
                           (stream.get('filesize') or stream.get('filesize_approx', 0)) > \
                           (current_best.get('filesize') or current_best.get('filesize_approx', 0)):
                            best_video_only_streams_by_height[height] = stream

                sorted_best_video_only_streams = sorted(best_video_only_streams_by_height.values(), key=lambda x: x.get('height', 0), reverse=True)

                # Add MP4 Video Only option (generic best quality)
                best_video_only_stream = next((f for f in video_info['formats'] if f.get('vcodec') != 'none' and f.get('acodec') == 'none' and f.get('ext') == 'mp4'), None)
                if best_video_only_stream:
                    video_only_filesize = best_video_only_stream.get('filesize') or best_video_only_stream.get('filesize_approx')
                    video_only_label = "MP4 Video Only (No Audio)"
                    if video_only_filesize:
                        video_only_label += f" - {round(video_only_filesize / (1024*1024), 2)} MB (best available)"
                    self.available_streams[video_only_label] = "bestvideo[ext=mp4]"
                    quality_options.append(ft.dropdown.Option(video_only_label))

                self.quality_dropdown.options = quality_options
                self.quality_dropdown.value = quality_options[0].key
                self.download_button.disabled = False
                self.status_text.value = "Streams fetched successfully!"
                self.page.update()
            else:
                self.status_text.value = "No video qualities found."
                self.page.update()


        except Exception as e:
            self._show_notification(f"An error occurred: {e}", is_error=True)
            self.status_text.value = "Failed to fetch streams."
            self.page.update()
        finally:
            self.progress_bar.value = 0
            self._set_ui_state(True)
            self.page.update()

    def _start_download_thread(self, e):
        self.page.run_thread(self._download_video)

    def _download_video(self):
        print("[_download_video] Method called.")
        url = self.url_input.value
        quality = self.quality_dropdown.value
        if not url or not quality or "No qualities" in quality:
            self._show_notification("Invalid URL or quality selected.", is_error=True)
            return

        self._set_ui_state(False)
        self.progress_bar.value = 0
        self.page.update()

        def my_hook(d):
            print(f"[_download_video] YT-DLP Hook Status: {d['status']}")
            if d['status'] == 'downloading':
                p = d['_percent_str']
                eta = d['_eta_str']
                speed = d['_speed_str']
                total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded_bytes = d.get('downloaded_bytes')

                if downloaded_bytes and total_bytes:
                    percentage = (downloaded_bytes / total_bytes) * 100
                    self.progress_bar.value = percentage / 100
                    self.progress_percentage_text.value = f"{int(percentage)}%"
                    self.status_text.value = f"Downloading: {p} at {speed} ETA {eta}"
                else:
                    self.status_text.value = f"Downloading: {p} at {speed} ETA {eta}"
                self.page.update()
            elif d['status'] == 'finished':
                self.status_text.value = "Post-processing..."
                self.page.update()

        try:
            format_id = self.available_streams[quality]
            os.makedirs(DOWNLOADS_DIR, exist_ok=True)
            print(f"[_download_video] Resolved DOWNLOADS_DIR: {DOWNLOADS_DIR}")

            ydl_opts = {
                'outtmpl': os.path.join(DOWNLOADS_DIR, '%(id)s.%(ext)s'), # Use ID for unique temporary name
                'noplaylist': True,
                'progress_hooks': [my_hook],

            }

            if quality == "MP3 Audio Only":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            elif "Video Only (No Audio)" in quality:
                ydl_opts['format'] = 'bestvideo[ext=mp4]'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }]
            else:
                # Combined video + audio logic: rely on yt-dlp's internal merging
                ydl_opts['format'] = format_id
                ydl_opts['merge_output_format'] = 'mp4'
            
            print(f"[_download_video] Final ydl_opts: {ydl_opts}") # Log final options

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True) # Download the files
                downloaded_temp_path = ydl.prepare_filename(info) # Path to the downloaded file (e.g., ID.ext)
            
            print(f"[_download_video] yt-dlp actually downloaded height: {info.get('height')}, format: {info.get('format')}, format_id: {info.get('format_id')}")
            print(f"[_download_video] Downloaded temporary path: {downloaded_temp_path}")

            # Determine the desired final filename (without autonumbering initially)
            # This requires getting the title from the info dict
            video_title = info.get('title', 'video')
            # original_ext = info.get('ext', 'mp4') # Get original extension from info - not needed, final_ext is determined below

            # Adjust extension based on download type
            if quality == "MP3 Audio Only":
                final_ext = "mp3"
            elif "Video Only (No Audio)" in quality:
                final_ext = "mp4"
            else:
                final_ext = "mp4"

            base_filename = f"{video_title}.{final_ext}"
            desired_final_path = os.path.join(DOWNLOADS_DIR, base_filename)

            # Handle autonumbering manually
            counter = 0
            while os.path.exists(desired_final_path):
                counter += 1
                base_filename = f"{video_title} ({counter}).{final_ext}"
                desired_final_path = os.path.join(DOWNLOADS_DIR, base_filename)
            
            print(f"[_download_video] Desired final path: {desired_final_path}")

            try:
                os.rename(downloaded_temp_path, desired_final_path)
                print(f"[_download_video] Successfully renamed {downloaded_temp_path} to {desired_final_path}")
            except FileNotFoundError:
                print(f"[_download_video] Error: Source file not found for rename: {downloaded_temp_path}")
                raise # Re-raise to be caught by outer except
            except PermissionError:
                print(f"[_download_video] Error: Permission denied when renaming to {desired_final_path}")
                raise # Re-raise to be caught by outer except
            except Exception as e:
                print(f"[_download_video] Unexpected error during rename: {e}")
                raise # Re-raise to be caught by outer except

            self._show_notification("Download completed successfully!")
            self.status_text.value = f"Video saved in Downloads folder: {os.path.basename(desired_final_path)}."
            self.progress_bar.value = 1.0 # Ensure 100%
            self.progress_percentage_text.value = "100%"
            self.page.update()

        except Exception as e:
            self._show_notification(f"An error occurred: {e}", is_error=True)
            self.status_text.value = f"Download failed: {e}"
            self.progress_bar.value = 0
            self.progress_percentage_text.value = "0%"
            self.page.update()
        finally:
            self._set_ui_state(True)
            self.progress_bar.value = 0
            self.progress_percentage_text.value = "0%"
            self.page.update()

def main(page: ft.Page):
    YouTubeDownloaderApp(page)

if __name__ == "__main__":
    ft.app(target=main)
