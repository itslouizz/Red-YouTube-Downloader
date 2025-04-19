# by itslouizz on github :)
# only use legal (for exsample: on your own video to back them up and not to watch them without ads or offline. Respect youtube<3)

import os
import pytube
from colorama import Fore, Style, init

init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red(text):
    print(Fore.RED + text + Style.RESET_ALL)

def print_header():
    clear_screen()
    print_red("=============================================")
    print_red("          RED YOUTUBE DOWNLOADER")
    print_red("=============================================")
    print()

def get_download_path():
    print("\nWhere would you like to save the video?")
    print("1. Downloads folder (default)")
    print("2. Custom location")
    choice = input("Enter choice (1-2): ")
    
    if choice == "2":
        path = input("Enter full path to download directory: ")
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def download_video():
    print_header()
    url = input("Enter YouTube video URL: ")
    
    try:
        yt = pytube.YouTube(url)
        
        print_red("\nVideo Information:")
        print(f"Title: {yt.title}")
        print(f"Author: {yt.author}")
        print(f"Length: {yt.length // 60} minutes {yt.length % 60} seconds")
        print(f"Views: {yt.views:,}")
        
        print_red("\nSelect Download Quality:")
        print("1. 720p")
        print("2. 1080p")
        quality_choice = input("Enter choice (1-2): ")
        
        if quality_choice == "1":
            stream = yt.streams.filter(progressive=True, file_extension='mp4', res="720p").first()
        else:
            video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', res="1080p").first()
            audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            if not video_stream or not audio_stream:
                print_red("1080p not available, falling back to 720p")
                stream = yt.streams.filter(progressive=True, file_extension='mp4', res="720p").first()
            else:
                download_path = get_download_path()
                print_red("\nDownloading 1080p video (this may take a while)...")
                video_path = video_stream.download(output_path=download_path, filename_prefix="video_")
                audio_path = audio_stream.download(output_path=download_path, filename_prefix="audio_")
                
                print_red("Merging video and audio...")
                final_path = os.path.join(download_path, f"{yt.title}.mp4")
                
                try:
                    from moviepy.editor import VideoFileClip, AudioFileClip
                    video_clip = VideoFileClip(video_path)
                    audio_clip = AudioFileClip(audio_path)
                    final_clip = video_clip.set_audio(audio_clip)
                    final_clip.write_videofile(final_path, codec='libx264', audio_codec='aac')
                    video_clip.close()
                    audio_clip.close()
                    os.remove(video_path)
                    os.remove(audio_path)
                    print_red(f"\nDownload complete! File saved to: {final_path}")
                    input("\nPress Enter to return to main menu...")
                    return
                except ImportError:
                    print_red("\nError: moviepy not installed. Cannot merge 1080p streams.")
                    print_red("Please install moviepy with: pip install moviepy")
                    input("\nPress Enter to return to main menu...")
                    return
        
        if not stream:
            print_red("Selected quality not available. Trying highest available quality...")
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        download_path = get_download_path()
        print_red("\nDownloading video (this may take a while)...")
        stream.download(output_path=download_path)
        print_red(f"\nDownload complete! File saved to: {download_path}")
        input("\nPress Enter to return to main menu...")
        
    except Exception as e:
        print_red(f"\nError: {str(e)}")
        input("\nPress Enter to return to main menu...")

def main():
    while True:
        print_header()
        print_red("MAIN MENU")
        print("1. Download YouTube Video")
        print("2. Exit")
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == "1":
            download_video()
        elif choice == "2":
            print_red("\nThank you for using Red YouTube Downloader!")
            break
        else:
            print_red("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        import pytube
    except ImportError:
        print_red("Error: pytube package not installed.")
        print("Please install it with: pip install pytube")
        exit(1)
    
    main()