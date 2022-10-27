import pandas as pd
import altair as alt


data = pd.DataFrame({'a': list('CCCDDDEEE'),
                     'b': [2, 7, 4, 1, 2, 6, 8, 4, 7]})

chart = alt.Chart(data).mark_point().encode(
    x='a',
    y='b'
)

# alt.renderers.enable('mimetype') # why is this not working? 

chart.show() # to display in altair viewer (must be installed separately)
# chart.save('filename.html') # manually save your chart as html and open it with a web browser