library(RSQLite)
library(DBI)

con <- dbConnect(RSQLite::SQLite(), "data/ac-dev_v-1.db")
disp <- dbGetQuery(con, "SELECT * FROM disp")

# Just use owners.
disp<-disp[disp$type == 'owner', ]
disp$type<-NULL

write.csv(disp, file="data/cleaned/disp.csv", row.names = FALSE)
