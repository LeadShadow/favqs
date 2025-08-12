# FavQsClient Tests

This repository contains tests for the `FavQsClient` Python client interacting with the FavQs API.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/LeadShadow/favqs.git
cd /favsq
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variable
Create a `.env` file in the project root containing:

```bash
FAVQS_API_KEY=your_api_token_here
```

## Run tests
**Run all tests:**
```bash
python -m pytest tests/
```