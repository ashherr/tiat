const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.static('.'));

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
}); 