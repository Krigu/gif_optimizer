from PIL import Image
from PIL import ImageSequence

from images2gif import writeGif


# Algorithm from Wikipedia
def compare_image(i1, i2):
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    difference = (dif / 255.0 * 100) / ncomponents
    print("Difference (percentage):", difference)
    return difference


def remove_multiple_frames(input_filename, output_filename):
    im = Image.open(input_filename)
    original_duration = im.info['duration']
    images = [frame.copy() for frame in ImageSequence.Iterator(im)]

    frame_durations = []
    unique_frames = []

    image_index = 0
    images_size = len(images) - 1
    while image_index <= images_size:
        current_frame = images[image_index + 1]
        next_frame = images[image_index + 1]
        frame_repetition = 1
        while compare_image(current_frame, next_frame) < 0.001:
            frame_repetition += 1
            image_index += 1
            if image_index >= images_size:
                break
            next_frame = images[image_index + 1]

        unique_frames.append(current_frame)
        frame_durations.append(frame_repetition * original_duration / 1000.0)
        image_index += 1

    print(unique_frames)
    print(frame_durations)
    assert len(unique_frames) == len(frame_durations)
    writeGif(output_filename, unique_frames, dither=0, duration=frame_durations)


if __name__ == '__main__':
    remove_multiple_frames('gifs/ABC_3frames-per-character.gif', 'gifs/converted_ABC_3frames-per-character.gif')
