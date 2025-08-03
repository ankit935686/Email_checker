# Holehe Web Frontend

A modern web interface for the Holehe OSINT tool that allows you to check if an email address is registered on 120+ websites through a beautiful web interface.

## Features

- 🌐 **Web Interface**: Modern, responsive design with Bootstrap 5
- ⚡ **Real-time Updates**: Live progress updates during analysis
- 📊 **Statistics Dashboard**: Shows total sites checked, accounts found, rate limits, etc.
- 📁 **CSV Export**: Export results to CSV file
- 🎨 **Beautiful UI**: Gradient backgrounds, card-based layout, and smooth animations
- 📱 **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Holehe** (if not already installed):
   ```bash
   python -m pip install -e .
   ```

## Running the Web Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Enter an email address** in the input field
2. **Click "Search"** to start the analysis
3. **Wait for results** - the analysis checks 120+ websites and may take 10-30 seconds
4. **View results** in the beautiful card-based interface
5. **Export results** to CSV if needed

## API Endpoints

- `GET /` - Main web interface
- `POST /check_email` - Start email analysis
- `GET /get_results/<email>` - Get analysis results
- `POST /clear_cache` - Clear cached results

## Features Explained

### Real-time Progress
- Shows a loading spinner during analysis
- Displays progress bar
- Polls the server every 2 seconds for updates

### Results Display
- **Green cards**: Account found on the website
- **Red cards**: Account not found
- **Orange cards**: Rate limited (try again later)
- **Gray cards**: Error occurred

### Statistics
- **Total Sites Checked**: Number of websites analyzed
- **Accounts Found**: Number of websites where the email is registered
- **Rate Limited**: Number of websites that blocked the request
- **Not Found**: Number of websites where the email is not registered

### Export Functionality
- Click "Export to CSV" to download results
- CSV includes site name, status, recovery email, phone number, and other info

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Async Processing**: Uses threading to handle long-running analysis
- **Caching**: Results are cached to avoid re-analysis
- **Error Handling**: Graceful error handling with user-friendly messages

## Security Notes

- The web interface is for local use only
- No authentication is implemented
- Results are stored in memory (not persistent)
- Consider adding authentication for production use

## Troubleshooting

1. **Port already in use**: Change the port in `app.py` line 89
2. **Module import errors**: Make sure holehe is properly installed
3. **Network errors**: Check your internet connection
4. **Slow performance**: Analysis can take 10-30 seconds for 120+ websites

## Development

To modify the web interface:

1. **Edit `templates/index.html`** for frontend changes
2. **Edit `app.py`** for backend changes
3. **Restart the Flask server** after changes

## License

Same as the original Holehe project - GNU General Public License v3.0 