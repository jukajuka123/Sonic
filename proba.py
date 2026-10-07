import youtube_dl

def download_youtube_video(video_url):
    try:
        with youtube_dl.YoutubeDL({
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s'
        }) as ydl:
            ydl.download([video_url])
            print(f"Video downloaded successfully: {video_url}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=8kosrQW7ZR8"
    download_youtube_video(video_url)