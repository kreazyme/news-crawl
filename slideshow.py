import cv2
import numpy as np
import urllib.request
from moviepy.editor import AudioFileClip,VideoFileClip

def download_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

# def get_audio_length(audio_url):
def create_video_from_images(imgfile, audio_url,video_dim=(1280, 720), fps=27,
    start_center=(0.4, 0.6), end_center=(0.5, 0.5),
    start_scale=0.9, end_scale=1.0, output_file="output.mp4"):

    
    audio_clip = AudioFileClip(audio_url)
    duration = audio_clip.duration
    duration_per_image= duration/imgfile.__len__()
    audio_clip.close()

    # print length of image
    print("Duration per image: ", duration_per_image)
    print("Duration per images: ", imgfile.__len__())
    print("Duration: ", duration)


    # Load images
    img = [download_image(file) for file in imgfile]
    orig_shape = img[0].shape[:2]
    
    # Define crop function
    def crop(image, x, y, w, h):
        x0, y0 = max(0, x - w // 2), max(0, y - h // 2)
        x1, y1 = x0 + w, y0 + h
        return image[y0:y1, x0:x1]

    # Calculate total frames
    num_frames = int(fps * len(imgfile) * duration_per_image)
    frames = []

    # Generate frames
    for i in range(len(img)):
        for alpha in np.linspace(0, 1, num_frames):
            rx = end_center[0] * alpha + start_center[0] * (1 - alpha)
            ry = end_center[1] * alpha + start_center[1] * (1 - alpha)
            x = int(orig_shape[1] * rx)
            y = int(orig_shape[0] * ry)
            scale = end_scale * alpha + start_scale * (1 - alpha)
            if orig_shape[1] / orig_shape[0] > video_dim[0] / video_dim[1]:
                h = int(orig_shape[0] * scale)
                w = int(h * video_dim[0] / video_dim[1])
            else:
                w = int(orig_shape[1] * scale)
                h = int(w * video_dim[1] / video_dim[0])
            currentIndex = int(i / duration_per_image)
            cropped = crop(img[i], x, y, w, h)
            print('currentIndex: ', currentIndex, 'i : ', i, 'duration_per_image: ', duration_per_image)
            scaled = cv2.resize(cropped, dsize=video_dim, interpolation=cv2.INTER_LINEAR)
            frames.append(scaled)

    # Write to MP4 file
    vidwriter = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, video_dim)
    for frame in frames:
        vidwriter.write(frame)
    vidwriter.release()
    
    # merge audio to video
    video = VideoFileClip(output_file)
    audio = AudioFileClip(audio_url)
    video = video.set_audio(audio)
    video.write_videofile(output_file, codec="libx264", audio_codec="aac")
    video.close()
    audio.close()



# Example usage
# imgfile = ["image.jpg", "image.jpg", "image.jpg"]
# create_video_from_images(imgfile)