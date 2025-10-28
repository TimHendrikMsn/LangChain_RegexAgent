# LangChain Regex Agent

This project utilizes LangChain to process text documents.

## Prerequisites
- Docker
- Make
- OpenAI API Key

## Setup
0. You need to have Docker installed and the Docker Daemon needs to be running.

1. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

2. Run the initial build:
```bash
make build
```

## Usage

### Running Tests
```bash
make test
```
Tests will use the sample document located at `app/data/test_doc.txt`.
At the moment the two tools are tested.

### Running the Application
```bash
make terminal
```

Before running the application, you need to:
1. Create a file named `document.txt` in the `app/data/` directory
2. Add your text content to be processed in this file

## File Structure

```
app/
├── data/
│   ├── document.txt    # Your input file (required for main.py)
│   └── test_doc.txt    # Sample document for testing
└── main.py            # Main application file
```

## Make Commands

- `make build`: Builds the Docker container and sets up the environment (run this first)
- `make terminal`: Opens a terminal in the Docker container to run the application
- `make test`: Runs the test suite using the test document

## Notes

- Ensure your `.env` file is properly configured with your OpenAI API key before running the application
- The application requires a `document.txt` file in the `app/data` directory for processing
- Test files already include a sample document at `app/data/test_doc.txt`
