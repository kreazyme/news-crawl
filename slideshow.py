import cv2
import numpy as np
import urllib.request
from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip


def download_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def create_video_from_images(imgfile, audio_url, video_dim=(1280, 720), fps=27,
                             start_center=(0.4, 0.6), end_center=(0.5, 0.5),
                             start_scale=0.9, end_scale=1.0, output_file="output.mp4"):

    # Tải clip âm thanh và lấy độ dài
    audio_clip = AudioFileClip(audio_url)
    duration = audio_clip.duration
    audio_clip.close()

    # Tính toán thời gian cho mỗi ảnh
    num_images = len(imgfile)
    duration_per_image = duration / num_images

    print("Thời gian cho mỗi ảnh: ", duration_per_image)
    print("Số lượng ảnh: ", num_images)
    print("Tổng thời gian: ", duration)

    # Tải ảnh
    img = [download_image(file) for file in imgfile]
    orig_shape = img[0].shape[:2]

    # Easing function để tạo hiệu ứng mượt mà hơn
    def easing(t):
        return t**3 * (t * (t * 6 - 15) + 10)  # Smoothstep easing function

    def crop(image, x, y, w, h):
        """
        Crop hình ảnh, đảm bảo không vượt ra ngoài biên và thêm padding nếu cần.
        """
        height, width = image.shape[:2]

        # Xác định biên crop
        x0 = max(0, int(x - w / 2))
        y0 = max(0, int(y - h / 2))
        x1 = min(width, int(x + w / 2))
        y1 = min(height, int(y + h / 2))

        # Crop ảnh
        cropped = image[y0:y1, x0:x1]

        # Nếu crop nhỏ hơn kích thước yêu cầu, thêm padding
        if cropped.shape[0] != h or cropped.shape[1] != w:
            padded = np.zeros((h, w, 3), dtype=np.uint8)  # Tạo khung đen
            offset_y = (h - cropped.shape[0]) // 2
            offset_x = (w - cropped.shape[1]) // 2
            padded[offset_y:offset_y + cropped.shape[0],
                   offset_x:offset_x + cropped.shape[1]] = cropped
            return padded

        return cropped

    # Tạo khung hình
    frames = []
    for i in range(num_images):
        for frame_index in range(int(fps * duration_per_image)):
            # Áp dụng easing
            alpha = easing(frame_index / (fps * duration_per_image))
            rx = end_center[0] * alpha + start_center[0] * (1 - alpha)
            ry = end_center[1] * alpha + start_center[1] * (1 - alpha)
            x = int(orig_shape[1] * rx)
            y = int(orig_shape[0] * ry)
            scale = end_scale * alpha + start_scale * (1 - alpha)

            # Tính toán kích thước ảnh
            if orig_shape[1] / orig_shape[0] > video_dim[0] / video_dim[1]:
                h = int(orig_shape[0] * scale)
                w = int(h * video_dim[0] / video_dim[1])
            else:
                w = int(orig_shape[1] * scale)
                h = int(w * video_dim[1] / video_dim[0])

            cropped = crop(img[i], x, y, w, h)
            scaled = cv2.resize(cropped, dsize=video_dim,
                                interpolation=cv2.INTER_CUBIC)  # Nội suy mượt hơn
            frames.append(scaled)

    # Ghi video với âm thanh
    # video_clip = ImageSequenceClip(
    #     [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames], fps=fps)
    # video_clip = video_clip.set_audio(AudioFileClip(audio_url))
    # video_clip.write_videofile(
    #     'out_' + output_file, codec="libx264", audio_codec="aac")

    # Export mp4 video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, video_dim)
    for frame in frames:
        out.write(frame)
    out.release()

    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(output_file)
    audio_background = mpe.AudioFileClip(audio_url)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile('outnameee.mp4', fps=fps)

    print("Video đã được tạo thành công!")
