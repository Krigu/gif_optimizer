from wand.image import Image


def get_repeated_frames(input_filename):
    with Image(filename=input_filename) as gif:

        frames = {}

        image_index = 0
        images_size = len(gif.sequence) - 1
        while image_index <= images_size:
            current_frame = gif.sequence[image_index]
            next_frame = gif.sequence[image_index + 1]
            added_delay = 0
            while current_frame.signature == next_frame.signature:
                image_index += 1
                added_delay += next_frame.delay
                if image_index >= images_size:
                    break
                next_frame = gif.sequence[image_index + 1]

            frames[current_frame.index] = added_delay + current_frame.delay
            image_index += 1

        return frames


def remove_repeated_frames(input_filename, output_filename):
    frames = get_repeated_frames(input_filename)

    with Image(filename=input_filename) as gif:
        for frame in reversed(gif.sequence):
            if frame.index not in frames:
                print("Delete with index " + str(frame.index))
                del gif.sequence[frame.index]
            else:
                with frame:
                    frame.delay = frames[frame.index]

        gif.save(filename=output_filename)


if __name__ == '__main__':
    remove_repeated_frames('gifs/abc.gif', 'gifs/abc2.gif')