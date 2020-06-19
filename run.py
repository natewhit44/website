from server import create_app

# Create instance of application
app = create_app()

# Run command
if __name__ == '__main__':
    app.run(debug=True)