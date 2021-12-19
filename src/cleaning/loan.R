library(RSQLite)
library(DBI)
source("./utils.R")

con_comp <- dbConnect(RSQLite::SQLite(), "data/ac-comp_v-1.db")
con_dev <- dbConnect(RSQLite::SQLite(), "data/ac-dev_v-1.db")

trans<-dbGetQuery(con_dev, "SELECT * FROM trans")
loan <- dbGetQuery(con_dev, "SELECT * FROM loan")

# DATA TREATMENT ========================
loan$date <- NULL
loan$loan_year <- as.factor(unclass(loan$loan_year))

# OUTLIERS ===============================
show_all_outliers_plot(loan[c("payments", "amount")])
show_all_distributions_plot(loan[c("payments", "amount")])
show_table_outliers(loan, "amount")

ggdensity(loan$amount, main="Amount")  

