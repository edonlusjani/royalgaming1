const express = require('express');
const fs = require('fs');
const cors = require('cors');
const nodemailer = require('nodemailer');

const app = express();
app.use(cors());
app.use(express.json());

// Temporary bookings database
let bookings = [];

// Nodemailer transporter configuration
const transporter = nodemailer.createTransport({
    service: 'Gmail',
    auth: {
        user: 'limanedon@gmail.com', // Replace with your email
        pass: 'zjjr ikii ssvg hdbb', // Replace with your app password
    },
});

// Fetch admin password from config.json
app.get('/admin-config', (req, res) => {
    const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
    res.json({ password: config.password });
});

// Create a booking (Pending by default)
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
    res.status(201).json({ message: "Booking submitted. Awaiting admin approval." });
});

// Fetch all bookings
app.get('/bookings', (req, res) => {
    res.json(bookings);
});

// Update a booking
app.put('/bookings/:id', (req, res) => {
    const booking = bookings.find(b => b.id === parseInt(req.params.id));
    if (booking) {
        Object.assign(booking, req.body); // Update the booking with new data
        res.json({ message: 'Booking updated successfully.', booking });
    } else {
        res.status(404).json({ message: 'Booking not found.' });
    }
});

// Approve a booking
app.put('/bookings/:id/approve', (req, res) => {
    const booking = bookings.find(b => b.id === parseInt(req.params.id));
    if (booking) {
        booking.status = 'Approved';

        // Send email notification
        const mailOptions = {
            from: 'your-email@gmail.com',
            to: booking.email,
            subject: 'Booking Approved - RoyalGaming',
            text: `Hello ${booking.name},\n\nYour booking for PCs ${booking.pcs.join(', ')} on ${booking.date} at ${booking.startTime} for ${booking.duration} hour(s) has been approved.\n\nThank you for choosing RoyalGaming!`,
        };

        transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.error('Error sending email:', error);
                return res.status(500).json({ message: 'Approval successful, but email failed to send.' });
            }
            console.log('Email sent successfully:', info.response);
            res.json({ message: 'Booking approved and customer notified via email.' });
        });
    } else {
        res.status(404).json({ message: 'Booking not found.' });
    }
});

// Reject a booking
app.put('/bookings/:id/reject', (req, res) => {
    const booking = bookings.find(b => b.id === parseInt(req.params.id));
    if (booking) {
        booking.status = 'Rejected';
        res.json({ message: 'Booking rejected successfully.' });
    } else {
        res.status(404).json({ message: 'Booking not found.' });
    }
});

// Delete a booking
app.delete('/bookings/:id', (req, res) => {
    bookings = bookings.filter(b => b.id !== parseInt(req.params.id));
    res.json({ message: 'Booking deleted successfully.' });
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
