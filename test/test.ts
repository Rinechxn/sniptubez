const express = require('express');
const cors = require('cors');
const app = express();

// Allow all origins () or specify your frontend domain
const corsOptions = {
  origin: '', // Change to your frontend domain (e.g., 'http://localhost:3000')
  allowedHeaders: ['Content-Type', 'Authorization', 'Video-Title'], // Add any other custom headers you want to expose
};

app.use(cors(corsOptions));

// Add your routes and other server configurations

app.listen(5000, () => {
  console.log('Server is running on port 5000');
});