def get_media_extension(path):
    photo_extensions = ['jpg', 'png', 'gif']
    video_extension = ['mp4', 'mpeg', 'avi', 'wmv', 'mov', 'webm']
    extension = str(path).split('.')[-1]
    if extension.lower() in photo_extensions:
        return 'PHOTO'
    if extension.lower() in video_extension:
        return 'VIDEO'
    return None
