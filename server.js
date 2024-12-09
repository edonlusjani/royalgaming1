const express = require('express');
const cors = require('cors');
const nodemailer = require('nodemailer');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// In-memory bookings storage
let bookings = [];

// Nodemailer configuration
const transporter = nodemailer.createTransport({
    service: 'Gmail',
    auth: {
        user: process.env.EMAIL_USER, // Use environment variables for sensitive data
        pass: process.env.EMAIL_PASS,
    },
});

// Routes

// Home route
app.get('/', (req, res) => {
    res.send('RoyalGaming Backend is running.');
});

// Create a booking
app.post('/book', (req, res) => {
    const { name, phone, email, pcs, date, startTime, duration } = req.body;
    const newBooking = {
        id: bookings.length + 1,
        name,
        phone,
        email,
        pcs,
        date,
        startTime,
        duration,
        status: 'Pending',
    };
    bookings.push(newBooking);
    res.status(201).json({ message: 'Booking created successfully!', booking: newBooking });
});

// Fetch all bookings
app.get('/bookings', (req, res) => {
    res.json(bookings);
});

// Approve a booking
app.put('/bookings/:id/approve', (req, res) => {
    const booking = bookings.find((b) => b.id === parseInt(req.params.id));
    if (!booking) {
        return res.status(404).json({ message: 'Booking not found.' });
    }
    booking.status = 'Approved';

    // Send approval email
    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: booking.email,
        subject: 'Booking Approved - RoyalGaming',
        text: `Hello ${booking.name},\n\nYour booking for PCs ${booking.pcs.join(', ')} on ${booking.date} at ${booking.startTime} for ${booking.duration} hour(s) has been approved.\n\nThank you for choosing RoyalGaming! \n\n Pershendetje ${booking.name},\n\nRezervimi juaj per pc ${booking.pcs.join(', ')} ne ${booking.date} prej ${booking.startTime} per ${booking.duration} ore eshte aprovuar.\n\nFaleminderit qe zgjodhet  RoyalGaming!`,
        

    transporter.sendMail(mailOptions, (error) => {
        if (error) {
            console.error('Error sending email:', error);
            return res.status(500).json({ message: 'Booking approved, but email could not be sent.' });
        }
        res.json({ message: 'Booking approved and email sent successfully!', booking });
    });
});

// Reject a booking
app.put('/bookings/:id/reject', (req, res) => {
    const booking = bookings.find((b) => b.id === parseInt(req.params.id));
    if (!booking) {
        return res.status(404).json({ message: 'Booking not found.' });
    }
    booking.status = 'Rejected';
    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: booking.email,
        subject: 'Booking Rejected - RoyalGaming',
        text: `Hello ${booking.name},\n\nYour booking for PCs ${booking.pcs.join(', ')} on ${booking.date} at ${booking.startTime} for ${booking.duration} hour(s) has been rejected.\n\nThank you for choosing RoyalGaming! Contact us directly for more details`,
    };

    transporter.sendMail(mailOptions, (error) => {
        if (error) {
            console.error('Error sending email:', error);
            return res.status(500).json({ message: 'Booking rejected, but email could not be sent.' });
        }
        res.json({ message: 'Booking rejected successfully.', booking });
    });
});

// Delete a booking
app.delete('/bookings/:id', (req, res) => {
    const bookingIndex = bookings.findIndex((b) => b.id === parseInt(req.params.id));
    if (bookingIndex === -1) {
        return res.status(404).json({ message: 'Booking not found.' });
    }
    bookings.splice(bookingIndex, 1);
    res.json({ message: 'Booking deleted successfully.' });
});

// Environment-aware port
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

// Admin Login Endpoint
app.post('/admin/config', (req, res) => {
    const { password } = req.body; // Extract password from request body
    const adminPassword = process.env.ADMIN_PASSWORD || 'admin123'; // Admin password (from environment or default)

    // Validate password
    if (password === adminPassword) {
        res.json({ success: true }); // Respond with success if password is correct
    } else {
        res.status(401).json({ success: false, message: 'Invalid password' }); // Respond with error if incorrect
    }
});
