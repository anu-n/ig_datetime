from flask import Flask, render_template, request
import instaloader
import pytz
from datetime import datetime

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
                utc_time_str = post.date_utc
                utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")
                utc_timezone = pytz.utc
                utc_time = utc_timezone.localize(utc_time)
                colombo_timezone = pytz.timezone("Asia/Colombo")
                local_time = utc_time.astimezone(colombo_timezone)
                print(local_time.strftime("%Y-%m-%d %H:%M:%S"))
                post_info = {
                    'date': local_time.strftime('%Y-%m-%d %H:%M:%S'),
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
    app.run(host='localhost', debug=True)
