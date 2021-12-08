library(RSQLite)
library(DBI)

con_comp <- dbConnect(RSQLite::SQLite(), "data/ac-comp_v-1.db")
con_dev <- dbConnect(RSQLite::SQLite(), "data/ac-dev_v-1.db")

client <- dbGetQuery(con_dev, "SELECT * FROM client")
loan <- dbGetQuery(con_dev, "SELECT * FROM loan")
#loan <- rbind(loan_comp, loan_dev)

disp <- dbGetQuery(con_dev, "SELECT * FROM disp")

client$birthdate <- NULL
client$sex<-unclass(as.factor(client$sex))
#client$district_id<-NULL

# Merge
merged <- merge(client, disp, by="client_id")
merged <- merge(merged, loan, by="account_id", suffixes=c("_client"))

# Sex from categorical to numerical.
merged$sex<-unclass(as.factor(merged$sex))
merged$type<-unclass(as.factor(merged$type))

# TODO: add to markdown
# cor.test(merged$sex, merged$status)


# Drop columns
merged$account_id<-NULL
merged$loan_id<-NULL
#merged$district_id<-NULL
merged$birthdate_month<-NULL
merged$birthdate_day<-NULL
merged$loan_date<-NULL
merged$loan_day<-NULL
merged$loan_month<-NULL
merged$disp_id<-NULL

# Analysis
write.csv(client, file="data/cleaned/client.csv", row.names = FALSE) 
