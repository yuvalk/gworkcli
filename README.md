# gworkcli

Upload a Markdown file as a Google Doc.

The first `#` heading in the file becomes the document title. If there is no heading, the filename is used instead.

## Setup

### 1. Create a Google Cloud project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** > **New Project**
3. Give it a name and click **Create**

### 2. Enable the Google Drive API

1. In your project, go to **APIs & Services** > **Library**
2. Search for **Google Drive API** and click **Enable**

### 3. Configure the OAuth consent screen

1. Go to **APIs & Services** > **OAuth consent screen**
2. Select **External** user type (or **Internal** if using a Workspace account) and click **Create**
3. Fill in the required fields (app name, user support email, developer contact email)
4. On the **Scopes** step, click **Add or Remove Scopes** and add `https://www.googleapis.com/auth/drive.file`
5. On the **Test users** step, add your Google account email
6. Click **Save and Continue** through the remaining steps

### 4. Create OAuth credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Select **Desktop app** as the application type
4. Click **Create**
5. Download the JSON file and save it as `credentials.json` in the same directory as `upload_doc.py`

### 5. Install dependencies

```
pip install -r requirements.txt
```

## Usage

```
python upload_doc.py document.md
```

On first run, a browser window will open (or a URL will be printed) for you to authorize access. After authorization, a `token.json` file is saved locally so you won't need to authorize again until the token expires.

The script prints the URL of the created Google Doc.

## Tests

```
pytest
```
