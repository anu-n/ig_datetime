from flask import Flask, render_template, request
import instaloader

app = Flask(__name__)
L = instaloader.Instaloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    posts_info = []
    if request.method == 'POST':
        username = request.form['url']
        limit = int(request.form.get('limit', 10))  # Default to 10 posts
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            for post in profile.get_posts():
                if len(posts_info) >= limit:
                    break
                post_info = {
                    'date': post.date_utc.strftime('%Y-%m-%d %H:%M:%S'),
                    'caption': post.caption if post.caption else 'No caption available',
                    'url': f"https://www.instagram.com/p/{post.shortcode}/",
                    'likes': post.likes,
                    'comments': post.comments,
                    'views': post.video_view_count if post.is_video else 'N/A'
                }
                posts_info.append(post_info)
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('index.html', posts=posts_info)

if __name__ == '__main__':
    app.run(debug=True)
