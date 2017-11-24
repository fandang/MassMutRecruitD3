
if(FALSE){
  install.packages("RSQLite")
  install.packages("maps")
  install.packages("ggplot2")
}


library("RSQLite")
library(ggplot2)

#setwd("~/Projects/MassMutual/recruitment/recruit-viz/R/")
setwd("C:/__MM/recruit-viz-prj/R/")


drv <- dbDriver("SQLite")
connection = dbConnect(drv=drv, dbname="../recruit.db")

#alltables = dbListTables(connection)
#alltables

query <- 'select * from customer'
df_customer = dbGetQuery(connection, query)

#head(df_customer)

p <- ggplot(df_customer, aes(income))
p <- p + geom_histogram(bins=50)
p

dbDisconnect(connection)


all_states <- map_data("state")
#plot all states with ggplot
p <- ggplot()
p <- p + geom_polygon( data=all_states, aes(x=long, y=lat, group = group),colour="white", fill="grey10" )
p

print("Finished.")
