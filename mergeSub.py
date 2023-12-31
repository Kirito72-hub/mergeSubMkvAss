import os
import subprocess


#calculate videos stream number 
def get_subtitle_count(video_file):
    ffprobe_command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 's',
        '-show_entries', 'stream=index',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_file
    ]

    try:
        result = subprocess.run(ffprobe_command, capture_output=True, text=True, check=True)
        subtitle_count = len(result.stdout.splitlines())
        return subtitle_count
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")
        return None

def process_video(input_video, ffmpeg_path, subtitle_count):
    # Print the current video file name
    print(f"Processing video: {input_video}")

    # Search for matching subtitle file
    subtitle_path = os.path.join(os.path.dirname(input_video), f"{os.path.splitext(os.path.basename(input_video))[0]}.ass")

    # Check if subtitle file exists
    if os.path.exists(subtitle_path):
        # Print subtitle file name
        print(f"Subtitle found: {os.path.basename(subtitle_path)}")

        # Step 4: Use ffmpeg to insert the subtitle
        output_directory = os.path.join(os.path.dirname(input_video), "Exports")
        output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_video))[0]}_with_subtitles.mkv")

        # Create the Exports folder if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Step 5: Run ffmpeg to export the file with subtitles
        subprocess.run([ffmpeg_path, '-i', input_video, '-i', subtitle_path, '-c:v', 'copy', '-c:a', 'copy', '-c:s', 'copy', '-map', '0:v:0', '-map', '0:m:language:jpn', '-map', '0:s', '-map', '1', '-metadata:s:s:'+str(subtitle_count)+'', 'language=ara','-max_interleave_delta', '0', '-y', output_path], check=True)
        print(f"Exported video: {output_path}")
    else:
        print(f"Subtitle not found for {os.path.basename(input_video)}")

    # Add a separator line for better readability
    print("---------------------")

def main():
    # Assign the default path to ffmpeg
    ffmpeg_path = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"

    # Step 2: Get the videos+subtitle directory from the user
    input_directory = input("Enter the path to the directory containing input video files: ")

    # Get all video files in the directory
    input_videos = [f for f in os.listdir(input_directory) if f.lower().endswith(('.mkv'))]

    # Loop through each video file and process it
    for input_video in input_videos:
        input_video_path = os.path.join(input_directory, input_video)
        subtitle_count = get_subtitle_count(input_video_path)
        if subtitle_count is not None:
            print(f"{input_video_path}: {subtitle_count} subtitles")
        process_video(input_video_path, ffmpeg_path, subtitle_count)

    print("Script execution completed.")

if __name__ == "__main__":
    main()

            