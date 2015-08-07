library('ggplot2')
source('visuals/multiplot.R')

tstmps = read.csv('datasets/timestamps.csv', stringsAsFactors=F)
tstmps$ts = strptime(tstmps$ts, '%Y-%m-%dT%H:%M:%S')
tstmps$month = cut(tstmps$ts, breaks='month')
tstmps$week_day = weekdays(tstmps$ts)
tstmps$month_day = months(tstmps$ts)

ds_linechart = as.data.frame(table(tstmps$month))
linechart_lbls = strftime(as.POSIXct(ds_linechart$Var1), '%b, %y')
ds_months = as.data.frame(table(tstmps$month_day))
ds_months$Var1 = factor(ds_months$Var1, levels = rev(month.name))
ds_days = as.data.frame(table(tstmps$week_day))
ds_days$Var1 = factor(ds_days$Var1, levels = rev(c("Monday", "Tuesday", "Wednesday", "Thursday", 
                                                 "Friday", "Saturday", "Sunday")))

line = qplot(data=ds_linechart, x=as.integer(Var1), y = Freq, geom='line') + 
  theme_bw() +
  ggtitle('OSM elements by month') +
  scale_y_continuous(name='Number of entries') +
  scale_x_discrete(breaks=seq(from=1, to=100, by=12),
                   labels=linechart_lbls[seq(from=1, to=100, by=12)],
                   name="")
print(line)

bars_month = qplot(data=ds_months, x=Var1, y = Freq, geom='bar',stat="identity") + 
  coord_flip() + 
  theme_bw() +
  theme(axis.ticks=element_blank()) +
  scale_y_continuous(name='') +
  scale_x_discrete(name="") +
  ggtitle('OSM elements\nbreakdown by month')


bars_weeks = qplot(data=ds_days, x=Var1, y = Freq, geom='bar',stat="identity") + 
  coord_flip() + 
  theme_bw() +
  theme(axis.ticks=element_blank()) +
  scale_y_continuous(name='Number of entries', limit=c(0,250000)) +
  scale_x_discrete(name="") +
  ggtitle('OSM elements\nbreakdown by week day')
  
multiplot(bars_month, bars_weeks)


