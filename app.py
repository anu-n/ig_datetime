from flask import Flask, render_template, request
import instaloader

app = Flask(__name__)
L = instaloader.Instaloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    post_date_time = None
    if request.method == 'POST':
        url = request.form['url']
        try:
            shortcode = url.split('/')[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            post_date_time = post.date_utc.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('index.html', post_date_time=post_date_time)

if __name__ == '__main__':
    app.run(debug=True)
