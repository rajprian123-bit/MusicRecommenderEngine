# Music Recommender Engine

A Python desktop application that helps users discover new music. It connects to the Last.fm API to fetch real-time data about songs, albums, and artists.

##  What I Built
I created this tool to move beyond simple search bars. This program allows users to:
* **Fetch Real-Time Data:** It connects to the web to get the latest global charts and song recommendations instantly.
* **Smart Search Logic:** It detects broad genres (like "Rap") and offers specific sub-genres (like Trap or Drill) through a popup window.
* **Parse Complex Data:** The app takes raw JSON data from the API and cleans it up into a readable list of songs and artists.
* **Modern Interface:** I transitioned the project from a command-line script to a responsive desktop application using `tkinter`. The interface uses event-driven programming to handle user inputs and features a custom high-contrast Dark Mode theme.

##  How It Works
1.  **Input:** The user types an artist or genre into the search bar.
2.  **Request:** The Python script sends a secure request to the Last.fm servers.
3.  **Processing:** The app filters the incoming data, removing errors and formatting the text.
4.  **Display:** The results are displayed in a scrollable window, allowing the user to browse songs or similar artists.

## Technologies Used
* **Python 3**
* **Tkinter (GUI)** - For the window, buttons, and visual layout.
* **Last.fm API** - The source of the music data.
* **Requests Library** - To handle the internet connection.

## How to Run It
1.  **Install the requirements:**
    ```bash
    pip install requests python-dotenv
    ```
2.  **Add your API Key:**
    Create a file named `.env` and paste your Last.fm key:
    ```
    LASTFM_API_KEY=your_key_here
    ```
3.  **Launch the App:**
    ```bash
    python gui.py
    ```
