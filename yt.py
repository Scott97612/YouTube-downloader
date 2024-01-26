from pytube import YouTube
import moviepy.editor as mpe
import sys, os

# change it to your desired download directory
download_folder = '/Users/<username>/Downloads' 

def get_720p(url: str):

    # videos with audio tracks, default download 720p
    yt = YouTube(url)
    try:
        video = yt.streams.get_by_resolution('720p')
        # size data is in bytes, to get byte -> kilobyte -> megabyte
        size = f'{video.filesize_mb} MB'
        print(f'Video: {yt.title} | Resolution: 720p | Filesize: {size}')
        confirm = input('Confirm download this video? Type "y" for yes.')
        
        if confirm == 'y':
            video.download(download_folder)
            print('Download finished!')
        else:
            sys.exit()

    except Exception as error:
        print(error)

def get_1080p_above_options(url: str, res: str):
    # videos without audio tracks

    yt = YouTube(url)
    try:
        v_list = yt.streams.filter(adaptive=True)
        exist_flag = False
        print('Here are available options of selected resolution:\n')
        for option in v_list:
            if res in str(option):
                exist_flag = True
                print(option, '\n')

        if exist_flag == False:
            print('Video with requested resolution NA.\n')
            sys.exit()
        else:
            confirm_tag = input('Type in the tag number of the video you want to download.')
            video = yt.streams.get_by_itag(confirm_tag)
            filename = f'{yt.title}.{str(video.mime_type)[-3:]}'
            pseudo_filename = f'{yt.title} (withoutAudio).{str(video.mime_type)[-3:]}'
            size = f'{video.filesize_mb} MB'
            print(f'Video: {yt.title} | Resolution: {res} | Filesize: {size}')
            confirm = input('Confirm download this video? Type "y" for yes.')
            
            video.download(download_folder, pseudo_filename) if confirm == 'y' else sys.exit()
            return f'{download_folder}/{filename}', f'{download_folder}/{pseudo_filename}'

    except Exception as error:
        print(error)

def get_audio(url: str):

    yt = YouTube(url)
    try:
        # the first audio option always starts with tag NO. 139
        audio = yt.streams.get_by_itag(139)
        audio.download(download_folder, 'Audio_track.mp3')
    except Exception as error:
        print(error)

def combine_video_audio(input_video: str, input_audio: str, output_video: str):

    video = mpe.VideoFileClip(input_video)
    audio = mpe.AudioFileClip(input_audio)
    video = video.set_audio(audio)
    """
    Argument "Preset" choices are: 
    
    ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo.

    The faster it runs, the bigger the output filesize.

    Default is medium.
    """
    video.write_videofile(filename=output_video, preset='medium')


if __name__ == "__main__":
    print('Paste url and select resolution.\nAcceptable resolutions: 720p, 1080p, 1440p, 2160p')
    url, res = input('URL here: '), input('Resolution here: ')
    
    if res == '720p':
        get_720p(url=url)
    else:
        # get the video without the audio track
        filename, pseudo_filename = get_1080p_above_options(url=url, res=res)
        # get the underlying audio track
        get_audio(url=url)
        # combine video with its audio track
        combine_video_audio(pseudo_filename, f'{download_folder}/Audio_track.mp3', filename)
        # delete by_product files from the middle processes
        os.remove(pseudo_filename)
        os.remove(f'{download_folder}/Audio_track.mp3')
        print('Download finished!')
