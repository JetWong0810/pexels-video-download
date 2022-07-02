'''
This script downloads the video from pexels when pexels video URL is passed

Usage: python main.py "{pexels_url}"
'''

from video_downloader import VideoDownloader
from image_downloader import ImageDownloader

if __name__ == "__main__":

    # search video
    video = VideoDownloader('/tmp/pexels_downloader.log')
    video.downloads_dir = "/Users/jetwong/Downloads/"
    video.resolution_width = 1080
    video.page = 3
    video.per_page = 3
    result = video.search_video("ocean")
    print(result)

    # image search
    # image = ImageDownloader('/tmp/pexels_downloader.log')
    # image.resolution_width = 1280
    # image.resolution_height = 720
    # result = image.get_image("bitcoin")
    # print(result)
