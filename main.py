from yt_stats import YTstats

API_KEY = 'AIzaSyAxMy49AfRKjIT6YIFfx0s7Fj_q7WlHOyk'

python_engineer_id = 'UCUGfDbfRIx51kJGGHIFo8Rw'
channel_id = python_engineer_id

yt = YTstats(API_KEY, channel_id)
yt.extract_all()
yt.dump()  # dumps to .json