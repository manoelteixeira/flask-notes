from app import create_app

app = create_app(config_file='config.cfg')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')