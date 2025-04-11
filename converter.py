from PIL import Image, ImageSequence

def convert_webp_to_gif_animated(webp_path, gif_path):
    with Image.open(webp_path) as im:
        if getattr(im, 'is_animated', False):
            frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=im.info.get('duration', 100),
                disposal=2
            )
        else:
            im.save(gif_path, format='GIF')
