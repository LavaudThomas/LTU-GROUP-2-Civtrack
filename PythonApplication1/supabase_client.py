from supabase import create_client

url = "https://rvdftdathllpluakvctf.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2ZGZ0ZGF0aGxscGx1YWt2Y3RmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUxNDgxODAsImV4cCI6MjA5MDcyNDE4MH0.Dvtom-c9UKncwdgvq6kx3PIKyu37-LHtEJem7s0gtAs"

supabase = create_client(url, key)
