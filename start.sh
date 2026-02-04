#!/bin/bash

# SecurePass Dashboard - Dev Start Script
# Starts both backend (Django) and frontend (Vite/React)

echo "🔐 Starting SecurePass Dashboard..."

# Start backend
echo "📦 Starting Django backend on http://localhost:8000..."
cd backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "⚛️  Starting React frontend on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ SecurePass Dashboard is running!"
echo ""
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers."

# Handle cleanup
trap "echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM

# Wait for both processes
wait
