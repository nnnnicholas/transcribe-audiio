import os
import sys
import whisper
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import argparse

def split_audio(audio_path, chunk_duration_ms=60000):  # 1-minute chunks
    audio = AudioSegment.from_mp3(audio_path)
    chunks = []
    for i, chunk in enumerate(audio[::chunk_duration_ms]):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            chunk.export(temp_file.name, format="mp3")
            chunks.append(temp_file.name)
    return chunks

def transcribe_chunk(model, chunk_path):
    try:
        result = model.transcribe(chunk_path)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing {chunk_path}: {str(e)}")
        return ""
    finally:
        os.unlink(chunk_path)  # Clean up the chunk file

def main(audio_path, output_path):
    # Split audio into chunks
    chunk_paths = split_audio(audio_path)

    # Initialize Whisper model
    model = whisper.load_model("base")  # Use "base" model for a balance of speed and accuracy

    # Transcribe chunks in parallel
    transcriptions = []
    with ThreadPoolExecutor() as executor:
        future_to_chunk = {executor.submit(transcribe_chunk, model, chunk): chunk for chunk in chunk_paths}
        for future in as_completed(future_to_chunk):
            chunk = future_to_chunk[future]
            try:
                transcription = future.result()
                transcriptions.append(transcription)
            except Exception as e:
                print(f"Chunk {chunk} generated an exception: {str(e)}")

    # Combine transcriptions
    full_transcription = " ".join(transcriptions)

    # Write to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_transcription)

    print(f"Transcription complete. Output written to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe an MP3 file to text.")
    parser.add_argument("input_file", help="Path to the input MP3 file")
    parser.add_argument("-o", "--output", default="transcription_output.txt", help="Path to the output text file (default: transcription_output.txt)")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: The file {args.input_file} does not exist.")
        sys.exit(1)

    if not args.input_file.lower().endswith('.mp3'):
        print("Warning: The input file does not have an .mp3 extension. Make sure it's an MP3 file.")

    main(args.input_file, args.output)