import greenbutton.greenbutton as gb
import matplotlib.pyplot as plt




plt.plot(gb.SAMPLE_DATA.kWh)
plt.show()

df = gb.SAMPLE_DATA

df_night_use = filter_by_time_of_day(df,datetime.time(23,0),datetime.time(5,0))

# Plot use per night 11pm to 5am
df_night_use_by_day = df_night_use.groupby(lambda x: df_night_use['Start Time'].loc[x].date()).sum()
plt.plot(df_night_use_by_day.Watts)
plt.show(block=False)


# Boxplot to show distribution in hourly use across all data
gb.boxplot_use_by_hour(gb.SAMPLE_DATA)

