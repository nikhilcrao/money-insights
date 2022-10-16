import trackr

if __name__ == '__main__':
    app = trackr.create_app()
    app.run(host='127.0.0.1', port=8080, debug=True)
