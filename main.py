import pymysql
import os;
from video_downloader import VideoDownloader

if __name__ == "__main__":
    pymysql.install_as_MySQLdb()

    conn = pymysql.connect(host='182.92.3.69',
                           user='lytian',
                           passwd="test123456",
                           db='pexels_video')
    cur = conn.cursor()

    #获取keyword 
    cur.execute(
        "SELECT keyword from video_keyword where is_del = 0 order by rand() limit 1")

    keyword = 'nature'
    for r in cur:
        keyword = r[0]

    print(f"当前获取到的关键词:{keyword}")

    cur.execute(
        "SELECT cur_page from video_info where keyword = %s order by cur_page desc limit 1",
        keyword)

    cur_page = 0
    for r in cur:
        cur_page = r[0]

    print(f"当前获取分页:{cur_page}")

    video = VideoDownloader('./download.log')
    video.downloads_dir = os.getenv('YOUTUBE_FILE_PATH') + '/mp4/'
    video.resolution_width = 1080
    video.page = cur_page + 1
    video.per_page = 20
    result = video.search_video(keyword)

    for r in result:
        if r == 'videos':
            for i in range(len(result[r])):
                video_item = dict([
                    (key, result[r][i][key])
                    for key in ['id', 'width', 'height', 'tags', 'url']
                ])

                cur.execute(
                    "SELECT video_id from video_info where video_id = %s",
                    video_item['id'])
                if cur.rowcount > 0:
                    continue

                title = video_item['url'].split('/')[-2].split('-')
                title.pop()
                title = " ".join(title).title()
                tags = ','.join(video_item['tags'])
                insert_item = (video_item['id'], video_item['url'], title,
                               tags, video_item['width'], video_item['height'],
                               keyword, video.page)

                cur.execute(
                    "INSERT INTO video_info(video_id, url, title, tags, width, height, keyword, cur_page) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                    % insert_item)

    cur.execute("SELECT id, video_id from video_info where is_download = 0")

    undownload_list = []

    for r in cur:
        undownload_list.append(r)

    for r in undownload_list:
        result = video.download(r[1])
        print(f"视频{r[1]}下载成功")
        download_file_path = f"{video.downloads_dir}{r[1]}.mp4"
        cur.execute(
            "UPDATE video_info SET file_path = '%s', is_download = 1 where id = '%s'"
            % (download_file_path, r[0]))

    conn.commit()

    cur.close()
    conn.close()

    print('视频已全部下载完毕！')