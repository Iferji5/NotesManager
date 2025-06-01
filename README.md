# Notes Assistant

**Notes Assistant** is a Django-based web application for managing personal notes. Users can sign up, log in, create, edit, view, and delete notes. Each note appears as a draggable “sticky note” on the main canvas, and its position is persisted in the database so that when the user returns (or refreshes), every note remains exactly where it was left. The frontend uses a pastel-themed design with rounded corners and subtle shadows for a clean, modern look.

---

## Key Features

- **User Authentication**  
  - Sign up for a new account  
  - Log in and log out securely  
  - Password hashing and built-in Django authentication

- **CRUD Operations for Notes**  
  - Create new notes (title + content)  
  - View note details in a “reader” mode  
  - Edit existing notes  
  - Delete notes (with a confirmation prompt)

- **Drag & Drop with Persistence**  
  - On the “Notes List” page, each note card can be dragged anywhere on the canvas  
  - When the user releases (drops) a note, its final (x, y) position is sent via AJAX to the server  
  - The server updates the note’s stored coordinates in the database  
  - When the user revisits the page, all notes re-render at their saved positions

- **Pastel-Themed, Responsive Design**  
  - Soft pastel background colors for each note  
  - Rounded corners and box-shadows for a “sticky note” aesthetic  
  - Responsive layout (mobile-friendly) using Bootstrap 5 utilities and custom CSS  
  - Reader mode with a pastel header, scrolling content area, and footer

---

## Technologies & Dependencies

- **Backend:**  
  - Python 3.7.4 
  - Django 5.2.1 (whichever version you prefer)  
  - Django’s built-in authentication system  
  - MySQL (as the primary database; you can switch to PostgreSQL or SQLite by updating `settings.py`)  

- **Frontend:**  
  - Bootstrap 5 (via CDN for quick utility classes)  
  - Vanilla JavaScript for drag-and-drop logic and AJAX calls  
  - Custom CSS (embedded in templates) for pastel colors, rounded corners, and shadows  

- **Other Tools:**  
  - Git for version control  
  - GitHub (or any Git hosting) for repository & documentation  
  - (Optional) GitHub Actions for continuous integration/testing  

---

## Installation & Setup

Follow these steps to get the project running on your local machine:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Iferji5/NotesManager.git
   cd NotesManagement
