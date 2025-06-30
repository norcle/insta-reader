## Setup

1. Ensure you are using **Python >3.12**.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your Instagram credentials.

```bash
cp .env.example .env
```

## Usage

Run the CLI with the `login` command to authenticate:

```bash
python scripts/instagram_cli.py login
```

If authentication is successful, you will see a confirmation message.

### Export followers list

Fetch the followers of a public account and save them to `exports/`.

```bash
python scripts/instagram_cli.py followers --username=zima_magazine --limit=20
```

The resulting file will be saved as `exports/followers_channelname.csv`.
