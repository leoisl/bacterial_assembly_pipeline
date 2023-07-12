# Create a pie chart with labels being placed outside the chart to avoid overlapping
plt.figure(figsize=(10, 8))
wedges, text, autotext = plt.pie(top_15_and_other['count'], labels=None, autopct='%1.1f%%', 
                                 pctdistance=0.85, colors=colors, startangle=140, wedgeprops=dict(width=0.3))

# Draw a circle at the center of pie to make it look like a donut
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')

# Increase the distance between autotexts and the center of the pie
plt.setp(autotext, size=8, weight="bold", color="black")
autotext[0].set_color('white')

plt.title('Top 15 Scientific Names and Others')

# Adding legend and lines connecting the labels to the chart
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    plt.annotate(top_15_and_other['scientific_name'][i] + " (" + top_15_and_other['simplified_count'][i] + ")", xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                 horizontalalignment=horizontalalignment, **kw)

plt.show()

