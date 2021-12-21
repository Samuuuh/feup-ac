library(RSQLite)
library(DBI)
source("src/cleaning/utils.R")

con_comp <- dbConnect(RSQLite::SQLite(), "data/ac-comp_v-1.db")
con_dev <- dbConnect(RSQLite::SQLite(), "data/ac-dev_v-1.db")

trans<-dbGetQuery(con_dev, "SELECT * FROM trans")
loan <- dbGetQuery(con_dev, "SELECT * FROM loan")

# DATA TREATMENT ========================
loan$date <- NULL
loan$loan_year <- as.factor(unclass(loan$loan_year))

# REDUNDANCY ============================
print("NUMBER OF NON EQUAL REDUNDANCY ===================")
loan$amount_ <- loan$payments * loan$duration
print("Number of rows where amount != duration * payments:")
print(nrow(loan[loan$amount != loan$amount_,]))
loan$amount<-NULL


# OUTLIERS ===============================
# Generate graphs to analyse outliers. 
show_all_outliers_plot(loan[c("payments")])
show_all_distributions_plot(loan[c("payments")])


write.csv(trans, file="data/cleaned/loan.csv", row.names = FALSE)