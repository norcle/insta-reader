## Setup

1. Ensure you are using **Python >3.12**.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your credentials.

```bash
cp .env.example .env
```


```bash
INSTAGRAM_LOGIN=your_username
INSTAGRAM_PASSWORD=your_password
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=Followers
```

The Airtable table must contain the columns `username`, `full_name` and
`profile_url`.

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

The resulting file will be saved as `exports/followers_channelname.csv` and the
same data will be uploaded to the configured Airtable table.

### Airtable export

To receive follower records in Airtable:

1. Create a base and table (e.g. `Followers`).
2. Add the fields `username`, `full_name` and `profile_url` (all text).
3. Set `AIRTABLE_API_KEY`, `AIRTABLE_BASE_ID` and `AIRTABLE_TABLE_NAME` in your
   `.env`.

Example record after running the command:

| username | full_name | profile_url |
|----------|-----------|-------------|
| johndoe  | John Doe  | https://instagram.com/johndoe |
