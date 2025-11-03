var express = require('express');
var app = express();
// 💡 New: Require the axios library
const axios = require('axios');

// Middleware to parse incoming request bodies (essential for POST requests)
app.use(express.json());
app.use(express.urlencoded({extended: true}));

app.set('view engine', 'ejs');
// Serve static files (like the CSS) from a 'public' folder
app.use(express.static('public')); 

// --- Configuration ---
const BACKEND_URL = 'http://localhost:8000/api'; 
// ---------------------

// --- Routes ---

// GET Route: Fetch all notes and render the homepage
app.get('/', async function(req, res) {
    try {
        //Axios GET request
        let response = await axios.get(BACKEND_URL + '/notes');
        // Axios wraps the response data in the 'data' property
        let data = response.data; 
        console.log(data);
        const processedNotes = data.map(note => ({
            // Extract the simple ID string
            id: note._id.$oid, 
            // Extract content and title as they are
            content: note.content,
            title: note.title,
            // You must define a color property or decide how to get it
            // For now, setting a default or fetching a random color
            color: 'default-yellow', // <--- You need to set this!
            
            // Optionally clean up date fields if you need them later
            created_at: new Date(note.created_at.$date)
        }));
        res.render('index', { notes: processedNotes }); 
    } catch (err) {
        // Axios errors have a response object with status, or a message if no response
        console.error('Error fetching notes:', err.message);
        // Render the page even on error, but with no notes
        res.render('index', { notes: [] }); 
    }
});

// POST Route: Create a new note
app.post('/note', async function(req, res) {
    const { note_title, note_content } = req.body;
    console.log("incoming --- ", note_title, note_content);
    try {
        const options = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: note_title, content: note_content }) // <-- Ensure 'title' is included
        };

        let url = `${BACKEND_URL}/notes/add`;
        console.log("url --- ", url);
        // Using fetch syntax as a conceptual placeholder, replace with your Axios logic
        let response = await axios.post(`${BACKEND_URL}/notes/add`, {
             title: note_title, 
             content: note_content 
        });

        // 💡 SUCCESS: Respond with a simple JSON object
        res.status(200).json({ success: true, message: 'Note created successfully!' });
        
    } catch (err) {
        console.log("error ---- ",err)
        // 💡 ERROR: Respond with a JSON object containing the error
        const status = err.response ? err.response.status : 500;
        const message = err.response ? err.response.data.message || err.response.statusText : err.message;

        res.status(status).json({ 
            success: false, 
            message: `Failed to create note: ${message}` 
        });
    }
});

// DELETE Route: Handle deletion request from the frontend JS
app.delete('/note/remove/:id', async function(req, res) {
    const noteId = req.params.id;
    
    try {
        // 💡 Axios DELETE call to the Flask/Python backend
        await axios.delete(`${BACKEND_URL}/notes/${noteId}`);

        // Success: Send a 200 OK response back to the client's JavaScript
        res.status(200).json({ success: true, message: 'Note deleted successfully!' });
        
    } catch (err) {
        // Error: Capture and send backend error details
        const status = err.response ? err.response.status : 500;
        const message = err.response ? err.response.data.message || err.response.statusText : err.message;

        console.error(`Error deleting note ${noteId}:`, message);

        res.status(status).json({ 
            success: false, 
            message: `Failed to delete note: ${message}` 
        });
    }
});

// PUT Route: Handle note update request from the frontend JS
app.put('/note/:id', async function(req, res) {
    const noteId = req.params.id;
    const { note_title, note_content } = req.body; // Data comes from the client form
    
    try {
        // 💡 Axios PUT call to the Flask/Python backend
        await axios.put(`${BACKEND_URL}/notes/${noteId}`, {
            title: note_title,   // Pass the updated title
            content: note_content // Pass the updated content
        });

        // Success: Send a 200 OK response back to the client's JavaScript
        res.status(200).json({ success: true, message: 'Note updated successfully!' });
        
    } catch (err) {
        // Error: Capture and send backend error details
        const status = err.response ? err.response.status : 500;
        const message = err.response ? err.response.data.message || err.response.statusText : err.message;

        console.error(`Error updating note ${noteId}:`, message);

        res.status(status).json({ 
            success: false, 
            message: `Failed to update note: ${message}` 
        });
    }
});

app.listen(3000, function() {
    console.log('The Fold is listening on port 3000! 📝');
});