# Audio file silence splitter script by Harry Upton

from pydub import AudioSegment, silence
import argparse

def Main(name, inputFormat, outputFormat, threshold, minSilenceLength, padding, br):
    # Make an audio segment object from the audio file.
    print("Creating audio segment object...")
    audio = AudioSegment.from_file(name, inputFormat)
    print("Done.")

    # Split the audio file into chunks to remove silence, according to parameters parsed.
    print("Splitting audio file on silence...")
    try:
        chunks = silence.split_on_silence(audio, min_silence_len = minSilenceLength, silence_thresh = threshold, keep_silence=padding)
    except UnboundLocalError:
        print("UnboundLocalError: pydub throws this error when there is either all silence or no silence in the audio file. Try adjusting the silence threshold.")
        return
    print("Done.")

    for i, chunk in enumerate(chunks):
        # Export the audio chunk with new bitrate.
        print("Exporting chunk{0}.{1}.".format(i, outputFormat))
        chunk.export(".//chunk{0}.{1}".format(i, outputFormat), bitrate = br, format = outputFormat)

if __name__ == "__main__":
    # Parse the arguments from the command line.
    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=str, help="The name/path of the audio file(must be in this directory), eg. 'songs.mp3'")
    parser.add_argument("input_format", type=str, help="The format of the input audio file, eg. 'wav' or 'mp3'. mp3 requires ffmpeg.")
    parser.add_argument("-f", "--output_format",type=str, help="The format of the input audio file, eg. 'wav' or 'mp3'. mp3 requires ffmpeg", default="mp3")
    parser.add_argument("-t", "--threshold", type=int, help="The threshold volume for a chunk to be considered silent, in dBFS. You may want to adjust this parameter if your audio file is quieter than the threshold silence. Default=-16", default=-16)
    parser.add_argument("-l", "--min_silence_length", type=int, help="The minimum silence length (in ms), that a chunk must be for a split. Default=2000", default=2000)
    parser.add_argument("-p", "--padding", type=int, help="The silence to keep either side of a chunk (in ms), so the clip doesn't end too abruptly. Default=250", default=250)
    parser.add_argument("-b", "--bitrate", type=str, help="The bitrate of the output file. Default='192k'", default="192k")

    args = parser.parse_args()
    
    Main(args.file, args.input_format, args.output_format, args.threshold, args.min_silence_length, args.padding, args.bitrate)
