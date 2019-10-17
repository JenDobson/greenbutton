import greenbutton.greenbutton as gb
import matplotlib.pyplot as plt
import datetime


df = gb.SAMPLE_DATA

# Plot daily use
df_use_by_day = df.groupby(lambda x: df['Start Time'].loc[x].date()).sum()
plt.plot(df_use_by_day.Wh)
plt.show()

# Plot nightly use (11pm to 5am)
df_night_use = gb.filter_by_time_of_day(df,datetime.time(23,0),datetime.time(5,0))
df_night_use_by_day = df_night_use.groupby(lambda x: df_night_use['Start Time'].loc[x].date()).sum()
plt.plot(df_night_use_by_day.Wh)
plt.show()

# Boxplot to show distribution in hourly use across all data
gb.boxplot_use_by_hour(gb.SAMPLE_DATA)
plt.show()
