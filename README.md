# Audio Transcription Script

This Python script automates the process of transcribing MP3 audio files to text using OpenAI's Whisper model. It's designed to efficiently handle large audio files by splitting them into smaller chunks and processing them in parallel.

## Features

- Accepts MP3 files as input
- Splits audio into manageable chunks for efficient processing
- Utilizes parallel processing for faster transcription
- Outputs transcription to a text file
- Handles errors gracefully, continuing even if individual chunks fail

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- FFmpeg installed on your system

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/audio-transcription-script.git
   cd audio-transcription-script
   ```

2. Install the required Python packages:
   ```
   pip install whisper pydub
   ```

## Usage

Run the script from the command line, providing the path to your MP3 file:

```
python transcribe_audio.py path/to/your/audio.mp3
```

By default, this will create a file named `transcription_output.txt` in the same directory.

To specify a custom output file:

```
python transcribe_audio.py path/to/your/audio.mp3 -o path/to/output.txt
```

## Options

- `-o, --output`: Specify the path for the output text file (default: `transcription_output.txt`)

## Performance

This script is optimized for multi-core processors and should perform well on systems like M1 Macs. The audio is split into 1-minute chunks by default, which are processed in parallel.

## Limitations

- Currently only supports MP3 input files
- Transcription accuracy depends on the Whisper model used (default is "base")

## Contributing

Contributions to improve the script are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- This script uses OpenAI's Whisper model for transcription
- Audio processing is handled by the pydub library
