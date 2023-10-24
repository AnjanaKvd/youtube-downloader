from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, video_url):
        self.video_url = video_url
        self.yt = YouTube(self.video_url)

    def show_video_details(self):
        print("Video Title:", self.yt.title)
        print("Video Author:", self.yt.author)
        print("Video Length:", self.yt.length, "seconds")
        print("Video Description:", self.yt.description)

    def download_video(self, download_path='./'):
        stream = self.yt.streams.get_highest_resolution()

        print("Downloading...")
        download_path = download_path.rstrip('/')

        try:
            stream.download(output_path=download_path)
            print("Download complete.")
        except Exception as e:
            print(f"Download failed: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")

    downloader = YouTubeDownloader(video_url)
    downloader.show_video_details()

    choice = input("Do you want to download this video? (y/n): ").strip().lower()

    if choice == 'y':
        download_path = input("Enter the path to save the video (default is the current directory): ").strip()
        if not download_path:
            download_path = "./"
        downloader.download_video(download_path)
    else:
        print("Download aborted.")
